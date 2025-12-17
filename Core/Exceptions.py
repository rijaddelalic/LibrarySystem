class LibraryError(Exception):
    """Osnovna klasa za sve greške u biblioteci."""
    pass

class UserNotFoundError(LibraryError):
    pass

class UserAlreadyExistsError(LibraryError):
    pass

class BookNotFoundError(LibraryError):
    pass

class BookAlreadyExistsError(LibraryError):
    pass

class AlreadyBorrowedError(LibraryError):
    pass

class NotBorrowedError(LibraryError):
    pass

class AlreadyReturnedError(LibraryError):
    pass