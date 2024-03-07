import sys
from csv import DictReader
import os
import termcolor
import argparse
from typing import List, TextIO, Iterator, Dict

#in the following class we are abstracting file open/close + the dict reading
class mycsv:
    filepath : str
    #my_csv_file : TextIO
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.my_csv_file.close()


    def __init__(self, fileurl):
        # Initialize any resources you need here
        self.filepath = fileurl
        rr = open(self.filepath, "r")
        if rr.readline().strip():
            rr.seek(0)


        self.my_csv_file = rr
        self.reader = DictReader(self.my_csv_file)

    def __iter__(self) -> Iterator[Dict[str, str]]:
        return self
    def __next__(self) -> Dict[str, str]:
        return next(self.reader)
    
    def __enter__(self):
        #print("i am going to enter")
        return self

class Misc:
    months : List[str] = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    col_max_temp_name : str = "Max TemperatureC"
    col_min_temp_name : str = "Min TemperatureC"
    col_min_humidity_name : str = " Min Humidity"
    col_mean_humidity_name : str = " Mean Humidity"
    col_date_name : str = "PKT"
    

    year : int = 0
    mode = ""
    yearinfo = ""
    data_dir_path : str = ""
    def set_path(self, datapath):
        self.data_dir_path = datapath
        
    def __init__(self) -> None:
        pass
    
    def check_path() -> bool:
        return True

    def get_file_name(self, month_name):
        file_ = f"lahore_weather_{self.yearinfo}_{month_name}.txt"
        full_file_name = f"{self.data_dir_path}\\{file_}"

        return full_file_name
    def get_filename_from_year_month(self):
        year = self.yearinfo[:4]
        month_num = int(self.yearinfo[5:])
        file_ = f"lahore_weather_{year}_{self.months[month_num-1]}.txt"
        full_file_name = f"{self.data_dir_path}\\{file_}"
        return full_file_name
        

def testing(ms : Misc):
    print("hello", ms.months[0])

class ClimateAnalytics:
#handles -e switch
    def annual_climate_summary(self, data : Misc):
        max_temp = {'val': 0, 'date': ''}
        min_temp = {'val': 0, 'date': ''}
        most_humid = {'val': 0, 'date': ''}
        baseline_set = False
        
        for month in data.months:
            
            full_file_name = data.get_file_name(month)
            #check if file exists before moving to open it:
            if not os.path.exists(full_file_name):
                print(f"file {full_file_name} does not exist")
                continue
            with mycsv(full_file_name) as myfile:
            #for line in csvlines[1:]:
                for row in myfile:
                    #want to check if the line is empty
                    if row[data.col_max_temp_name] == None:
                        continue

                    row_max_temp = row[data.col_max_temp_name]
                    row_min_temp = row[data.col_min_temp_name]
                    row_max_humidity = row[data.col_min_humidity_name]
                    row_datevalue = row[data.col_date_name]

                    if not baseline_set:
                        """max_temp = int(line[col_max_temp])
                        min_temp = int(line[col_min_temp])
                        most_humid = int(line[col_humidity])
                        """
                        if not row_max_temp.isdigit():
                            continue #we cant set base data until we find a valid data, we cant initialize with zeros either, it has to be real data
                        max_temp['val'] = int(row_max_temp)
                        min_temp['val'] = int(row_min_temp)
                        most_humid['val'] = int(row_max_humidity)
                        max_temp['date'] = min_temp['date'] = most_humid['date'] = row_datevalue
                        

                        baseline_set = True
                    else:
                        if (row_max_temp.isdigit() and int(row_max_temp) > max_temp["val"]):
                            max_temp["val"] = int(row_max_temp)
                            max_temp["date"] = row_datevalue
                        if (row_min_temp.isdigit() and int(row_min_temp) < min_temp["val"]):
                            min_temp["val"] = int(row_min_temp)
                            min_temp["date"] = row_datevalue
                        if (row_max_humidity.isdigit() and int(row_max_humidity) > most_humid["val"]):
                            most_humid["val"] = int(row_max_humidity)
                            most_humid["date"] = row_datevalue
            
        #print(f"max temp for year {year} are follows:")
        print(f"Highest {max_temp['val']}C on {max_temp['date']}")
        print(f"Lowest {min_temp['val']}C, on {min_temp['date']}")
        print(f"Humid {most_humid['val']}%, on {most_humid['date']}")

    #handles -a switch
    def monthly_average_conditions(self, data : Misc):
        file_ = data.get_filename_from_year_month()
        print(f"file: {file_}")
        highest_temp_sum = 0
        lowest_temp_sum = 0
        humidity_sum = 0
        count = 0
        #for line in csvlines[1:]:
        with mycsv(file_) as myfile: 
            for line in myfile:
                #want to check if the line
                if line[data.col_max_temp_name] == None: #len(row) != 23:
                        continue

                if len(line) != 23:
                    continue
                high_temp = int(line[data.col_max_temp_name]) if line[data.col_max_temp_name].isdigit() else 0
                low_temp = int(line[data.col_min_temp_name]) if line[data.col_min_temp_name].isdigit() else 0
                humidity = int(line[data.col_mean_humidity_name]) if line[data.col_mean_humidity_name] else 0
                #add to sums
                highest_temp_sum += high_temp
                lowest_temp_sum += low_temp
                humidity_sum += humidity
                count += 1

        #results
        print(f"Highest Average : {round(highest_temp_sum/count,0)}C")
        print(f"Lowest Average : {round(lowest_temp_sum/count,0)}C")
        print(f"Humidity Average : {round(humidity_sum/count,0)}%")

    def getDayNum(self, date):
        return date.split("-")[-1]

    def draw_temperature_barcharts(self, data : Misc, twolines):
        
        print(f"{data.months[int(data.yearinfo[5:])-1]} {data.yearinfo[:4]}")
        with mycsv(data.get_filename_from_year_month()) as myfile:
            for line in myfile:
                if line[data.col_max_temp_name] == None:
                    continue

                high_temp = int(line[data.col_max_temp_name]) if line[data.col_max_temp_name].isdigit() else 0
                low_temp = int(line[data.col_min_temp_name]) if line[data.col_min_temp_name].isdigit() else 0
                dayNum = getDayNum(line[data.col_date_name])
                if not twolines: # 1 line signs
                    print(f"{dayNum} {termcolor.colored('+'*low_temp, 'blue')}{termcolor.colored('+'*high_temp, 'red')} {low_temp}C - {high_temp}C")
                else: #2 lines signs
                    print(f"{dayNum} {termcolor.colored('+'*high_temp, 'red')} {high_temp}C")
                    print(f"{dayNum} {termcolor.colored('+'*low_temp, 'blue')} {low_temp}C")


def select_functionality2(args):
    data = Misc()
    data.yearinfo = args.point_in_time
    data.data_dir_path = args.data_path;

    climatestuff = ClimateAnalytics()    
    if args.mode == "e":
        climatestuff.annual_climate_summary(data)
    elif args.mode == 'a':
        climatestuff.monthly_average_conditions(data)
    elif args.mode == 'c':
        climatestuff.draw_temperature_barcharts(data, True)
    elif args.mode == 'd':
        climatestuff.draw_temperature_barcharts(data, False)
    else:
        print("functionality not found.")
        sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(description='weather manager!')
    parser.add_argument('mode',choices=['e', 'a', 'c', 'd'], help='type of function to execute.')
    parser.add_argument('point_in_time', help='year or year/month')
    parser.add_argument('data_path', help='path of data files')

    return parser.parse_args()

ff = parse_arguments()

select_functionality2(ff)



