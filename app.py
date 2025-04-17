from dash import Dash
import dash_mantine_components as dmc
from callbacks import chart_callbacks  # this is important even if unused

app = Dash(__name__, external_stylesheets=[dmc.styles.ALL])
dmc.add_figure_templates(default="mantine_light")

server = app.server
