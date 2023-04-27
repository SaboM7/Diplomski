from urllib.request import urlopen
from urllib.request import Request
from pathlib import Path
from bs4 import BeautifulSoup as bs
import cyrtranslit
import regex
from datetime import datetime
import base64
import webbrowser
import os

link_list = []
list_of_paths = []
temp_number = 0
url = "https://www.mod.gov.rs/"
url1 = "https://www.mod.gov.rs/lat"
url2 = "https://www.blic.rs/"


def check_page(url: str, words: str, temp_number: int, path_list: list):
    """
    Checks page if it contains string, then it tries to mark string in html and saves it to temp.
    :param url: URL that you want to search on
    :param words: string that you search
    :param temp_number: number of temp file
    :param path_list: list of paths to save path on
    :return: Result if string is found and if the page has marked words and if page has Cyrilic characters
    """
    match = True
    # link_list.append(url)                                               #??
    req = Request(url, headers={'User-Agent': "Magic Browser"})
    html_contents = urlopen(req).read()
    string_byte_decoded = html_contents.decode("UTF-8")                 # decoding html page

    if regex.search(r'\p{IsCyrillic}', words) is not None :
        temp_words = cyrtranslit.to_latin(words)                            # convert words to latin if cyr
    else:
        temp_words = cyrtranslit.to_cyrillic(words)                         # convert words to cyr if latin
    cyr_flag = regex.search(r'\p{IsCyrillic}', string_byte_decoded) is not None

    if string_byte_decoded.lower().find(" "+words.lower()) >= 0 :     # checking if words exist in text
        marked = encoding_saving_marking(string_byte_decoded, words, path_list, temp_number)
        return match, marked, cyr_flag
    elif string_byte_decoded.lower().find(" "+temp_words.lower()) >= 0:
        marked = encoding_saving_marking(string_byte_decoded, temp_words, path_list, temp_number)
        return match, marked, cyr_flag
    else:
        match = False
        marked = False
        return match, marked, cyr_flag


def encoding_saving_marking(string_to_encode_: str, words: str, path_list: list, temp_number: int):
    """
    Reduces code repetition in my functions.
    :param string_to_encode_: String to encode
    :param words: String to mark
    :param path_list: List of paths to temp pages
    :param temp_number: Number of temp page
    :return: True if words are marked, false if not
    """
    marked = True
    string_to_encode = mark_string(string_to_encode_, words)
    if string_to_encode == string_to_encode_:
        marked = False                                          # checking if it is really marked and saving value
    html_contents = string_to_encode.encode()
    path_list.append(save_to_temp(html_contents, temp_number))  # saving html page to temp and saving path
    return marked

def open_file_update_list(list_of_links: list):
    """
    Updates list of links to search from.
    :param list_of_links: List to update.
    :return: Nothing.
    """
    try:
        path = Path(__file__).parent / "links.txt"
        open(path, "x")                                     # creating file if it doesnt exist
    except FileExistsError:
        pass
    finally:
        f = open(path, "r+")
        for link in f:
            list_of_links.append(link)
        f.close()


def save_links(list_of_links):
    """
    Saves links to txt file.
    :param list_of_links: List that gets saved to file.
    :return: Nothing.
    """
    try:
        path = Path(__file__).parent / "links.txt"
        open(path, "x")                         # creating txt file to save links to
    except FileExistsError:
        pass
    finally:
        f = open(path, "w")
        for link in list_of_links:
            if not link.endswith("\n"):
                link = link +"\n"
            f.write(link)
        f.close()


def getting_time():
    """
    Getting formatted string of time.
    :return: String containing time.
    """
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")               # formatting
    return dt_string


def save_to_temp(html_contents: bytes, temp_num):
    """
    Saving html page in bytes to temp file.
    :param html_contents: Html page in bytes.
    :param temp_num: Number of temp file.
    :return: Path to them file that page is saved to.
    """
    try:
        os.mkdir("tmp")                                     # making temp directory if it doesnt exist
    except FileExistsError:
        pass
    finally:
        os.chdir("tmp")
        path = os.path.abspath(f"temp{temp_num}.html")      # creating path
        os.chdir("..")
        with open(path, 'wb') as f:                         # opening file
            f.write(html_contents)                          # saving page to file
        return path


def mark_string (string_for_marking: str, words: str):
    """
    Marking string in html page.
    :param string_for_marking:
    :param words: String to mark.
    :return: Marked string.
    """
    string_for_return = string_for_marking.replace(" " + words + " ", f" <mark>{words}</mark> ")  # marking words
    string_for_return = string_for_return.replace(" " + words.capitalize() + " ", f" <mark>{words.capitalize()}</mark> ")
    string_for_return = string_for_return.replace(" " + words.lower() + " ", f" <mark>{words.lower()}</mark> ")
    string_for_return = string_for_return.replace(" " + words.upper() + " ", f" <mark>{words.upper()}</mark> ")
    return string_for_return


# print(getting_time())
# open_file_update_list(link_list)
# for i,link in enumerate(link_list,0) :
#     a,b,c= check_page(link,"vučević",len(list_of_paths),list_of_paths)
#     print(f"{a} {b} {c}")
# for path in list_of_paths :
#     webbrowser.open(path)
#
# save_links(link_list)

# req = Request("https://www.politika.rs/sr", headers={'User-Agent' : "Magic Browser"})
# html_contents = urlopen( req )
# html_contents = urlopen("https://www.politika.rs/sr").read()
# with open("test.html", 'wb') as f:  # opening file
#     f.write(html_contents)
# webbrowser.open("test.html")

# a, b, c = check_page(url, "вучевић", 0, list_of_paths)
# a, b, c = check_page(url2, "vučević", 1, list_of_paths)
# a, b, c = check_page(url1, "vučević", 2, list_of_paths)
#
# webbrowser.open(list_of_paths[0])
# webbrowser.open(list_of_paths[1])
