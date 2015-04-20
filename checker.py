import os
import boto.ec2.cloudwatch
from sqs import (make_SQS_connection, get_queue, queue_size, )
from cloudwatch import (make_cloudwatch_connection, update_metric, )

# Define AWS credentials
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = 'us-west-2'

# Set queue name variables
COMPOSITE_QUEUE = 'snapsat_composite_queue'
PREVIEW_QUEUE = 'snapsat_preview_queue'

# Set metric name variables
COMPOSITE_QUEUE_METRIC = 'number_jobs_composite_queue'
PREVIEW_QUEUE_METRIC = 'number_jobs_preview_queue'

# Set metric namespace
NAMESPACE = 'Snapsat'

# Create SQS connction
SQSconn = make_SQS_connection(REGION,
                              AWS_ACCESS_KEY_ID,
                              AWS_SECRET_ACCESS_KEY)


# Monitor size of queue
def monitor_queue(conn, queue_name, metric_name):
    queue = get_queue(conn, queue_name)
    size = queue_size(queue)
    update_metric(conn, NAMESPACE, metric_name, size)
