import csv
import os

import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.corpus import stopwords
import requests
from bs4 import BeautifulSoup
import nltk

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vaderModuleFound = True
except:
    vaderModuleFound = False


nltk.download('stopwords')

nltk_data_custom = os.path.dirname(os.path.abspath(__file__)) +\
    os.path.sep + 'nltk_data' + os.path.sep + 'corpora' + os.path.sep +\
    'stopwords' + os.path.sep + 'custom'

custom_stopwords = []
with open(nltk_data_custom, 'r') as f:
    for line in f:
        for word in line.split():
            custom_stopwords.append(word)

stopwords = set(stopwords.words('english')).union(custom_stopwords)

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


def set_session_parameters(debug_mode=False):
    if debug_mode:
        url = "https://incels.co/forums/inceldom-discussion.2/"
        ui = True
        max_pages = 9999
    else:
        try:
            url = input("What is the URL for the discussion site: ")
            if url == "":
                url = "https://incels.co/forums/inceldom-discussion.2/"

            ui_ans = input("Do you want ui (y/n): ")
            if ui_ans == 'y':
                ui = True
            elif ui_ans == 'n':
                ui = False
            else:
                raise ValueError('Not valid')

            max_pages = int(input("Set max page depth: "))

        except BaseException:
            url, ui, max_pages = set_session_parameters()

        if isinstance(
                ui, bool) and isinstance(
                    max_pages, int) and max_pages >= 1:
            pass
        else:
            url, ui, max_pages = set_session_parameters()

    return url, ui, max_pages


def get_topics(url="", debug_mode=False):
    if url == "" or debug_mode:
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

            # Get topic prefix id
            prefix_start = 'value="'
            prefix_end = '">'
            prefix_id = str_opt[str_opt.find(
                prefix_start) + len(prefix_start):str_opt.rfind(prefix_end)]

            topics_dict[prefix_id] = topic

    return topics_dict


def select_topic(topics_dict, debug_mode=False):
    if not debug_mode:
        print("The available topics are:")
        for key in topics_dict:
            print('\t', key, topics_dict[key])
        topic_id = input("Which topic would you like to scrape: ")
    else:
        topic_id = "1"

    ret = topics_dict[topic_id]
    print("you've selected: ", ret)

    return topic_id, ret

############## Scraping Procedures ##############


def scrape_topic_headers(
        base_url,
        topic_id,
        topic,
        max_pages=9999,
        debug_mode=False):
    if debug_mode:
        num_pages = 2
    else:
        try:
            num_pages = get_number_of_topic_pages(base_url, topic_id, topic)
        except BaseException:
            num_pages = 1
        num_pages = min(num_pages, max_pages)

    words = []
    df_fin = pd.DataFrame()
    for ii in range(1, num_pages + 1):
        page_id = str(ii)
        print("Scraping page", page_id, "/", num_pages, "on", topic)
        # progress = int(page_id) / int(num_pages) * 100
        # print(topic, 'scraping progress [%d%%]\r'%progress, end="")
        # if progress == 100:
        #     print("")

        words += scrape_words_of_title(base_url, topic_id, topic, page_id)
        df_entry = df_dict_from_entry(base_url, topic_id, topic, page_id)
        df_fin = pd.concat([df_fin, df_entry], axis=0)
    return words, df_fin


def scrape_words_of_title(base_url, topic_id, topic, page_id):
    page_url = base_url + "page-" + page_id + "?prefix_id=" + topic_id
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'lxml')

    all_words = []
    all_post_urls = []
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

                post_url = base_url + 'threads/' + title_str + '/'
                all_post_urls += [post_url]

        except UnicodeEncodeError:
            pass

    return all_words

