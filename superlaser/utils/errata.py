class ErrorHandler(Exception):
    """
    Custom error handler for specific ValueError instances.
    """

    api_key = """API key not provided. Please set the RUNPOD_API_KEY \
    environment variable for proper API security."""