from dash.dependencies import Input, Output
from dash import dcc, html


import pandas as pd

df = pd.read_csv('data/processed_data.csv')


def register_callbacks(app):

    @app.callback(Output('output-tab1', 'children'),
              [
               Input('country_select', 'value')])
    def update_output_tab1(country):
        if country == []:
            return html.Div('Please select a continent and a country.')
        else:
            filtered_df = df[df['Country'] == country]
            return dcc.Graph(
                figure={
                    'data': [
                        {'x': filtered_df['Country'], 'y': filtered_df['Cost of Living Index'], 'type': 'bar', 'name': 'Cost of Living Index'},
                        {'x': filtered_df['Country'], 'y': filtered_df['Rent Index'], 'type': 'bar', 'name': 'Rent Index'}
                    ],
                    'layout': {
                        'title': 'Cost of Living Index and Rent Index by Selected Country',
                        'xaxis': {'title': 'Country'},
                        'yaxis': {'title': 'Value'},
                        'barmode': 'group'
                    }
                }
            )

