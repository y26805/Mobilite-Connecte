import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import math

df = pd.read_csv('airport_as_origin_count.csv')
df.head()

df['text'] = df['name'] + '<br>Accessibility factor: ' + (df['count']/85*100).astype(int).astype(str)

# Define how to classify
limits = [(0,5),(6,10),(11,20),(21,50),(51,220)]
labels = ['1st - 5th','6th - 10th', '11th - 20th','21st - 50th', '51st -']

# Choose colors for the legend
colors = ["rgb(24,150,151)","rgb(55,201,202)","rgb(97,220,221)","rgb(145,235,236)","rgb(205,240,240)"]
cities1 = []
cities2 = []
cities3 = []
cities4 = []
cities5 = []
listnames = [cities1, cities2,cities3,cities4,cities5]

for i in range(len(limits)):
	lim = limits[i]
	# Create a subset of data frame
	df_sub = df[lim[0]:lim[1]]

	displaySize = df_sub['count']/85*100
	if displaySize.any() == 0:
		size = 0.5

	city = dict(
		type = 'scattergeo',
		lat = df_sub['lat'],
		lon = df_sub['lon'],
		text = df_sub['text'],
		marker = dict(
			# Define size as factor of count divided by maximum count
			size = displaySize,
			color = colors[i],
			opacity = 0.5,
			line = dict(width = 0.5, color = 'rgb(40,40,40)'),
			# Diameter or area
			sizemode = 'diameter'
		),
		name = labels[i]
	)
	listnames[i].append(city)

layout = dict(
	font = dict(
		family = 'Arial',
	),
	autosize = False,
	width = 1400,
	height = 800,
	showlegend = True,
	title = '<b>Hubs in Europe served by Lufthansa</b><br>(Hover for airport name)<br>Source: <a href="https://developer.lufthansa.com/page">Lufthansa API</a>',
	geo = dict(
		projection = dict( type='mercator', scale = 3,),
		scope = 'europe',
		showland = True,
		showcountries = True,
		landcolor = 'rgb(250,250,250)',
		subunitcolor = 'rgb(217, 217, 217)',
		countrycolor = 'rgb(217,217,217)',
		countrywidth = 2,
		subunitwidth = 0.5,
		),
	legend = dict(
		traceorder = 'reversed'
	)
	)


plotly.offline.plot({"data":cities5 + cities4 + cities3 + cities2 + cities1, "layout":layout})
