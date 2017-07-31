from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty
from nio.signal.base import Signal

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
        new_signals = []
        for signal in signals:
            try:
                self.logger.debug("Sending message via {} queue".format(
                    self.queue_url(signal)))

                response = self.client.send_message(
                    QueueUrl=self.queue_url(signal),
                    DelaySeconds=self.delay_seconds(signal),
                    MessageBody=self.message_body(signal))
                new_signals.append(Signal(response))

            except:
                self.logger.exception("Message failed to send")

        self.notify_signals(new_signals)
