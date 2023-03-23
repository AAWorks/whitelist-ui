import sqlite3
from notanorm import SqliteDb
import pandas as pd

''' Database-related Functions '''

class Database:
    def __init__(self, db_file: str):
        self.__db = SqliteDb(db_file)
        self.__db.query("CREATE TABLE IF NOT EXISTS people (firstname TEXT, \
                lastname TEXT, status INTEGER;") #1: whitelisted, 0: blacklisted
        self._db.close()

    def parse_names(self, names):
        return names + ["None"] if len(names) > 2 else [names[0], names[-1]]
    
    def __add_name(self, names: list, status: int):
        names = self.parse_names(names)
        self.__db.insert("people", firstname=names[0], 
                       lastname=names[1], status=status)
    
    def add_whitelist():
        

    def add_blacklist(self, sheet):
        raw = pd.read_csv(sheet, sep=",")
        lst = [x.lower() for x in raw.Name.values.tolist() if type(x) == str]
        for name in lst:
            self.__add_name(name.split(" "), 0)
    
    def get_matches(self, names: list) -> list[dict]:
        names = self.parse_names(names)
        first_matches = self.__db.select("people", firstname=names[0])
        last_matches = self.__db.select("people", lastname=names[1])
        return first_matches + last_matches
