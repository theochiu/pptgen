import dash
import dash_core_components as dcc
import dash_html_components as html
import os

import plotly.plotly as py
import plotly.figure_factory as ff

from dash.dependencies import *
# import dash_table_experiments as dt

external_stylesheets = ['https://getbootstrap.com/docs/4.1/dist/css/bootstrap.min.css']

app = dash.Dash(__name__)

external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", 
                external_stylesheets,
                ]

for css in external_css:
    app.css.append_css({"external_url": css})

SONGLIST = []



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

		html.H3(html.Label("Set title")),
		html.P(dcc.Input(type="text")),

		html.H3(html.Label("Set leader")),
		html.P(dcc.Input(placeholder="Theodore",type="text")),


		html.H2(children="Choose songs"),


		dcc.Dropdown(options=options, id="song_options"),

		html.P(),
		html.P(),

		html.Div([
			html.Button("Add", id="add_button", n_clicks=0),
			html.Button("Edit", id="edit_button")

		], style={"columnCount" : "2"}),

	], style= {'width': '44%', 
			'display': 'inline-block',
			'margin-right' : '100px',
			'margin-left' : '25px'

	}),


	# RIGHT SIDE
	html.Div([
		html.H1("Setlist"),
		html.P("set table here"),
		html.Div(id="set_table"),

		# html.H1("datatable test"),
		# dt.DataTable(
		# 	id="datatable",
		# 	rows=[1,2,3],
		# 	editable=False,
		# 	row_selectable=True,
		# 	filterable=True,
		# 	selected_row_indices=[]
		# ),

		html.P(),
		html.P(),

		html.Div([
			html.Button("Remove", id="remove_button"),
			html.Button("Build", id="build_button", n_clicks=0),
		]),



	], style= {'width': '44%', 'display': 'inline-block', "position" : "absolute"})

], style={"columnCount": "1"})


# EVENT LISTENERS

setlist = []
# @app.callback(Output("textarea", "value"),
# 	[Input("add_button", "n_clicks")],
# 	[State("song_options", "value"),
# 	State("textarea", "value")
# 	],
# )

# def update_setlist(n_clicks, song_input, oldsong):
# 	print("callback")
# 	print(song_input)
# 	if n_clicks > 0 and song_input in SONGLIST :
# 		setlist.append(str(song_input))
# 		text_out = ""
# 		for song in setlist:
# 			text_out += song + "\n"
# 		return text_out
# 	return ""

@app.callback(Output("set_table", "children"),
	[Input("add_button", "n_clicks")],
	[State("song_options", "value")]
)
def generate_table(n_clicks, song_input):

	print("generate_table")
	print(song_input)
	if n_clicks > 0 and song_input in SONGLIST :
		setlist.append(str(song_input))

	return html.Table(
		# Header
		[html.Tr(html.Th("Setlist"), style={"text-align" : "left"})] +

		# Body
		[html.Tr([html.Td(song)]) for song in setlist ],

	
	)



if __name__ == '__main__':
	app.run_server(debug=True, port=3000)


