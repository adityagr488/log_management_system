<a name="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/adityagr488/log_management_system">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">
    Log Management System
    <a href="https://log-management-api.onrender.com/">[Live]</a>
  </h3>

  <p align="center">
    An API for seamless log ingestion and retrieval, empowering users to efficiently manage and query their log data.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#architecture">Architecture</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li>
          <a href="#installation">Installation</a>
          <ul>
            <li><a href="#install-using-docker-recommended">Install Using Docker</a></li>
            <li><a href="#manual-installation">Manual Installation</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About The Project

![Query Interface UI][query-interface-ui]

Introducing a log ingestor system designed to efficiently manage extensive log data. This solution offers a straightforward interface for querying data through full-text search or specific field filters, providing a versatile tool for log analysis.

### Built With

- Python
- Django
- Django REST Framework
- Elasticsearch
- Docker

### Architecture

![Architecture Diagram][architecture]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Make sure you have installed the following in your local environment

- [Python and PIP][Python-download]
- [Elasticsearch][Elasticsearch-download]
- [Docker][Docker-download] (Optional)

### Installation

_There are two ways of installation:_

#### Install Using Docker (Recommended)

1. Clone the respository

```sh
git clone https://github.com/adityagr488/log_management_system.git
```

2. Go to the folder containing the `docker-compose.yml` file.

```sh
cd log_management_system/
```

3. Open the `docker-compose.yml` file, make the following changes and save the file.

- Update the volume path with your folder's path

```sh
services:
  elasticsearch:
    (other configurations...)
    volumes:
      - /path/to/your/folder:/usr/share/elasticsearch/data
```

- Edit the environment variables for the log_server

```sh
  log_server:
    (other configurations...)
    environment:
      - ELASTICSEARCH_HOST=elasticsearch
      - ELASTICSEARCH_PORT=9200
      - ELASTICSEARCH_INDEX=(name of the elasticsearch index)
      - DJANGO_SECRET_KEY=(change me)
      - DEBUG_MODE=TRUE (set to false for production)

```

4. Run the script using docker-compose

```sh
  docker-compose up -d
```

5. Create an index in elastic search

- Once the services are up and running, go to `http://localhost:9200/`, if you see info about elastic search without any errors, elasticsearch is ready to use.
- Create an index along with its mapping in elasticsearch. (This is similar to creating a table in MySQL database)
- Use the same index name that was used in the log_server's environment variable **ELASTICSEARCH_INDEX** in `docker-compose.yml` file.

  > An index is collection of documents and each document is a collection of fields, which are the key-value pairs that contain your data.
  > Mapping defines how a document, and the fields it contains, are stored and indexed.

```sh
curl -X PUT "http://localhost:9200/<your_index_name>" -H 'Content-Type: application/json' -d '
{
    "mappings": {
        "properties": {
            "level": {
                "type": "keyword"
            },
            "message": {
                "type": "text"
            },
            "resourceId": {
                "type": "keyword"
            },
            "timestamp": {
                "type": "date"
            },
            "traceId": {
                "type": "keyword"
            },
            "spanId": {
                "type": "keyword"
            },
            "commit": {
                "type": "keyword"
            },
            "metadata": {
                "properties": {
                    "parentResourceId": {
                        "type": "keyword"
                    }
                }
            }
        }
    }
}'
```

- **_Note_**:
  - Postman and Thunder client can also be used.

6. Go to `http://localhost:3000` to access the Query Interface UI.

7. Go to `http://localhost:3000/docs` to access the Swagger UI docs.

#### Manual Installation

1. Set up [elasticsearch][Elasticsearch-Setup] on you local machine.

