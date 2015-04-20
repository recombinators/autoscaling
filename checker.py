import os

# Define AWS credentials
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
REGION = 'us-west-2'

# Set queue name variables
COMPOSITE_QUEUE = 'snapsat_composite_queue'
PREVIEW_QUEUE = 'snapsat_preview_queue'
