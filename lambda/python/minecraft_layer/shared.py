from boto3 import client

PARAMATER_NAMES = {
    "TARGET_INSTANCE_ID": "/minecraft-server/target-instance-id",
}

REGION_NAME = "us-east-1"

ssm = client("ssm", region_name=REGION_NAME)
ec2 = client("ec2", region_name=REGION_NAME)
