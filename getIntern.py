# -*- coding:utf-8 -*-
# A module with functions about getting information from webs and checking updates
import requests
import re
import time
import shelve
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

__all__ = ["get_sxs", "send_mail"]


def get_sxs(place=None, keyword="python", day=None, month=None, salary=None, degree=None, remain=None):
    """
    This function is used to get newly-posted infomation from shixiseng.com according to your selected conditions.
    :param place: The place where the intern chances is located.
    :param keyword: Type(s) of the intern chances or Name of certain company
    :param day: How many days a week are required, which also means how many days a week can you spare for internship.
    :param month: How many month does the internship period takes.
    :param salary: How much(￥) Per Day do you want to earn from the internship
    :param degree: The minus academic degree that the intern chance requires.
    :param remain: Whether possible or not for you to stay in the company as a full-time worker after this internship.
    :return: URLs of newly_posted internship chance, in the form of a Python Set.
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

    # Try to open the shelve file and get the old_set;
    try:
        slv_file = shelve.open(r"shelve/old_set")
        old_set = slv_file["old_set"]
    except KeyError:  # The first time get_sxs is called, there will be no shelve file, so the old_set is set to be "set()".
        old_set = set()
    finally:
        slv_file.close()

    # Update the old_set with the new searching results
    with shelve.open(r"shelve/old_set") as slv:
        slv["old_set"] = link_set
    return link_set - old_set


def send_mail(title, content, from_nick, from_name, from_code, to_nick, to_name):
    flag = True  # A flag to mark whether the e-mail has been sent successfully
    try:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = formataddr([from_nick, from_name])
        msg['To'] = formataddr([to_nick, to_name])
        msg['Subject'] = title

        server = smtplib.SMTP("smtp.163.com", 25)
        server.login(from_name, from_code)  # from_code needs to be set via mail service's website
        server.sendmail(from_name, to_name, msg.as_string())
        server.quit()
    except:
        flag = False
    return flag


def test():
    print(get_sxs(place=110100, day=3))

if __name__ == "__main__":
    test()
