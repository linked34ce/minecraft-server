from botocore.exceptions import ClientError

from .logger import show_error_log, show_success_log
from .models import FuncResult
from .shared import ec2
from .utils import is_running


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
