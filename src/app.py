# import dash
# import dash_bootstrap_components as dbc
# import pandas as pd

# from dash.dependencies import Input, Output
# from dash import dcc, html

# df = pd.read_csv('../data/processed_data.csv')

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# server = app.server
# # =========================
# # UI
# # =========================
# # the style arguments for the sidebar. We use position:fixed and a fixed width
# SIDEBAR_STYLE = {
#     "position": "fixed",
#     "top": 0,
#     "left": 0,
#     "bottom": 0,
#     "width": "13rem",
#     "padding": "2rem 1rem",
#     "background-color": "#f8f9fa",
# }


# sidebar = html.Div([
#         html.H2("Filter"),
#         html.Hr(),
#         dbc.Nav(
#             [dcc.Dropdown(id='country_select',
#                         options=[{'label': i, 'value': i} for i in df['Country'].unique()],
#                         multi=False,
#                         placeholder="Select countries"
#                         )
#             ],
#             vertical=True,
#             pills=True
#         )
#     ]
#     , style=SIDEBAR_STYLE)

# content = html.Div([
#         dbc.Row(html.H2("Title")),
#         dbc.Row([
#             dbc.Col(html.Div(id='output-tab1'), width=6),
#             dbc.Col(html.Div([
#                         html.H4("2nd col"),
#                         html.Hr()
#                         ]
#                     ), width=6)
#         ])
# ])


# # layout = html.Div([sidebar,content])
# layout = html.Div([
#     dbc.Row([
#         dbc.Col(sidebar, width=2),
#         dbc.Col(content, width=10)
#     ])
# ])
# app.layout = layout
# # =========================
# # Server
# # =========================


# @app.callback(Output('output-tab1', 'children'),
#             [
#             Input('country_select', 'value')])
# def update_output_tab1(country):
#     if country == []:
#         return html.Div('Please select a continent and a country.')
#     else:
#         filtered_df = df[df['Country'] == country]
#         return dcc.Graph(
#             figure={
#                 'data': [
#                     {'x': filtered_df['Country'], 'y': filtered_df['Cost of Living Index'], 'type': 'bar', 'name': 'Cost of Living Index'},
#                     {'x': filtered_df['Country'], 'y': filtered_df['Rent Index'], 'type': 'bar', 'name': 'Rent Index'}
#                 ],
#                 'layout': {
#                     'title': 'Cost of Living Index and Rent Index by Selected Country',
#                     'xaxis': {'title': 'Country'},
#                     'yaxis': {'title': 'Value'},
#                     'barmode': 'group'
#                 }
#             }
#         )

# if __name__ == '__main__':
#     app.run_server(debug=True)


# V2
import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

server = app.server

# get data
df = pd.read_csv('../data/processed_data.csv')
# drop unused column
df = df.drop(['Rank'], axis=1)

# =========================
# UI
# =========================
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Overview", href="/")),
        dbc.NavItem(dbc.NavLink("Table", href="/table")),
        dbc.NavItem(dbc.NavLink("Description", href="/description")),
    ],
    brand="Cost Viewer",
    brand_href="#",
    color="dark",
    dark=True,
)

kpi_card_1 = dbc.Card(
    id='kpi-card-1',
    style={"width": "18rem"}
)
kpi_card_2 = dbc.Card(
    id='kpi-card-2',
    style={"width": "18rem"}
)
kpi_card_3 = dbc.Card(
    id='kpi-card-3',
    style={"width": "18rem"}
)
overview_layout = html.Div([
                            dbc.Row([
                                    dbc.Col(kpi_card_1),
                                    dbc.Col(kpi_card_2),
                                    dbc.Col(kpi_card_3),
                                    dcc.Graph(id='map', style={"marginBottom": "5px"}),
                                    dcc.Graph(id='scatter')

                                     ])

                            ], id='overview-content')
table_layout = html.Div(
    [html.H2("Filtered Data Table"),
     dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                          id='datatable',
                          page_action='native',
                          page_current=0,
                          page_size=15,
                          style_table={'overflowX': 'auto'})

     ], id='table-content')
