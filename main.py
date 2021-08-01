import os
from flask import Flask, redirect, url_for, request,render_template
import available_drives
from db_management import dbm
import threading
import os

app = Flask(__name__)

def find_files(filename, search_path):
    """ Finds the location of files whose name matches with the filename

        Args:
            filename (str): The file to be searched in each drive
            search_path (str): The path i.e. the drive in which te file has to be searched in

        Returns:
            result: A list of all locations of the file
    """

    global result
    result = []
    # The loop passes through all directories, and sub-directories in the search path to find the file
    for root, dir, files in os.walk(search_path):
        # Parses through different files to see if the file name matches the file searched
        for file in files:
            # Splits the extension from the file name
            file_lst = file.split('.')
            # Checks if the file found matches the filename
            if filename in file_lst[0]:
                new_loc = os.path.join(root, file)
                # Adds the entire location of the file to the result list
                result.append(new_loc)
    return result


@app.route('/')
def search():
    return render_template('search.html')
    
    
@app.route('/result', methods=['POST','GET'])
def result():
   
   global result
   # To save thread objects
   obj_lst = []
   if request.method == 'POST':
      filename = request.form['nm']
      DBMS = dbm(filename)
      DBMS.table_creation()
      db_results = DBMS.get_from_db()
      drives = available_drives.system_drives()

      if len(db_results) == 0:
      # If the database did not contain information needed
      # threads are created for each drive and the files are found simultaneously
         for drive in drives:
            thread = threading.Thread(target=find_files, args=(filename, drive,))
            # threads are stored in an array to help in join easily later
            obj_lst.append(thread)
            thread.start()

         # Thread is joined to get results from different drives and output is printed
         for thread in obj_lst:
            thread.join()
         
         if len(result) != 0:
                # New lists are created to bring the data in a format suitable to insert into the database
            new_li = []
            main_li = []

            for item in result:
                new_li.append(filename)
                new_li.append(item)
                main_li.append(tuple(new_li))
                new_li = []
            # The main_li is a list of tuples containing the filename followed by its location
            # It is then added to the database
            DBMS.add_files(main_li)
            DBMS.commit_to_database()
            return render_template('results.html', name = main_li)
         else:
            return render_template('results.html', name ='', file = filename )
      else:
         return render_template('results.html', name = db_results)
         

      
    
   

if __name__ == '__main__':
   app.run(debug = True)