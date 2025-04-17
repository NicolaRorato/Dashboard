from dash import html, dcc
import dash_mantine_components as dmc
# from components.dropdowns import x_axis_dropdown, y_axis_dropdown, y_axis_2_dropdown
# from components.chart import chart
from components.chart_block import create_chart_block
from components.icons import toggle_icon

# Add data here
from data import create_dataframe, df_store_data
dfs = [
    df_store_data,
    create_dataframe().to_dict(),
    df_store_data,
    df_store_data,
    create_dataframe().to_dict(),
    df_store_data,

]

# main_layout = html.Div([
#     dmc.MantineProvider(
#         theme={"colorScheme": "light"},
#         children=html.Div([
#             dcc.Store(id='df-store', data=df_store_data),
#             dcc.Store(id="store-dropdown-visible", data={"visible": True}),
#             toggle_icon,
#             dmc.Grid(id="grid-container", children=[
#                 dmc.GridCol(x_axis_dropdown, span=4),
#                 dmc.GridCol(y_axis_dropdown, span=4),
#                 dmc.GridCol(y_axis_2_dropdown, span=4),
#             ], gutter='md'),
#             chart,
#         ])
#     )
# ])

blocks = len(dfs)
main_layout = html.Div([
    dmc.MantineProvider(
        theme={"colorScheme": "light"},
        children=html.Div([
            create_chart_block(block_id=f"block-{i + 1}", df_store_data=dfs[i])
            for i in range(blocks)
        ])
    )
])