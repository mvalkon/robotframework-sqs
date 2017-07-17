import boto3

from botocore.client import Config


AWS_REGION = 'eu-central-1'


class SQSClient(object):
    """
    Implements a subset of operations for the AWS SQS
    """
    ROBOT_LIBRARY_SCOPE = 'Global'

    def __init__(self, queue_name):
        self._resource = boto3.resource(
                'sqs',
                config=Config(signature_version='s3v4'),
                region_name=AWS_REGION)
        self._queue = self.__get_queue(queue_name)
        self._queue_name = queue_name
        self._queue_url = self._queue.meta.client.get_queue_url(
                QueueName=self.name).get('QueueUrl')

    @property
    def name(self):
        return self._queue_name

    @property
    def url(self):
        return self._queue_url

    def __get_queue(self, queue_name):
        """ Returns a queue from ``region`` with ``queue_name`` """
        return self._resource.get_queue_by_name(QueueName=queue_name)

    def __get_attributes(self, attribute_names=None):
        """ Dynamically fetches new attributes for the queue. If
        ``attribute_names`` is not provided, we fetch all attributes.
        """
        if not attribute_names:
            attribute_names = ['All']

        if not isinstance(attribute_names, list):
            attribute_names = [attribute_names]

        client = self._queue.meta.client

        return client.get_queue_attributes(
                    QueueUrl=self.url,
                    AttributeNames=attribute_names
                    ).get('Attributes')


    def __get_no_of_all_messages(self):
        """
        Returns the number of both available and in-flight messages
        """
        queue_attrs = self.__get_attributes(attribute_names=[
            'ApproximateNumberOfMessages',
            'ApproximateNumberOfMessagesNotVisible'])
        return sum(int(x) for x in queue_attrs.values())

    def purge_queue(self):
        """ Clears the queue of ALL messages. This action is
        not reversable """
        self._queue.purge()

    def queue_should_be_empty(self):
        """ Asserts that the queue is empty """
        if self.__get_no_of_all_messages() > 0:
            raise AssertionError("The queue was not empty")

    def queue_should_not_be_empty(self):
        """ Asserts that the queue is not empty """
        if self.__get_no_of_all_messages() == 0:
            raise AssertionError("The queue was empty")

    def get_number_of_in_flight_messages_in_queue(self):
        """
        Returns the number of in flight messages in the queue
        """
        key = "ApproximateNumberOfMessagesNotvisible"
        return int(self.__get_attributes(attribute_names=[key]).get(key))

    def get_number_of_available_messages_in_queue(self):
        """
        Returns the number of visible messages in the queue
        """
        key = 'ApproximateNumberOfMessages'
        return int(self.__get_attributes(attribute_names=key).get(key))
