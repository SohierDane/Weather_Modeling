import boto



def get_aws_keys():
    # extracts AWS access keys
    credential_path = '/Users/sohier/.aws/aws_credentials.csv'
    with open(credential_path, 'r') as aws_data:
        keys = aws_data.read().split(',')
    access_key = keys[-2]
    secret_access_key = keys[-1]
    return access_key, secret_access_key


def get_instance_ids():
    id_path = '/Users/sohier/.aws/instance_ids.txt'
    with open(id_path, 'r') as inst_data:
        instances = inst_data.read().strip().split(',')
    return instances


if __name__ == '__main__':
    access_key, secret_access_key = get_aws_keys()
    instance_id = get_instance_ids()[0]
#    conn = boto.ec2.connect_to_region("us-west-2",
#                                      aws_access_key_id=access_key,
#                                      aws_secret_access_key=secret_access_key)


    ip = 'ec2-54-213-214-240.us-west-2.compute.amazonaws.com'