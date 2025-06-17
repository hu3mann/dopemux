class ValidationError(Exception):
    def __init__(self, errors):
        super().__init__('validation failed')
        self._errors = errors
    def errors(self):
        return self._errors

class BaseModel:
    def __init__(self, **data):
        self.__dict__.update(data)
