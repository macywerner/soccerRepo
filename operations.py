import mysql.connector


class db_operations():
    def __init__(self): # constructor with connection path to db
        self.connection = mysql.connector.connect(
        host="34.134.23.43",
        user="root",
        password="rootPassword",
        database="soccer"
        )
        self.cursor = self.connection.cursor()
        print("connection made..")

    def insert_one(self,query):
        self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    # function for bulk inserting records
    def bulk_insert(self,query,records):
        self.cursor.executemany(query,records)
        self.connection.commit()
        print("query executed..")

    # function to return a single value from table
    def single_record(self,query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def single_attribute(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        #results.remove(None) -- throws errors
        return results

    # function to return all attributes of a single record from table
    def all_attributes(self,query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        for i in results:
            print (i)
        return


    # SELECT with named placeholders
    def name_placeholder_query(self,query,dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results

    # execute query
    def execute_query(self,query):
        self.cursor.execute(query)
        self.connection.commit()
        return

    # close connection
    def destructor(self):
        self.connection.close()
