import dash
from dash import dcc, html, _dash_renderer
from dash.dependencies import Input, Output, State
import dash_mantine_components as dmc
from dash_iconify import DashIconify
import plotly.express as px
import pandas as pd

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dmc.styles.ALL])
dmc.add_figure_templates(default="mantine_light")

# TO BE UPDATED WITH REAL DATA - Load dataframes
from create_dataframe import create_dataframe

df = px.data.gapminder()
df2 = create_dataframe()

# Layout for file upload
file_upload = dcc.Upload(
    id='upload-data',
    children=html.Button('Upload DataFrame'),
    multiple=False
)

# Button to toggle visibility
toggle_icon = dmc.ActionIcon(
    DashIconify(icon="clarity:settings-line"),
    color="blue",
    variant='subtle',
    id="toggle-icon",
    style={"cursor": "pointer"},
)

# Layout
x_axis_dropdown = html.Div([
    dmc.Select(
        label='x-axis',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=None,  # This will be set dynamically once df is available
        radius='lg',
        placeholder="Select x-axis column",
        id='x-axis-dropdown',
    ),
],
    style={
        'margin': '20px',
    }
)

y_axis_dropdown = html.Div([
    dmc.MultiSelect(
        label='y-axis (left)',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select line-type columns",
        id='line-chart-dropdown',
        style={
            'marginBottom': '5px'
        }
    ),
    dmc.MultiSelect(
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select area-type columns",
        id='area-chart-dropdown',
        style={
            'marginBottom': '5px'
        }
    ),
    dmc.MultiSelect(
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Select scatter-type columns",
        id='scatter-chart-dropdown',
        style={
            'marginBottom': '5px'
        }
    ),
],
    style={
        'margin': '20px',
    }
)

y_axis_2_dropdown = html.Div([
    dmc.MultiSelect(
        label='y-axis (right)',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=[],  # Default: No columns selected
        radius='lg',
        clearable=True,
        placeholder="Move to secondary y-axis",
        id='secondary-yaxis-dropdown',
    ),
    dmc.Select(
        label='color',
        data=[],  # This will be populated dynamically based on the DataFrame
        value=None,  # This will be set dynamically once df is available
        radius='lg',
        placeholder="Select color column",
        id='color-dropdown',
    ),
],
    style={
        'margin': '20px',
    }
)

app.layout = html.Div([
    dmc.MantineProvider(
        theme={"colorScheme": "light"},
        children=html.Div([
            dcc.Store(id='df-store', data=df.to_dict('records')),
            dcc.Store(id="store-dropdown-visible", data={"visible": True}),
            # Button to toggle visibility
            toggle_icon,
            dmc.Grid(id="grid-container", children=[
                dmc.GridCol(x_axis_dropdown, span=4),  # span=4 to split window in 3 cols
                dmc.GridCol(y_axis_dropdown, span=4),
                dmc.GridCol(y_axis_2_dropdown, span=4),
            ],
                gutter='md',
                styles={
                    'marginBottom': '20px',
                }
            ),
            dcc.Graph(
                id='chart',
                style={
                    'display': 'none',  # This will hide the graph initially
                }
            ),
        ])
    ),
])


@app.callback(
    Output("grid-container", "style"),  # The div that wraps the grid of dropdowns
    Input("toggle-icon", "n_clicks"),
    State("store-dropdown-visible", "data"),
)
def toggle_dropdowns_visibility(n_clicks, store_data):
    if n_clicks is None:
        return {"display": "block"}  # Initially visible if no clicks yet

    # Toggle the visibility based on n_clicks
    if store_data["visible"]:
        return {"display": "none"}  # Hide the grid
    else:
        return {"display": "block"}  # Show the grid


@app.callback(
    Output("store-dropdown-visible", "data"),
    Input("toggle-icon", "n_clicks"),
    State("store-dropdown-visible", "data"),
)
def update_visibility_state(n_clicks, store_data):
    if n_clicks is None:
        return store_data  # Do nothing if no clicks yet

    # Toggle the visibility state
    store_data["visible"] = not store_data["visible"]
    return store_data

# Function to determine if the color column is numeric or categorical
def get_color_scale(df, color_col):
    if pd.api.types.is_numeric_dtype(df[color_col]):
        # If the color column is numeric, use a continuous colorscale
        color_scale = 'Viridis'  # You can choose any continuous color scale
        color_values = df[color_col]
    else:
        # If the color column is categorical, use a discrete colorscale
        unique_categories = df[color_col].unique()
        color_scale = 'Set1'  # Choose a discrete color scale
        color_map = {cat: i for i, cat in enumerate(unique_categories)}
        color_values = df[color_col].map(color_map)
    return color_values, color_scale

