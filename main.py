import matplotlib.pyplot as plt
import incel_scraper as islib  # Glorious abbriviation
import os

db_mode = False


def main():
    if not os.path.exists('results'):
        os.makedirs('results')

    islib.start_up_prompt()
    discussion_url, UI, max_pages = islib.set_session_parameters(
        debug_mode=db_mode)

    topics = islib.get_topics()

    word_dict = {}
    if UI:
        topic_id, topic = islib.select_topic(
        topics, debug_mode=db_mode)
        words = islib.scrape_topic_headers(
            discussion_url,
            topic_id,
            topic,
            max_pages=max_pages,
            debug_mode=db_mode)
        word_dict[topics[topic_id]] = words
    else:
        for t_id in topics:
            words = islib.scrape_topic_headers(
                discussion_url,
                t_id,
                topics[t_id],
                max_pages=max_pages,
                debug_mode=db_mode)
            word_dict[topics[t_id]] = words

    for t_name in word_dict:
        print("Filtering words from ", t_name)
        filtered_words = islib.filter_words(word_dict[t_name])

        print("counting words from ", t_name)
        islib.words_to_csv(filtered_words, t_name)

        print("Wordclouding words from ", t_name)
        islib.words_to_wordcloud(filtered_words, t_name)

main()
