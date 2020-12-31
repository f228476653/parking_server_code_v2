import os,shutil
from datetime import datetime, timedelta
from pathlib import Path
from pprint import pprint

class CsvParser:
    """ this is not secure at all, however we don't have time to deal this """
    # TODO please re-write entire class to find a better way for generating keys
    
    def __init__(self, directory:str,parser_name:str):
        # self.__start_date = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        self.__timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H%M%S")
        self.__location = directory
        self.__p = Path(self.__location)
        self.__l = list(self.__p.glob('*.csv'))
        self.__n = parser_name 
    
    def read_files_in_directory(self)->dict:
        """ read files in direcotry"""
        csvCollection = {}
        for z in self.__l:
            with z.open('rb') as f:
                data = f.read().decode('utf8', 'ignore')
                csvCollection[str(z)] = data
        
        return csvCollection

    def move_files_to_bakcup_directory(self):
        path = 'csvs/'+ self.__n + '/backup/'+ self.__timestamp
        if not os.path.exists(path):
            os.makedirs(path)
        for z in self.__l:
            print(z._str)
            shutil.copy(z._str, "csvs/"+ self.__n + "/backup/"+ self.__timestamp + "/"+z.name)
            os.remove(z._str)