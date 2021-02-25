"""Topics Details tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA

# Set tab id
TAB_ID = 'topics-details-tab'


# Jumbotron
title = 'Example jumbo'
jum_col_1 = 'Desc text in col 1'
topics_details_jumbotron = jumbotron_2_columns(title, jum_col_1)


topics_details_card_1 = dbc.Card([
    dbc.CardHeader('First card header and stuff', className='lead'),
    dbc.CardBody([
        dbc.InputGroup([
            dbc.InputGroupAddon('Select Topic: ', addon_type='prepend'),
            dbc.Select(
                options=[
                    {'label': t, 'value': t} for t in DATA['TOPIC_MAPPINGS_DF'].index
                ],
                id='topics-details-select',
                value=DATA['TOPIC_MAPPINGS_DF'].index[0]
            ),
        ]),
        dbc.Container()
    ])
])

topics_details_words_card = dbc.Card([
    dbc.CardHeader('Top 10 words'),
    dbc.CardBody([
        html.Div(id='topics-details-words-table')
    ])
])

topics_details_articles_card = dbc.Card([
    dbc.CardHeader('Top 10 articles'),
    dbc.CardBody([
        html.Div(id='topics-details-articles-table')
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
topics_details_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topics_details_jumbotron,
        ])
    ]),

    dbc.Row([
        dbc.Col([
            topics_details_card_1
        ], width=3),
        dbc.Col([
            topics_details_words_card,
            topics_details_articles_card
        ]),
    ]),
], fluid=True, id=TAB_ID)


def make_html_table():
    return


# callbacks go below
@app.callback(
    Output('topics-details-words-table', 'children'),
    Input('topics-details-select', 'value'),
)
def update_topics_details_words_table(topic):
    words = DATA['TOPIC_WORDS_DF'].loc[topic].nlargest(10).index
    return [html.P(f'{word} - {", ".join(f"{t} ({p:.4f})" for t, p in DATA["TOPIC_WORDS_DF"][word].nlargest(10).items())}') for word in words]


@app.callback(
    Output('topics-details-articles-table', 'children'),
    Input('topics-details-select', 'value')
)
def update_topics_details_articles_table(topic):
    articles = DATA['DOC_TOPICS_DF'][topic].nlargest(10).index
    d = []
    for article in articles:
        tops = DATA['DOC_TOPICS_DF'].loc[article].nlargest(10)
        md = DATA["METADATA_DF"].loc[article]
        d.append(html.P([f'{md["title"]} | {md["journal_id"]} | {md["period"]}',
                         html.Br(), f'{", ".join(f"{t} ({p:.4f})" for t, p in tops.items())}']))
    return d


