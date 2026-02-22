from .shared import PARAMATER_NAMES, ec2, ssm
from .logger import show_error_log
from .models import FuncResult
from .utils import is_running


def _get_instance_statuses() -> FuncResult:
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


def get_target_instances() -> FuncResult:
    """
    Gets a list of instances a Minecraft service is running on.
    It is expected that the list has only one instance.

    Args:
      None

    Returns:
      result(FuncResult): Information about EC2 instances a Minecraft service is running on, or an error repsponse.

    """
    instance_statuses_result = _get_instance_statuses()

    if not instance_statuses_result.is_successful:
        return instance_statuses_result

    try:
        target_instance_id = ssm.get_parameter(
            Name=PARAMATER_NAMES["TARGET_INSTANCE_ID"], WithDecryption=False)["Parameter"]["Value"]
        target_instances = [
            x for x in instance_statuses_result.data["instances"] if x["InstanceId"] == target_instance_id
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