2. Create an index in elastic search (Refer Step 5 of [Install using Docker](#install-using-docker-recommended) )

3. Clone the respository

```sh
git clone https://github.com/log_management_system.git
```

4. Manually update the elasticsearch host, port and index in the elastic_config.py file or set them using environment variables.

- Go to the `log_ingestor` folder, open the `elastic_config.py` file.

```sh
cd log_management_system/log_management_system/log_ingestor/
```

- Update the following values:

```sh
ELASTICSEARCH_HOST = (your host name)
ELASTICSEARCH_PORT = (your host port)
ELASTICSEARCH_INDEX = (your index name)
```

OR

- Pass them as environment variables.

```sh
export ELASTICSEARCH_HOST=(your host name)
export ELASTICSEARCH_PORT=(your host port)
export ELASTICSEARCH_INDEX=(your index name)
```

5. Go to the folder containing the `manage.py` file

6. Start the server

```sh
python manage.py runserver 3000
```

7. Go to `http://localhost:3000` to access the Query Interface UI.

8. Go to `http://localhost:3000/docs` to access the Swagger UI docs.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->

## Usage

The API is simple to use. It has only two endpoints:

#### Log Ingestion endpoint `/logs` :

- **Description:** Ingest logs into the database seamlessly using this endpoint.
- **Request Method:** `POST`
- **Request Body (JSON Format):**

  ```json
  {
    "level": "string",
    "message": "string",
    "resourceId": "string",
    "timestamp": "string (date and time in ISO 8601 format)",
    "traceId": "string",
    "spanId": "string",
    "commit": "string",
    "metadata": {
      "parentResourceId": "string"
    }
  }
  ```

- **Example Usage:**

  ```sh
  curl -X POST -H "Content-Type: application/json" -d '{
  "level": "error",
  "message": "Failed to connect to DB",
  "resourceId": "server-1234",
  "timestamp": "2023-09-15T08:00:00Z",
  "traceId": "abc-xyz-123",
  "spanId": "span-456",
  "commit": "5e5342f",
  "metadata": {
      "parentResourceId": "server-0987"
  }
  }' http://localhost:3000/logs
  ```

  **_NOTE:_** All the fields are required and should be in the given format.

#### Query endpoint `/query` :

- **Description:** Query the logs by passing various filter options using a this endpoint.
- **Request Method:** `POST`
- **Request Body (JSON Format):**

  ```json
  {
    "size": 0,
    "level": "string",
    "message": "string",
    "resourceId": "string",
    "timestamp": "string (date and time in ISO 8601 format)",
    "date": {
      "from_date": "string (date and time in ISO 8601 format)",
      "to_date": "string (date and time in ISO 8601 format)"
    },
    "traceId": "string",
    "spanId": "string",
    "commit": "string",
    "parentResourceId": "string"
  }
  ```

- **Query Parameters:**

  - `size`: (integer) Limit the number of results (use 0 for no results, useful for counting).
  - `level`: (string) Filter logs by log level.
  - `message`: (string) Filter logs by message content.
  - `resourceId`: (string) Filter logs by resource identifier.
  - `timestamp`: (string) Filter logs by a specific timestamp (date and time in ISO 8601 format).
  - `date`: (object) Specify a date range:
    - `from_date`: (string, required) Start date and time in ISO 8601 format.
    - `to_date`: (string, optional) End date and time in ISO 8601 format. If not provided, the current date is used.
  - `traceId`: (string) Filter logs by trace identifier.
  - `spanId`: (string) Filter logs by span identifier.
  - `commit`: (string) Filter logs by commit identifier.
  - `parentResourceId`: (string) Filter logs by parent resource identifier.

  - **Example Usage:**

    ```sh
    curl -X POST -H "Content-Type: application/json" -d '{
    "size": 10,
    "level": "error",
    "resourceId": "server-1234",
    "timestamp": "2023-09-15T08:00:00Z",
    "date": {
    "from_date": "2023-09-15T00:00:00Z",
    "to_date": "2023-09-15T23:59:59Z"
    },
    "traceId": "abc-xyz-123"
    }' http://localhost:3000/query
    ```

    **_NOTE:_**

    - All parameters are optional, and users can use any combination to filter logs.
    - Use the `size` parameter to limit the number of results.
    - Use the `date` object to specify a date range. `from_date` parameter is required; the `to_date` is optional, defaulting to the current date if not provided.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->

## Features

- [x] Add logs
- [x] Log format validation
- [x] Query logs using a simple Web UI
- [x] Search within specific date ranges
- [x] Combining multiple filters
- [x] Proper response code and error messages
- [x] Real-time log ingestion and searching
- [x] Swagger UI for testing

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[query-interface-ui]: images/InterfaceUI.png
[architecture]: images/Architecture.jpeg
[Python-download]: https://www.python.org/downloads
[Elasticsearch-download]: https://www.elastic.co/downloads/elasticsearch
[Elasticsearch-Setup]: https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html
[Docker-download]: https://www.docker.com/products/docker-desktop/
