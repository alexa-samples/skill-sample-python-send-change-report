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

# TODO: Update with your refresh token, or a call that retrieves your refresh token from a secure location.
refresh_token = "Your Refresh Token"
# TODO: Update with your Client Id for calling the Login with Amazon (LWA) API.
client_id = "Your Client Id"
# TODO: Update with your client secret for calling the LWA API.
client_secret = "Your Client Secret"

# The Login With Amazon API for using a refresh token to get a new access token.
lwa_token_url = "https://api.amazon.com/auth/o2/token"

data = urllib.parse.urlencode(
    {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }).encode("utf-8")

headers = {
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
}

request = urllib.request.Request(lwa_token_url, data, headers, "POST")

try:
    with urllib.request.urlopen(request) as response:
        """
        Response will contain the following:
        - access_token: Used in the change reports you send to the Alexa Event Gateway.
        - refresh_token: Used to obtain a new access_token from LWA when this one expires.
        - token_type: Expected token type is Bearer.
        - expires_in: Number of seconds until access_token expires (expected to be 3600, or one hour).
        """
        lwa_tokens = json.loads(response.read().decode("utf-8"))

        logger.info("Success!")
        logger.info(f"access_token: {lwa_tokens['access_token']}")
        logger.info(f"refresh_token: {lwa_tokens['refresh_token']}")
        logger.info(f"token_type: {lwa_tokens['token_type']}")
        logger.info(f"expires_in: {lwa_tokens['expires_in']}")
except HTTPError as http_error:
    logger.error(f"An error occurred: {http_error.read().decode('utf-8')}")
