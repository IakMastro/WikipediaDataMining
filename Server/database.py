from mysql import connector

class Database:
    def __init__(self):
        super().__init__()
        self.WikipediaDataMiningDB = connector.connect(
            host="localhost",
            user="thedoctor",
            passwd="123"
        )
        self.cursor = self.WikipediaDataMiningDB.cursor()
