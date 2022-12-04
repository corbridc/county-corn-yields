from dash import Dash, html, dcc, Output, Input, State
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
from map import Map
from model import Model
import plotly.express as px

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = "Corn Yields"

df = pd.read_csv('data/combine_data.csv')
df = df.dropna(subset=['Year', 'corn_yield_per_acre'])

preds = pd.read_csv('data/iowa_results_sample.csv')

graph = Map(df)

inputs = dbc.Form([
    dbc.Row(
        [
            dbc.Col([dbc.Label("State", html_for="state"),
                   dcc.Dropdown(np.sort(df.state_name.str.capitalize().unique()), "Iowa", id="state"),
                   dbc.Label("Corn Price Per Bushel", html_for="price"),
                   dcc.Dropdown(np.sort(preds.corn_price_per_bushel.unique()),id="price"),
                   dbc.Label("Total Rain (inches)", html_for="total_rain"),
                   dcc.Dropdown(np.sort(preds.total_rain.unique()),id="total_rain"),
                   dbc.Label("Max Temperature", html_for="max_temp"),
                   dcc.Dropdown(np.sort(preds.max_temp.unique()),id="max_temp"),      
                   dbc.Label("Days with temperature above 95 degrees", html_for="too_hot_days"),
                   dcc.Dropdown(np.sort(preds.too_hot_days.unique()),id="too_hot_days"),
                   html.Br(),
    ], width=6),
    dbc.Col([
                   dbc.Label("County", html_for="county"),

                   dcc.Dropdown(np.sort(df.county.str.capitalize().unique()),id="county"),

                   dbc.Label("Land rental price ($/ac)", html_for="land_rental_price"),
                   dcc.Dropdown(np.sort(preds.land_rental_price.unique()),id="land_rental_price"),
   
                   dbc.Label("Number of rainy days", html_for="rain_days"),
      
                   dcc.Dropdown(np.sort(preds.rain_days.unique()),id="rain_days"),
                   dbc.Label("Min Temperature", html_for="min_temp"),
         
                   dcc.Dropdown(np.sort(preds.min_temp.unique()),id="min_temp"),
                   dbc.Label("Days with temperature below 50 degrees", html_for="too_cold_days"),
             
                   dcc.Dropdown(np.sort(preds.too_cold_days.unique()),id="too_cold_days"),
                   
                   html.Br(),
                   
    ], width=6), dbc.Button("Get Corn Yield Prediction for 2022", id="run", color="primary"),
                   html.Br(), html.Br(), html.Div(id='dd-output-container')]
        
    )
    
                   
                   
])
#find counties of state
@app.callback(
    Output('county', 'options'),
    Input('state', 'value'))
def set_county_options(selected_state):
    return np.sort(df[df.state_name.str.capitalize() == selected_state].county.str.capitalize().unique())

#set placeholder as first county (alphabetically in state)
@app.callback(
    Output('county', 'value'),
    Input('county', 'options'))
def set_county_value(available_options):
    return available_options[0]

#set placeholder as highest corn price
@app.callback(
    Output('price', 'value'),
    Input('price', 'options'))
def set_county_value(available_options):
    return available_options[-1]

@app.callback(
    Output('total_rain', 'value'),
    Input('total_rain', 'options'))
def set_county_value(available_options):
    return available_options[0]

