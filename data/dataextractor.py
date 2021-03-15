import pandas as pd
import pickle
from config import DATA_PATHS
from sklearn.manifold import TSNE


def format_authors(authors):
    for c in '()[]\'':
        authors = authors.replace(c, '')
    return authors


def make_dfs_from_xlsx():
    """Makes dataframes from xlsx source file and saves them as pickles

    If raw_data was updated with a new version, do the following modifications on the xlsx file before running:
        - Erase A1 cells on imported sheets, it messes with columns/index
        - Remove the average topic weights row (last one) on Doc vs Topic sheet
        - Make a new col 'Article_id' with formula =CONCATENATE("art_",A2), to be used as index
        - In 'Top 50 Topics Words' tab, delete columns BJ+
    """

    f = open('raw_data.xlsx', 'rb')

    topic_words_df = pd.read_excel(f, 'Words vs Topics', index_col=0, engine='openpyxl').transpose()
    df = pd.read_excel(f, 'Doc vs Topic', index_col=0, engine='openpyxl')
    topic_mappings_df = pd.read_excel(f, 'Top 50 Topics Words', index_col=0, engine='openpyxl').dropna()

    df = df.set_index('Article_id')
    df['Dom_topic'] = df['Dom_topic'].map(lambda x: f'topic_{x}')
    df['Author'] = df['Author'].map(format_authors)

    doc_topics_df = df[[f'Topic_{i}' for i in range(25)]].copy()
    metadata_df = df[['Journal_id', 'Title', 'Author', 'Year', 'Citation', 'N_Token', 'Lang_Detect1+manual_for_multi', 'Dom_topic', 'Period']].copy()
    topic_mappings_df = topic_mappings_df[['Topic ID', 'Topic label (post-clustering)', 'Cluster ID', 'Cluster name', 'Cluster letter + topic (ID)', 'Color code topic', 'Color code category']]

    metadata_df.rename(columns={'Lang_Detect1+manual_for_multi': 'lang'}, inplace=True)
    metadata_df.rename(columns={col: col.lower().replace(' ', '_') for col in metadata_df.columns}, inplace=True)
    doc_topics_df.rename(columns={col: col.lower().replace(' ', '_') for col in doc_topics_df.columns}, inplace=True)
    topic_words_df.rename(index={ind: ind.lower().replace(' ', '_') for ind in topic_words_df.index}, inplace=True)
    topic_mappings_df.rename(columns={'Topic label (post-clustering)': 'topic_name'}, inplace=True)
    topic_mappings_df.rename(index={ind: ind.lower().replace(' ', '_') for ind in topic_mappings_df.index},
                             columns={col: col.lower().replace(' ', '_') for col in topic_mappings_df.columns},
                             inplace=True)

    metadata_df[['tsne_2d_x', 'tsne_2d_y']] = TSNE(n_components=2, random_state=211).fit_transform(doc_topics_df)
    metadata_df[['tsne_3d_x', 'tsne_3d_y', 'tsne_3d_z']] = TSNE(n_components=3, random_state=211).fit_transform(doc_topics_df)
    metadata_df['lang'] = metadata_df['lang'].map({'en': 'English', 'de': 'German', 'fr': 'French', 'nl': 'Dutch'})
    print(topic_mappings_df)
    print(topic_mappings_df.index)

    pickle.dump(doc_topics_df, open(DATA_PATHS['DOC_TOPICS_DF'], 'wb'))
    pickle.dump(metadata_df, open(DATA_PATHS['METADATA_DF'], 'wb'))
    pickle.dump(topic_words_df, open(DATA_PATHS['TOPIC_WORDS_DF'], 'wb'))
    pickle.dump(topic_mappings_df, open(DATA_PATHS['TOPIC_MAPPINGS_DF'], 'wb'))


if __name__ == '__main__':
    make_dfs_from_xlsx()


