# -*- coding:utf-8 -*-
# A small script to get the city-code in shixiseng.com and use shelve module to save all the parameters' change rules.
import re
import requests
import shelve


def get_city_code():
    """
    This Function is used to get the names and codes of the cities supported by shixiseng.com.
    :return: A dictionary with all city names as its key and corresponding city codes as its value.
    """
    html = requests.get("http://www.shixiseng.com/interns/").text
    name_code_tuple = re.findall(r'<dd class="city_btn" data-val="(.+?)" *?>(.+?)</dd>', html)
    name_code_dict = {name_code_tuple[i][1]: name_code_tuple[i][0] for i in range(len(name_code_tuple))}
    name_code_dict["全国"] = None
    name_code_dict[""] = None  # If the input is "", It should be None.
    return name_code_dict


# Then we use three other dicts to set the rules for changing parameters.
salary_dict = {
    "": None,
    "0": None,
    "1": "0,50",
    "2": "50,100",
    "3": "100,150",
    "4": "150,200",
    "5": "200,300",
    "6": "300,0"
}

degree_dict = {
    "": None,
    "0": None,
    "1": "dazhuan",
    "2": "benke",
    "3": "shuoshi",
    "4": "boshi"
}

remain_dict = {
    "": None,
    "0": None,
    "1": "entry",
    "2": "noentry",
    "3": "notsure"
}

day_dict = {
    "0": None,
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5"
}

month_dict = {
    "0": None,
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "8",
    "8": "10",
    "9": "12"
}

frequency_dict = {
    "0": 1,
    "1": 3,
    "2": 7
}

if __name__ == "__main__":
    city_dict = get_city_code()
    for key in city_dict:
        print("'" + key + "'", end=", ")
    with shelve.open("shelve/para_change_dict") as slv:
        slv["city"] = city_dict
        slv["salary"] = salary_dict
        slv["degree"] = degree_dict
        slv["remain"] = remain_dict
        slv["day"] = day_dict
        slv["month"] = month_dict
        slv["frequency"] = frequency_dict
