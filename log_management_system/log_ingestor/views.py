from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from elasticsearch.exceptions import ConnectionError, NotFoundError
import logging

from log_ingestor.serializers import LogEntrySerializer
from log_ingestor.elastic_config import getESobject, ELASTICSEARCH_INDEX

logging.basicConfig(
    level=logging.ERROR, format="%(asctime)s - %(levelname)s - %(message)s"
)


class LogIngestor(generics.CreateAPIView):
    """
    Stores the log data into elasticsearch
    """

    serializer_class = LogEntrySerializer

    def post(self, request):
        try:
            # serializing the request data
            request_payload = LogEntrySerializer(data=request.data)

            # validating the request data
            request_payload.is_valid(raise_exception=True)

            log_entry = request_payload.data

            ES = getESobject()

            res = ES.index(index=ELASTICSEARCH_INDEX, document=log_entry)

            if res["result"] != "created":
                logging.error(
                    "Could not write the log entry to elasticsearch",
                    {"log": log_entry, "response": res},
                )
                raise Exception

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            if isinstance(e, ValidationError):
                return Response(
                    request_payload.errors, status=status.HTTP_400_BAD_REQUEST
                )

            elif isinstance(e, ConnectionError):
                logging.error(e.message)

            elif isinstance(e, NotFoundError):
                logging.error(f"Index not found: {ELASTICSEARCH_INDEX}")

            return Response(
                {"msg": "Error ingesting log"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
