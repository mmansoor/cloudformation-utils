import boto3
import yaml
import sys


# Check command-line arguments
if len(sys.argv) < 2:
    sys.exit("Usage: python script.py <region> <VPC_ID>")

region = sys.argv[1]
vpc_id = sys.argv[2]

# Initialize a session using Amazon EC2
session = boto3.Session(region_name=region)
ec2 = session.client('ec2')


# Describe security groups in the specified VPC
response = ec2.describe_security_groups(
    Filters=[
        {'Name': 'vpc-id', 'Values': [vpc_id]}
    ]
)

# Extract security groups
security_groups = response['SecurityGroups']

if not security_groups:
    print(f"Warning: No security groups found for VPC ID {vpc_id} in region {region}.")
    sys.exit(1)

# Initialize CloudFormation template structure
cfn_template = {
    "AWSTemplateFormatVersion": "2010-09-09",
    "Resources": {}
}

# Convert each security group into a CloudFormation resource
for sg in security_groups:
    sg_resource = {
        "Type": "AWS::EC2::SecurityGroup",
        "Properties": {
            "GroupDescription": sg['Description'],
            "VpcId": sg['VpcId'],
            "SecurityGroupIngress": []
        }
    }

    for permission in sg['IpPermissions']:
        for ip_range in permission.get('IpRanges', []):
            ingress_rule = {
                "CidrIp": ip_range['CidrIp'],
                "FromPort": permission.get('FromPort', 0),
                "ToPort": permission.get('ToPort', 65535),
                "IpProtocol": permission['IpProtocol']
            }
            sg_resource["Properties"]["SecurityGroupIngress"].append(ingress_rule)

    # Add the security group to the CloudFormation template
    cfn_template["Resources"][sg['GroupId']] = sg_resource

# Output the CloudFormation template as YAML
output_filename = f"security_groups_{vpc_id}.yaml"
with open(output_filename, 'w') as f:
    yaml.dump(cfn_template, f, default_flow_style=False)

print(f"CloudFormation template written to {output_filename}")
