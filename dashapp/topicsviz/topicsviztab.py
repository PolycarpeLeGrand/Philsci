"""Basic tab layout

A tab's main component should be a dbc.Container or html.Div, which is added to index.py
Subcomponents and callbacks can be declared here or in submodules to keep things clean
"""

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go

from tools.factories import jumbotron_2_columns
from dashapp import app, DATA, TOPICVIZ_MD, cache

# Set tab id
TAB_ID = 'topicsviz-tab'


# Most content will be held in cars, that can be defined here or imported
# If cards are self contained, it's nicer to split them in individual files
topicsviz_card_1 = dbc.Card([
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                html.H4('Overview of topics throughout the corpus'),
                html.Hr(style={'width': '10%', 'text-align': 'left', 'margin-left': '0px'}),
                html.Br()
            ])
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Markdown(TOPICVIZ_MD, className='h6'),
                dbc.InputGroup([
                    dbc.Label('Number of dims'),
                    dbc.RadioItems(id='topicsviz-view-radio',
                                   options=[{'label': '3d', 'value': 3}, {'label': '2d', 'value': 2}],
                                   value=3),
                ]),
                html.Div(html.H5('Click a point to see article details.'), id='topicsviz-details-text', style={'padding-top': '5vh'})
            ], width=3),
            dbc.Col([
                dcc.Graph(figure=px.scatter(), id='topicsviz-scatter', style={'height': '80vh'})
            ], width=9),
        ])

    ])
])

# tab container, which is imported by tabindex
# divided in rows with dbc.Row() and then cols with dbc.Col()
# each col typically holds one card
topicsviz_tab_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            topicsviz_card_1
        ], width=12),
        dbc.Col([
            # ex_card_2
        ]),
    ]),
], fluid=True, id=TAB_ID)


# callbacks go below
@cache.memoize()
def make_topicsviz_2d_scatter():
    df = DATA['METADATA_DF']
    fig = px.scatter(df, x='tsne_2d_x', y='tsne_2d_y', title='Scatterplot documents-topics', color='dom_topic_name',
                     color_discrete_map=DATA['TOPIC_MAPPINGS_DF']['color_code_topic'].to_dict(),
                     hover_name=df.apply(lambda x: f'{x["author"]}, ({x["year"]})', axis=1),
                     hover_data={
                         'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                         'Main Topic': df['dom_topic_name'],
                         'Category': df['dom_topic_name'].map(DATA['TOPIC_MAPPINGS_DF']['cluster_name']),
                         'Journal': df['journal_id'],
                         'Period': df['period'],
                         'Language': df['lang'],
                         'tsne_2d_x': False,
                         'tsne_2d_y': False,
                         'dom_topic': False,
                         'dom_topic_name': False},
                     custom_data=[df.index],
                     category_orders={'dom_topic_name': DATA['ORDERED_TOPICS']})
    # color_discrete_sequence=px.colors.qualitative.Dark24, )
    fig.update_traces(marker={'size': 3})
    fig.update_layout(legend_title='Topics', legend_itemsizing='constant')\
        .update_xaxes(range=[-100, 100]).update_yaxes(range=[-110, 110])
    return fig

@cache.memoize()
def make_topicsviz_3d_scatter():
    df = DATA['METADATA_DF']
    fig = px.scatter_3d(df, x='tsne_3d_x', y='tsne_3d_y', z='tsne_3d_z', title='Scatterplot documents-topics',
                        color='dom_topic_name',
                        color_discrete_map=DATA['TOPIC_MAPPINGS_DF']['color_code_topic'].to_dict(),
                        hover_name=df.apply(lambda x: f'{x["author"]} ({x["year"]})', axis=1),
                        hover_data={
                            'Title': df['title'].map(lambda x: x if len(x) < 60 else x[:60] + '...'),
                            'Main Topic': df['dom_topic_name'],
                            'Category': df['dom_topic_name'].map(DATA['TOPIC_MAPPINGS_DF']['cluster_name']),
                            'Journal': df['journal_id'],
                            'Period': df['period'],
                            'Language': df['lang'],
                            'tsne_3d_x': False,
                            'tsne_3d_y': False,
                            'tsne_3d_z': False,
                            'dom_topic': False,
                            'dom_topic_name': False},
                        custom_data=[df.index],
                        category_orders={'dom_topic_name': DATA['ORDERED_TOPICS']})
    # color_discrete_sequence=px.colors.qualitative.Dark24, )
    fig.update_traces(marker={'size': 2})
    fig.update_layout(legend_title='Topics', legend_itemsizing='constant')
    #fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False)

    return fig

@app.callback(
    Output('topicsviz-scatter', 'figure'),
    [Input('topicsviz-view-radio', 'value')]
)
def update_topicsviz_scatter(n_dims):
    # return make_topicviz_periods_scatter()
    fig = make_topicsviz_2d_scatter() if int(n_dims) == 2 else make_topicsviz_3d_scatter()
    return fig


@app.callback(
    [Output('topicsviz-details-text', 'children')],
    [Input('topicsviz-scatter', 'clickData')], prevent_initial_call=True
)
def update_topicsvix_article_details(click_data):
    article_id = click_data['points'][0]['customdata'][0]
    article_data = DATA['METADATA_DF'].loc[article_id]
    top_topics = DATA['DOC_TOPICS_DF'].loc[article_id].nlargest(10)
    c = [html.Div([
        dbc.Row([
            dbc.Col([
                html.H4(article_data['title']),
                html.P(f'{article_data["author"]} ({article_data["year"]})'),
                html.P(f'Journal: {article_data["journal_id"]}', className='lead'),
                html.P(f'Period: {article_data["period"]}'),
                html.P(f'Language: {article_data["lang"]}'),
            ], width=4),
            dbc.Col(
                [html.H4('Topic distribution')] + [html.P(f'{t} ({p:.4f})') for t, p in top_topics.items()]
            )
        ])
    ])]

    d = [html.Div([
            html.H5(article_data['title']),
            html.P(article_data['citation']),
            #html.P([f'{article_data["author"]} ({article_data["year"]})', html.Br(), html.P(f'{article_data["journal_id"]}, {article_data["period"]}, {article_data["lang"]}'),]),
            html.Div([
                html.H5('Topic distribution'),
                dcc.Markdown("  \n".join(f'{t} ({p:.4f})' for t, p in top_topics.items()), style={'margin': '0px'})
            ])
    ])]

    return d
