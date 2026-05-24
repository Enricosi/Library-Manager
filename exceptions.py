class LibraryManagerError(Exception):
    """Base exception for expected business logic errors in the Issue Tracker.

    Raised when the user's input is valid but violates a business rule
    (e.g. deleting a developer with open issues). Caught in main() and
    printed as a plain message, without a traceback.
    """
    pass