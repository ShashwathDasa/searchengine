import sqlite3


class dbm:
    cursor, conn =0,0

    def __init__(self,filename):
        self.filename =filename


    def table_creation(self):
        """ Creates a connection with a database and creates a table in it.
            If the table already exists, it just continues

        Args:
            The function does not take any arguments

        Returns:
            Does not return any value
        """
        # The cursor and connection variables are set as global so that it can be accessed throughout the file
        
        # Create a connection
        dbm.conn = sqlite3.connect('hackathon.db')
        # Create a cursor to access data
        dbm.cursor = dbm.conn.cursor()

        # A tabled called trial is created with filename and location only if does not already exist.
        dbm.cursor.execute("""CREATE TABLE IF NOT EXISTS hackathon (filename text, location text)""")


    def get_from_db(self):
        """ Returns the data from the database which has the same filename as the argument.

            Args:
                filename (str): The name of the file which has to be searched

            Returns:
                results: returns a list of tuples containing the filename and its locations
        """
        # Selects all the data whose filename matches the argument
        dbm.cursor.execute("SELECT * FROM hackathon WHERE filename = ?", (self.filename,))
        # The results are stored in this variable
        results = dbm.cursor.fetchall()
        return results


    def add_files(self,main_li):
        """ Add the data obtained from the search engine to the database.

            Args:
                main_li (list): The list of files and their locations

            Returns:
                Does not return a value
        """
        for i in main_li:
            dbm.cursor.execute("INSERT INTO hackathon VALUES (?,?)", i)


    def commit_to_database(self):
        """ Commit the data into the database.

            Args:
                No arguments
            Returns:
                Does not return a value
        """   
        dbm.conn.commit()
        dbm.conn.close()
