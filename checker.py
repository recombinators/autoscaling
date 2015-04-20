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
FULL_COMPOSITE_METRIC = 'number_jobs_composite_queue'
PREVIEW_COMPOSITE_METRIC = 'number_jobs_preview_queue'

# Set metric namespace
NAMESPACE = 'Snapsat'

# Create SQS connction
SQSconn = make_SQS_connection(REGION,
                              AWS_ACCESS_KEY_ID,
                              AWS_SECRET_ACCESS_KEY)

# Creaet CW connection
CWconn = make_CW_connection(REGION,
                            AWS_ACCESS_KEY_ID,
                            AWS_SECRET_ACCESS_KEY)


# Monitor size of queue
def monitor_queue(SQSconn, CWconn, queue_name, metric_name):
    queue = get_queue(SQSconn, queue_name)
    size = queue_size(queue)
    update_metric(CWconn, NAMESPACE, metric_name, size)


# Create queue size check timer funciton
def queue_check_timer(SQSconn, CWconn, queue_name, metric_name, interval):
    return Timer(interval, monitor_queue(SQSconn,
                                         CWconn,
                                         queue_name,
                                         metric_name))


# Check queue sizes every 20 seconds
def main():
    full_timer = queue_check_timer(SQSconn,
                                   CWconn,
                                   FULL_COMPOSITE_QUEUE,
                                   FULL_COMPOSITE_METRIC,
                                   20)

    preview_timer = queue_check_timer(SQSconn,
                                      CWconn,
                                      PREVIEW_COMPOSITE_QUEUE,
                                      PREVIEW_COMPOSITE_METRIC,
                                      20)

    full_timer.start()
    preview_timer.start()

if __name__ == '__main__':
    main()
