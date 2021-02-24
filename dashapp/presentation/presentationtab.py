"""Presentation tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from tools.factories import jumbotron_2_columns
from dashapp import app

# Set tab id
TAB_ID = 'presentation-tab'


# Jumbotron
title = 'Project Overview'
jum_col_1 = 'Desc text in col 1'
pres_jumbotron = jumbotron_2_columns(title, jum_col_1)


# Most content will be held in cars, that can be defined here or imported
# If cards are self contained, it's nicer to split them in individual files
pres_card_abstract = dbc.Card([
    dbc.CardHeader('Article abstract and citation', className='lead'),
    dbc.CardBody([
        dcc.Markdown('Card text', className='h6')
    ])
])

pres_card_howto = dbc.Card([
    dbc.CardHeader('How to use this app', className='lead'),
    dbc.CardBody([
        dcc.Markdown('Explanations')
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
presentation_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            pres_jumbotron,
        ])
    ]),

    dbc.Row([
        dbc.Col([
            pres_card_abstract
        ], width=4),
        dbc.Col([
            pres_card_howto
        ], width=4),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below

