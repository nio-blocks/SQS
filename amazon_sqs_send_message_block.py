from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty
from .amazon_sqs_base_block import SQSBase


@discoverable
class SQSSendMessage(SQSBase):
    """Send message over Amazon SQS
        User needs to specify a queue url and message body"""

    message_body = StringProperty(
        title="Message Body", default="Hello Mr. SQS", allow_none=False)
    delay_seconds = IntProperty(
        title="Delay sending message", default=0, allow_none=True)

    def process_signals(self, signals):
        for signal in signals:
            try:
                self.logger.debug("Sending message via {} queue".format(
                    self.queue_url(signal)))

                self.client.send_message(QueueUrl=self.queue_url(signal),
                                         DelaySeconds=self.delay_seconds(signal),
                                         MessageBody=self.message_body(signal))

                # RESPONSE
                # {
                #     'MD5OfMessageBody': 'string',
                #     'MD5OfMessageAttributes': 'string',
                #     'MessageId': 'string',
                #     'SequenceNumber': 'string'
                # }

            except:
                self.logger.exception("Message failed to send")
