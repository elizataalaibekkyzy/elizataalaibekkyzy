from tkinter import *;
from tkinter import filedialog;
import datetime;
import csv;
import sys,os;

dir = os.path.dirname(__file__)

class Project:
    
    def __init__(self):
        self._text_box = Text(window, width=10, height=10)
        self._text_field = Label(window, text = "Select files only txt types").pack(padx=150, pady=20)
        self._select_btn = Button(window, text= 'select file', bg='#000000', width = 20, command= self._parse_file, highlightbackground='lightgray').pack(padx=150, pady=20)
        self._exit_btn = Button(text = "Exit", width = 20, command = window.destroy, highlightbackground='lightgray').pack()
        self._date_list = []
        self._time_list = []
        self._speed_list = []
        self._dist_list = []
        self._desc_list = []
        self._header_list = []
        pass

    def _open_file_dialog(self):

        file_path = filedialog.askopenfilename()
        try:
            file = open(file_path, 'r')
        except:
            #self._text_box.insert("File selection failes")  NEED TO FIX
            raise RuntimeError ("File selection failes")
        return file_path

    def _parse_file(self):

        file_path = self._open_file_dialog()
        if('.txt' in file_path):
            self._parse_txt(file_path)
        else:
            #self._text_box.insert("File type is not suported!")  NEED TO FIX
            raise RuntimeError ("File is not supported! Please choose only xml or txt type files.")
        pass
        
    def _parse_txt(self, file_path):
        file = open(file_path, 'r')
        for row_num, line in enumerate(file):
            # Remove the new line at the end and then split the string based on
            # tabs. This creates a python list of the values.
            values = line.split('\t')
            if row_num == 0: # first line is the header
                for key in values:
                    self._header_list.append(key.strip())
            else:
                for val in values:
                    if self._check_date_pattern(val.strip()):
                        dt = datetime.datetime.strptime(val, '%Y/%d/%m')
                        new_dt = '{0}.{1}.{2}'.format(dt.day, dt.month, dt.year)
                        self._date_list.append(new_dt)
                    elif self._check_time_pattern(val.strip()):
                        new_time = self._time_conversion(val.strip())
                        self._time_list.append(new_time)
                    elif 'm/s' in val:
                        knots = self._convert_to_knots(val.strip())
                        str_val = '{0} kn'.format(knots)
                        self._speed_list.append(str_val)
                    elif 'km' in val:
                        miles = self._convert_to_miles(val.strip())
                        str_val = '{0} miles'.format(miles)
                        self._dist_list.append(str_val)
                    else:
                        self._desc_list.append(val.strip())
        self._store_data_into_csv()
        pass
    
    def _check_date_pattern(self, date):
        res = True
        try:
            datetime.datetime.strptime(date, '%Y/%d/%m')
        except ValueError as error:
            res = False
        return res

    def _check_time_pattern(self, time):
        res = True
        try:
            datetime.datetime.strptime(time, '%I:%M:%S %p')
        except ValueError as error:
            res = False
        return res
    
    def _time_conversion(self, str_time):
        if str_time[-2:] == "AM" :
            if str_time[:2] == '12':
                converted_time = str('00' + str_time[2:8])
            else:
                converted_time = str_time[:-2]
        else:
            if str_time[:2] == '12':
                converted_time = str_time[:-2]
            else:
                converted_time = str(int(str_time[:2]) + 12) + str_time[2:8]
        return converted_time

    def _convert_to_knots(self, speed):
        arr = speed.split(' ')
        knots = float(arr[0]) * 1.9
        return knots

    def _convert_to_miles(self, kilometers):
        arr = kilometers.split(' ')
        miles = float(arr[0]) * 0.621371
        return miles

    def _get_timestamp(self):
        now = datetime.datetime.now()
        timestamp = now.strftime('%Y-%m-%dT%H:%M:%S') + ('-%02d' % (now.microsecond / 10000))
        return timestamp

    def _store_data_into_csv(self):
        timestamp = self._get_timestamp()
        filename = timestamp + '.csv'
        filepath = os.path.join(dir, 'genereted_files', filename)
        # open the file in the write mode
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self._header_list)
            for i in range(len(self._date_list)):
                # write a row to the csv file
                row = []
                if i < len(self._date_list):
                    row.append(self._date_list[i])
                else:
                    row.append(',')
                if i < len(self._time_list):    
                    row.append(self._time_list[i])
                else:
                    row.append(',')
                if i < len(self._speed_list):      
                    row.append(self._speed_list[i])
                else:
                    row.append(',')
                if i < len(self._dist_list):      
                    row.append(self._dist_list[i])
                else:
                    row.append(',')
                if i < len(self._desc_list):      
                    row.append(self._desc_list[i])
                else:
                    row.append(',')
                
                writer.writerow(row)
        pass


if __name__ == '__main__':
    window = Tk()
    window.geometry('700x400+70+70')
    window.title("files parser program")
    Project()
    window.mainloop()