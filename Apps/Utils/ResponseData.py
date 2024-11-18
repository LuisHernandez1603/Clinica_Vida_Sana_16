class ResponseData:
    pass
    def __init__(self, Success, Status, Message, Record = None):
        self.Success= Success
        self.Status= Status
        self.Message= Message
        self.Record= Record

    def toResponse(self):
        return self.__dict__