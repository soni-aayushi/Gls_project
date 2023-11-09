import dash
from dash import dcc, html, callback, Output, Input, State, no_update
import dash_bootstrap_components as dbc
import requests


dash.register_page(__name__, path="/forgotPassword", name="forgotPassword")

layout = html.Div(className='center-div', children=[
    html.Div(className='simple-form', children=[
        dcc.Input(id="email", type="email", placeholder="Enter Email", className='input-field'),
        html.Button("submit", id="submit", n_clicks=0, disabled=True, className=""),
    ]),
])
     


@callback(
    Output('submit', 'disabled'),
    # Output('show-alert', 'children'),
    Input('email', 'value'),
    Input('submit', 'n_clicks'),
)
def show_data(email, submit):
    if email:
        if submit > 0:
            data = {"email": email}
            print("DATA -------------> ", data)
            return no_update
        return False
    

    return True 



