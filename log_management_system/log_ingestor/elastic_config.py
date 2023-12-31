from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import os

ELASTICSEARCH_HOST = os.environ.get("ELASTICSEARCH_HOST", "localhost")
ELASTICSEARCH_PORT = os.environ.get("ELASTICSEARCH_PORT", "9200")
ELASTICSEARCH_INDEX = os.environ.get("ELASTICSEARCH_INDEX", "dyte_logs")


# returns a new es object
def getESobject():
    try:
        # creating elasticsearch url
        ELASTICSEARCH_URL = (
            "http://" + ELASTICSEARCH_HOST + ":" + ELASTICSEARCH_PORT + "/"
        )

        # creating a new elastic search instance
        es = Elasticsearch([ELASTICSEARCH_URL])

        # checking is elasticsearch is reachable
        # ping() returns True if elasctisearch is reachable, false otherwise
        if not es.ping():
            raise ConnectionError(message=f"Unable to reach host: {ELASTICSEARCH_URL}")

        return es

    except ConnectionError:
        raise