description_layout = html.Div(html.H1("Description"), id='description-content')

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Nav(navbar, style={"marginBottom": "5px"}),
    html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.Label('Select a continent', style={
                                   "marginBottom": "5px"}),
                        dcc.Dropdown(
                            id='continent-dropdown',
                            options=[
                                {'label': 'Africa', 'value': 'Africa'},
                                {'label': 'Asia', 'value': 'Asia'},
                                {'label': 'Europe', 'value': 'Europe'},
                                {'label': 'North America',
                                 'value': 'North America'},
                                {'label': 'South America',
                                 'value': 'South America'},
                                {'label': 'Oceania', 'value': 'Oceania'}
                            ],
                            value=['Africa', 'Asia', 'Europe',
                                   'North America', 'South America', 'Oceania'],
                            multi=True,
                            placeholder='Select a continent',
                            clearable=False
                        )
                    ])
                ),
                dbc.Col(html.Div([
                    html.Label('Select an index of interest',
                               style={"marginBottom": "5px"}),
                    dcc.Dropdown(
                        id='index-dropdown',
                        options=[
                            {'label': 'Cost of Living Index',
                             'value': 'Cost of Living Index'},
                            {'label': 'Rent Index',
                             'value': 'Rent Index'},
                            {'label': 'Cost of Living Plus Rent Index',
                             'value': 'Cost of Living Plus Rent Index'},
                            {'label': 'Groceries Index',
                             'value': 'Groceries Index'},
                            {'label': 'Restaurant Price Index',
                             'value': 'Restaurant Price Index'},
                            {'label': 'Local Purchasing Power Index',
                             'value': 'Local Purchasing Power Index'}
                        ],
                        value='Cost of Living Index',
                        clearable=False
                    )])
                ),
                dbc.Col(html.Div([
                    html.Label(
                        id='index-range-label', children='Select a range', style={"marginBottom": "5px"}),
                    dcc.RangeSlider(
                        id='index-slider',
                        min=0,
                        max=160,
                        step=20,
                        value=[0, 160],
                        marks={
                            0: {'label': '0', 'style': {'color': '#77b0b1'}},
                            20: {'label': '20'},
                            40: {'label': '40'},
                            60: {'label': '60'},
                            80: {'label': '80'},
                            100: {'label': '100 (NYC)', 'style': {'color': '#1950b5'}},
                            120: {'label': '120'},
                            140: {'label': '140'},
                            160: {'label': '160', 'style': {'color': '#f50'}}},
                        allowCross=False,
                        tooltip={"placement": "bottom",
                                 "always_visible": True}
                    )
                ])
                ),
            ], style={"padding": "10px"}),
        dbc.Row([
            dbc.Alert(
                "Index slider value must be a range instead of a single value",
                id="alert-fade",
                dismissable=True,
                is_open=False,
                color='warning'
            ),
            dbc.Alert(
                "Must select at least 1 continent (set to default selection with all continents)",
                id="alert-fade2",
                dismissable=True,
                is_open=False,
                color='warning'
            )], style={"padding": "10px"}),

        # dynamic page content
        dbc.Row(html.Div([overview_layout, table_layout, description_layout]))

    ], className='container'),

])


# =========================
# Server
# =========================
# -------------------------
# Edge case selection notification / enforcement
# -------------------------
@app.callback(Output('index-range-label', 'children'),
              Input('index-dropdown', 'value'))
def update_label(index_value):
    return f'Select a {index_value} range'


@app.callback(
    Output("alert-fade", "is_open"),
    Output('index-slider', 'value'),
    Input('index-slider', 'value')
)
def enforce_range(value):
    if value[0] == value[1]:
        if value[0] < 160:
            return True, [value[0], value[0] + 20]
        if value[0] == 160:
            return True, [value[0] - 20, value[1]]
    return False, value


@app.callback(
    Output("alert-fade2", "is_open"),
    Output('continent-dropdown', 'value'),
    Input('continent-dropdown', 'value')
)
def enforce_continent_select(value):
    if len(value) == 0:
        return True, ['Africa', 'Asia', 'Europe', 'North America', 'South America', 'Oceania']
    else:
        return False, value

# -------------------------
# Dynamic page layout
# -------------------------


@app.callback(
    Output("overview-content", "style"),
    Output("table-content", "style"),
    Output("description-content", "style"),
    Input("url", "pathname")
)
def render_page_content(pathname):
    if pathname == "/":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif pathname == "/table":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif pathname == "/description":
        return {"display": "none"}, {"display": "none"}, {"display": "block"}
    else:
        return {"display": "none"}, {"display": "none"}, {"display": "none"}

