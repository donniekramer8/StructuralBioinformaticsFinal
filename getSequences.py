from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup
import re
import time

# open firefox
firefox_path = FirefoxBinary(
    '/Applications/Firefox.app/Contents/MacOS/firefox')
browser = webdriver.Firefox(firefox_binary=firefox_path)

# get html from website
# website is new entries of on PDB
browser.get(
    "https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_accession_info.initial_release_date%22%2C%22operator%22%3A%22greater_or_equal%22%2C%22value%22%3A%222023-03-15T00%3A00%3A00Z%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%221221ebeea841216759cfba7bd5a0e59c%22%7D%7D"
)


def get_acc_numbers() -> list:
    html = browser.page_source

    # make soup object
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(10)

    tag_contents = []  # 4 letter alpha-numeric digits within <a> tags of html

    for tag in soup.find_all('a', string=re.compile(r"[A-Za-z0-9]")):
        if len(tag.contents[0]) == 4:
            print(tag.contents)
            tag_contents.append(tag.contents[0])

    # some 4 letter contents in 'a' tags are not accession numbers, but
    # tag_contents[5:29] are all of the accession numbers on the page
    return tag_contents[5:29]


def update_pdb_page():
    browser.get(
        "https://www.rcsb.org/search?request=%7B%22query%22%3A%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22type%22%3A%22group%22%2C%22nodes%22%3A%5B%7B%22parameters%22%3A%7B%22attribute%22%3A%22rcsb_accession_info.initial_release_date%22%2C%22operator%22%3A%22greater_or_equal%22%2C%22value%22%3A%222023-03-15T00%3A00%3A00Z%22%7D%2C%22type%22%3A%22terminal%22%2C%22service%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%5D%2C%22logical_operator%22%3A%22and%22%2C%22label%22%3A%22text%22%7D%5D%2C%22logical_operator%22%3A%22and%22%7D%2C%22return_type%22%3A%22entry%22%2C%22request_options%22%3A%7B%22paginate%22%3A%7B%22start%22%3A0%2C%22rows%22%3A25%7D%2C%22results_content_type%22%3A%5B%22experimental%22%5D%2C%22sort%22%3A%5B%7B%22sort_by%22%3A%22score%22%2C%22direction%22%3A%22desc%22%7D%5D%2C%22scoring_strategy%22%3A%22combined%22%7D%2C%22request_info%22%3A%7B%22query_id%22%3A%221221ebeea841216759cfba7bd5a0e59c%22%7D%7D"
    )


def get_uniprot_num(pdb_num):
    website = "https://www.rcsb.org/sequence/" + str(pdb_num)
    print(website)
    browser.get(website)
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    # with open('uniprot.txt', 'w') as f:
    #     f.write(soup.prettify())


if __name__ == '__main__':
    pdb_acc_nums = []
    for _ in range(1):
        pdb_acc_nums = pdb_acc_nums + get_acc_numbers()
    print(pdb_acc_nums)

    file_name_prefix = 'https://files.rcsb.org/view/'
    file_name_suffix = '.cif'
    files_names = []
    for i in pdb_acc_nums:
        files_names.append(file_name_prefix + i + file_name_suffix)

    print(files_names)
