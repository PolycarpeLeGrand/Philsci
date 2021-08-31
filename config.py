from pathlib import Path
from dotenv import load_dotenv
from os import environ


# Load project settings
PROJECT_PATH = Path(__file__).parent
load_dotenv(PROJECT_PATH / '.env')
LOCAL_IP = environ.get('LOCAL_IP')
#BASE_STORAGE_PATH = Path(environ.get('LOCAL_STORAGE_PATH'))
BASE_STORAGE_PATH = PROJECT_PATH / 'data'
CACHE_PATH = PROJECT_PATH / 'cache'
IS_PROD = environ.get('IS_PROD') == 'True'
PORT = 33

DATAFRAMES_PATH = PROJECT_PATH / 'data/dfs'
MARKDOWNS_PATH = PROJECT_PATH / 'data/markdowns'

# Set paths to data files here.
DATA_PATHS = {
    'TEST_DATA_DF': PROJECT_PATH / 'data' / 'test_data_df.p',
    'DOC_TOPICS_DF': DATAFRAMES_PATH / 'doctopics_df.p',
    'TOPIC_WORDS_DF': DATAFRAMES_PATH / 'topicwords_df.p',
    'METADATA_DF': DATAFRAMES_PATH / 'metadata_df.p',
    'TOPIC_MAPPINGS_DF': DATAFRAMES_PATH / 'topic_mappings_df.p',
}


# Browser tab title
PROJECT_TITLE = 'Philsci'

# Title and subtitle to display on header
HEADER_TITLE = 'Philsci Title'
HEADER_SUBTITLE = 'Philsci Subtitle'

# Name and bio of the project contributors. Displayed in About tab.
CONTRIBUTORS = {
    'Name McName': 'This person is working on something ',
    'Person Person': 'This person also contributed to the project. Here is some gibberish to see what happens'
                     ' when there is more text and multiple lines might be needed.',
    }


# Cache config
if False:#IS_PROD:
    CACHE_CONFIG = {'CACHE_TYPE': 'redis', 'CACHE_REDIS_HOST': '127.0.0.1', 'CACHE_DEFAULT_TIMEOUT': 0,}
else:
    CACHE_CONFIG = {'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 0,}

