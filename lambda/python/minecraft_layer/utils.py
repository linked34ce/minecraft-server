from .models import FuncResult


def is_running(target_instances_result: FuncResult) -> bool:
    """
    Check if the Minecraft server is running.

    Args:
      target_instances_result(FuncResult): Information about EC2 instances a Minecraft service is running on.

    Returns:
      is_running(bool): Whether the Minecraft server is running or not.

    """
    return len(target_instances_result.data["target_instances"]) == 1
