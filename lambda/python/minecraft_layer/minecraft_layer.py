from boto3 import client
from botocore.exceptions import ClientError

from .minecraft_models import FuncResult


PARAMATER_NAMES = {
    "TARGET_INSTANCE_ID": "/minecraft-server/target-instance-id",
}

REGION_NAME = "us-east-1"

ssm = client("ssm", region_name=REGION_NAME)
ec2 = client("ec2", region_name=REGION_NAME)


def show_error_log(err: Exception, message: str) -> None:
    """
    Outputs an error log.

    Args:
      err(Exception): An error to show its log.
      message(str): A message about the error.

    Returns:
      None

    """
    print(message)
    print(f"{err.__class__.__name__}: {err}")


def show_success_log(message):
    """
    Outputs a success log.

    Args:
      message(str): A success message.

    Returns:
      None

    """
    print(message)


def get_instance_statuses() -> FuncResult:
    """
    Gets the statuses of EC2 instances running on the AWS environment.

    Args:
      None

    Returns:
      result(FuncResult): EC2 instance statuses or an error repsponse.

    """
    try:
        instances = ec2.describe_instance_status()["InstanceStatuses"]
    except Exception as e:
        message = "Failed to get the instance statuses."
        show_error_log(e, message)
        return FuncResult(
            is_successful=False,
            response={
                "statusCode": 500,
                "status": "error",
                "message": message,
            })

    return FuncResult(is_successful=True, data={"instances": instances})


def get_target_instances(instances: FuncResult) -> FuncResult:
    """
    Gets a list of instances a Minecraft service is running on.
    It is expected that the list has only one instance.

    Args:
      instances(FuncResult): EC2 instance statuses.

    Returns:
      result(FuncResult): Information about EC2 instances a Minecraft service is running on, or an error repsponse.

    """
    try:
        target_instance_id = ssm.get_parameter(
            Name=PARAMATER_NAMES["TARGET_INSTANCE_ID"], WithDecryption=False)["Parameter"]["Value"]
        target_instances = [
            x for x in instances if x["InstanceId"] == target_instance_id
        ]
    except Exception as e:
        message = f"Failed to get the parameter: '{PARAMATER_NAMES['TARGET_INSTANCE_ID']}'"
        show_error_log(e, message)
        return FuncResult(
            is_successful=False,
            response={
                "statusCode": 500,
                "status": "error",
                "message": message,
            })

    return FuncResult(
        is_successful=True,
        data={
            "target_instances": target_instances,
            "target_instance_id": target_instance_id,
        })


def is_running(target_instances_result: FuncResult) -> bool:
    return len(target_instances_result.data["target_instances"]) == 1


def get_server_status(target_instances_result) -> FuncResult:
    """
    Gets the status of the Minecraft server.

    Args:
      target_instances_result(FuncResult): Information about EC2 instances a Minecraft service is running on.

    Returns:
      result(FuncResult): A status of the Minecraft server or an error repsponse.

    """
    reservations = ec2.describe_instances()["Reservations"]
    target_instance = [
        i for r in reservations
        for i in r["Instances"]
        if i["InstanceId"] == target_instances_result.data["target_instance_id"]
    ][0]

    return FuncResult(
        is_successful=True,
        response={
            "statusCode": 200,
            "status": "success",
            "isRunning": is_running(target_instances_result),
            "ipAddress": target_instance.get("PublicIpAddress"),
        })


def start_server(target_instances_result: FuncResult) -> FuncResult:
    """
    Starts the Minecraft server.

    Args:
      target_instances_result(FuncResult): Information about EC2 instances a Minecraft service is running on.

    Returns:
      result(FuncResult): A successful response or an error repsponse.

    """
    if is_running(target_instances_result):
        return FuncResult(
            is_successful=True,
            response={
                "statusCode": 200,
                "status": "success",
                "message": "The Minecraft server has already been started.",
            })
    else:
        try:
            ec2.start_instances(
                InstanceIds=[
                    target_instances_result.data["target_instance_id"]
                ])
        except ClientError as e:
            return FuncResult(
                is_successful=True,
                response={
                    "statusCode": 200,
                    "status": "success",
                    "message": "The Minecraft server is stopping now. Wait a minute and try again later.",
                })
        except Exception as e:
            message = "Failed to start the Minecraft server."
            show_error_log(e, message)
            return FuncResult(
                is_successful=False,
                response={
                    "statusCode": 500,
                    "status": "error",
                    "message": message,
                })

    return FuncResult(
        is_successful=True,
        response={
            "statusCode": 200,
            "status": "success",
            "message": "Successfully started the Minecraft server.",
        })


def stop_server(target_instances_result) -> FuncResult:
    """
    Stops the Minecraft server.

    Args:
      target_instances_result(FuncResult): Information about EC2 instances a Minecraft service is running on.

    Returns:
      result(FuncResult): A successful response or an error repsponse.

    """
    if is_running(target_instances_result):
        try:
            ec2.stop_instances(
                InstanceIds=[
                    target_instances_result.data["target_instance_id"]
                ])
        except Exception as e:
            message = "Failed to stop the Minecraft server."
            show_error_log(e, message)
            return FuncResult(
                is_successful=False,
                response={
                    "statusCode": 500,
                    "status": "error",
                    "message": message,
                })
    else:
        return FuncResult(
            is_successful=True,
            response={
                "statusCode": 200,
                "status": "success",
                "message": "The Minecraft server has already been stopped.",
            })

    return FuncResult(
        is_successful=True,
        response={
            "statusCode": 200,
            "status": "success",
            "message": "Successfully stopped the Minecraft server.",
        })


def automatically_stop_server(target_instances_result) -> None:
    """
    Automatically stops the Minecraft server.

    Args:
      target_instances_result(FuncResult): Information about EC2 instances a Minecraft service is running on.

    Returns:
      None

    """
    try:
        if is_running(target_instances_result):
            ec2.stop_instances(
                InstanceIds=[
                    target_instances_result.data["target_instance_id"]
                ])
            show_success_log("Successfully stopped the Minecraft server.")
        else:
            show_success_log(
                "The Minecraft server is not started. There is nothing to do.")
    except Exception as e:
        show_error_log(e, "Failed to stop the Minecraft server.")
