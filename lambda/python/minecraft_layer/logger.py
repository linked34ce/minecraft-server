from typing import Self


class Logger():
    """
    Manages logging processes.

    """

    def success(self: Self, message: str) -> None:
        """
        Outputs a success log.

        Args:
          message(str): A success message.

        Returns:
          None

        """
        print(message)

    def error(self: Self, err: Exception, message: str) -> None:
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
