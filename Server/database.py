from mysql import connector

class Database:
    def __init__(self):
        super().__init__()       
        self.__WikipediaDataMiningDB = connector.connect(
            host="localhost",
            user="thedoctor",
            passwd="123",
            database="WikipediaDataMining"
        )
        self.__cursor = self.__WikipediaDataMiningDB.cursor()

    def __search(self, name) -> bool:
        self.__cursor.execute(f"SELECT name FROM person WHERE name = '{name}'")
        result = self.__cursor.fetchone()
        if result is None:
            return False
        return True

    def insert(self, name, birthday, deathday) -> bool:
        try: 
            if not self.__search(name):
                self.__cursor.execute(f"INSERT INTO person (name, day_of_birth, day_of_death) VALUES" +
                    f"('{name}', '{birthday}', '{deathday}')")
                self.__WikipediaDataMiningDB.commit()
                return True

        except KeyError:
            return False

    def delete(self, name) -> bool:
        try:
            if self.__search(name):
                self.__cursor.execute(f"DELETE FROM person WHERE name = '{name}'")
                self.__WikipediaDataMiningDB.commit()
                return True

        except KeyError:
            return False

    def select(self):
        self.__cursor.execute("SELECT * FROM person");
        records = self.__cursor.fetchall()
        return records
