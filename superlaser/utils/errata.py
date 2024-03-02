class ApiKeyError(Exception):
    """
    Raised when API key is not provided.
    """

    def __init__(self):
        super().__init__(
            "API key not provided. Please set the RUNPOD_API_KEY environment variable for proper API security."
        )


class RoleError(Exception):
    """
    Raised when attempting to specify a role when chat is False.
    """

    def __init__(self, message="Cannot specify 'role' when chat=False"):
        super().__init__(message)
