import sqlite3
from sqlite3.dbapi2 import IntegrityError


class DB:

    def __init__(self):
        # make connection
        self.conn = sqlite3.connect("./students.db", check_same_thread=False)

        # make cursor
        self.cur = self.conn.cursor()

    # commit db

    def conn_commit(self):
        self.conn.commit()

    # get all std

    def get_all(self):
        self.cur.execute("""SELECT * FROM std_info""")
        return self.cur.fetchall()

    # register student
    def reigster_std(self, std_id, name, collage=""):
        status = False
        try:
            self.cur.execute("""INSERT INTO std_info (std_id,name,department) VALUES ("{}","{}","{}")""".format(
                std_id, name, collage))
            self.conn_commit()
            status = True
        except IntegrityError:
            pass
        return status

    # create srach student function

    def search_std(self, std_id):
        try:
            self.cur.execute(
                '''SELECT * FROM std_info WHERE std_id = "{}"'''.format(std_id))
            return self.cur.fetchall(), True
        except:
            return False

    # update student

    def update_std(self, std_id, name, collage):
        try:
            self.cur.execute('''UPDATE std_info set name = "{}",department = "{}" WHERE std_id = "{}"'''.format(
                name, collage, std_id))
            self.conn_commit()
            return True
        except:
            return False

    # delete student

    def delete_std(self, std_id):
        try:
            self.cur.execute(
                """DELETE FROM std_info WHERE std_id = {}""".format(std_id))
            self.conn_commit()
            return True

        # any error
        except:
            return False
