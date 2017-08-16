# -*- coding:utf-8 -*-
# This version is mainly used for a test. It doesn't have a GUI yet.
import shelve
from getIntern import get_sxs

# Use shelve to get parameter changing rules.
with shelve.open("shelve/para_change_dict") as slvFile:
    city_dict = slvFile["city"]
    salary_dict = slvFile["salary"]
    degree_dict = slvFile["degree"]
    remain_dict = slvFile["remain"]

# Input your requirements for Intern Chances.
keyword = input("Please input A Keyword of Your Interested Intern Chance or Company:\n")

city = input("Please input A City Name for your Internship:\n")

salary = input("Please Input A Number for Salary (￥/Day) ==》\n "
               "0: Don't care;\n"
               "1: 0-50;\n"
               "2: 50-100;\n"
               "3: 100-150;\n"
               "4: 150-200;\n"
               "5: 200-300;\n"
               "6: > 300.\n")

degree = input("Please Input A Number for Minimum Degree Requirement.\n"
               "0: Don't care;\n"
               "1: College;\n"
               "2: Bachelor;\n"
               "3: Master;\n"
               "4: Doctor.\n")

remain = input("Please Input A Number for Whether to Stay or Not After the Internship.\n"
               "0: Don't care;\n"
               "1: Yes;\n"
               "2: No;\n"
               "3: Not Sure.\n")

day = input("Please Input A Number for How Many Days A Week Can You Work:\n"
            "If You Don't Care, Just Type in 0.\n")

month = input("Please Input A Number for How Many Months Can You Keep On Work:\n"
              "If You Don't Care, Just Type in 0.\n")

frequency = input("Please Input A Number for How Often (in hours) Do You Want To Get An Update Reminder.\n")

# Now we change the parameters.
if day == "" or day == "0":
    day = None
if month == "" or month == "0":
    month = None
if frequency == "":
    frequency = 24
city = city_dict[city]
salary = salary_dict[salary]
degree = degree_dict[degree]
remain = remain_dict[remain]

# Now We Check The Inputs.
results = get_sxs(place=city, keyword=keyword, day=day, month=month, salary=salary, degree=degree, remain=remain)
print(results)
