from wordcloud import WordCloud
import pickle
from config import PROJECT_PATH

TW = pickle.load(open('dfs/topicwords_df.p', 'rb'))
MP = pickle.load(open('dfs/topic_mappings_df.p', 'rb'))
topic_colors_mapping = MP['color_code_topic'].to_dict()


def color_mapping_funct(word, *args, **kwargs):
    return topic_colors_mapping[TW[word].idxmax()]


# plotly blue: rgb(229, 236, 246)
# rgb(8, 8, 8) rgb(11, 11, 27)
if __name__ == '__main__':
    wc = WordCloud(background_color='rgb(90, 90, 90)', color_func=color_mapping_funct)

    for t in TW.index:
        wc.fit_words(TW.loc[t].nlargest(25).to_dict())
        wc.to_file(PROJECT_PATH / f'dashapp/assets/wordclouds/wc_{t}.png')
