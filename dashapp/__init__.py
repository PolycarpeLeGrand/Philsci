import dash
import pickle
import dash_bootstrap_components as dbc
import codecs
from flask_caching import Cache

from config import PROJECT_TITLE, IS_PROD, DATA_PATHS, MARKDOWNS_PATH, CACHE_CONFIG


# compile style
#sass.compile(dirname=('dashapp/assets/sass', 'dashapp/assets/css'), output_style='compressed')

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SIMPLEX],
                title=PROJECT_TITLE,
                suppress_callback_exceptions=IS_PROD)

cache = Cache(app.server, config=CACHE_CONFIG)
cache.clear()

# cache.clear()

# Load data
def load_df_from_pickle(path):
    with open(path, 'rb') as f:
        return pickle.load(f)


def load_markdown_file(filename, path=MARKDOWNS_PATH):
    with codecs.open(path / filename, 'r', 'utf-8') as f:
        return f.read()


DATA = {name: load_df_from_pickle(path) for name, path in DATA_PATHS.items()}

DATA['ORDERED_PERIODS'] = DATA['METADATA_DF']['period'].sort_values(key=lambda x: x.apply(lambda y: int(y[:4]))).unique()
# .apply(lambda x: f'{x} ({DATA["TOPIC_MAPPINGS_DF"]["topic_name"]})')

# Map topic numbre to assinged names
# DATA['TOPIC_MAPPINGS_DF']['topic_name'] = DATA['TOPIC_MAPPINGS_DF']['topic_name'] + ' (' + DATA["TOPIC_MAPPINGS_DF"]["cluster_name"] + ')'
# DATA['TOPIC_MAPPINGS_DF']['topic_name'] = DATA['TOPIC_MAPPINGS_DF']['topic_name'] + ' (' + DATA["TOPIC_MAPPINGS_DF"]["cluster_name"] + ')'

topic_name_col = 'cluster_letter_+_topic_(id)' # 'topic_name'
DATA['METADATA_DF']['dom_topic_name'] = DATA['METADATA_DF']['dom_topic'].map(DATA['TOPIC_MAPPINGS_DF'][topic_name_col])
DATA['DOC_TOPICS_DF'].rename(columns=DATA['TOPIC_MAPPINGS_DF'][topic_name_col], inplace=True)
DATA['TOPIC_WORDS_DF'].rename(index=DATA['TOPIC_MAPPINGS_DF'][topic_name_col], inplace=True)

DATA['TOPIC_MAPPINGS_DF'].set_index(topic_name_col, inplace=True)

#DATA['ORDERED_TOPICS'] = [t for _, d in DATA['TOPIC_MAPPINGS_DF'].groupby('cluster_name') for t in d.sort_index().index]
DATA['ORDERED_TOPICS'] = list(DATA['TOPIC_MAPPINGS_DF'].sort_index().index)


DATA['JOURNAL_COLORS_MAPPING'] = {
    'BJPS': '#66C5CC',
    'EJPS': '#F6CF71',
    'ERK': '#F89C74',
    'ISPS': '#DCB0F2',
    'JGPS': '#87C55F',
    'PS': '#9EB9F3',
    'SHPSA': '#FE88B1',
    'SYN': '#C9DB74',
    'en': '#F89C74',
    'de': '#F6CF71',
    'fr': '#66C5CC',
    'nl': '#DCB0F2',
}

# Load markdowns

PROJECT_MD = load_markdown_file('presentation.md')
REFERENCES_MD = load_markdown_file('references.md')
HOWTO_MD = load_markdown_file('howto.md')
METADATA_MD = load_markdown_file('metadata.md')
TOPICVIZ_MD = load_markdown_file('topicviz.md')
TOPICDETAILS_MD = load_markdown_file('topicdetails.md')

# dark theme: 'text': 'rgb(233, 233, 233)', 'background': 'rgb(8, 8, 8)'
# green + darkinsh: 'rgb(233, 233, 233)', 'background': 'rgb(41, 41, 41)'

GRAPH_COLORS = {
    'text': 'white',
    'background': 'rgb(63, 63, 63)'
}

