import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import os

class RainfallDashboard:
    def __init__(self):
        self.app = dash.Dash(__name__)
        self.df = self.load_data()
        self.setup_layout()
        self.setup_callbacks()

    def load_data(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(current_dir, 'IDCJAC0009_066214_2018_Data.csv')
        df = pd.read_csv(csv_path)
        df['Date'] = pd.to_datetime(df[['Year', 'Month', 'Day']])
        return df

    def setup_layout(self):
        self.app.layout = html.Div([
            html.H1('Australische Niederschlagsübersicht'),
            
            html.Div([
                html.Label('Jahr auswählen:'),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[{'label': str(year), 'value': year} for year in sorted(self.df['Year'].unique())],
                    value=self.df['Year'].max()
                ),
            ], style={'width': '30%', 'display': 'inline-block'}),
            
            html.Div([
                html.Label('Monat auswählen:'),
                dcc.Dropdown(
                    id='month-dropdown',
                    options=[{'label': str(month), 'value': month} for month in range(1, 13)],
                    value=1
                ),
            ], style={'width': '30%', 'display': 'inline-block'}),
            
            dcc.Graph(id='rainfall-graph'),
            
            html.Div([
                html.H3('Monatliche Statistik'),
                html.Div(id='monthly-stats')
            ])
        ])

# Callback zur Aktualisierung des Graphen definieren
    def setup_callbacks(self):
        @self.app.callback(
            [Output('rainfall-graph', 'figure'),
             Output('monthly-stats', 'children')],
            [Input('year-dropdown', 'value'),
             Input('month-dropdown', 'value')]
        )
        def update_graph(selected_year, selected_month):
            filtered_df = self.df[(self.df['Year'] == selected_year) & (self.df['Month'] == selected_month)]
            
            fig = px.line(filtered_df, x='Date', y='Rainfall amount (millimetres)', 
                          title=f'Täglicher Niederschlag in {selected_year}-{selected_month:02d}')
            fig.update_xaxes(title='Datum')
            fig.update_yaxes(title='Niederschlag (mm)')
            
            total_rainfall = filtered_df['Rainfall amount (millimetres)'].sum()
            avg_rainfall = filtered_df['Rainfall amount (millimetres)'].mean()
            max_rainfall = filtered_df['Rainfall amount (millimetres)'].max()
            
            stats = html.Div([
                html.P(f"Niderschlag insgesamt: {total_rainfall:.2f} mm"),
                html.P(f"durchschnittlicher Niederschlag pro Tag: {avg_rainfall:.2f} mm"),
                html.P(f"maximaler Niederschlag pro Tag: {max_rainfall:.2f} mm")
            ])
            
            return fig, stats

    def run(self, debug=True):
        self.app.run_server(debug=debug)