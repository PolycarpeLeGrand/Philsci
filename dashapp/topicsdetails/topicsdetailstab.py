"""Topics Details tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA, TOPICDETAILS_MD

# Set tab id
TAB_ID = 'topics-details-tab'

# Jumbotron
title = 'Example jumbo'
jum_col_1 = 'Desc text in col 1'
topics_details_jumbotron = jumbotron_2_columns(title, jum_col_1)

topics_details_title_div = html.Div([
    html.H4('Topic details: top words and articles'),
    html.Hr(style={'width': '10%', 'text-align': 'left', 'margin-left': '0px'}),
    html.Br()
])

topics_details_context_div = html.Div([
    dcc.Markdown(TOPICDETAILS_MD, className='h6'),
    dbc.InputGroup([
        dbc.InputGroupAddon('Topic: ', addon_type='prepend'),
        dbc.Select(
            options=[
                {'label': t, 'value': t} for t in DATA['ORDERED_TOPICS']  # DATA['TOPIC_MAPPINGS_DF'].sort_index().index
            ],
            id='topics-details-select',
            value=DATA['ORDERED_TOPICS'][0],  # DATA['TOPIC_MAPPINGS_DF'].sort_index().index[0]
        ),
    ], style={'max-width': '300px'}),
], style={'max-width': '500px'})


topics_details_card_1 = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col(
                topics_details_title_div
            )
        ]),

        dbc.Row([
            dbc.Col([
                topics_details_context_div
            ], width=6),
        ]),

        dbc.Row([
            dbc.Col([
                html.Img(src='assets/wordclouds/wc_topic_0.png',
                         style={'width': '100%',
                                'border': 'solid', 'border-width': '1px'},
                         id='topics-details-wordcloud'),
            ], width=6),
            dbc.Col([
                html.Div(id='topics-details-words-table')
            ], width=6),

        ], style={'margin-top': '30px'}),


    ])
])


topics_details_articles_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4('Articles in which the selected topic is most prominent'),
                html.Hr(style={'width': '10%', 'text-align': 'center', 'margin-left': '0px'}),
                html.Br(),
                html.Div(id='topics-details-articles-table')
            ]),
        ])
    ])
], style={'margin-top': '30px'})

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
topics_details_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topics_details_card_1
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col([
            topics_details_articles_card
        ], width=12)
    ]),
], fluid=True, id=TAB_ID)


def make_html_table():
    return


# callbacks go below
@app.callback(
    Output('topics-details-wordcloud', 'src'),
    Input('topics-details-select', 'value'),
)
def update_wordcloud(topic_name):
    return f'assets/wordclouds/wc_topic_{int(DATA["TOPIC_MAPPINGS_DF"].loc[topic_name]["topic_id"])}.png'


@app.callback(
    Output('topics-details-words-table', 'children'),
    Input('topics-details-select', 'value'),
)
def update_topics_details_words_table(topic):
    words = DATA['TOPIC_WORDS_DF'].loc[topic].nlargest(10).index
    return [
        html.P([
            html.B(f'{word} ({DATA["TOPIC_WORDS_DF"].loc[topic][word]:.4f})'),
            html.Br(),
            f'{", ".join(f"{t[:-4]} ({p:.4f})" for t, p in DATA["TOPIC_WORDS_DF"][word].nlargest(5).items())}'])
        for i, word in enumerate(words)]


@app.callback(
    Output('topics-details-articles-table', 'children'),
    Input('topics-details-select', 'value')
)
def update_topics_details_articles_table(topic):
    articles = DATA['DOC_TOPICS_DF'][topic].nlargest(10).index
    d = []
    for article in articles:
        tops = DATA['DOC_TOPICS_DF'].loc[article].nlargest(5)
        md = DATA["METADATA_DF"].loc[article]
        d.append(html.P([
            html.B(f'{md["citation"]}'),
            html.Br(), f'{", ".join(f"{t[:-4]} ({p:.4f})" for t, p in tops.items())}'
        ]))
    return d
