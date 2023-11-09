# to do (working in progress)

import dash 
import dash_bootstrap_components as dbc
import requests
from dash import html, dcc,Output,Input,callback, no_update


external_stylesheets = [dbc.themes.BOOTSTRAP]+['assets/style.css']
dash.register_page(__name__, path='/changePassword', name='changePassword', external_stylesheets=['assets/registration.css']),


layout = html.Div(className='center-div', children=[
    html.Div(className='simple-form', children=[
        dcc.Input(placeholder="Email", id='email-input', type="email", className="input-field"),
        dcc.Input(placeholder="Old Password", id='old-password-input', type="password", className="input-field"),
        dcc.Input(placeholder="New Password", id='new-password-input', type="password", className="input-field"),
        html.Button("Change Password", id='change-password-button', className="simple-button"),
        html.Div(id='outputdiv'),
        dcc.Location(id='redirect', refresh=True),
    ]),
])
   

@callback(
    Output('redirect', 'pathname'),
    Output('outputdiv', 'children'),
    Input('change-password-button', 'n_clicks'),
    Input('old-password-input', 'value'),
    Input('new-password-input', 'value'),
    Input('email-input', 'value'),


)

def change_password(n_clicks, old_password, new_password,email):
    if n_clicks:
        data = {"email": email,"old_password": old_password, "new_password": new_password}
        print("DATA -------------> ", data)
        response = requests.post("http://127.0.0.1:8000/changePassword", json=data)
        print("Response : ------------> ", response)

        if response.status_code == 200:
            return html.Div(), '/'

        return no_update, html.Div("Incorrect Password")
    
    return no_update, no_update

layout = None


