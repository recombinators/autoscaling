import os
from sqs import (make_SQS_connection, get_queue, queue_size, )
from cloudwatch import (make_CW_connection, update_metric, )
from threading import Timer

# Define AWS credentials
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = 'us-west-2'

# Set queue name variables
FULL_COMPOSITE_QUEUE = 'snapsat_composite_queue'
PREVIEW_COMPOSITE_QUEUE = 'snapsat_preview_queue'

# Set metric name variables
FULL_COMPOSITE_METRIC = 'number_jobs_full_queue'
PREVIEW_COMPOSITE_METRIC = 'number_jobs_preview_queue'

# Set metric namespace
NAMESPACE = 'Snapsat'

# Set size check intervals
FULL_INTERVAL = 10
PREVIEW_INTERVAL = 10

# Create SQS connction
SQSconn = make_SQS_connection(REGION,
                              AWS_ACCESS_KEY_ID,
                              AWS_SECRET_ACCESS_KEY)

# Create CW connection
CWconn = make_CW_connection(REGION,
                            AWS_ACCESS_KEY_ID,
                            AWS_SECRET_ACCESS_KEY)


# Monitor size of queue
def monitor_queue(SQSconn, CWconn, queue_name, metric_name):
    queue = get_queue(SQSconn, queue_name)
    size = queue_size(queue)
    update_metric(CWconn, NAMESPACE, metric_name, size)


# Create full queue size check timer funciton
def full_queue_timer(SQSconn, CWconn, queue_name, metric_name, interval):
    monitor_queue(SQSconn, CWconn, queue_name, metric_name)
    return Timer(interval,
                 full_queue_timer,
                 args=[SQSconn, CWconn, queue_name, metric_name, interval]
                 ).start()


# Create preview queue size check timer funciton
def preview_queue_timer(SQSconn, CWconn, queue_name, metric_name, interval):
    monitor_queue(SQSconn, CWconn, queue_name, metric_name)
    return Timer(interval,
                 full_queue_timer,
                 args=[SQSconn, CWconn, queue_name, metric_name, interval]
                 ).start()


# Check queue sizes every 20 seconds
def main():
    full_queue_timer(SQSconn,
                     CWconn,
                     FULL_COMPOSITE_QUEUE,
                     FULL_COMPOSITE_METRIC,
                     FULL_INTERVAL)

    preview_queue_timer(SQSconn,
                        CWconn,
                        PREVIEW_COMPOSITE_QUEUE,
                        PREVIEW_COMPOSITE_METRIC,
                        PREVIEW_INTERVAL)

if __name__ == '__main__':
    main()
