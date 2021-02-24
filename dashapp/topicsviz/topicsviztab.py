"""Basic tab layout

A tab's main component should be a dbc.Container or html.Div, which is added to index.py
Subcomponents and callbacks can be declared here or in submodules to keep things clean
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA

# Set tab id
TAB_ID = 'topicsviz-tab'


# Jumbotron
title = 'Topics Visualizations jumbo'
jum_col_1 = 'Tab description'
topicsviz_jumbotron = jumbotron_2_columns(title, jum_col_1)


# Most content will be held in cars, that can be defined here or imported
# If cards are self contained, it's nicer to split them in individual files
topicsviz_card_1 = dbc.Card([
    dbc.CardHeader('T-SNE viz', className='lead'),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.InputGroup([
                    dbc.Label('InputGroup 1'),
                    dbc.RadioItems(id='topicsviz-view-radio'),
                ]),
            ], width=2),
            dbc.Col([
                dcc.Graph(id='topicsviz-scatter', style={'height': '70vh'})
            ]),
        ])

    ])
])


# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
topicsviz_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topicsviz_jumbotron,
        ])
    ]),

    dbc.Row([
        dbc.Col([
            topicsviz_card_1
        ], width=10),
        dbc.Col([
            # ex_card_2
        ]),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below
@app.callback(
    Output('topicsviz-scatter', 'figure'),
    [Input('topicsviz-view-radio', 'value')]
)
def update_topicsviz_scatter(view_values):
    df = DATA['METADATA_DF']
    fig = px.scatter(df, x='tsne_2d_x', y='tsne_2d_y', title='Scatterplot documents-topics', color='dom_topic_name',
                     color_discrete_map=DATA['TOPIC_MAPPINGS_DF']['color_code_topic'].to_dict(),
                     hover_name=df.index,
                     hover_data={
                         'Main Topic': df['dom_topic'],
                         'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                         'Journal': df['journal_id'],
                         'Period': df['period'],
                         'Language': df['lang'],
                         'tsne_2d_x': False,
                         'tsne_2d_y': False,
                         'dom_topic': False},)
                     #color_discrete_sequence=px.colors.qualitative.Dark24, )
    fig.update_traces(marker={'size': 3})
    fig.update_layout(paper_bgcolor='#FCFCFC', plot_bgcolor='#FCFCFC')

    return fig