from pathlib import Path
import pandas as pd

import plotly.express as px
from shiny import reactive
from shiny.express import input, ui, render
from shinywidgets import render_plotly

ui.page_opts(title='Sales Dashboard - Video 1 of 5', fillable=True)
# various options on how the page is displayed on the browser
ui.input_numeric("n", "Number of Items", 5, min=0, max=20)

@reactive.calc 
# perform calculation based on reactive dependencies. 
# separates calculations from rendering, so that calculations are not repeated when rendering multiple outputs.
def dat():
    # here, specifically, we are reading a csv file which may be updated in the future 
    # and may need time consuming pre-processing that must not be repeated for each rendering process
    infile = Path(__file__).parent / 'data' / 'sales.csv'
    return pd.read_csv(infile)

with ui.layout_columns():
# column-based grid layouts
    @render_plotly
    def plot1():
        df = dat()
        top_sales = df.groupby('product')['quantity_ordered'].sum().nlargest(input.n()).reset_index()
        return px.bar(top_sales, x='product', y='quantity_ordered', color='product')
    