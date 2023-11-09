import dash 
import dash_bootstrap_components as dbc
import requests
from dash import html, dcc,Output,Input,callback, no_update
import requests

dash.register_page(__name__, path='/registration', name='registration')

layout = html.Div(className="simple-form", children=[
    
])
layout = html.Div(className='center-div', children=[
    html.Div(className='simple-form', children=[
        html.H2("Registration Form"),
        dcc.Input(placeholder="Username",id='username-input', type="text", className="input-field"),
        dcc.Input(placeholder="Email", id='email-input', type="email", className="input-field"),
        dcc.Input(placeholder="Password", id='password-input', type="password", className="input-field"),
        html.Button("Register", id='registerbutton', className="simple-button"),
        html.P([ "If you already registor than, ",
                dcc.Link("login here", id="registration", href="/", className="registration-link"),
            ]),  
        html.Div(id='output-div2'),
        dcc.Location(id='redirect-page', refresh=True),
    ]),
])


@callback(
    Output('output-div2', 'children'),
    Output('redirect-page', 'pathname'),
    Input('registerbutton', 'n_clicks'),
    Input('username-input', 'value'),
    Input('email-input', 'value'),
    Input('password-input', 'value')
)
def register_user(n_clicks, username, email, password):
    if n_clicks:
        data = {"username": username, "email": email, "password": password}
        print("DATA -------------> ", data)
        response = requests.post("http://127.0.0.1:8000/account/register", json=data)
        print("Response : ------------> ", response)

        if response.status_code == 200:
            return html.Div(), '/'
        else:
            return html.Div(children=[dbc.Alert("Invalid username or password!", color="dark", className="alert-box")],
                            className='static-info'
                            ), '/'

    return no_update, no_update


