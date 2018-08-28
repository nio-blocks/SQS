from unittest.mock import patch

from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase

from ..amazon_sqs_send_message_block import SQSSendMessage
from ..amazon_sqs_receive_message_block import SQSReceiveMessage


class TestSQS(NIOBlockTestCase):

    @patch('boto3.client')
    def test_client(self, mock_client):
        creds = {
            "aws_access_key_id": "foo",
            "aws_secret_access_key": "bar",
            "aws_session_token": "baz",
            "region_name": "us-east-1"
        }
        blk = SQSSendMessage()
        self.configure_block(blk, {
            "queue_url": "thequeueforyou.com",
            "message_body": "{{ $message_body }}",
            "delay_seconds": "{{ $delay_seconds }}",
            "creds": creds,
        })
        blk.start()
        mock_client.assert_called_once_with(
            'sqs',
            aws_access_key_id=creds['aws_access_key_id'],
            aws_secret_access_key=creds['aws_secret_access_key'],
            aws_session_token=creds['aws_session_token'],
            region_name='us-east-1')

    def test_send_message(self):
        """Signals ..."""
        blk = SQSSendMessage()
        self.configure_block(blk, {
            "queue_url": "thequeueforyou.com",
            "message_body": "{{ $message_body }}",
            "delay_seconds": "{{ $delay_seconds }}"
        })
        blk.start()
        with patch.object(blk, "client") as patched_client:
            patched_client.send_message.return_value = {
                'MD5OfMessageBody': 'string',
                'MD5OfMessageAttributes': 'string',
                'MessageId': 'string',
                'SequenceNumber': 'string'
            }
            blk.process_signals([Signal({
                "message_body": "ayyo1120",
                "delay_seconds": 0,
            })])
            patched_client.send_message.assert_called_once_with(
                QueueUrl="thequeueforyou.com",
                DelaySeconds=0,
                MessageBody="ayyo1120"
            )

        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {
                'MD5OfMessageBody': 'string',
                'MD5OfMessageAttributes': 'string',
                'MessageId': 'string',
                'SequenceNumber': 'string'
            }
        )

    def test_receive_message(self):
        """Signals ..."""
        blk = SQSReceiveMessage()
        self.configure_block(blk, {
            "region_name": "{{ $region_name }}",
            "aws_access_key_id": "{{ $aws_access_key_id }}",
            "aws_secret_access_key": "{{ $aws_secret_access_key }}",
            "queue_url": "{{ $queue_url }}",
            "max_number_of_messages": "{{ $max_number_of_messages }}",
        })

        blk.start()
        with patch.object(blk, "client") as patched_client:
            patched_client.receive_message.return_value = {
                'Messages': [
                    {
                        'MessageId': 'string',
                        'ReceiptHandle': 'string',
                        'MD5OfBody': 'string',
                        'Body': 'string',
                        'Attributes': {
                            'string': 'string'
                        },
                        'MD5OfMessageAttributes': 'string',
                        'MessageAttributes': {
                            'string': {
                                'StringValue': 'string',
                                'BinaryValue': b'bytes',
                                'StringListValues': [
                                    'string',
                                ],
                                'BinaryListValues': [
                                    b'bytes',
                                ],
                                'DataType': 'string'
                            },
                        }
                    },
                ]
            }
            blk.process_signals([Signal({
                "region_name": "urMomsHouse",
                "aws_access_key_id": "keyID",
                "aws_secret_access_key": "ssssssecret",
                "queue_url": "thequeueforyou.com",
                "max_number_of_messages": 3,
            })])
            patched_client.receive_message.assert_called_once_with(
                QueueUrl="thequeueforyou.com",
                MaxNumberOfMessages=3,
                ReceiveRequestAttemptId='',
                VisibilityTimeout=0,
                WaitTimeSeconds=10
            )

        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {
                'Messages': [
                    {
                        'MessageId': 'string',
                        'ReceiptHandle': 'string',
                        'MD5OfBody': 'string',
                        'Body': 'string',
                        'Attributes': {
                            'string': 'string'
                        },
                        'MD5OfMessageAttributes': 'string',
                        'MessageAttributes': {
                            'string': {
                                'StringValue': 'string',
                                'BinaryValue': b'bytes',
                                'StringListValues': [
                                    'string',
                                ],
                                'BinaryListValues': [
                                    b'bytes',
                                ],
                                'DataType': 'string'
                            },
                        }
                    },
                ]
            }
        )
