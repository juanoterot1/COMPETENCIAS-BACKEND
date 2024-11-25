import boto3
import json
import os

class SQSUtils:
    @staticmethod
    def send_message(message_body):
        """
        Envía un mensaje a una cola SQS.
        :param queue_url: URL de la cola.
        :param message_body: Cuerpo del mensaje.
        """
        client = boto3.client("sqs")
        try:
            response = client.send_message(
                QueueUrl=os.getenv('SQS_QUEUE_URL'),
                MessageBody=json.dumps(message_body)
            )
            return response
        except Exception as e:
            raise Exception(f"Error sending message to SQS: {str(e)}")
