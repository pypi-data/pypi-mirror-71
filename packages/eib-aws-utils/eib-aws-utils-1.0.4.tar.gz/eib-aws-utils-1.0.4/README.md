# eib-aws-utils

Helper used by Engie Impact Sustainability Solution EMEAI to develop services based on AWS.


**This package is in alpha version**

## Background jobs

For lambdas and batch background job, meaning not exposed though API-Gateway, you can use
the _entry_point_ decorator to manage the error handling and to configure the logging.
This decorator must be used only on the main handler.
It will:
* configure the standard logging package to use JSON format ([see](#logging-configuration)).
* catch all exception and log them correctly.

### Usage
````python
from eib_aws_utils.backgound_job import entry_point

@entry_point("my_package_name")
def my_handler(event, context):
    pass
````

## API-Endpoints

Lambda exposing data behind API-Gateway can use the _http_endpoint_ decorator.
This decorator manage the error handling, the logging configuration and the serialization of the output.

### Error handling

There is two category of error.

* The _BackendError_ who are internal errors.
Meaning errors occurring inside the application and don't have any link with the end users.
For example, missing data on an external source. These errors should be catch somewhere in the application.
If they are not catch then the decorator will log the error and return a _500 - Internal Server Error_ to the end user.

* The _ClientError_ are error that must be return to the end user.
They will be catch by the decorator and logged as warning.
The error will then be serialized and returned as a JSON.
For example, if the resource didn't exist you can raise a _NotFoundError_.

### Logging configuration

The decorator will use the _configure_logging_ function to configure properly the logging.
For the details [see the logging section](#logging-configuration).

### Serialization

The decorator also manage the serialisation of the lambda output to match the api-gateway format.
Your function can return only the body or a tuple with the body and the http status code.

The body can be an object or a dictionary. If it's an object then it must have a _to_dict()_ function 
that return a dictionary representation of the object.
If it's a dictionary then it will be serialized as a JSON string.
In addition to the python basic data types, the dictionary can contain the following types:
* Decimal -> float
* datetime -> ISO string
* ClientError -> dictionary
* object with _to_dict_ function -> dictionary

### Usage

````python
from eib_aws_utils.api import http_endpoint

@http_endpoint("my_package_name")
def my_handler(event, context):
    pass
````

## Logging configuration

This library also manage the logging configuration.

The _configure_logging_ function will configure the standard logging package to use JSON format.
In addition, it get the _aws_request_id_ from the context to add it in every log.
This allow use to track every logs that belong to the same run.

The root level of logging will be set to _INFO_ and for the package gave in parameter
it will use the level defined by the _LOGGING_LEVEL_ environment variable.

This function must be used at the beginning of the handler if you don't use one of the decorator.
Otherwise the decorator manage the configuration for you.

### Usage

````python
from eib_aws_utils.logging import configure_logging

def my_handler(event, context):
    configure_logging("my_package_name", context)
````

## DynamoDB Utils

### Float compatible resource

The dynamoDB serializer can be changed to map Decimal values to float. And the reverse.
By patching the default serializer you can work with float for decimal values instead of Decimal.

For this you can patch yourself the serializer when you create your boto3 resource.
Or you can use the _create_resource_with_float_serializer_ function to get the patched version of the resource.

### Usage
If you patch the dynamo resource manually when you create it:
````python
import boto3
from unittest.mock import patch
from eib_aws_utils.dynamo_utils import FloatSerializer, FloatDeserializer

with patch("boto3.dynamodb.types.TypeSerializer", new=FloatSerializer), \
     patch("boto3.dynamodb.types.TypeDeserializer", new=FloatDeserializer):
    dynamodb = boto3.resource("dynamodb")
````

Or get directly the patched version:
````python
from eib_aws_utils import dynamo_utils

dynamodb = dynamo_utils.create_resource_with_float_serializer()
````

### Query all results page at once

The _query_all_items_ function will iterate over all results page of the query and give you all the items.
You need to provide the DynamoDB resource, the table name and then you can use all the arguments
available with the _query_ function of the DynamoDB Table.


### Usage
````python
from eib_aws_utils import dynamo_utils
from boto3.dynamodb.conditions import Key

all_customer = dynamo_utils.query_all_items(
   dynamodb_resource,
   "my-table-name",
    KeyConditionExpression=Key('partition_key').eq('123456'), ScanIndexForward=False, ...
)
````

## Http Utils

You can create easily a requests session with the retry policy and 
API key authentication with the _create_requests_session_ function. 
You can pass the API key in parameter. This key will be set in the _x-api-key_ header.
You can also provide other headers in the parameters, configure the exponential backoff or change the default timeout.
The default timeout can always be override on each call.

### Usage
````python
from eib_aws_utils import http_utils

# The most simple session with authentication
session = http_utils.create_requests_session(api_gateway_key="MY-API-KEY")

# A more complex example
session = http_utils.create_requests_session(
  headers={"Accept": "application/json"},
  api_gateway_key="MY-API-KEY",
  max_retry=25,
  backoff_factor=1.5,
  timeout=30
)
````
