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


def show_success_log(message: str) -> None:
    """
    Outputs a success log.

    Args:
      message(str): A success message.

    Returns:
      None

    """
    print(message)
