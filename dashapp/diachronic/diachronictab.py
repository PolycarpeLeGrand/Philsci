"""Diachronic tab layout"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA, GRAPH_COLORS, cache


def make_topicviz_periods_scatter():
    df = DATA['METADATA_DF']
    df['color_code'] = df['dom_topic_name'].map(DATA['TOPIC_MAPPINGS_DF']['color_code_topic'].to_dict())
    fig = go.Figure()
    for period, period_df in df.groupby('period'):
        fig.add_trace(go.Scattergl(x=period_df['tsne_2d_x'], y=period_df['tsne_2d_y'], name=period,
                                   mode='markers',
                                   marker_color=period_df['color_code'],
                                   marker_size=6,
                                   legendgroup='Topics',
                                   text=period_df['title'].map(
                                       lambda x: f'Title: {x}' if len(x) < 60 else f'Title: {x[:60]}...')))
        # marker={'color': period_df['color_code'], 'size': 3}))
    fig.update_traces(hoverinfo='text', selector=dict(type='scattergl')) \
        .update_traces(showlegend=False, selector=dict(type='scattergl')) \
        .update_xaxes(range=[-90, 90]) \
        .update_xaxes(autorange=False) \
        .update_yaxes(autorange=False) \
        .update_yaxes(range=[-100, 100]) \
        .update_layout(title='Period: Whole Corpus',)
    return fig


# Set tab id
TAB_ID = 'diachronic-tab'

# Most content will be held in cars, that can be defined here or imported
# If cards are self contained, it's nicer to split them in individual files
diachronic_graph_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4('Evolution of topics through time'),
                html.Hr(style={'width': '10%', 'text-align': 'left', 'margin-left': '0px'}),
                html.Br(),
            ]),
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Label('Select data to show ' + u'\U0001F6C8', id='diachronic-bar-select-help'),
                dbc.Tooltip('Choose between the average values for each topic or the proportion of articles where a topic is dominent.', target='diachronic-bar-select-help', placement='right'),
                dbc.RadioItems(id='diachronic-histo-select',
                               options=[{'label': 'Average topic probabilities', 'value': 'avg'},
                                        {'label': 'Proportion of article with topic as dominant', 'value': 'dom'}],
                               value='avg')
            ], width=3),
            dbc.Col([
                dcc.Graph(id='diachronic-histo-graph', style={'height': '70vh'}),
            ]),
        ]),
    ])
])

diachronic_animation_card = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Select(
                    id='diachronic-animation-select',
                    options=[{'label': p, 'value': p} for p in DATA['ORDERED_PERIODS']] + [{'label': 'Whole Corpus', 'value': 'corpus'}],
                    value=DATA['ORDERED_PERIODS'][0]
                ),
                dbc.Button('Prev', id='diachronic-animation-prev'),
                dbc.Button('Next', id='diachronic-animation-next'),
                html.Div(id='diachronic-animation-log', children='prev:0 next:0 last:0', style={'display': 'none'}),
                html.Div(id='diachronic-scatter-details')
                # Next / Prev
                # Show legend
            ], width=2),
            dbc.Col([
                dcc.Graph(figure=make_topicviz_periods_scatter(), id='diachronic-scatter', style={'height': '80vh'}),
                #dcc.Interval(interval=2000, id='diachronic-interval', disabled=True),
            ]),
        ]),
    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
diachronic_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            diachronic_graph_card,
        ], width=12),
        dbc.Col([
            # ex_card_2
        ]),
    ], style={'margin-bottom': '20px'}),

    dbc.Row([
        dbc.Col([
            diachronic_animation_card,
        ]),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below
@app.callback(
    Output('diachronic-histo-graph', 'figure'),
    [Input('diachronic-histo-select', 'value')]

)
@cache.memoize()
def update_diachronic_histo(val):
    if val == 'avg':
        df = DATA['DOC_TOPICS_DF'].groupby(DATA['METADATA_DF']['period']).mean()
        x, y, color = df.index, df.columns, None
    else:
        df = DATA['METADATA_DF'].groupby(['period', 'dom_topic_name']).size().reset_index(name='counts')
        df['counts'] = df.groupby('period')['counts'].apply(lambda x: x / x.sum())
        x, y, color = 'period', 'counts', 'dom_topic_name'

    fig = px.bar(df, x=x, y=y, color=color,
                 category_orders={'period': DATA['ORDERED_PERIODS'],
                                  'variable': DATA['ORDERED_TOPICS'],
                                  'dom_topic_name': DATA['ORDERED_TOPICS']},
                 color_discrete_map=DATA['TOPIC_MAPPINGS_DF']['color_code_topic'].to_dict(),)
    fig.update_layout(bargap=0.0, legend_title='Topics', legend_traceorder='reversed',
                      plot_bgcolor='white',
                      paper_bgcolor='white',
                      title='Topic distributions by time periods',
                      xaxis_title='Time periods',
                      yaxis_title='Topic distributions')\
        .update_traces(marker_line_width=0.0, selector={'type': 'bar'})
    return fig


def make_diachronic_details_paras(tops, means):
    return [html.P(f'{name} - {pct * 100:.2f}% - {means[name]:.4f}',
                   style={'color': f'{DATA["TOPIC_MAPPINGS_DF"].loc[name]["color_code_topic"]}'})
            for name, pct in tops.items()]
    # return html.P(f'{name} - {pct*100:.2f}%', style={'color': f'{DATA["TOPIC_MAPPINGS_DF"].loc[name]["color_code_topic"]}'})


@app.callback(
    [Output('diachronic-scatter', 'figure'),
     Output('diachronic-scatter-details', 'children')],
    [Input('diachronic-animation-select', 'value')],
    State('diachronic-scatter', 'figure'), prevent_initial_call=False
)
@cache.memoize()
def scroll_period(p, fig):
    fig = go.Figure(fig)
    if p == 'corpus':
        p = 'Whole Corpus'
        fig.update_traces(visible=True, selector=dict(type='scattergl'))
        tops = DATA['METADATA_DF']['dom_topic_name'].value_counts().nlargest(10) / len(DATA['METADATA_DF'])
        means = DATA['DOC_TOPICS_DF'][tops.index].mean()
    else:
        fig.update_traces(visible=False, selector=dict(type='scattergl'))
        fig.update_traces(visible=True, selector=dict(name=p))
        g = DATA['METADATA_DF'].groupby('period').get_group(p)
        tops = g['dom_topic_name'].value_counts().nlargest(10) / len(g)
        means = DATA['DOC_TOPICS_DF'].loc[g.index][tops.index].mean()

    details = make_diachronic_details_paras(tops, means)
    # details = [make_diachronic_details_para(name, pct) for name, pct in tops.items()]
    fig.update_layout(title_text=f'Time period: {p}')
    return fig, details


@app.callback(
    [Output('diachronic-animation-log', 'children'),
     Output('diachronic-animation-select', 'value')],
    [Input('diachronic-animation-prev', 'n_clicks'),
     Input('diachronic-animation-next', 'n_clicks')],
    [State('diachronic-animation-log', 'children'),
     State('diachronic-animation-select', 'value')], prevent_initial_call=True
)
def diachronic_animation_buttons(prev, next, log, s_period):
    if not prev:
        prev = 0
    if not next:
        next = 0
    values = dict([i.split(':') for i in log.split(' ')])
    move = 1 if next > int(values['next']) else -1

    if s_period == 'corpus':
        if move == 1:
            new_period = DATA['ORDERED_PERIODS'][0]
        else:
            new_period = DATA['ORDERED_PERIODS'][-1]
    else:
        if (s_period == DATA['ORDERED_PERIODS'][0] and move == -1) or \
                (s_period == DATA['ORDERED_PERIODS'][-1] and move == 1):
            new_period = 'corpus'
        else:
            new_period = DATA['ORDERED_PERIODS'][list(DATA['ORDERED_PERIODS']).index(s_period) + move]

    return f'prev:{prev} next:{next} last:{move}', new_period


