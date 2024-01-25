import sys
import csv
import os
import termcolor

data_files_path = ""
#  months array
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
col_max_temp = 1
col_min_temp = 3
col_humidity = 7

def read_csv(filename):
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        lines = [line for line in csv_reader]
        
    return lines

#handles -e switch
def stats_yearly(year):
    global data_files_path
    max_temp = {'val': 0, 'date': ''}
    min_temp = {'val': 0, 'date': ''}
    most_humid = {'val': 0, 'date': ''}
    baseline_set = False
    for month in months:
        file_ = f"lahore_weather_{year}_{month}.txt"
        full_file_name = f"{data_files_path}\\{file_}"
        #print(f"file should be {full_file_name}")
        csvlines = read_csv(full_file_name)
        for line in csvlines[1:]:
            if len(line) != 23:
                #print(f"skipping line {line} because it is not 23 long")
                continue
            #print("line length is "+str(len(line)))
            #print("max temp is " + line[col_max_temp])
            if not baseline_set:
                """max_temp = int(line[col_max_temp])
                min_temp = int(line[col_min_temp])
                most_humid = int(line[col_humidity])
                """
                max_temp['val'] = int(line[col_max_temp])
                min_temp['val'] = int(line[col_min_temp])
                most_humid['val'] = int(line[col_humidity])
                max_temp['date'] = line[0]
                min_temp['date'] = line[0]
                most_humid['date'] = line[0]

                baseline_set = True
            else:
                if (line[col_max_temp].isdigit() and int(line[col_max_temp]) > max_temp["val"]):
                    max_temp["val"] = int(line[col_max_temp])
                    max_temp["date"] = line[0]
                if (line[col_min_temp].isdigit() and int(line[col_min_temp]) < min_temp["val"]):
                    min_temp["val"] = int(line[col_min_temp])
                    min_temp["date"] = line[0]
                if (line[col_humidity].isdigit() and int(line[col_humidity]) > most_humid["val"]):
                    most_humid["val"] = int(line[col_humidity])
                    most_humid["date"] = line[0]
        
    #print(f"max temp for year {year} are follows:")
    print(f"Highest {max_temp['val']}C on {max_temp['date']}")
    print(f"Lowest {min_temp['val']}C, on {min_temp['date']}")
    print(f"Humid {most_humid['val']}%, on {most_humid['date']}")

#converts the passed file related info to a filename and returns    
def getFile(year_month, data_location):
    year = year_month[:4]
    month_num = int(year_month[5:])
    file_ = f"lahore_weather_{year}_{months[month_num-1]}.txt"
    full_file_name = f"{data_location}\\{file_}"
    return full_file_name

#handles the -a switch (averages of month)
def stats_yearmonth_avrg(year_month, data_location):
    file_ = getFile(year_month, data_location)
    print(f"file: {file_}")
    csvlines = read_csv(file_)
    highest_temp_sum = 0
    lowest_temp_sum = 0
    humidity_sum = 0
    count = 0
    for line in csvlines[1:]:
        if len(line) != 23:
            continue
        high_temp = int(line[col_max_temp])
        low_temp = int(line[col_min_temp])
        humidity = int(line[col_humidity])
        highest_temp_sum += high_temp
        lowest_temp_sum += low_temp
        humidity_sum += humidity
        count += 1

    print(f"Highest Average : {round(highest_temp_sum/count,0)}C")
    print(f"Lowest Average : {round(lowest_temp_sum/count,0)}C")
    print(f"Humidity Average : {round(humidity_sum/count,0)}%")

def draw_graph(year_month, data_location, twolines):
    
    csvlines = read_csv(getFile(year_month, data_location))
    count = 1
    for line in csvlines[1:]:
        if len(line) != 23:
            continue
        high_temp = int(line[col_max_temp])
        low_temp = int(line[col_min_temp])
        if not twolines: # 1 line signs
            print(f"{count} {termcolor.colored('+'*high_temp, 'red')}{termcolor.colored('+'*low_temp, 'blue')} {low_temp}C - {high_temp}C")
        else: #2 lines signs
          print(f"{count} {termcolor.colored('+'*high_temp, 'red')} {high_temp}C")
          print(f"{count} {termcolor.colored('+'*low_temp, 'blue')} {low_temp}C")

        count+=1


def select_functionality():
    global data_files_path
    # see what args have been passed and which functionality to call
    if len(sys.argv) != 4:
        print(f"{len(sys.argv)} args passed, not good!")

        print("usage: weatherman.py <code> <year/month> <filepath>")
        sys.exit(1)

    data_files_path = sys.argv[3]
    if not os.path.exists(data_files_path):
        print(f"{data_files_path} does not exist! supply a valid directory.")
        sys.exit(1)

    if sys.argv[1] == "-e":
        stats_yearly(sys.argv[2])
    elif sys.argv[1] == "-a":
        stats_yearmonth_avrg(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == "-c":
        draw_graph(sys.argv[2], sys.argv[3], True)
    elif sys.argv[1] == "-d":
        draw_graph(sys.argv[2], sys.argv[3], False)
    else:
        print("usage: weatherman.py <year> <month>")
        sys.exit(1)


select_functionality() # call the function to select the functionality to use.

def read_file():
    print("not implemented buddy!!")


