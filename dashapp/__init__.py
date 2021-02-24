import dash
import pickle
import dash_bootstrap_components as dbc

from config import PROJECT_TITLE, IS_PROD, DATA_PATHS

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SIMPLEX], title=PROJECT_TITLE,
                suppress_callback_exceptions=IS_PROD)


# Load data
def load_df_from_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


DATA = {name: load_df_from_pickle(path) for name, path in DATA_PATHS.items()}

DATA['ORDERED_PERIODS'] = DATA['METADATA_DF']['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
DATA['METADATA_DF']['dom_topic_name'] = DATA['METADATA_DF']['dom_topic'].map(DATA['TOPIC_MAPPINGS_DF']['topic_name'])

map_topics = True
if map_topics:
    DATA['DOC_TOPICS_DF'].rename(columns=DATA['TOPIC_MAPPINGS_DF']['topic_name'], inplace=True)
    DATA['TOPIC_WORDS_DF'].rename(index=DATA['TOPIC_MAPPINGS_DF']['topic_name'], inplace=True)
    DATA['TOPIC_MAPPINGS_DF'].set_index('topic_name', inplace=True)

