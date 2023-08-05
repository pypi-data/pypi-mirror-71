import os
import pytz
import requests
import boto3
import json
import traceback

from smart_open import open
from datetime import datetime
from abc import ABC, abstractmethod
from extractlib.enums import MessageStatus
from extractlib.config_loader import ConfigLoader


class BaseExtract(ABC):
    @property
    @abstractmethod
    def etl_id(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def namespace(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def data_provider(self):
        raise NotImplementedError

    @property
    def upload_path(self):
        """Default location in the data lake to where data is uploaded.
        """
        path = "/".join(
            [
                self.env_config["env_code"],
                "data_provider=" + self.data_provider,
                "namespace=" + self.namespace,
                "year=" + self.time_created.strftime("%Y"),
                "month=" + self.time_created.strftime("%m"),
                "day=" + self.time_created.strftime("%d"),
            ]
        )

        return f"s3://{self.env_config['upload_bucket']}/{path}/"

    def __init__(self, *args, **kwargs):
        assert "env" in kwargs
        self.env_config = ConfigLoader.get_config(kwargs["env"])

        if "file_locations" in kwargs:
            self.file_locations = kwargs["file_locations"]

        self.time_created = datetime.now()

    @abstractmethod
    def should_extract(self):
        """User-defined mechanism for short-circuiting out of an extract
            Return False to cancel the extract
        """
        return True

    def get_run(self):
        """Make a POST to Oasis to create a Run object, which tracks the execution of this ETL"""
        data = {
            "etl": self.etl_id,
            "started_by": self.env_config["user_pk"],
            "extract_start": str(datetime.now(pytz.utc)),
        }

        run_endpt = f"{self.env_config['oasis_url']}/data_service/api/v1/runs/"
        headers = {"authorization": self.env_config["auth_token"]}
        return requests.post(run_endpt, json=data, headers=headers).json()["uuid"]

    def emit_event(self, run, event_status, message):
        """Communicate a state change to Oasis by sending an Event object via AWS SNS"""
        event = {
            "event_type": "extract",
            "status": event_status.value,
            "message": message,
            "object_id": self.etl_id.replace("-", ""),
            "run": run.replace("-", ""),
            "content_type": "etl",
        }

        self.sns.publish(
            TopicArn=self.env_config["event_queue_arn"], Message=json.dumps(event)
        )

    def set_inputs(self):
        """Set the inputs for the spark job. 
            By default, uses the path to which files are uploaded.
        """
        self.inputs = [
            {"data_location": self.upload_path, "input_name": "Default Input"}
        ]

    def create_spark_message(self, run):
        """Create the spark message needed to kick off a transform job"""
        run_message_body = {}
        spark_config_keys = {
            "spark_driver_cores",
            "spark_driver_memory",
            "spark_executor_cores",
            "spark_executor_memory",
            "spark_num_executors",
            "spark_queue",
        }

        for key in spark_config_keys:
            run_message_body[key] = self.env_config[key]
        run_message_body["etl"] = self.etl_id
        run_message_body["run"] = run
        run_message_body["args"] = ["--namespace", self.namespace, "--run-uuid", run]
        run_message_body["file"] = self.env_config["jar_file"]
        run_message_body["applied_data_inputs"] = []
        for input_dict in self.inputs:
            run_message_body["applied_data_inputs"].append(input_dict)
        self.run_message_body = run_message_body

    def submit_spark_message(self):
        """Post spark message to Oasis"""
        header = {
            "Accept": "application/json, application/json",
            "Content-Type": "application/json",
            "Authorization": self.env_config["auth_token"],
        }
        requests.post(
            self.env_config["start_spark_url"],
            headers=header,
            json=self.run_message_body,
        )

    def get_download_file_stream(self, file_location):
        """Use smart_open to get the file stream from which to download a file"""
        return open(file_location)

    def get_upload_file_stream(self, file_name):
        """Use smart_open to get the file stream to which to upload a file"""
        if file_name.endswith('.gz'):
            file_name = file_name[:-3]
        return open(self.upload_path + file_name, 'w')

    def process_line(self, line):
        """Process a single line of data from the download file before uploading"""
        return line

    def transfer_data(self):
        """Move data from the data source to the data lake"""
        for file_location in self.file_locations:
            file_name = os.path.basename(file_location)
            with self.get_download_file_stream(file_location) as r:
                with self.get_upload_file_stream(file_name) as w:
                    for line in r:
                        w.write(self.process_line(line))

    def extract(self):
        """The main function executes an extract from end to end"""
        self.sns = boto3.client("sns")
        if self.should_extract():
            run = self.get_run()
            try:
                self.transfer_data()
                self.set_inputs()
                self.create_spark_message(run)
                self.submit_spark_message()
                self.emit_event(run, MessageStatus.SUCCESS, "Ready for Transfrom")
            except Exception as ex:
                self.emit_event(run, MessageStatus.ERROR, traceback.format_exc())
