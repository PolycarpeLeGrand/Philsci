import pandas as pd
import pickle
from config import DATA_PATHS
from sklearn.manifold import TSNE


def make_dfs_from_xlsx():
    """Makes dataframes from xlsx source file and saves them as pickles

    If raw_data was updated with a new version, do the following modifications on the xlsx file before running:
        - Erase A1 cells on imported sheets, it messes with columns/index
        - Remove the average topic weights row (last one) on Doc vs Topic sheet
        - Make a new col 'Article_id' with formula =CONCATENATE("art_",A2), to be used as index
        - In 'Top 50 Topics Words' tab, delete columns BJ+
    """

    f = open('raw_data.xlsx', 'rb')

    tw = pd.read_excel(f, 'Words vs Topics', index_col=0, engine='openpyxl').transpose()
    df = pd.read_excel(f, 'Doc vs Topic', index_col=0, engine='openpyxl')
    nf = pd.read_excel(f, 'Top 50 Topics Words', index_col=0, engine='openpyxl').dropna()

    df = df.set_index('Article_id')
    df['Dom_topic'] = df['Dom_topic'].map(lambda x: f'topic_{x}')

    tf = df[[f'Topic_{i}' for i in range(25)]]
    mf = df[['Journal_id', 'Title', 'Author', 'Year', 'Citation', 'N_Token', 'Lang_Detect1+manual_for_multi', 'Dom_topic', 'Period']]
    nf = nf[['Topic ID', 'Topic label (post-clustering)', 'Cluster ID', 'Cluster name', 'Cluster letter + topic (ID)', 'Color code topic', 'Color code category']]

    mf = mf.rename(columns={'Lang_Detect1+manual_for_multi': 'lang'})
    mf = mf.rename(columns={col: col.lower().replace(' ', '_') for col in mf.columns})
    tf = tf.rename(columns={col: col.lower().replace(' ', '_') for col in tf.columns})
    tw = tw.rename(index={ind: ind.lower().replace(' ', '_') for ind in tw.index})
    nf = nf.rename(columns={'Topic label (post-clustering)': 'topic_name'})
    nf = nf.rename(index={ind: ind.lower().replace(' ', '_') for ind in nf.index}, columns={col: col.lower().replace(' ', '_') for col in nf.columns})

    mf[['tsne_2d_x', 'tsne_2d_y']] = TSNE(n_components=2, random_state=211).fit_transform(tf)

    print(nf)
    print(nf.index)

    pickle.dump(tf, open(DATA_PATHS['DOC_TOPICS_DF'], 'wb'))
    pickle.dump(mf, open(DATA_PATHS['METADATA_DF'], 'wb'))
    pickle.dump(tw, open(DATA_PATHS['TOPIC_WORDS_DF'], 'wb'))
    pickle.dump(nf, open(DATA_PATHS['TOPIC_MAPPINGS_DF'], 'wb'))


if __name__ == '__main__':
    make_dfs_from_xlsx()


