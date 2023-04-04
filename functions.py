from urllib.request import urlopen
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
    :return: Result if string is found, if found returns if the string is marked in html
    """
    link_list.append(url)                                               #??
    html_contents = urlopen(url).read()                                 # downloading html page
    string_byte_decoded = html_contents.decode("UTF-8")                 # decoding html page

    # soup = bs(html_contents)
    # body = soup.body.text.lower()
    # if regex.search(r'\p{IsCyrillic}', body) is not None:            #searching for Cyrillic words
    #     body = cyrtranslit.to_latin(body)                             #translating  cyr to latin

    if string_byte_decoded.lower().find(words.lower()) >= 0:             # checking if words exist in text
        marked = True                                                    # setting that word is marked when displayed
        string_to_encode = mark_string(string_byte_decoded, words)
        if string_to_encode == string_byte_decoded:
            marked = False                                            # checking if it is really marked and saving value
        html_contents = string_to_encode.encode()
        path_list.append(save_to_temp(html_contents, temp_number))        # saving html page to temp and saving path
        return True, marked
    else:
        return False, None


def open_file_update_list(list_of_links: list):
    """
    Updates list of links to search from.
    :param list_of_links: List to update.
    :return: Nothing.
    """
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
    """
    Saves links to txt file.
    :param list_of_links: List that gets saved to file.
    :return: Nothing.
    """
    try:
        open("links.txt", "x")                          # creating txt file to save links to
    except FileExistsError:
        pass
    finally:
        f = open("links.txt", "w+")
        for link in list_of_links:
            f.writelines(link)
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
    string_for_return = string_for_marking.replace(" " + words + " ", f"<mark>{words}</mark>")  # marking words
    string_for_return = string_for_return.replace(" " + words.capitalize() + " ", f"<mark>{words.capitalize()}</mark>")
    string_for_return = string_for_return.replace(" " + words.lower() + " ", f"<mark>{words.lower()}</mark>")
    string_for_return = string_for_return.replace(" " + words.upper() + " ", f"<mark>{words.upper()}</mark>")
    return string_for_return

# a, b = check_page(url, "Vučević", 0, list_of_paths)
# a, b = check_page(url2, "Vučević", 1, list_of_paths)
# a, b = check_page(url1, "Vučević", 2, list_of_paths)

# webbrowser.open(list_of_paths[0])
