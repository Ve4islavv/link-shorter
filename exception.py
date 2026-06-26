

class ShortenerBaseError(Exception):
    pass


class NoLongerUrlFoundError(ShortenerBaseError):
    pass


class SlugAlreadyExistError(ShortenerBaseError):
    pass