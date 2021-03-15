"""Presentation tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from tools.factories import jumbotron_2_columns
from dashapp import PROJECT_MD, REFERENCES_MD, HOWTO_MD

# Set tab id
TAB_ID = 'presentation-tab'


# Jumbotron
title = 'Eight journals over eight decades: a computational topic-modeling approach to contemporary philosophy of science'
jum_col_1 = 'Desc text in col 1'
pres_jumbotron = jumbotron_2_columns(title, jum_col_1)


# Most content will be held in cars, that can be defined here or imported
# If cards are self contained, it's nicer to split them in individual files
pres_card_abstract = dbc.Card([
    dbc.CardBody([
        html.H4('Eight journals over eight decades: a computational topic-modeling approach to contemporary philosophy of science'),
        html.Hr(style={'width': '30%', 'text-align': 'left', 'margin-left': '0px'}),
        html.Br(),
        dcc.Markdown(PROJECT_MD, className='h6'),
        html.Hr(style={'width': '30%', 'text-align': 'left', 'margin-left': '0px'}),
        html.Br(),
        dcc.Markdown(REFERENCES_MD, className='h6')
    ])
])

pres_card_howto = dbc.Card([
    dbc.CardBody([
        html.H4('How to use this app'),
        html.Hr(style={'width': '30%', 'text-align': 'left', 'margin-left': '0px'}),
        html.Br(),
        dcc.Markdown(HOWTO_MD, className='h6'),
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
presentation_tab_layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            pres_card_abstract
        ], width=8),
        dbc.Col([
            pres_card_howto
        ], width=4),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below

