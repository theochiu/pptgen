import dash
import dash_core_components as dcc
import dash_html_components as html
import os

import plotly.plotly as py
import plotly.figure_factory as ff

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

SONGLIST = []



data_matrix = [['Country', 'Year', 'Population'],
			   ['United States', 2000, 282200000],
			   ['Canada', 2000, 27790000],
			   ['United States', 2005, 295500000],
			   ['Canada', 2005, 32310000],
			   ['United States', 2010, 309000000],
			   ['Canada', 2010, 34000000]]


def getSonglist(songlist):
	""" Populates argument songlist with songs from directory """
	# Purges contents of the old listbox
	songs = []
	for file_name in os.listdir(os.getcwd() + "/song database/"):
		root, ext = os.path.splitext(file_name)
		if ext == ".txt":
			songs.append(root)
	songs = sorted(songs)
	for song in songs:
		songlist.append(song)



getSonglist(SONGLIST)

options = []
for song in SONGLIST:
	options.append({"label" : song, "value": song})


app.layout = html.Div([

	# LEFT SIDE
	html.Div([
		html.Link(href='style.css', rel='stylesheet'),

		html.H1("Powerpoint generator"),

		html.P(html.Label("Set title")),
		html.P(dcc.Input(type="text")),

		html.P(html.Label("Set leader")),
		html.P(dcc.Input(placeholder="Theodore",type="text")),


		html.H2(children="Choose songs"),


		dcc.Dropdown(options=options),

		html.P(),
		html.P(),

		html.Div([
			html.Button("Add", id="submit_button"),
			html.Button("Edit", id="edit_button")

		], style={"columnCount" : "2"}),

	], style= {'width': '44%', 
			'display': 'inline-block',
			'margin-right' : '100px'

	}),


	# RIGHT SIDE
	html.Div([
		html.H1("Setlist"),
		html.P("set table here"),
		html.Button("Build", id="build_button")




	], style= {'width': '44%', 'display': 'inline-block', "position" : "absolute"})

], style={"columnCount": "1"})

if __name__ == '__main__':
	app.run_server(debug=True, port=3000)


