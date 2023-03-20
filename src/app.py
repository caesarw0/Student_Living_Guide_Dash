import dash
from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.title = 'Cost Viewer'

server = app.server

# get data
df = pd.read_csv('../data/processed_data.csv')
# drop unused column
df = df.drop(['Rank'], axis=1)
indices = ['Cost of Living Index', 'Rent Index',
           'Cost of Living Plus Rent Index', 'Groceries Index',
           'Restaurant Price Index', 'Local Purchasing Power Index']

# get today's year
today = datetime.date.today()
year = today.year

# =========================
# UI
# =========================
GITHUB_LOGO = 'https://raw.githubusercontent.com/simple-icons/simple-icons/develop/icons/github.svg'
navbar = dbc.NavbarSimple(
    [
        dbc.NavItem(dbc.NavLink("Overview", href="/")),
        dbc.NavItem(dbc.NavLink("Table", href="/table")),
        dbc.NavItem(dbc.NavLink("Description", href="/description")),
        html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=GITHUB_LOGO, height="30px")),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="https://github.com/caesarw0/Student_Living_Guide_Dash.git",
                style={"textDecoration": "none"},
            )
    ],
    brand="Cost Viewer",
    brand_href="#",
    color="dark",
    dark=True,
)

kpi_card_1 = dbc.Card(
    id='kpi-card-1',
    #style={"width": "18rem"}
)
kpi_card_2 = dbc.Card(
    id='kpi-card-2',
    #style={"width": "18rem"}
)
kpi_card_3 = dbc.Card(
    id='kpi-card-3',
    #style={"height": "90px"}
)
overview_layout = html.Div([
    dbc.Row([
        dbc.Col([dcc.Graph(id='map'),
                 dcc.Graph(id='corr'),
                 ], width=4),
        dbc.Col([
            dbc.Row([
                dbc.Col(kpi_card_1),
                dbc.Col(kpi_card_2),
                dbc.Col(kpi_card_3), ]),
            dbc.Row([
                dbc.Col(
                    dcc.Graph(id='country_bar'), width=4),
                dbc.Col(
                    dcc.Graph(id='scatter'), width=8),
            ], style={"margin": "0px", "padding": "0px"}),
            dbc.Row([dcc.Graph(id='stack'), ])
        ], width=8)
    ])

], id='overview-content',
    style={"margin": "0px", "padding": "0px"})
table_layout = html.Div(
    [html.H3("Filtered Data Table"),
     dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                          id='datatable',
                          page_action='native',
                          page_current=0,
                          page_size=15,
                          style_table={'overflowX': 'auto'})

     ], id='table-content')
description_layout = html.Div(
    [html.H3("Description"),
     dcc.Markdown('''
    The [Numbeo](https://www.numbeo.com/cost-of-living/) Cost of Living Index dataset contains information on 
    the cost of living in cities across the globe. 
    The five primary indices included in the dataset are `Cost of Living Index`, `Rent Index`, `Groceries Index`, 
    `Restaurant Price Index` and `Local Purchasing Power Index`. All the indices take New York City with a value of 
    100 as a reference point.

    The `Cost of Living Index` will be the primary emphasis of our dashboard. 
    It is determined by measuring the cost of living throughout each region with that in New York City for a 
    standard set of goods and services, including housing, transportation, and utilities. 
    A city with a `Cost of Living Index` of 80, for instance, suggests that housing costs there are 20% lower than in New York City.

    The `Rent Index` which is derived by contrasting the monthly rental rates in that city with those in New York, 
    is further included in the Numbeo dataset. As their names imply, the `Groceries Index` and 
    `Restaurant Index` are indices that compare the cost of groceries and restaurant meals in relation to New York.

    The `Local Purchasing Power Index` calculates the difference between a city's average income and New York City's 
    purchasing power, with a score of 100 denoting equal purchasing power. In other words, cities with scores more than 
    100 have average salaries that can buy more goods and services than those in New York City, while cities with scores 
    lower than 100 have average salaries that can buy less goods and services than those in New York City.

    Together with the key indices, we also performed data preprocessing to acquire the continent, latitude, 
    and longitude of the nation or city, which will enable us to view the data on a map.
''')],                        id='description-content')

