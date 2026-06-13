class LibraryManagerError(Exception):
    """Base exception for expected business logic errors in the Library Manager.

    Raised when the user's input is valid but violates a business rule
    (e.g. removing a book that still has copies). Caught in main() and
    printed as a plain message, without a traceback.
    """
    pass