class DbClass:
    def __init__(self):
        import mysql.connector as connector

        self.__dsn = {
            "host": "localhost",
            "user": "maarten",
            "passwd": "password",
            "db": "securitycam"
        }

        self.__connection = connector.connect(**self.__dsn)
        self.__cursor = self.__connection.cursor()

    def getDataFromDatabase(self, table):
        # Query zonder parameters
        sqlQuery = "SELECT * FROM {table}"
        sqlCommand = sqlQuery.format(table=table)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def getDataFromDatabaseMetVoorwaarde(self, table, column, value):
        # Query met parameters
        sqlQuery = "SELECT * FROM {table} WHERE {column} = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(table = table, column = column, param1 = value)
        
        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def insertMedia(self, triggered, name, type, date):
        # Query met parameters
        sqlQuery = "INSERT INTO media (triggered, name, type, date) VALUES ('{triggered}', '{name}', '{type}', '{date}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(triggered=triggered, name=name, type=type, date=date)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def delete_media(self, id):
        # Query met parameters
        sqlQuery = "DELETE FROM media WHERE ID = {id}"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(id=id)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def getMedia(self, type, triggered, name, volgorde):
        # Query met parameters
        sqlQuery = "SELECT * FROM media " \
        "WHERE (type = {type}) AND (triggered = {triggered}) " \
        "AND (name LIKE '%{name}%') " \
        "ORDER BY date {volgorde}"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(type=type, triggered=triggered, name=name, volgorde=volgorde)

        self.__cursor.execute(sqlCommand)
        result = self.__cursor.fetchall()
        self.__cursor.close()
        return result

    def setDataToDatabase(self, table, column, value):
        # Query met parameters
        sqlQuery = "INSERT INTO {table} ({column}) VALUES ('{param1}')"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(table=table, column=column, param1=value)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()

    def updateData(self, table, column, value):
        # Query met parameters
        sqlQuery = "UPDATE {table} SET {column} = '{param1}'"
        # Combineren van de query en parameter
        sqlCommand = sqlQuery.format(table=table, column=column, param1=value)

        self.__cursor.execute(sqlCommand)
        self.__connection.commit()
        self.__cursor.close()