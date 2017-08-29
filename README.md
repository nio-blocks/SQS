SQSReceiveMessage
=================
Retrieves one or more messages (up to 10), from the specified queue.

Properties
----------
- **creds**: [AWS Credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
- **max_number_of_messages**: The maximum number of messages to return. Amazon SQS never returns more messages than this value (however, fewer messages might be returned). Valid values are 1 to 10. Default is 1.
- **queue_url**: The URL of the Amazon SQS queue from which messages are received. Queue URLs are case-sensitive.
- **receive_request_attempt_id**: The token used for deduplication of ReceiveMessage calls.
- **visibility_timeout**: The duration (in seconds) that the received messages are hidden from subsequent retrieve requests after being retrieved by a ReceiveMessage request.
- **wait_time_seconds**: The duration (in seconds) for which the call waits for a message to arrive in the queue before returning. If a message is available, the call returns sooner than WaitTimeSeconds.

Inputs
------
- **default**: Any list of signals

Outputs
-------
- **default**: List of signals with repsonse from receive

Commands
--------
None

Dependencies
------------
boto3

SQSSendMessage
==============
Delivers a message to the specified queue.

Properties
----------
- **creds**: [AWS Credentials](http://boto3.readthedocs.io/en/latest/guide/configuration.html)
- **delay_seconds**: The length of time, in seconds, for which to delay a specific message. Valid values: 0 to 900.
- **message_body**: The message to send. The maximum string size is 256 KB.
- **queue_url**: The URL of the Amazon SQS queue from which messages are received. Queue URLs are case-sensitive.

Inputs
------
- **default**: Any list of signals

Outputs
-------
- **default**: List of signals with repsonse from send

Commands
--------
None

Dependencies
------------
boto3

