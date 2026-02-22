from minecraft_layer import get_target_instances, automatically_stop_server


def lambda_handler(event, context) -> None:
    """
    Automatically stops the Minecraft server.

    Args:
      event(dict): a Lambda event.
      context(dict): a Lambda context.

    Return:
      None

    """
    target_instances_result = get_target_instances()

    if not target_instances_result.is_successful:
        return target_instances_result.response

    automatically_stop_server(target_instances_result)
