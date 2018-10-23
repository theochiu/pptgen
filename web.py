import dash
import dash_core_components as dcc
import dash_html_components as html
from gui import *

app = dash.Dash(__name__)

SONGLIST = []
getSongList(SONGLIST)


app.layout = html.Div(children=[
	html.H1(children="Powerpoint generator"),

	html.Label("Set title"),
	dcc.Input(type="text"),

	html.Label("Set leader"),
	dcc.Input(value="Theodore",type="text")


	html.Div(children="Choose songs"),

	options = []
	for song in SONGLIST:
		options.append({"label" : song, "value", song})

	dcc.Dropdown(options=options),


])
