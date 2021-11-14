
import math
import os
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.npyio import load
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from matplotlib import pyplot as plt

def load_data():
    screen_ranges = []
    with open('screentime.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
         for row in spamreader:
             start_time = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S %z")
             end_time = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S %z")
             start_time = start_time.astimezone(ZoneInfo("America/New_York"))
             end_time = end_time.astimezone(ZoneInfo("America/New_York"))
             screen_ranges.append([start_time, end_time])
    
    return screen_ranges

def total_time_days(screen_ranges):
    total_times = []
    days = []
    day_count = 10
    start_date = datetime.strptime("2021-11-7", "%Y-%m-%d")
    start_date = start_date.astimezone(ZoneInfo("America/New_York"))
    for single_date in (start_date + timedelta(n) for n in range(day_count)):
        total_time = 0
        for time_range in screen_ranges:
            if (same_day(single_date, time_range[0]) and same_day(single_date, time_range[1])): # time range fully in day
                total_time += (time_range[1] - time_range[0]) / timedelta(hours=1)
            elif (same_day(single_date, time_range[0])): # start at start time, end at midnight
                total_time += ((single_date + timedelta(1)) - time_range[0]) / timedelta(hours=1)
            elif (same_day(single_date, time_range[1])): # start at midnight, end at end time
                # print((time_range[1] - single_date) / timedelta(hours=1))
                # print(time_range[1])
                # print(single_date)
                total_time += (time_range[1] - single_date) / timedelta(hours=1)
        total_times.append(total_time)
        days.append(single_date.day)
    return total_times, days

def same_day(day_1, day_2):
    if (day_1.day == day_2.day and day_1.month == day_2.month and day_1.year == day_2.year):
        return True
    return False


def main():
    times, days = total_time_days(load_data())
    plt.bar(days, times)
    plt.legend(["Hours of Screen Time"])
    plt.xlabel("Day")
    plt.ylabel("Screen Times")
    plt.title("Screen Time by Day")
    plt.savefig("screentime.png")
    plt.close()


if __name__ == "__main__":
    main()