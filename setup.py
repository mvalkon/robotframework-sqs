from setuptools import setup, find_packages

setup(
    name='robotframework-sqs',
    version='0.0.1',
    description='A robot framework library for interacting with AWS SQS',
    url='https://github.com/mvalkon/robotframework-sqs',
    author='Mikko Valkonen',
    author_email='msvalkon@gmail.com',
    install_requires=['boto3', 'botocore'],
    packages=['sqs']
)
