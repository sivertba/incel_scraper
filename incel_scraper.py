import header
# import urllib.request
import requests
from bs4 import BeautifulSoup

############## User Interface Procedures ##############


def start_up_prompt():
    print(" ____  _  _  ___  ____  __                 ")
    print("(_  _)( \\( )/ __)( ___)(  )                ")
    print(" _)(_  )  (( (__  )__)  )(__               ")
    print("(____)(_)\\_)\\___)(____)(____)              ")
    print(" ___   ___  ____    __    ____  ____  ____ ")
    print("/ __) / __)(  _ \\  /__\\  (  _ \\( ___)(  _ \\")
    print("\\__ \\( (__  )   / /(__)\\  )___/ )__)  )   /")
    print("(___/ \\___)(_)\\_)(__)(__)(__)  (____)(_)\\_)")
    print("                                           ")


def get_discussion_url():
    return input("What is the URL for the discussion site: ")


def get_topics(url="", debug_mode=False):
    if url == "" or debug_mode:
        print("No URL provided!")
        url = "https://incels.co/forums/inceldom-discussion.2/"
        print("Using: ", url)

    filter_page = requests.get(url + "filters")

    soup = BeautifulSoup(filter_page.text, 'lxml')

    # a = soup.find_all("select", name="prefix_id")
    topics_dict = {}
    for opt in soup.find_all('option'):
        str_opt = str(opt)
        if "prefix" in str_opt:

            # Get topic name
            topic_start = '['
            topic_end = ']'
            topic = str_opt[str_opt.find(
                topic_start) + len(topic_start):str_opt.rfind(topic_end)]
            # print(topic)

            # Get topic prefix id
            prefix_start = 'value="'
            prefix_end = '">'
            prefix_id = str_opt[str_opt.find(
                prefix_start) + len(prefix_start):str_opt.rfind(prefix_end)]

            topics_dict[prefix_id] = topic

    return topics_dict


def select_topic(topics_dict, debug_mode=False):
    print("The available topics are:")
    for key in topics_dict:
        print('\t', key, topics_dict[key])

    if not debug_mode:
        topic_id = input("Which topic would you like to scrape: ")
    else:
        topic_id = "1"

    ret = topics_dict[topic_id]
    print("you've selected: ", ret)

    return topic_id, ret

############## Scraping Procedures ##############


def scrape_topic_headers(base_url, topic_id, topic, debug_mode=False):
    if debug_mode:
        num_pages = 1
    else:
        num_pages = get_number_of_topic_pages(base_url, topic_id, topic)

    words = []
    for ii in range(1,num_pages+1):
        page_id = str(ii)
        print("Scraping page", page_id,"/",num_pages, "on", topic)
        words += scrape_words_on_page(base_url, topic_id, topic, page_id)

    return words


def scrape_words_on_page(base_url, topic_id, topic, page_id):
    page_url = base_url + "page-" + page_id + "?prefix_id=" + topic_id
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'lxml')

    all_words = []
    all_post_urls =[]
    for tag in soup.find_all('a', href=True):
        tag_str = str(tag)

        try:
            if 'data-preview-url' in tag_str:
                title_start = 'data-preview-url="/threads/'
                title_end = '/preview'
                title_str = tag_str[tag_str.find(
                    title_start) + len(title_start):tag_str.rfind(title_end)]
                title = title_str.replace('-', ' ').split('.')[0]

                words = title.split(' ')
                all_words += words

                post_url = base_url+'threads/'+title_str+'/'
                all_post_urls += [post_url]

        except UnicodeEncodeError:
            pass

    return all_words



def get_number_of_topic_pages(base_url, topic_id, topic):
    topic_page = requests.get(base_url + "?prefix_id=" + topic_id)
    soup = BeautifulSoup(topic_page.text, 'lxml')

    for tag in soup.find_all('a', href=True):
        tag_str = str(tag)

        try:
            if 'pageNavSimple-el pageNavSimple-el--last' in tag_str:
                num_start = 'page-'
                num_end = '?prefix'
                num_str = tag_str[tag_str.find(
                    num_start) + len(num_start):tag_str.rfind(num_end)]
                num_pages = int(num_str)
        except UnicodeEncodeError:
            pass

    return num_pages
