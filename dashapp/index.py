import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash

from dashapp import app
from dashapp.header import header
from dashapp.example.exampletab import example_tab_layout
from dashapp.about.abouttab import about_tab_layout


# Register tabs following this format
# {'name': 'tab-X', 'ulr': '/tabname', 'label': 'Tab Name', 'container': this_tab_layout}
TABS = [
    {'name': 'tab-0', 'url': '/extab', 'label': 'Example Tab', 'container': example_tab_layout},
    {'name': 'tab-1', 'url': '/about', 'label': 'About', 'container': about_tab_layout},
]


# Builds tabs from TABS. Don't touch.
tabs = dbc.Tabs(
    [dbc.Tab(label=tab['label'], label_style={'cursor': 'pointer'}) for tab in TABS],
    id='tabs', active_tab='tab-0', style={'padding-left': '10px', }
)


layout = html.Div([
    dcc.Location(id='url', refresh=False, pathname=TABS[0]['url']),
    header,
    html.Div([
        tabs,
    ], className='pt-2 bg-dark text-light'),
    dbc.Container([], id='tab-container', fluid=True, className='bt-2 pt-3'),
])


@app.callback(
    [Output(component_id='tab-container', component_property='children'),
     Output(component_id='tabs', component_property='active_tab'),
     Output(component_id='url', component_property='pathname'),],
    [Input(component_id='tabs', component_property='active_tab'),
     Input(component_id='url', component_property='pathname')]
)
def update_tab(selected_tab, curr_url):
    """Updates selected tab and tab container on url update"""

    ctx = dash.callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    tab = next(filter(lambda x: x['name'] == selected_tab, TABS)) if trigger_id == 'tabs' else \
        next(filter(lambda x: x['url'] == curr_url, TABS))

    return tab['container'], tab['name'], tab['url']

