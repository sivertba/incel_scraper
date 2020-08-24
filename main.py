import os
import incel_scraper as islib  # Glorious abbriviation

DB_MODE = False


def main():
    if not os.path.exists('results'):
        os.makedirs('results')

    if DB_MODE:
        s_or_l = 's'
    else:
        s_or_l = input("Do you want to scrape or load data (s/l): ")

    if s_or_l == 's':
        word_dict = scrape()
    elif s_or_l == 'l':
        print("Not yet implemented ...")
        print("Will scrape instead ")
        word_dict = scrape()
        pass
    else:
        print('Unintelligble input, will scrape data')
        word_dict = scrape()

    print("")
    for t_name in word_dict:
        print("\tFiltering words from ", t_name)
        filtered_words = islib.filter_words(word_dict[t_name])

        print("\tCounting words from ", t_name)
        islib.words_to_csv(word_dict[t_name], t_name)
        islib.words_to_csv(filtered_words, t_name+'_filtered')

        print("\tWordclouding words from ", t_name)
        islib.words_to_wordcloud(filtered_words, t_name)


def scrape():
    islib.start_up_prompt()
    discussion_url, ui, max_pages = islib.set_session_parameters(
        debug_mode=DB_MODE)

    topics = islib.get_topics(discussion_url)

    word_dict = {}
    if ui:
        topic_id, topic = islib.select_topic(
            topics, debug_mode=DB_MODE)
        words, df = islib.scrape_topic_headers(
            discussion_url,
            topic_id,
            topic,
            max_pages=max_pages,
            debug_mode=DB_MODE)
        word_dict[topics[topic_id]] = words
        df.to_csv('results/'+topic+'_record.csv')
    else:
        for t_id in topics:
            words, df = islib.scrape_topic_headers(
                discussion_url,
                t_id,
                topics[t_id],
                max_pages=max_pages,
                debug_mode=DB_MODE)
            word_dict[topics[t_id]] = words
            df.to_csv('results/'+topics[t_id]+'_record.csv')
    return word_dict


main()
