# Byteline Python SDK
Website: [https://www.byteline.io](https://www.byteline.io)

This document describes how to call Byteline REST APIs using the Python SDK.

## Messaging Service
Messaging service is used to send emails or text messages.
### How to send emails?

#### Installation

```
pip install byteline-sdk
```

#### Usage

###### To send emails using a template: 
Specify the `apiKey`, `templateId` from your Byteline [console](https://console.byteline.io). `templateParams` are the parameters defined in your template. See details at https://www.byteline.io/email-service.html#templates 

```
import messaging

messaging.send_templated_email({apiKey}, {templateId}, 'myfriend@gmail.com', {templateParams})
```

###### To send email using body:
Specify the `apiKey` from your Byteline [console](https://console.byteline.io).

```
import messaging

messaging.send_email({apiKey},'Zoom Party','Let's talk tomorrow evening?','myfriend@gmail.com')
```
 
