class ApiResponse():
    def __init__(self,data,has_error:bool = False, message:str = 'success'):
        self.data=data
        self.has_error = has_error
        self.message=message
        return

    def asdict(self):
        return self.__dict__