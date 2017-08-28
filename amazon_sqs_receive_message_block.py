from nio.util.discovery import discoverable
from nio.properties import StringProperty, IntProperty, VersionProperty
from nio.signal.base import Signal

from .amazon_sqs_base import SQSBase


class SQSReceiveMessage(SQSBase):
    """Receive message from Amazon SQS
        User needs to specify a queue url"""

    version = VersionProperty("1.0.0")
    max_number_of_messages = IntProperty(
        title="Max Number Messages to Receive", default=1, allow_none=True)
    visibility_timeout = IntProperty(
        title="Visibility Timeout", default=0, allow_none=True)
    wait_time_seconds = IntProperty(
        title="Time to wait for messages", default=10, allow_none=True)
    receive_request_attempt_id = StringProperty(
        title="ID to attempt retry", default="", allow_none=True)

    def process_signals(self, signals):
        new_signals = []
        for signal in signals:
            try:
                self.logger.debug("Receiving message from {} queue".format(
                    self.queue_url(signal)))

                message = self.client.receive_message(
                    QueueUrl=self.queue_url(signal),
                    MaxNumberOfMessages=self.max_number_of_messages(signal),
                    VisibilityTimeout=self.visibility_timeout(signal),
                    WaitTimeSeconds=self.wait_time_seconds(signal),
                    ReceiveRequestAttemptId=self.receive_request_attempt_id(
                        signal)
                )

                new_signals.append(Signal(message))

            except:
                self.logger.exception("Message failed to be received")

        self.notify_signals(new_signals)
