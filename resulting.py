import pandas as pd
from bokeh.layouts import column, row, gridplot, layout
from bokeh.plotting import figure, curdoc, output_file
from bokeh.models import Div, ColumnDataSource, HoverTool, SingleIntervalTicker, LinearAxis, DatePicker
from bokeh.io import show
from bokeh.palettes import GnBu3,Category20c
from bokeh.transform import cumsum

def get_data(date_select,data_source,feature):
    data_got = data_source[data_source["date"] == date_select].groupby(by = ["race"])[feature].agg("sum").reset_index(name='value')
    data_got['angle'] = data_got['value'] / data_got['value'].sum() * 2*3.14
    data_got['color'] = Category20c[len(data_got.values)]
    data_got['percentage'] = (data_got['value'] / data_got['value'].sum())*100
    data_got['num'] = data_got['value']
    data_got['date'] = date_select
    return data_got

def get_data2():
    new_data = {}
    date = pd.to_datetime(date_picker.value)
    new_data["x"] = [date]
    new_data["y"] = [data_total[data_total["date"] == date]["confirmed_cases"]]
    return new_data

# read data
data_total = pd.read_csv("https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-positive-test-rate.csv")
data_race = pd.read_csv("https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-race-ethnicity.csv")
last_date = data_race.iloc[1,0]

# title
title1 = Div(text="""This is a visualization of covid-19 data. These data can shows: <br>1. number of nnew covid-19 cases in CA on a particular day in August.
<br>2. The %percent cases by race compared to their representation in general population in a particular day. <br>3. The %percent death by race compared to their representation in general population in a particular day.
<br>All data was collected from 'Los Angeles Times Data and Graphics Department', url=<a href="https://github.com/datadesk/california-coronavirus-data">https://github.com/datadesk/california-coronavirus-data</a>"
<br><b>Last updated on:{}</b>""".format(last_date),
width=1000, height=120)

# data picker
date_picker = DatePicker(title='Select date', value="2020-08-15", min_date="2020-08-01", max_date="2020-08-31")
date_picker2 = DatePicker(title='Select date', value="2020-08-16", min_date="2020-05-14", max_date=last_date)
date1 = pd.to_datetime(date_picker.value)
date2 = pd.to_datetime(date_picker2.value)
data_total['date'] = pd.to_datetime(data_total['date'])
data_race['date'] = pd.to_datetime(data_race['date'])

# p1 aug plot
Aug = data_total[(data_total["date"]>="2020-08-01") & (data_total["date"]<"2020-09-01")]
output_file("datetime.html")
data_got = get_data2()
hover1 = HoverTool(
	tooltips=[
		("date", "@x{%Y-%m-%d}"),
		("cases", "@y"),
	],
    formatters={
        '@x': 'datetime',}
)

plot1 = figure(x_axis_type="datetime",x_axis_label='date', y_axis_label='# covid-19 cases',plot_width=1000, plot_height=600,tools='crosshair,pan,box_zoom')
plot1.add_tools(hover1)
plot1.title.text = "New COVID-19 Cases in California on August"
plot1.title.align = "center"
plot1.title.text_font_size = "20px"
plot1.align = "center"
r = plot1.text(x=[date1], y=[data_total[data_total["date"] == date1]["confirmed_cases"]], text=[str(data_total[data_total["date"] == date1]["confirmed_cases"].values[0])],
 text_color=["black"], text_font_size="14px",text_baseline="middle", text_align="center")
plot1.line(Aug["date"],Aug["confirmed_cases"], color='navy', alpha=0.5,legend_label="confirmed_cases")

# p2 plot
data_got1 = get_data(date2,data_race,"confirmed_cases_total")
plot2 = figure(plot_height=350, title="%percent cases by race",tools="hover", tooltips="@race: @percentage", x_range=(-0.4, 0.8))
plot2.title.align = "center"
plot2.title.text_font_size = "20px"
p_case = plot2.wedge(x=0, y=1, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='race', source=data_got1)

# p3 plot
data_got2 = get_data(date2,data_race,"deaths_total")
plot3 = figure(plot_height=350, title="%percent death by race",tools="hover", tooltips="@race: @percentage", x_range=(-0.4, 0.8))
plot3.title.align = "center"
plot3.title.text_font_size = "20px"
p_death = plot3.wedge(x=0, y=1, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='race', source=data_got2)

data_got3 = get_data(date2,data_race,"population_percent")
plot4 = figure(plot_height=350, title="%percent population by race",tools="hover", tooltips="@race: @percentage", x_range=(-0.4, 0.8))
plot4.title.align = "center"
plot4.title.text_font_size = "20px"
p_num = plot4.wedge(x=0, y=1, radius=0.3,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='race', source=data_got3)

ds = r.data_source
def callback(attr, old, new):
    new_data = {}
    date = pd.to_datetime(date_picker.value)
    new_data["x"] = [date]
    new_data["y"] = [data_total[data_total["date"] == date]["confirmed_cases"]]
    new_data['text_color'] = ["black"]
    new_data['text'] = [str(data_total[data_total["date"] == date]["confirmed_cases"].values[0])]
    ds.data = new_data

data_case = p_case.data_source
data_death = p_death.data_source
data_num = p_num.data_source
def callback2(attr, old, new):
    date = pd.to_datetime(date_picker2.value)
    data_case.data = get_data(date,data_race,"confirmed_cases_total")
    data_death.data = get_data(date,data_race,"deaths_total")
    data_num.data = get_data(date,data_race,"population_percent")

plot2.axis.axis_label=None
plot2.axis.visible=False
plot2.grid.grid_line_color = None
plot3.axis.axis_label=None
plot3.axis.visible=False
plot3.grid.grid_line_color = None
plot4.axis.axis_label=None
plot4.axis.visible=False
plot4.grid.grid_line_color = None


date_picker.on_change("value", callback)
date_picker2.on_change("value", callback2)

title2 = Div(text="""Comparison of COVID-19 case/death to its population by race""",
width=1000, height=120)
title2.default_size = 50

curdoc().add_root(layout([[title1],[plot1, date_picker],[plot2,plot3],[plot4,date_picker2]]))