# -------------------------
# Update data table content
# -------------------------


@app.callback(
    Output('datatable', 'data'),
    Input('continent-dropdown', 'value'),
    Input('index-dropdown', 'value'),
    Input('index-slider', 'value'))
def update_data(continent_value, index_value, range_value):
    filtered_data = df.loc[df['Continent'].isin(continent_value)]
    filtered_data = filtered_data.loc[filtered_data[index_value].between(
        range_value[0], range_value[1])]
    return filtered_data.to_dict('records')

# -------------------------
# Update plot
# -------------------------

@app.callback(
    Output('scatter', 'figure'),
    Input('index-dropdown', 'value'),
    Input('datatable', 'data')
)
def update_scatter(index_value, data):
    if len(data) == 0:
        fig = go.Figure()
        fig.add_annotation(x=1, y=1, text='No resulting data',
                           showarrow=False, font=dict(size=20))
        return fig
    df = pd.DataFrame(data)
    fig = px.scatter(df, x='Cost of Living Index', y=index_value, color='Continent', 
                     hover_name='Country',
                     title=f'Cost of Living Index vs. {index_value}')
    fig.update_layout(legend_title='Continent')
    return fig

@app.callback(
    Output('kpi-card-1', 'children'),
    Output('kpi-card-2', 'children'),
    Output('kpi-card-3', 'children'),
    Input('index-dropdown', 'value'),
    Input('datatable', 'data')
)
def update_kpi(index_value, data):
    if len(data) == 0:
        card_body = html.H4(f"No resulting data")
        card_body2 = card_body
        card_body3 = card_body
    else:
        df = pd.DataFrame(data)
        max_value = df[index_value].max()
        max_country = df.loc[df[index_value] == max_value, 'Country'].iloc[0]
        max_continent = df.loc[df[index_value] == max_value, 'Continent'].iloc[0]
        min_value = df[index_value].min()
        min_country = df.loc[df[index_value] == min_value, 'Country'].iloc[0]
        min_continent = df.loc[df[index_value] == min_value, 'Continent'].iloc[0]

        mean_value = df[index_value].mean()

        card_body = [html.H5(f"{max_value:.2f}", className="card-title"),
                        html.P(
                            f'{max_country} ({max_continent})',
                            className="card-text",
                        )]
        card_body2 = [html.H5(f"{min_value:.2f}", className="card-title"),
                        html.P(
                            f'{min_country} ({min_continent})',
                            className="card-text",
                        )]
        card_body3 = [html.H5(f"{mean_value:.2f}", className="card-title"),]
    value = [
            dbc.CardHeader("Max Index Value"),
            dbc.CardBody(
                    card_body
            ),
            ]

    value2 = [
            dbc.CardHeader("Min Index Value"),
                dbc.CardBody(
                        card_body2
                ),
            ]
    value3 = [
            dbc.CardHeader("Mean Index Value"),
                dbc.CardBody(
                        card_body3
                ),
            ]
    return value, value2, value3

@app.callback(
        Output('map', 'figure'),
        Input('index-dropdown', 'value'),
        Input('datatable', 'data')
)
def update_map(index_value, data):
    
    
    if len(data) == 0:
        df = pd.DataFrame()

        fig = px.scatter_mapbox(df, lat=[], lon=[], height=500, zoom=1)
        fig.update_layout(
            mapbox_style='open-street-map',
            margin=dict(l=20, r=20, t=20, b=20),
            annotations=[
                dict(
                    text='No resulting data',
                    x=0.5,
                    y=0.5,
                    xref='paper',
                    yref='paper',
                    showarrow=False,
                    font=dict(size=20)
                )
            ]
        )
        return fig
    
    # if we have data, plot the map
    df = pd.DataFrame(data)
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        hover_name="Country",
        hover_data=[index_value],
        zoom=3,
        size=index_value,
        color=index_value,
        color_continuous_scale=px.colors.diverging.Temps,  # Change the color scale here
    )
    
    fig.update_layout(title=f'{index_value} Scatter Plot', 
                      mapbox_style="open-street-map",
                      margin={"r": 20, "t": 50, "l": 20, "b": 20})
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
