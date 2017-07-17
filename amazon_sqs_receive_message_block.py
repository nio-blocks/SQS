from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty
from .amazon_sqs_base_block import SQSBase


@discoverable
class SQSReceiveMessage(SQSBase):
    """Send message over Amazon SQS
        User needs to specify a queue url and message body
        If specifying a message attribute,
        it must include a name, type, and value"""

    max_number_of_messages = IntProperty(
        title="Max Number Messages to Receive", default=1, allow_none=True)
    visibility_timeout = IntProperty(
        title="Visibility Timeout", default=0, allow_none=True)
    wait_time_seconds = IntProperty(
        title="Time to wait for messages", default=10, allow_none=True)
    receive_request_attempt_id = StringProperty(
        title="ID to attempt retry", default="", allow_none=True)
        # ^ FIFO queues only

    def process_signals(self, signals):
        for signal in signals:
            try:
                self.logger.debug("Sending message via {} queue".format(
                    self.queue_url(signal)))

                self.client.receive_message(
                    QueueUrl=self.queue_url(signal),
                    MaxNumberOfMessages=self.max_number_of_messages(signal),
                    VisibilityTimeout= self.visibility_timeout(signal),
                    WaitTimeSeconds= self.wait_time_seconds(signal),
                    ReceiveRequestAttemptId= self.receive_request_attempt_id(signal)
                )

                # RESPONSE
                # {
                #     'Messages': [
                #         {
                #             'MessageId': 'string',
                #             'ReceiptHandle': 'string',
                #             'MD5OfBody': 'string',
                #             'Body': 'string',
                #             'Attributes': {
                #                 'string': 'string'
                #             },
                #             'MD5OfMessageAttributes': 'string',
                #             'MessageAttributes': {
                #                 'string': {
                #                     'StringValue': 'string',
                #                     'BinaryValue': b'bytes',
                #                     'StringListValues': [
                #                         'string',
                #                     ],
                #                     'BinaryListValues': [
                #                         b'bytes',
                #                     ],
                #                     'DataType': 'string'
                #                 }
                #             }
                #         },
                #     ]
                # }

            except:
                self.logger.exception("Message failed to send")
