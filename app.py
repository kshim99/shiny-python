from pathlib import Path
import pandas as pd
import calendar

import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

ui.page_opts(title='Sales Dashboard - Video 2 of 5', fillable=False)
# various options on how the page is displayed on the browser
ui.input_numeric("n", "Number of Items", 5, min=0, max=20)
# inputs are defined in a way that when inputs are updated, only the plots that are dependent on the inputs are updated
# much more computationally efficient this way, especially when dealing with large datasets and complex visualizations
ui.input_checkbox("barcolor", "Make Bars Red?", False)

@reactive.calc
def color():
    return "red" if input.barcolor() else "blue"

@reactive.calc 
# perform calculation based on reactive dependencies. 
# separates calculations from rendering, so that calculations are not repeated when rendering multiple outputs.
def dat():
    # here, specifically, we are reading a csv file which may be updated in the future 
    # and may need time consuming pre-processing that must not be repeated for each rendering process
    infile = Path(__file__).parent / 'data' / 'sales.csv'
    df = pd.read_csv(infile)
    df['order_date'] = pd.to_datetime(df['order_date'])
    df['month'] = df['order_date'].dt.month_name()
    return df


@render_plotly
def plot1():
    df = dat()
    top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
    fig = px.bar(top_sales, x='product', y='quantity_ordered', color='product')
    fig.update_traces(marker_color=color())
    return fig

ui.input_selectize("city","Select a City", 
                   choices = [
                       'Dallas (TX)', 
                       'Boston (MA)', 
                       'Los Angeles (CA)', 
                       'San Francisco (CA)', 
                       'Seattle (WA)', 
                       'Atlanta (GA)', 
                       'New York City (NY)', 
                       'Portland (OR)', 
                       'Austin (TX)', 
                       'Portland (ME)'
                       ], 
                   multiple=False,
                   selected = ['Dallas (TX)'])

@render_plotly
def sales_over_time():
    df = dat() # if you want to make additional changes to dataframe specific to this plot, make a copy of data first to avoid affecting other plots
    sales = df.groupby(['city', 'month'])['quantity_ordered'].sum().reset_index()
    sales_by_city = sales[sales['city'] == input.city()]
    month_orders = calendar.month_name[1:13]
    fig = px.bar(sales_by_city, title = "Sales over time in " + input.city(), x='month', y='quantity_ordered', category_orders={'month':month_orders})
    fig.update_traces(marker_color=color())
    return fig


with ui.card():
    ui.card_header("Sample data")
    @render.data_frame
    def sample_sales_data():
        return dat().head(50)