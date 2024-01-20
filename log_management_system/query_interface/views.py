from rest_framework import generics, status
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from elasticsearch.exceptions import ConnectionError, NotFoundError
from drf_spectacular.utils import extend_schema
import datetime
import logging

from query_interface.serializers import QuerySerializer
from log_ingestor.elastic_config import getESobject, ELASTICSEARCH_HOST, ELASTICSEARCH_INDEX
from log_ingestor.serializers import LogEntrySerializer


# from_date and to_date should be in YYYY-MM-DDTHH:MM:SSZ format
def get_datetime_range_query(date_payload):
    try:
        # get the values of from_date and to_date
        # use current date if to_date is not provided
        from_date = date_payload["from_date"]
        to_date = date_payload.get(
            "to_date",
            datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ"),
        )

        from_date_object = datetime.datetime.strptime(from_date, "%Y-%m-%dT%H:%M:%SZ")
        to_date_object = datetime.datetime.strptime(to_date, "%Y-%m-%dT%H:%M:%SZ")

        if from_date_object > to_date_object:
            raise ValueError("From date cannot be greater that To date")

        time_range_query = {
            "range": {
                "timestamp": {
                    "gte": from_date_object.isoformat(),
                    "lte": to_date_object.isoformat(),
                }
            }
        }

        return time_range_query

    except ValueError:
        raise


def prepareQuery(request_payload):
    try:
        # removing the size parameter if present in the request
        try:
            request_payload.pop("size")
        except:
            pass

        must_query = []

        for key in request_payload:
            query = {}
            if key == "message":
                query = {"match": {key: request_payload[key]}}

            elif key == "parentResourceId":
                query = {"term": {"metadata." + key: request_payload[key]}}

            elif key == "date":
                query = get_datetime_range_query(request_payload["date"])

            else:
                query = {"term": {key: request_payload[key]}}

            must_query.append(query)

        query = {"query": {"bool": {"must": must_query}}}
        return query
    except Exception:
        raise


def format_response(raw_response):
    formated_response = []
    for response in raw_response["hits"]["hits"]:
        formated_response.append(response["_source"])
    return formated_response


class QueryInterface(generics.CreateAPIView):
    """
    Returns logs based on the filters passed in the request
    """

    @extend_schema(
        request=QuerySerializer, responses={200: LogEntrySerializer(many=True)}
    )
    def post(self, request):
        try:
            request_payload = QuerySerializer(data=request.data)
            request_payload.is_valid(raise_exception=True)

            result_size = request_payload.data.get("size", 10)

            query = prepareQuery(request_payload.data)

            ES = getESobject()

            raw_response = ES.search(
                index=ELASTICSEARCH_INDEX, size=result_size, body=query
            )

            formatted_response = format_response(raw_response)

            return Response(formatted_response, status=status.HTTP_200_OK)

        except Exception as e:
            if isinstance(e, ValidationError):
                return Response(
                    request_payload.errors, status=status.HTTP_400_BAD_REQUEST
                )

            if isinstance(e, ValueError):
                return Response(
                    {"msg": e.args},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if isinstance(e, ConnectionError):
                message = f"Unable to reach Elasticsearch Host"

            elif isinstance(e, NotFoundError):
                message = f"Index not found: {ELASTICSEARCH_INDEX}"

            logging.error(message)

            return Response(
                {"msg": message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QueryInterfaceUI(generics.RetrieveAPIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request):
        return Response(template_name="query_interface/index.html")
