"""Metadata tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA, GRAPH_COLORS, METADATA_MD, cache

# Set tab id
TAB_ID = 'metadata-tab'


# metadata_bar_checklist_options = [{'label': lang, 'value': lang} for lang in DATA['METADATA_DF']['lang'].unique()]
# metadata_bar_checklist_values = [option['value'] for option in metadata_bar_checklist_options]
meta_card_bar = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4('8 journals over 8 decades'),
                html.Hr(style={'width': '10%', 'text-align': 'left', 'margin-left': '0px'}),
                html.Br(),
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown(METADATA_MD, className='h6'),
                html.Br(),
                dbc.Label('Include articles published in:'),
                dbc.Checklist(
                    options=[{'label': lang, 'value': lang} for lang in DATA['METADATA_DF']['lang'].unique()],
                    # value=metadata_bar_checklist_values,
                    value=[lang for lang in DATA['METADATA_DF']['lang'].unique()],
                    id='metadata-bar-checklist',
                    style={'padding-left': '20px'}
                ),
            ], width=4),
            dbc.Col([
                dcc.Graph(id='metadata-bar-graph', figure=px.bar()),
            ]),
        ]),
    ])
])

meta_card_pie = dbc.Card([
    dbc.CardHeader('Periods Details', className='lead'),
    dbc.CardBody([
        dcc.RangeSlider(id='metadata-periods-slider', min=0, max=len(DATA['ORDERED_PERIODS']) - 1, step=4,
                        value=[0, len(DATA['ORDERED_PERIODS']) - 1],
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
        ], style={'max-width': '60%'}),
        dcc.Graph(id='metadata-periods-pie', figure=px.pie())
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
metadata_tab_layout = dbc.Container([

    dbc.Row([
        dbc.Col([
            meta_card_bar
        ], width=12),
        #dbc.Col([
            #meta_card_pie
        #], width=4),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below
@app.callback(
    Output('metadata-bar-graph', 'figure'),
    [Input('metadata-bar-checklist', 'value')], prevent_initial_callbacks=True
)
@cache.memoize()
def update_journals_bar(checkedvalues):
    df = DATA['METADATA_DF'][['journal_id', 'period', 'lang']]
    df = df.loc[df['lang'].isin(checkedvalues)]
    groups = ['journal_id', 'period']
    df = df.groupby(groups).size().reset_index(name='counts')

    fig = px.bar(df, x='period', y='counts', color='journal_id',
                 category_orders={'period': DATA['ORDERED_PERIODS']},
                 color_discrete_map=DATA['JOURNAL_COLORS_MAPPING'],)

    fig.update_layout(legend_title='Journals', xaxis_title='Time periods',
                      yaxis_title='Number of articles', title='Number of articles by time periods')# plot_bgcolor=GRAPH_COLORS['background'], paper_bgcolor=GRAPH_COLORS['background'], font_color=GRAPH_COLORS['text'])
    show_labels = True
    if show_labels:
        label_group = df.groupby('period')['counts'].sum()
        y_offset = 0.05 * label_group.max()
        fig.update_layout(annotations=[{'x': p, 'y': n + y_offset, 'text': n, 'showarrow': False} for p, n in
              df.groupby('period')['counts'].sum().items()])

    return fig

'''
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
    df = DATA['METADATA_DF'].loc[DATA['METADATA_DF']['period'].isin(periods)][value_name]  # ['journal_id']

    # remove ['Journal_id'] from above, then add
    # df = df['] if value_name == whatev else df['Lang']

    years_str = f'Showing data for years {period_a[:4]} to {period_b[-4:]}'
    docs_str = f'Includes {len(df)} docs out of {len(DATA["METADATA_DF"])}'
    df = df.value_counts()

    f = px.pie(values=df.values, names=df.index, color=df.index, color_discrete_map=DATA['JOURNAL_COLORS_MAPPING'])
    f.update_layout(plot_bgcolor=GRAPH_COLORS['background'], paper_bgcolor=GRAPH_COLORS['background'], font_color=GRAPH_COLORS['text'])
    return f, years_str, docs_str

'''