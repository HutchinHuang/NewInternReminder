# -*- coding:utf-8 -*-
# A module with functions about getting information from webs and checking updates
import requests
import re
import time
__all__ = ["get_sxs"]


def get_sxs(place=None, keyword="python", day=None, month=None, salary=None, degree=None, remain=None):
    """
    This function is used to get infomation from shixiseng.com according to your selected conditions.
    :param place: The place where the intern chances is located.
    :param keyword: Type(s) of the intern chances or Name of certain company
    :param day: How many days a week are required, which also means how many days a week can you spare for internship.
    :param month: How many month does the internship period takes.
    :param salary: How much(￥) Per Day do you want to earn from the internship
    :param degree: The minus academic degree that the intern chance requires.
    :param remain: Whether possible or not for you to stay in the company as a full-time worker after this internship.
    :return: URLs of every searching results, in the form of a Python Set.
    """
    # Firstly, use dictionaries to change the input numbers into correct form that can be used in the search_url.

    # Then, modify the search_url according to those input numbers.
    search_url = "http://www.shixiseng.com/interns/"
    if place is not None:
        search_url += "c-" + str(place) + "_"  # "place" needs to be replaced after input
    if salary is not None:
        search_url += "s-" + str(salary) + "_"  # salary also needs to be replaced
    if day is not None:
        search_url += "d-" + str(day) + "_"
    if month is not None:
        search_url += "m-" + str(month) + "_"
    if degree is not None:
        search_url += "x-" + str(degree) + "_"  # degree needs to be replaced
    if remain is not None:
        search_url += "ch-" + str(remain) + "_"  # remain needs to be replaced
    search_url += "?k={}".format(keyword)
    # Besides, there's also a parameter 'P' in the website's URL
    # It means "Pages of Searching Results" if there is more than one page.
    # So we should judge at first whether there's more than one page of results:
    results = requests.get(search_url).text
    a = re.search(r'(\d+?)">尾页', results)
    if a is None:  # Now there is only one page.
        intern_href = re.findall(r'"(/intern.+?)"', results)
        link_set = set()
        for element in intern_href:
            link_set.add("http://www.shixiseng.com" + element)
    else:  # Now there is more than one page.
        page_num = int(a.group(1))
        link_set = set()
        for page in range(page_num):
            search_url_page = search_url + "&p={}".format(page)
            results = requests.get(search_url_page).text
            intern_href = re.findall(r'"(/intern/.+?)"', results)
            for element in intern_href:
                link_set.add("http://www.shixiseng.com" + element)
            time.sleep(1)
    return link_set


def test():
    print(get_sxs(place=110100, day=3))

if __name__ == "__main__":
    test()
