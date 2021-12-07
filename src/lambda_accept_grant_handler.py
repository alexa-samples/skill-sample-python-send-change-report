"""
Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: LicenseRef-.amazon.com.-AmznSL-1.0
Licensed under the Amazon Software License  http://aws.amazon.com/asl/
"""
import json
import logging
import urllib.request
import urllib.parse
from urllib.error import HTTPError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO: Update with your Client Id for calling the Login with Amazon (LWA) API.
client_id = "Your Client Id"
# TODO: Update with your Client Secret for calling the LWA API.
client_secret = "Your Client Secret"
# TODO: Update with your Endpoint Id.
endpoint_id = "device_id"


def handle_accept_grant(alexa_request):
    auth_code = alexa_request["directive"]["payload"]["grant"]["code"]
    message_id = alexa_request["directive"]["header"]["messageId"]

    # The Login With Amazon API for getting access and refresh tokens from an auth code.
    lwa_token_url = "https://api.amazon.com/auth/o2/token"

    data = urllib.parse.urlencode(
        {
            "grant_type": "authorization_code",
            "code": auth_code,
            "client_id": client_id,
            "client_secret": client_secret
        }
    ).encode("utf-8")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    url_request = urllib.request.Request(lwa_token_url, data, headers, "POST")

    try:
        with urllib.request.urlopen(url_request) as response:
            """
            Response will contain the following:
            - access_token: Used in the ChangeReports you send to the Alexa Event Gateway.
            - refresh_token: Used to obtain a new access_token from LWA when this one expires.
            - token_type: Expected token type is Bearer.
            - expires_in: Number of seconds until access_token expires (expected to be 3600, or one hour).
            """
            lwa_tokens = json.loads(response.read().decode("utf-8"))

            # TODO: Save the LWA tokens in a secure location, such as AWS Secrets Manager.
            logger.info("Success!")
            logger.info(f"access_token: {lwa_tokens['access_token']}")
            logger.info(f"refresh_token: {lwa_tokens['refresh_token']}")
            logger.info(f"token_type: {lwa_tokens['token_type']}")
            logger.info(f"expires_in: {lwa_tokens['expires_in']}")
    except HTTPError as http_error:
        logger.error(f"An error occurred: {http_error.read().decode('utf-8')}")

        # Build the failure response to send to Alexa
        response = {
            "event": {
                "header": {
                    "messageId": message_id,
                    "namespace": "Alexa.Authorization",
                    "name": "ErrorResponse",
                    "payloadVersion": "3"
                },
                "payload": {
                    "type": "ACCEPT_GRANT_FAILED",
                    "message": "Failed to retrieve the LWA tokens from the user's auth code."
                }
            }
        }
    else:
        # Build the success response to send to Alexa
        response = {
            "event": {
                "header": {
                    "namespace": "Alexa.Authorization",
                    "name": "AcceptGrant.Response",
                    "messageId": message_id,
                    "payloadVersion": "3"
                },
                "payload": {}
            }
        }

    logger.info(f"accept grant response: {json.dumps(response)}")

    return response


def handle_discovery(alexa_request):
    message_id = alexa_request["directive"]["header"]["messageId"]

    # TODO: Update the Discovery Response with your device details
    response = {
        "event": {
            "header": {
                "namespace": "Alexa.Discovery",
                "name": "Discover.Response",
                "payloadVersion": "3",
                "messageId": message_id
            },
            "payload": {
                "endpoints": [
                    {
                        "endpointId": endpoint_id,
                        "manufacturerName": "Smart Device Company",
                        "friendlyName": "Demo Switch",
                        "description": "Smart Device Switch",
                        "displayCategories": [
                            "SWITCH"
                        ],
                        "additionalAttributes": {
                            "manufacturer": "Smart Device Company",
                            "model": "Sample Model",
                            "serialNumber": "U11112233456",
                            "firmwareVersion": "1.24.2546",
                            "softwareVersion": "1.036",
                            "customIdentifier": "Sample custom ID"
                        },
                        "cookie": {
                            "key1": "arbitrary key/value pairs for skill to reference this endpoint.",
                            "key2": "There can be multiple entries",
                            "key3": "but they should only be used for reference purposes.",
                            "key4": "This is not a suitable place to maintain current endpoint state."
                        },
                        "capabilities": [
                            {
                                "type": "AlexaInterface",
                                "interface": "Alexa",
                                "version": "3"
                            },
                            {
                                "interface": "Alexa.PowerController",
                                "version": "3",
                                "type": "AlexaInterface",
                                "properties": {
                                    "supported": [
                                        {
                                            "name": "powerState"
                                        }
                                    ],
                                    "retrievable": True,
                                    "proactivelyReported": True
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }

    logger.info(f"Discovery response: {json.dumps(response)}")

    return response


def lambda_handler(request, context):
    logger.info(f"request: {request}")

    namespace = request["directive"]["header"]["namespace"]
    name = request["directive"]["header"]["name"]

    if namespace == "Alexa.Authorization" and name == "AcceptGrant":
        return handle_accept_grant(request)

    if namespace == "Alexa.Discovery" and name == "Discover":
        return handle_discovery(request)
