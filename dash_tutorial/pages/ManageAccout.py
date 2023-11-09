import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, callback, no_update
import requests


""" PLOTLY_LOGO is a object from s3 bucket."""
PLOTLY_LOGO = "https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png"

dash.register_page(
    __name__,
    path="/manageAccount",
    name="manageAccount",
    title="manageAccount",
)

""" nav_iteam can be used for mention links on header parts. """
nav_item = dbc.NavItem(dbc.NavLink("Sign out", href="#"))
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("change password", href='/changePassword'),
        dbc.DropdownMenuItem("Entry 2"),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Entry 3"),
    ],
    nav=True,
    in_navbar=True,
    label="Menu",
)

""" navbar layout """
navbar = html.Div(
    [
        dbc.Navbar(
            dbc.Container(
                [
                    html.A(
                        dbc.Row(
                            [
                                dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            ],
                            # align="center",
                            # className="g-0",
                        ),
                        href="https://myteamplanner.s3.eu-north-1.amazonaws.com/logo.png",
                        style={"textDecoration": "none"},
                    ),
                    dbc.NavbarToggler(id="navbar-toggler2", n_clicks=0),
                    dbc.Collapse(
                        dbc.Nav(
                            [dropdown, nav_item],
                            className="ms-auto",
                            navbar=True,
                        ),
                        id="navbar-collapse2",
                        navbar=True,
                    ),
                ],
            ),
            color="dark",
            dark=True,
            # className="mb-5",
        ),
        dcc.Location(id="url"),  # Add the URL location component
    ],
)

''' slide bar header is atteched on slidebar      '''
sidebar_header = dbc.Row(
    [
        dbc.Col(html.H2("Sidebar", className="display-4")),
        dbc.Col(
            [
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,.1)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            width="auto",
            align="center",
        ),
    ],
)


''' this is sidebar i try to mention in logo '''
sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "A responsive sidebar layout with collapsible navigation "
                    "links.",
                    className="lead",
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Home", href="/", active="exact"),
                    dbc.NavLink("Page 1", href="/page-1", active="exact"),
                    dbc.NavLink("Page 2", href="/page-2", active="exact"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
    className='child'
)

change_password = html.Div(className='center-div', children=[
    html.Div(className='simple-form', children=[
        dcc.Input(id="email", type="text", placeholder="Enter Email", className='input-field'),
        dcc.Input(placeholder="Old Password", id='old-password-input', type="password", className="input-field"),
        dcc.Input(placeholder="New Password", id='new-password-input', type="password", className="input-field"),
        html.Button("Change Password", id='change-password-button', className="simple-button"),
        html.Div(id='outputdiv'),
        dcc.Location(id='redirect', refresh=True),
    ]),
])
   
''' html page main div tag which is content side bar and nav bar with content.'''
layout = html.Div(
    children=[
        html.Div(children=[sidebar, navbar], className="child",),
        html.Div(
            children=[
                html.Div([], className="child"),
                html.Div([change_password], className="child content"),
            ],
            className="main",
        ),
        html.Div("footer", className="child"),
    ],
    className="parent",
)


@callback(
    Output('redirect', 'pathname'),
    Output('outputdiv', 'children'),
    Input('change-password-button', 'n_clicks'),
    Input('email', 'value'),
    Input('old-password-input', 'value'),
    Input('new-password-input', 'value')
)

def change_password(n_clicks, email, old_password, new_password):
    if n_clicks:
        data = {"email":email ,"old_password": old_password, "new_password": new_password}
        print("DATA -------------> ", data)
        response = requests.post("http://127.0.0.1:8000/account/change-password", json=data)
        print("Response : ------------> ", response)

        if response.status_code == 200:
            return html.Div(), '/'

        return no_update, html.Div("Incorrect Password")
    
    return no_update, no_update


def function():
    return html.H1('keval here.')