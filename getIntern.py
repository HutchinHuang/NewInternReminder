# -*- coding:utf-8 -*-
# A module with functions about getting information from webs and checking updates
import requests
import lxml.html
import lxml
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
        search_url += "x-" + str(degree) + "_"  # salary needs to be replaced
    if remain is not None:
        search_url += "ch-" + str(remain) + "_"
    search_url += "?k={}".format(keyword)
    # There's also a parameter 'P' in the website's URL
    # I don't know what it means now. Maybe you can help by sending me an Issue.
    results = requests.get(search_url).text
    tree = lxml.html.fromstring(results)
    a_elements = tree.cssselect("div.po-name a")
    link_set = set()
    for element in a_elements:
        link_set.add("http://www.shixiseng.com" + element.get("href"))
    return link_set


def test():
    print(get_sxs())


if __name__ == "__main__":
    test()
