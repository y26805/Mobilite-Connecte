import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv('airport_clean.csv')
df.head()

# Create text as explanation when mouse over.
df['text'] = df['airport_name'] + '\n' + df['airport_code']

data = [ dict(
	type = 'scattergeo',
	lat = df['latitude'],
	lon = df['longitude'],
	text = df['text'],
	mode = 'markers',
	marker = dict(
		size = 5,
		opacity = 0.8,
		symbol = 'squares',
		))]

layout = dict(
	title = '<b>Airports around the world</b><br>(Hover for airport code)<br>Source:<a href="https://developer.lufthansa.com/page">Lufthansa API</a>',
	geo = dict(
		projection=dict( type='mercator'),
		showland = True,
		showcountries = True,
		landcolor = 'rgb(250,250,250)',
		subunitcolor = 'rgb(217, 217, 217)',
		countrycolor = 'rgb(217,217,217)',
		countrywidth = 2,
		subunitwidth = 0.5
		)
	)


plotly.offline.plot({"data":data, "layout":layout})
