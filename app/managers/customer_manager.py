

class CusomterManager:
    """ management all garage related service """
    _db = None
    _log_service = None
    _syslog = None
    _user: Account = None

    def __init__(self, db, user: Account):
        self._db = db
        self._user =user
        self._log_service = SystemlogService(self._db)
        self._syslog = {}
        

    async def add(self):
        pass
    
    async def delete(self):
        pass

    async def update(self):
        pass
    
    async def select(self):
        pass