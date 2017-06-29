import boto3

from botocore.client import Config


AWS_REGION = 'eu-central-1'


class SQS(object):
    """
    Implements a subset of operations for the AWS SQS
    """
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self, queue_name):
        self._resource = boto3.resource(
                'sqs',
                config=Config(signature_version='s3v4'),
                region_name=AWS_REGION)
        self._queue = self._get_queue(queue_name)

    def _get_queue(self, queue_name, region='eu-central-1'):
        """ Returns a queue from ``region`` with ``queue_name`` """
        return self._resource.Queue(
            url='https://sqs.{}.amazonaws.com/882181966078/{}'.format(
                region, queue_name))

    @staticmethod
    def is_empty(queue_attrs):
        """Checks for the ``ApproxmiateNumberOfMessages`` in the queue attributes
        and returns True when the value is 0 or if the attribute is not found.
        """
        approx = sum(int(queue_attrs.get(m, '0')) for m in [
            'ApproximateNumberOfMessages',
            'ApproximateNumberOfMessagesNotVisible'])
        return True if approx == 0 else False

    def inspect_queue(self):
        """ Inspects a queue and returns whether or not the queue is empty """
        return SQS.is_empty(self._queue.attributes)

    def purge(self):
        """ Clears a queue ``queue_name`` of ALL messages. This action is
        not reversable """
        self._queue.purge()

    def queue_should_be(self, empty):
        """ Asserts that the queue is either empty or not """
        expected = True if empty == 'empty' else False
        actual = self.inspect_queue()
        if actual != expected:
            raise AssertionError("Expected the queue to be {} but, got {}".format(
                empty, actual))