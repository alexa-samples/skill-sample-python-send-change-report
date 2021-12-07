## Instructions
This project contains three files with sample code to help you send a change report to the Alexa Event Gateway. The first section below lists the steps that must take place to send a successful change report event. The remaining sections map to these steps and explain how to use the sample code.

This project assumes you have a working Smart Home skill and does not teach you how to implement every step. If you don't have a Smart Home skill, follow the [Steps to Build a Smart Home Skill](https://developer.amazon.com/en-US/docs/alexa/smarthome/steps-to-build-a-smart-home-skill.html) documentation or this [Smart Home Fireplace](https://github.com/alexa-samples/skill-sample-smarthome-fireplace-python) tutorial on GitHub.

## Steps for sending a change report to the Alexa Event Gateway
1. The skill developer [enables permissions](https://developer.amazon.com/en-US/docs/alexa/smarthome/authenticate-a-customer-permissions.html#enable-alexa-event-permissions) for their skill to send Alexa events (e.g. change report) to the Alexa Event Gateway. **Client Id** and **Client Secret** are obtained.
2. The skill user enables the skill and gives permission to send events.
    * Alexa sends an [AcceptGrant](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-authorization.html) directive to the skill with an auth code for the user.
    * Skill sends the auth code to the Login with Amazon (LWA) API to retrieve an **access token** and **refresh token** for the user. The call to LWA requires the **Client Id** and **Client Secret** obtained in step #1.
    * If successful, the skill sends a success message to Alexa and the skill is enabled.
    * If unsuccessful, the skill sends a failure message to Alexa and the skill remains disabled.
3. Alexa sends a Discovery request to the skill.
4. The skill sends the device details to Alexa in the [Discovery Response](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-discovery.html), including the **endpointId** for the device, and the **proactivelyReported** field set to true.
5. The skill user changes the state of the device (e.g. physically turning it off).
6. The skill developer sends a change report to the Alexa Event Gateway with the current **access token** and the **endpointId** of the device.
7. Since the **access token** expires after one hour, the skill developer uses the **refresh token** to get a new **access token** from LWA. The call to LWA requires the **Client Id** and **Client Secret**.

## Step 1: Enable Permissions
Follow the steps in the link above to enable permissions. Store the **Client Id** and **Client Secret**, as they are used in later steps.

## Step 2: Handle the AcceptGrant
The [lambda_accept_grant_handler.py](lambda_accept_grant_handler.py) file has sample code for handling the AcceptGrant. The lambda_handler function checks the request from Alexa to see if the namespace is "Alexa.Authorization" and if the name is "AcceptGrant". If it is, the handle_accept_grant function is called. The handle_accept_grant function retrieves the auth code, and uses it to get the access and refresh tokens from LWA. Copy this code to the Lambda function for your skill. You'll need to replace the **Client Id** and **Client Secret** in the code with the values retrieved in step #1. Once you deploy the Lambda code, test it by disabling and re-enabling your skill.

### Test Output
* If you see a "[skill name] has been successfully linked" message, your code is working correctly. 
* If you see a message saying your skill could not be linked, go to the CloudWatch log group for your skill to see what went wrong.

## Step 3: Alexa sends a Discovery Request
This request is automatically sent by Alexa after the AcceptGrant has been handled successfully.

## Step 4: Skill sends a Discovery Response
The [lambda_accept_grant_handler.py](lambda_accept_grant_handler.py) file has sample code for sending a Discovery Response. The lambda_handler function checks the request from Alexa to see if the namespace is "Alexa.Discovery" and if the name is "Discover". If it is, the handle_discovery function is called. The handle_discovery function returns the Discovery Response.

### Notes
* The **endpointId** is set to "device_id". You can change it, but it has to match the **endpointId** you send in the change report in step #6 below.
* The **proactivelyReported** field is set to true. This tells Alexa that you'll be sending change reports to the Alexa Event Gateway for this device.
* The Discovery Response sets up a smart switch called "Demo Switch." You can change the name to whatever you like.
* The Discovery Response declares the [PowerController](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-powercontroller.html) interface, which supports the powerState property. If you alter the code to use a different interface, you'll need to update the corresponding property in step #6 below (i.e. something other than powerState).

## Step 5: User changes the state of the device
You'll implement the code that detects this on your own. Your code will send a change report when it detects an event, as described in the next step. For now, you can fire a change report manually by running a script locally and hard-coding the powerState (see step #6).

## Step 6: Send a change report
The [send_change_report.py](send_change_report.py) file contains sample code for sending a change report to the Alexa Event Gateway. You'll need to replace the **access token** with the current **access token**. If the **access token** is over an hour old, it is expired. You'll need to refresh the **access token** (see step #7 below) or disable and re-enable your skill.

### Notes
* This code will need to be run outside of your skill, (e.g. in a separate Lambda function). It can be run locally on-demand in the meantime.
* The **endpointId** you send in the change report has to match the **endpointId** you sent in the Discovery Response (step #4).
* The sample code sends a change in the powerState, which is used by skills that implement the [PowerController](https://developer.amazon.com/en-US/docs/alexa/device-apis/alexa-powercontroller.html) interface. If your skill doesn't implement PowerController, replace powerState with a field your skill supports. 

### Test Output
* If you see a "Success!" message, the change report was accepted by the Alexa Event Gateway.
* If you see an "An error occurred" message, the call failed. Look at the error message to determine what went wrong, then fix the code and try again. Error codes and there definitions are listed [here](https://developer.amazon.com/en-US/docs/alexa/smarthome/send-events-to-the-alexa-event-gateway.html#error-codes).

## Step 7: Refresh the Access Token
The [refresh_access_token.py](refresh_access_token.py) file contains sample code for refreshing the **access token**. You'll need to replace the **Client Id** and **Client Secret** with the values retrieved in step #1.

### Notes
* The **access token** expires every hour.
* This code will need to be run outside of your skill, (e.g. in a separate Lambda function). It can be run locally on-demand in the meantime. 

### Test Output
* If you see a "Success!" message, you successfully refreshed the **access token**. Use the new **access token** until it expires.
* If you see an "An error occurred" message, the call failed. Look at the error message to determine what went wrong, then fix the code and try again.