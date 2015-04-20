import os
import boto.ec2.cloudwatch
from sqs import (make_SQS_connection, get_queue, queue_size, )
# Define AWS credentials
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = 'us-west-2'

# Set queue name variables
COMPOSITE_QUEUE = 'snapsat_composite_queue'
PREVIEW_QUEUE = 'snapsat_preview_queue'

# Set metric name variables
COMPOSITE_QUEUE_METRIC = 'number_jobs_composite_queue'
PRVIEW_QUEUE_METRIC = 'number_jobs_preview_queue'

# Create SQS connction
SQSconn = make_SQS_connection(REGION,
                              AWS_ACCESS_KEY_ID,
                              AWS_SECRET_ACCESS_KEY)


# Publish metric
def publish(metric_name):


# Monitor full size composite queue
def moniter_queue(conn, queue_name):
    queue = get_queue(conn, queue_name)
    size = queue_size(queue)
