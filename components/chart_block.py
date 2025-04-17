from dash import dcc, html
import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_chart_block(block_id, df_store_data):
    # Store the df for this block
    block_data_store = dcc.Store(id=f'df-store-{block_id}', data=df_store_data)
    block_dropdown_visibility = dcc.Store(id=f'store-dropdown-visible-{block_id}', data={"visible": True})
    block_dropdown_visibility_button = dmc.ActionIcon(
        DashIconify(icon="clarity:settings-line"),
        color="blue",
        variant='subtle',
        id=f'toggle-icon-{block_id}',
        style={"cursor": "pointer"},
    )

    # Dropdowns
    x_axis_dropdown = html.Div([
        dmc.Select(
            id=f'x-axis-dropdown-{block_id}',
            label="x-axis",
            data=[],
            value=None,  # This will be set dynamically once df is available
            radius='lg',
            placeholder="Select x-axis column",
        ),
    ],
        style={
            'margin': '20px',
        }
    )

    # y_axis_dropdown = html.Div([
    line_dropdown = dmc.MultiSelect(
        id=f'line-chart-dropdown-{block_id}',
        label='y-axis (left)',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select line-type columns",
        style={
            'marginBottom': '5px'
        }
    )
    area_dropdown = dmc.MultiSelect(
        id=f'area-chart-dropdown-{block_id}',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select area-type columns",
        style={
            'marginBottom': '5px'
        }
    )
    scatter_dropdown = dmc.MultiSelect(
        id=f'scatter-chart-dropdown-{block_id}',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select scatter-type columns",
        style={
            'marginBottom': '5px'
        }
    )

    secondary_y_dropdown = dmc.MultiSelect(
        id=f'secondary-y-axis-dropdown-{block_id}',
        label='y-axis (right)',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Move to secondary y-axis",
    )
    color_dropdown = dmc.Select(
        id=f'color-dropdown-{block_id}',
        label='color',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=None,  # This will be set dynamically once df is available
        radius='lg',
        placeholder="Select color column",
    )

    block_dropdowns = dmc.Grid(
        id=f'grid-container-{block_id}',
        children=[
            dmc.GridCol(x_axis_dropdown, span=4),
            dmc.GridCol([line_dropdown, area_dropdown, scatter_dropdown], span=4),
            dmc.GridCol([secondary_y_dropdown, color_dropdown], span=4),
        ],
        gutter='md',
        styles={
            'marginBottom': '20px',
        }
    )

    block_chart = dcc.Graph(
        id=f'chart-{block_id}',
        style={
            'display': 'none'  # This will hide the graph initially
        }
    )

    return html.Div([
        block_data_store,
        block_dropdown_visibility,
        block_dropdown_visibility_button,
        block_dropdowns,
        block_chart,
    ], style={"marginBottom": "10px"})
