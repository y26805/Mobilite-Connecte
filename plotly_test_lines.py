import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

df_airports = pd.read_csv('EUairports.csv')
df_airports.head()

df_flight_paths = pd.read_csv('flights_EU_0120.csv')
df_flight_paths.head()

airports = [ dict(
	type = 'scattergeo',
	lat = df_airports['lat'],
	lon = df_airports['lon'],
	hoverinfo = 'text',
	text = df_airports['airportName'],
	mode = 'markers',
	marker = dict(
		size = 1,
		color = 'rgb(255,0,0)',
		opacity = 0.8,
		line = dict(
			width = 3,
			color = 'rgba(68,68,68,0)'
		)
	))]

flight_paths = []
for i in range( len( df_flight_paths ) ):
    flight_paths.append(
        dict(
            type = 'scattergeo',
            locationmode = 'europe',
            lon = [ df_flight_paths['start_lon'][i], df_flight_paths['end_lon'][i] ],
            lat = [ df_flight_paths['start_lat'][i], df_flight_paths['end_lat'][i] ],
            mode = 'lines',
            line = dict(
                width = 1,
                color = 'red',
            ),
            opacity = 0.1,
        )
    )

layout = dict(
	autosize = False,
	width = 1400,
	height = 800,
	showlegend = False,
	title = '<b>European connections</b><br>(Hover for airport name)<br>Source:<a href="https://developer.lufthansa.com/page">Lufthansa API</a>',
	geo = dict(
		projection=dict( type='mercator'),
		scope = 'europe',
		showland = True,
		showcountries = True,
		landcolor = 'rgb(250,250,250)',
		subunitcolor = 'rgb(217, 217, 217)',
		countrycolor = 'rgb(217,217,217)',
		countrywidth = 2,
		subunitwidth = 0.5
		)
	)


plotly.offline.plot({"data":flight_paths + airports, "layout":layout})
