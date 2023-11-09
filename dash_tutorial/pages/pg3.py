import dash

import dash_bootstrap_components as dbc

from dash import Input, Output, State, dcc, html, callback

from .ManageAccout import function

 

dash.register_page(

    __name__,

    path="/p3",

    name="p3",

)

 

layout = None