app.layout = html.Div([
    dcc.Location(id="url"),
    html.Nav(navbar),
    html.Div([
        dbc.Row(
            [
                dbc.Col(
                    html.Div([
                        html.Label('Select Continent(s)', style={
                                   "marginBottom": "5px", "fontWeight": "bold"}),
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
                            placeholder='Select Continent(s)',
                            clearable=False
                        )
                    ])
                ),
                dbc.Col(html.Div([
                    html.Label('Select an Index of Interest',
                               style={"marginBottom": "5px", "fontWeight": "bold"}),
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
                        id='index-range-label', children='Select a range', style={"marginBottom": "5px", "fontWeight": "bold"}),
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
            ], style={"padding": "2px"}),
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
            )], style={"padding": "5px"}),

        # dynamic page content
        dbc.Row(html.Div([overview_layout, table_layout, description_layout])),

        dbc.Row(
            html.Footer(f"© {year} UBC-MDS All Right Reserved.",className="d-flex justify-content-center")
            ,class_name="d-flex justify-content-center"
            )

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
    return f'Select a {index_value} Range'


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
        max_continent = df.loc[df[index_value]
                               == max_value, 'Continent'].iloc[0]
        min_value = df[index_value].min()
        min_country = df.loc[df[index_value] == min_value, 'Country'].iloc[0]
        min_continent = df.loc[df[index_value]
                               == min_value, 'Continent'].iloc[0]

        mean_value = df[index_value].mean()

        card_body = [html.P(f"{max_value:.2f} - {max_country} ({max_continent})",
                            className="card-text", style={"font-size": "12px", "fontWeight": "bold"}), ]
        card_body2 = [html.P(f"{min_value:.2f} - {min_country} ({min_continent})",
                             className="card-text", style={"font-size": "12px", "fontWeight": "bold"}), ]
        card_body3 = [html.P(f"{mean_value:.2f}",
                             className="card-text", style={"font-size": "12px", "fontWeight": "bold"}), ]
    value = [
        dbc.CardHeader("Max Index Value", style={"font-size": "14px"}),
        dbc.CardBody(
            card_body
        ),
    ]

    value2 = [
        dbc.CardHeader("Min Index Value", style={"font-size": "14px"}),
        dbc.CardBody(
            card_body2
        ),
    ]
    value3 = [
        dbc.CardHeader("Mean Index Value", style={"font-size": "14px"}),
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
        fig.update_layout(title=f'<b>{index_value} World Map</b>')
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
        color_continuous_scale=px.colors.diverging.Temps,
    )

    fig.update_layout(title=f'<b>{index_value} World Map</b>',
                      mapbox_style="open-street-map",
                      margin={"r": 0, "t": 30, "l": 0, "b": 0},
                      coloraxis_colorbar=dict(
                          title='',
                          thickness=10,
                          yanchor="middle",
                          y=0.5,
                          ticks="outside",
                          ticklen=2,
                          tickfont=dict(size=10),
                      ))
    return fig


@app.callback(
    Output('country_bar', 'figure'),
    Input('map', 'clickData'),
    Input('datatable', 'data')
)
def display_click_data(clickData, data):
    if clickData is not None and len(data) > 0:
        df = pd.DataFrame(data)
        country_name = clickData['points'][0]['hovertext']

        filtered_df = df.query(f"Country == '{country_name}'")
        if len(filtered_df) > 0:
            filtered_df = filtered_df[indices].T
            fig = go.Figure(
                data=[go.Bar(x=filtered_df.index, y=filtered_df.iloc[:, 0])])
            fig.update_layout(title=f'<b>{country_name} Index Value</b>', xaxis_tickangle=45,
                              margin={"r": 0, "t": 45, "l": 0, "b": 0},
                              height=250,
                              xaxis=dict(showticklabels=False,)
                              #xaxis={'showticklabels': False, 'title': 'Hover to check index name', 'title_font': {'size': 12}}
                              )
            return fig

    fig = go.Figure()
    fig.add_annotation(x=2, y=2, text='Click on the map to select',
                       showarrow=False, font=dict(size=15))
    fig.update_layout(title='<b>Country Index Value</b>',
                      margin={"r": 0, "t": 45, "l": 0, "b": 0},
                      height=250)
    return fig


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
        fig.update_layout(title=f'<b>Cost of Living Index vs. {index_value}</b>',
                          margin={"r": 0, "t": 45, "l": 0, "b": 0},
                          height=250)
        return fig
    df = pd.DataFrame(data)
    fig = px.scatter(df, x='Cost of Living Index', y=index_value, color='Continent',
                     hover_name='Country',
                     title=f'<b>Cost of Living Index vs. {index_value}</b>')
    fig.update_layout(legend_title='Continent',
                      margin={"r": 0, "t": 45, "l": 0, "b": 0},
                      height=250)
    return fig


@app.callback(
    Output('corr', 'figure'),
    Input('datatable', 'data')
)
def update_correlation(data):
    if len(data) == 0:
        fig = go.Figure()
        fig.add_annotation(x=1, y=1, text='No resulting data',
                           showarrow=False, font=dict(size=20))
        fig.update_layout(title='<b>Correlation Matrix Heatmap</b>',
                          margin={"r": 0, "t": 60, "l": 0, "b": 0})
        return fig
    df = pd.DataFrame(data)

    # calculate the correlation matrix
    corr_matrix = df[indices].corr()

    heatmap = go.Heatmap(
        x=indices,
        y=indices,
        z=corr_matrix.values,
        colorscale='Viridis',
    )

    layout = go.Layout(
        title='<b>Correlation Matrix Heatmap</b>',
        margin={"r": 0, "t": 60, "l": 0, "b": 0}
    )

    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


@app.callback(
    Output('stack', 'figure'),
    Input('index-dropdown', 'value'),
    Input('datatable', 'data')
)
def update_stack(index_value, data):
    if len(data) == 0:
        fig = go.Figure()
        fig.add_annotation(x=1, y=1, text='No resulting data',
                           showarrow=False, font=dict(size=20))
        fig.update_layout(title='<b>Top N Most Expensive Country</b>',
                          margin={"r": 0, "t": 50, "l": 0, "b": 0})
        return fig

    df = pd.DataFrame(data)
    sorted_df = df.sort_values(by=index_value, ascending=False)

    top_n = 10
    if len(data) < 10:
        top_n = len(data)

    top_df = sorted_df.head(top_n)
    fig = px.bar(top_df, x="Country", y=indices,
                 title=f"<b>Cost of Living Breakdown for the Top {top_n} Most Expensive Countries</b>")
    fig.update_layout(margin={"r": 0, "t": 50, "l": 0, "b": 0})
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
