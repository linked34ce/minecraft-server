from minecraft_layer import get_target_instances, get_server_status, MinecraftApiResponse


def lambda_handler(event, context) -> MinecraftApiResponse:
    """
    Get the status of the Minecraft Server.

    Args:
      event(dict): a Lambda event.
      context(dict): a Lambda context.

    Return:
      response(MinecraftApiResponse): a well-formed API Response.

    """
    target_instances_result = get_target_instances()

    if not target_instances_result.is_successful:
        return target_instances_result.response

    server_status_result = get_server_status(target_instances_result)
    return server_status_result.response
