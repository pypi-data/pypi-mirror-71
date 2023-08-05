# Copyright 2019 Cognite AS

import os

import grpc

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic.protos import ingest_service_pb2_grpc as ingest_serv
    from cognite.seismic.protos import query_service_pb2_grpc as query_serv
    from cognite.seismic._api.file import FileAPI
    from cognite.seismic._api.job import JobAPI
    from cognite.seismic._api.slice import SliceAPI
    from cognite.seismic._api.survey import SurveyAPI
    from cognite.seismic._api.time_slice import TimeSliceAPI
    from cognite.seismic._api.trace import TraceAPI
    from cognite.seismic._api.volume import VolumeAPI


class CogniteSeismicClient:
    """
    Main class for the seismic client
    """

    def __init__(self, api_key=None, base_url=None, port=None):
        # configure env
        self.api_key = api_key or os.getenv("COGNITE_API_KEY")
        if self.api_key is None or self.api_key == "":
            raise ValueError(
                "You have either not passed an api key or not set the COGNITE_API_KEY environment variable."
            )
        self.base_url = base_url or "api.cognitedata.com"
        self.port = port or "443"
        self.url = self.base_url + ":" + str(self.port)
        self.metadata = [("api-key", self.api_key)]

        # start the connection
        credentials = grpc.ssl_channel_credentials()
        channel = grpc.secure_channel(
            self.url,
            credentials,
            options=[
                ("grpc.max_receive_message_length", 10 * 1024 * 1024),
                ("grpc.keepalive_time_ms", 5000),
                ("grpc.keepalive_permit_without_calls", 1),
                ("grpc.http2.max_pings_without_data", 0),
                ("grpc.http2.min_time_between_pings_ms", 5000),
            ],
        )
        self.query = query_serv.QueryStub(channel)
        self.ingestion = ingest_serv.IngestStub(channel)

        self.survey = SurveyAPI(self.query, self.ingestion, self.metadata)
        self.file = FileAPI(self.query, self.ingestion, self.metadata)
        self.trace = TraceAPI(self.query, self.metadata)
        self.slice = SliceAPI(self.query, self.metadata)
        self.volume = VolumeAPI(self.query, self.metadata)
        self.time_slice = TimeSliceAPI(self.query, self.metadata)
        self.job = JobAPI(self.ingestion, self.metadata)
