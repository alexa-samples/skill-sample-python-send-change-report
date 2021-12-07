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
from datetime import datetime, timezone

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# TODO: Update with the current access token, or a call that retrieves the current access token from a secure location.
access_token = "Your access token"
# TODO: Update with the endpointId you sent in the Discover.Response when the skill was enabled.
endpoint_id = "device_id"
# TODO: Update with a call that retrieves the actual device state. Hard-coding is fine during testing.
power_state = "ON"

# TODO: Verify you're calling the correct URL for the Alexa Event Gateway.
# North America: https://api.amazonalexa.com/v3/events
# Europe: https://api.eu.amazonalexa.com/v3/events
# Far East: https://api.fe.amazonalexa.com/v3/events
gateway_url = "https://api.amazonalexa.com/v3/events"  # North America

change_report = {
    "event": {
        "header": {
            "namespace": "Alexa",
            "name": "ChangeReport",
            "messageId": "<message id>",
            "payloadVersion": "3"
        },
        "endpoint": {
            "scope": {
                "type": "BearerToken",
                "token": access_token
            },
            "endpointId": endpoint_id
        },
        "payload": {
            "change": {
                "cause": {
                    "type": "PHYSICAL_INTERACTION"
                },
                "properties": [
                    {
                        "namespace": "Alexa.PowerController",
                        "name": "powerState",
                        "value": power_state,
                        "timeOfSample": datetime.now(timezone.utc).isoformat(),
                        "uncertaintyInMilliseconds": 0
                    }
                ]
            }
        }
    },
    "context": {}
}

data = json.dumps(change_report).encode("utf-8")

headers = {
    "Authorization": "Basic {}".format(access_token),
    "Content-Type": "application/json"
}

request = urllib.request.Request(gateway_url, data, headers, "POST")

try:
    # Call Alexa Event Gateway
    with urllib.request.urlopen(request) as response:
        # The 202 code means the request is authorized, and the event is valid and accepted by Alexa.
        if response.getheader("status") == "202":
            logger.info("Success!")
except HTTPError as http_error:
    logger.error(f"An error occurred: {http_error.read().decode('utf-8')}")
