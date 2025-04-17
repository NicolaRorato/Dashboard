import dash_mantine_components as dmc
from dash import html

x_axis_dropdown = html.Div([
    dmc.Select(
        label='x-axis',
        data=[],
        value=None,
        radius='lg',
        placeholder="Select x-axis column",
        id='x-axis-dropdown',
    )
], style={'margin': '20px'})

y_axis_dropdown = html.Div([
    dmc.MultiSelect(
        label='y-axis (left)',
        data=[],
        value=[],
        radius='lg',
        clearable=True,
        placeholder="Select line-type columns",
        id='line-chart-dropdown',
        style={'marginBottom': '5px'}
    ),
    dmc.MultiSelect(
        data=[],
        value=[],
        radius='lg',
        clearable=True,
        placeholder="Select area-type columns",
        id='area-chart-dropdown',
        style={'marginBottom': '5px'}
    ),
    dmc.MultiSelect(
        data=[],
        value=[],
        radius='lg',
        clearable=True,
        placeholder="Select scatter-type columns",
        id='scatter-chart-dropdown',
        style={'marginBottom': '5px'}
    ),
], style={'margin': '20px'})

y_axis_2_dropdown = html.Div([
    dmc.MultiSelect(
        label='y-axis (right)',
        data=[],
        value=[],
        radius='lg',
        clearable=True,
        placeholder="Move to secondary y-axis",
        id='secondary-yaxis-dropdown',
    ),
    dmc.Select(
        label='color',
        data=[],
        value=None,
        radius='lg',
        placeholder="Select color column",
        id='color-dropdown',
    )
], style={'margin': '20px'})