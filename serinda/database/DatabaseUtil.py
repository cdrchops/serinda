# https://www.sqlitetutorial.net/sqlite-python/
# https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
import sqlite3

from serinda.settings.IndividualSetting import IndividualSetting

class DatabaseUtil:
    # add ~ to projects path for user
    db_file = r"\projects\serinda_flask\db\serinda.db"

    def __init__(self):
        print("firing up")

    def readSqliteTable(self):
        reply = []
        try:
            conn = sqlite3.connect(self.db_file)
            print("Connected to SQLite")

            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # t = ('wakeword',)
            # for row in conn.execute('SELECT * FROM settings where settingkey=?', t):
            for row in conn.execute('SELECT * FROM settings'):
                indivSetting = IndividualSetting()
                indivSetting.settingkey = row[1]
                indivSetting.settingvalue = row[2]
                reply.append(indivSetting)

            cursor.close()
        except sqlite3.Error as error:
            print("Failed to read data from sqlite table", error)
        finally:
            if (conn):
                conn.close()
                print("The SQLite connection is closed")

        return reply