#set placeholder as lowest rainy days
@app.callback(
    Output('rain_days', 'value'),
    Input('rain_days', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output('max_temp', 'value'),
    Input('max_temp', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output('min_temp', 'value'),
    Input('min_temp', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output('too_hot_days', 'value'),
    Input('too_hot_days', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output('too_cold_days', 'value'),
    Input('too_cold_days', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output('land_rental_price', 'value'),
    Input('land_rental_price', 'options'))
def set_county_value(available_options):
    return available_options[0]

@app.callback(
    Output("yield-graph", "figure"), 
    Input("county", "value"),
    Input("state", "value"))
def update_line_chart(county, state):
    county_df = df[(df.county.str.capitalize() == county)&((df.state_name.str.capitalize() == state))]
    fig = px.line(county_df, 
        x="year", y="corn_yield_per_acre", 
        title= f"Historical Corn Yield in Bu/Acre for {county.capitalize()}, {state}",
        labels={
            "corn_yield_per_acre":"Corn Yield Per Acre",
            "year":"Year"
        })
    return fig



filterMap = dbc.Form([
    dbc.Label("Year", html_for="year"),
    dcc.Dropdown(np.sort(df.Year.unique()), 2021, id="year"),
    html.Br(),
    dbc.Label("State", html_for="state_map"),
    dcc.Dropdown(np.sort(df.state_id.unique()), "IA", id="state_map"),
    html.Br(),
    dbc.Col(dbc.Button("filter", id="filterMap", color="primary"))]
)

body = dbc.Row([
    # input
    html.H3("Yield Prediction"),
    dbc.Row([
        # input
        dbc.Col(md=4, children=[inputs]),
        
        # graph
        dbc.Col(dbc.Spinner([dcc.Graph(id="yield-graph")], color="primary", type="grow"), md=8)
    ]),

    html.H3("Predicted Yield"),
    dbc.Row([
        # result
        # TODO Make result look better
        dbc.Col(html.P(id='result'), md=4),
]),


    html.H3("Historical Yield"),
    dbc.Row([
        # filter
        dbc.Col(filterMap, md=4),
        # map
        dbc.Col(dbc.Spinner([dcc.Graph(id="plot")], color="primary", type="grow"), md=8)])
])


@app.callback(output=[Output(component_id="result", component_property="children")],
              inputs=[Input(component_id="run", component_property="n_clicks")],
              state=[State("county", "value"), 
              State("state", "value"), 
              State("price", "value"),
              State("total_rain", "value"),
              State("rain_days", "value"), 
              State("max_temp", "value"),
              State("min_temp", "value"),
              State("too_hot_days", "value"), 
              State("too_cold_days", "value"),
              State("land_rental_price", "value"),
              ])
def results(n_clicks, county, state, price, total_rain, rain_days, 
    max_temp, min_temp, too_hot_days, too_cold_days, land_rental_price):
    
    if len(preds[
        (preds.state_name.str.capitalize()==state) & 
        (preds.county.str.capitalize()==county) &
        (preds.corn_price_per_bushel == price) &
        (preds.total_rain == total_rain) &
        (preds.rain_days == rain_days) &
        (preds.max_temp == max_temp) &
        (preds.min_temp == min_temp) &
        (preds.too_hot_days == too_hot_days) &
        (preds.too_cold_days == too_cold_days) & 
        (preds.land_rental_price == land_rental_price)
        ]
        .pred_corn_yield_per_acre) > 0:

        pred = preds[
            (preds.state_name.str.capitalize()==state) & 
            (preds.county.str.capitalize()==county) &
            (preds.corn_price_per_bushel == price) &
            (preds.total_rain == total_rain) &
            (preds.rain_days == rain_days) &
            (preds.max_temp == max_temp) &
            (preds.min_temp == min_temp) &
            (preds.too_hot_days == too_hot_days) &
            (preds.too_cold_days == too_cold_days) & 
            (preds.land_rental_price == land_rental_price)
            ].pred_corn_yield_per_acre.values[0]
    else:
        pred = 200
    return ["Predicted Yield: " + str(round(pred, 2))]


@app.callback(output=[Output(component_id="plot", component_property="figure")],
              inputs=[Input(component_id="filterMap", component_property="n_clicks")],
              state=[State("year", "value"), State("state_map", "value")])
def show_map(n_clicks, year, state):
    print('In result with year: ' + str(year) + ' and ' + state)
    return [graph.plot(year, state)]


app.layout = dbc.Container([
    html.H1("Predicting Local Corn Yield", id="nav-pills"),
    body
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
