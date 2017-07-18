# AWS Simple Queue Service (SQS) library for Robot Framework
This library implements a small subset of keywords for the Amazon Simple Queue Service (SQS).

## Getting started
Install the library by cloning the repository and use `pip` to install.

```bash
$ git clone https://github.com/mvalkon/robotframework-sqs
$ pip install .
```

## How to use
Import the library in your test case, and pass your SQS Queue name as `queue_name`, like so:

```RobotFramework
*** Settings *** 
Library     sqs.sqs.SQSClient   queue_name
```

## Supported keywords
Currently we support a small subset of SQS operations, which are listed below as keywords:

* `queue should be empty` – The Queue should be empty (it must not contain any available or in-flight messages)
* `queue should not be empty` – The Queue should contain at least one message of any type
* `purge queue` – Purges the queue of all messages
* `get number of inflight messages in queue` – Returns the number of in-flight messages in the queue
* `get number of available messages in queue` – Returns the number of available messages in the queue

## Example test case

In the test case below, we first purge the queue from any messages, make sure it is empty
and then expect to find a single message of any type.

```RobotFramework
*** Settings ***
Library     sqs.sqs.SQSClient   my-sqs-queue


*** Test Cases ***
Clear the queue of messages
    purge queue

Wait and check the queue is empty for 90s
    Wait Until Keyword Succeeds  90 sec  1 sec  queue should be empty

Wait until the queue contains messages for 90s
    Wait Until Keyword Succeeds  90 sec  1 sec  queue should not be empty
```