def df_dict_from_entry(base_url, topic_id, topic, page_id):
    page_url = base_url + "page-" + page_id + "?prefix_id=" + topic_id
    page = requests.get(page_url)
    soup = BeautifulSoup(page.text, 'lxml')

    if vaderModuleFound:
        analyzer = SentimentIntensityAnalyzer()

    # df_columns=['title', 'url', 'neg', 'neu',
    #             'pos', 'compound', 'time']

    df_frame = pd.DataFrame()

    replies = False
    df_dict = dict()

    for tag in soup.find_all():
        tag_str = str(tag)

        try:
            if '<dt>Replies</dt>' in tag_str:
                replies = True

            if '<div class="structItem-title" uix-data-href=' in tag_str:
                if len(df_dict.keys()) <= 1:
                    df_dict = dict()
                elif vaderModuleFound and len(df_dict.keys()) == 10:
                    df_row = pd.DataFrame.from_dict(df_dict,
                                                    orient='index')
                    df_frame = pd.concat([df_frame,df_row],axis=1)
                    df_dict = dict()

                elif len(df_dict.keys()) == 7:
                    df_row = pd.DataFrame.from_dict(df_dict,
                                                    orient='index')
                    df_frame = pd.concat([df_frame,df_row],axis=1)
                    df_dict = dict()

                title_start = 'uix-data-href="/threads/'
                title_end = '/">'
                title_str = tag_str[tag_str.find(
                    title_start) + len(title_start):tag_str.rfind(title_end)]
                title = title_str.replace('-', ' ').split('.')[0]

                df_dict['title'] = title

            elif'<dd>' in tag_str:
                if replies:
                    r_num = tag_str.split('>')[1].split('<')[0]
                    if not any( e.isdigit() for e in r_num ):
                        continue
                    else:
                        r_num = r_num.replace('K','000')
                        r_num = r_num.replace('M','000000')
                        df_dict["replies"] = float(r_num)
                        replies = False

                else:
                    v_num = tag_str.split('>')[1].split('<')[0]
                    if not any( e.isdigit() for e in v_num ):
                        continue
                    else:
                        v_num = v_num.replace('K','000')
                        v_num = v_num.replace('M','000000')
                        df_dict["views"] = float(v_num)
                        replies = True

            elif '<li><span class="username">' in tag_str:
                uname = tag_str.split("</span></span></li>")[0].split('">')[-1]
                df_dict['op_username'] = uname


            elif 'rel="nofollow"><time class="structItem-latestDate u-dt"' in tag_str:
                time_start = 'data-date-string="'
                time_end = '"'
                time_str = tag_str[tag_str.find(
                    time_start) + len(time_start):tag_str.rfind(time_end)]
                df_dict['date'] = time_str.split('"')[0]

                #just to get them in the right order
                post_url = 'https://incels.co/threads/' + title_str.split('">')[0]
                df_dict['url'] = post_url

                if vaderModuleFound:
                    vs = analyzer.polarity_scores(title)
                    df_dict['neg'] = vs['neg']
                    df_dict['neu'] = vs['neu']
                    df_dict['pos'] = vs['pos']
                    df_dict['compound'] = vs['compound']

        except UnicodeEncodeError:
            pass

    return pd.DataFrame.transpose(df_frame)


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

############## Formating Procedures ##############


def filter_words(words):
    #s = set(stopwords.words('english')).union(set(stopwords.words('custom')))
    s = stopwords
    subset_words = list(filter(lambda w: w not in s, words))
    subset_words = [x for x in subset_words if any(c.isalpha() for c in x)]
    return list(subset_words)


def words_to_wordcloud(words, topic):
    list_words = list(words)
    concat_words = " ".join(list_words)
    wordcloud = WordCloud(width=1200, height=1200,
                          background_color='white',
                          min_font_size=10).generate(concat_words)

    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.title("Topic: " + topic)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)

    plt.savefig('results/' + topic + '_wordcloud.png')


def words_to_csv(words, topic):
    list_words = list(words)
    set_of_words = set(list_words)

    word_count_dict = {}
    for e in set_of_words:
        word_count_dict[e] = list_words.count(e)

    csv_columns = ['Word', 'Count']
    csv_file = 'results/' + topic + "_wordcount.csv"

    try:
        with open(csv_file, 'w') as f:
            for key in word_count_dict.keys():
                f.write("%s,%s\n" % (key, word_count_dict[key]))
    except IOError:
        print("I/O error")
