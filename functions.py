from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import cyrtranslit
import regex
from datetime import datetime
import base64
import webbrowser
import os

link_list = []
list_of_paths= []
temp_number= 0
url = "https://www.mod.gov.rs/"
url1 = "https://www.mod.gov.rs/lat"
url2 = "https://www.blic.rs/"


def check_page(url, words,temp_number,path_list):
    link_list.append(url)
    html_contents = urlopen(url).read()
    path_list.append(save_to_temp(html_contents,temp_number))
    soup = bs(html_contents)
    body = soup.body.text.lower()
    if regex.search(r'\p{IsCyrillic}', body) is not None:
        body = cyrtranslit.to_latin(body)
    result = body.find(words)
    body[result] = "<mark>"
    if result >= 0:
        return True
    else:
        return False


# res = check_page(url2, "hronika")
def open_file_update_list(list_of_links):
    try:
        open("links.txt", "x")
    except FileExistsError:
        pass
    finally:
        f = open("links.txt", "r+")
        for link in f:
            list_of_links.append(link)
        f.close()


def save_links(list_of_links):
    try:
        open("links.txt", "x")
    except FileExistsError:
        pass
    finally:
        f = open("links.txt", "w+")
        for link in list_of_links:
            f.writelines(link)
        f.close()


def getting_time():
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")  # formatting
    return dt_string

def save_to_temp(html_contents, temp_num):
    try:
        os.mkdir("tmp")
    except FileExistsError :
        pass
    finally:
        os.chdir("tmp")
        path = os.path.abspath(f"temp{temp_num}.html")
        os.chdir("..")
        with open(path, 'wb') as f:
            f.write(html_contents)
        return path


# html_contents = urlopen(url1).read()
#
# string_byte = html_contents.decode("UTF-8")
#
# string_byte = string_byte.replace("Vučević","<mark>Vučević</mark>")
#
# html_contents = string_byte.encode()
#
# with open("temp0.html", 'wb') as f:
#     f.write(html_contents)
# webbrowser.open("temp0.html")


print()


# check_page(url,"vučičević",0,list_of_paths)
# check_page(url2,"vučičević",1,list_of_paths)
# check_page(url1,"vučičević",2,list_of_paths)

# webbrowser.open(list_of_paths[0])
