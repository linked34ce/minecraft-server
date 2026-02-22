from minecraft_layer import get_target_instances, start_server, MinecraftApiResponse


def lambda_handler(event, context) -> MinecraftApiResponse:
    """
    Starts the Minecraft server.

    Args:
      event(dict): a Lambda event.
      context(dict): a Lambda context.

    Return:
      response(MinecraftApiResponse): a well-formed API Response.

    """
    target_instances_result = get_target_instances()

    if not target_instances_result.is_successful:
        return target_instances_result.response

    start_server_result = start_server(target_instances_result)
    return start_server_result.response