# Callback to update the chart
@app.callback(
    Output('chart', 'figure'),
    Output('chart', 'style'),
    [
        Input('x-axis-dropdown', 'value'),
        Input('line-chart-dropdown', 'value'),
        Input('area-chart-dropdown', 'value'),
        Input('scatter-chart-dropdown', 'value'),
        Input('secondary-yaxis-dropdown', 'value'),
        Input('color-dropdown', 'value'),
    ]
)
def update_chart(x_axis, line_columns, area_columns, scatter_columns, secondary_yaxis_columns, color):
    # If no columns are selected, return an empty figure
    if not x_axis:
        return {}, {"display": "none"}

    # Create an empty figure
    fig = px.line()

    if color is not None:
        color_values, color_scale = get_color_scale(df, color)
        color_params = {
            'marker': dict(color=color_values),
            'text': df[color],
        }
    else:
        color_params = {}
    # Plot line charts
    if line_columns:
        for col in line_columns:
            yaxis = 'y2' if col in secondary_yaxis_columns else 'y'
            name = f'{col} (right)' if col in secondary_yaxis_columns else f'Line - {col}'
            fig.add_scatter(x=df[x_axis], y=df[col], mode='lines+markers', name=name, yaxis=yaxis,
                            **color_params,
                            )

    # Plot area charts
    if area_columns:
        for col in area_columns:
            yaxis = 'y2' if col in secondary_yaxis_columns else 'y'
            name = f'{col} (right)' if col in secondary_yaxis_columns else f'Line - {col}'
            fig.add_scatter(x=df[x_axis], y=df[col], fill='tozeroy', name=name, yaxis=yaxis,
                            **color_params,
                            )

    # Plot scatter charts
    if scatter_columns:
        for col in scatter_columns:
            yaxis = 'y2' if col in secondary_yaxis_columns else 'y'
            name = f'{col} (right)' if col in secondary_yaxis_columns else f'Line - {col}'
            # Get the color values and scale
            fig.add_scatter(x=df[x_axis], y=df[col], mode='markers', name=name, yaxis=yaxis,
                            **color_params,
                            )


    # Customize the layout with secondary Y-axis
    fig.update_layout(
        title=f'Chart of {x_axis} vs ({", ".join(list(set(line_columns+area_columns+scatter_columns)))})',
        xaxis_title=x_axis,
        yaxis_title='y-axis (left)',
        # template='plotly_dark',
        xaxis=dict(
            ticks='outside',  # Optional: Move the ticks outside the plot
        ),
        yaxis=dict(
            ticks='outside',  # Optional: Move the ticks outside the plot
        ),
        yaxis2=dict(
            overlaying='y',
            side='right',
            title='y-axis (right)',
            ticks='outside',  # Optional: Move the ticks outside the plot
        ),
        margin=dict(
            l=100,  # Left margin (distance from left edge to y-axis)
            r=100,  # Right margin (distance from right edge to y-axis)
            t=100,  # Top margin (distance from top edge to title)
            b=100  # Bottom margin (distance from bottom edge to x-axis)
        ),
        height=500,
        hoverlabel=dict(
            namelength=30,  # Limit trace name length in hover to 15 characters
        ),
    )

    return fig, {'display': 'block'}


def generate_dropdown_options(columns):
    return [{'label': col, 'value': col} for col in columns]


# Callback to populate dropdown options based on DataFrame in dcc.Store
@app.callback(
    [Output('x-axis-dropdown', 'data'),
     Output('line-chart-dropdown', 'data'),
     Output('area-chart-dropdown', 'data'),
     Output('scatter-chart-dropdown', 'data'),
     Output('secondary-yaxis-dropdown', 'data'),
     Output('color-dropdown', 'data')],
    Input('df-store', 'data')  # When the dataframe is updated
)
def populate_dropdowns(df_data):
    if not df_data:
        return dash.no_update  # If no data available, don't update dropdowns

    # Convert stored data back to DataFrame
    df = pd.DataFrame(df_data)
    df_columns = df.columns

    # Generate options for each dropdown
    options = [{'label': col, 'value': col} for col in df_columns]

    # Return the same options for each dropdown (can customize per dropdown)
    return options, options, options, options, options, options


if __name__ == '__main__':
    app.run(debug=True)
