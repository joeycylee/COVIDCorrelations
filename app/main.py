# myapp.py

from random import random

# Bokeh basics 
from bokeh.io import curdoc
from bokeh.models.widgets import Tabs

from bokeh.layouts import column, row
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource,DataRange1d

import pandas as pd
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
#server = 'tcp:myserver.database.windows.net' 

drivers = [item for item in pyodbc.drivers()]
print(f"{drivers=}\n\n")
driver = drivers[-1]
print(f"{driver=}\n\n")

server = '172.17.0.2,1433'
database = 'COVIDCorrelations' 
username = 'SA' 
password = 'StrongPassword1' 
constr = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'


conn= pyodbc.connect(constr)
cursor = conn.cursor()

q = """
SET NOCOUNT ON;
SELECT * FROM [COVIDCorrelations].[dbo].[OntarioCOVIDData];
"""

df = pd.read_sql_query(q,conn)

df['date'] = pd.to_datetime(df.date)

df = df.set_index(['date'])

# create a plot and style its properties
p = figure(x_axis_type="datetime", plot_width=800, tools="", toolbar_location=None)
#p.border_fill_color = 'white'
#p.background_fill_color = 'white'
#p.outline_line_color = 'green'
#p.grid.grid_line_color = None

source = ColumnDataSource(data = df)
p.line(x = 'date', y='TotalCases', source = source)
p.x_range = DataRange1d(range_padding=0.0)

plot = figure(x_axis_type="datetime", plot_width=800, tools="", toolbar_location=None)
plot.title.text = "WEATHER"
plot.line(x=[1,3,4], y=[2,3,4])

    
curdoc().add_root(row(p))
curdoc().title = "COVID-19"
