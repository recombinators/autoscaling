from boto.ec2.cloudwatch import connect_to_region


def make_CW_connection(region_name,
                       aws_access_key_id,
                       aws_secret_access_key):
    """
    Make a Cloudwatch connection to an AWS account. Pass in region, AWS access
    key id, and AWS secret access key
    """
    return connect_to_region(region_name,
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key)


def update_metric(conn, namespace, metric_name, value=None, timestamp=None,
                  unit=None, dimensions=None, statistics=None):
    """
    Update metric with the given name and namespace, or create metric with name
    and namespace
    """
    return conn.put_metric_data(namespace, metric_name, value)
