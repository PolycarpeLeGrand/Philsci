"""Metadata tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA

# Set tab id
TAB_ID = 'metadata-tab'


# Jumbotron
title = 'Metadata jumbo'
jum_col_1 = 'Desc text in col 1 meta'
meta_jumbotron = jumbotron_2_columns(title, jum_col_1)

# metadata_bar_checklist_options = [{'label': lang, 'value': lang} for lang in DATA['METADATA_DF']['lang'].unique()]
# metadata_bar_checklist_values = [option['value'] for option in metadata_bar_checklist_options]
meta_card_bar = dbc.Card([
    dbc.CardHeader('Journals and Periods', className='lead', id='metadata-bar-card-head'),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Label('Select Languages:'),
                dbc.Checklist(
                    options=[{'label': lang, 'value': lang} for lang in DATA['METADATA_DF']['lang'].unique()],
                    #value=metadata_bar_checklist_values,
                    value=[lang for lang in DATA['METADATA_DF']['lang'].unique()],
                    id='metadata-bar-checklist',
                ),
            ], width=2),
            dbc.Col([
                dcc.Graph(id='metadata-bar-graph', figure=px.bar()),
            ]),
        ]),
    ])
])

meta_card_pie = dbc.Card([
    dbc.CardHeader('Periods Details', className='lead'),
    dbc.CardBody([
        dcc.RangeSlider(id='metadata-periods-slider', min=0, max=len(DATA['ORDERED_PERIODS'])-1, step=4, value=[0, len(DATA['ORDERED_PERIODS'])-1],
                        marks={i: period[2:4] for i, period in enumerate(DATA['ORDERED_PERIODS'])}),
        html.P(id='metadata-periods-years', style={'text-align': 'center'}),
        html.P(id='metadata-periods-docs', style={'text-align': 'center'}),
        dbc.InputGroup([
            dbc.InputGroupAddon('Select value to show: ', addon_type='prepend'),
            dbc.Select(
                options=[
                    {'label': 'Journal', 'value': 'journal_id'},
                    {'label': 'Language', 'value': 'lang'}
                ],
                id='metadata-pie-values-select',
                value='journal_id'
            ),
        ], style={'max-width': '40%'}),
        dcc.Graph(id='metadata-periods-pie', figure=px.pie())
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
metadata_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            meta_jumbotron,
        ])
    ]),

    dbc.Row([
        dbc.Col([
            meta_card_bar
        ], width=6),
        dbc.Col([
            meta_card_pie
        ], width=6),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below
@app.callback(
    Output('metadata-bar-graph', 'figure'),
    [Input('metadata-bar-checklist', 'value')], prevent_initial_callbacks=True
)
def update_journals_bar(checkedvalues):
    df = DATA['METADATA_DF'][['journal_id', 'period', 'lang']]
    df = df.loc[df['lang'].isin(checkedvalues)]
    groups = ['journal_id', 'period']
    df = df.groupby(groups).size().reset_index(name='counts')
    return px.bar(df, x='period', y='counts', color='journal_id', category_orders={'period': DATA['ORDERED_PERIODS']})


@app.callback(
    [Output('metadata-periods-pie', 'figure'),
     Output('metadata-periods-years', 'children'),
     Output('metadata-periods-docs', 'children')],
    [Input('metadata-periods-slider', 'value'),
     Input('metadata-pie-values-select', 'value')]
)
def update_periods_pie(slider_vals, value_name):
    periods = DATA['ORDERED_PERIODS'][slider_vals[0]:slider_vals[1] + 1]
    period_a, period_b = periods[0], periods[-1]
    df = DATA['METADATA_DF'].loc[DATA['METADATA_DF']['period'].isin(periods)][value_name] #['journal_id']

    # remove ['Journal_id'] from above, then add
    #df = df['] if value_name == whatev else df['Lang']

    years_str = f'Showing data for years {period_a[:4]} to {period_b[-4:]}'
    docs_str = f'Includes {len(df)} docs out of {len(DATA["METADATA_DF"])}'
    df = df.value_counts()
    f = px.pie(values=df.values, names=df.index)
    return f, years_str, docs_str

