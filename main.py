import matplotlib.pyplot as plt
import incel_scraper as islib  # Glorious abbriviation
import os

db_mode = False
UI = False


def main():
    if not os.path.exists('results'):
        os.makedirs('results')

    # command line prompt as UI to set parameters
    # islib.start_up_prompt()
    # discussion_url = islib.get_discussion_url()
    discussion_url = "https://incels.co/forums/inceldom-discussion.2/"

    topics = islib.get_topics()
    topic_id, topic = islib.select_topic(topics, debug_mode=db_mode)

    if UI:
        a = islib.scrape_topic_headers(
            discussion_url,
            topic_id,
            topic,
            debug_mode=db_mode)
    else:
        for t_id in topics:
            a = islib.scrape_topic_headers(
                discussion_url,
                t_id,
                topics[t_id],
                debug_mode=db_mode)

    print(a)

    # islib.get_prefixes(discussion_url)

    # procedures to scrape in specified manner

    # structuring of data into desired data format

    # visualization of results

    # storing of structured data and resulting plots


main()
