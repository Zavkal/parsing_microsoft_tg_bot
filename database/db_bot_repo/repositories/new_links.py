from database.db_bot import DataBase


class NewLinksRepository:
    def __init__(self, db: DataBase):
        self.db = db

