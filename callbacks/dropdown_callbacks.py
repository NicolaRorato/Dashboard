from dash import Input, Output, no_update
import pandas as pd


# def register_callbacks(app):
#     @app.callback(
#         Output('x-axis-dropdown', 'data'),
#         Output('line-chart-dropdown', 'data'),
#         Output('area-chart-dropdown', 'data'),
#         Output('scatter-chart-dropdown', 'data'),
#         Output('secondary-yaxis-dropdown', 'data'),
#         Output('color-dropdown', 'data'),
#         Input('df-store', 'data')
#     )
#     def populate_dropdowns(df_data):
#         if not df_data:
#             return [no_update] * 6
#
#         df = pd.DataFrame(df_data)
#         options = [{'label': col, 'value': col} for col in df.columns]
#         return options, options, options, options, options, options

def register_dropdown_callbacks(app, block_id):
    # Scoped component IDs
    store_id = f'df-store-{block_id}'
    x_dropdown = f'x-axis-dropdown-{block_id}'
    line_dropdown = f'line-chart-dropdown-{block_id}'
    area_dropdown = f'area-chart-dropdown-{block_id}'
    scatter_dropdown = f'scatter-chart-dropdown-{block_id}'
    y2_dropdown = f'secondary-y-axis-dropdown-{block_id}'
    color_dropdown = f'color-dropdown-{block_id}'

    @app.callback(
        Output(x_dropdown, 'data'),
        Output(line_dropdown, 'data'),
        Output(area_dropdown, 'data'),
        Output(scatter_dropdown, 'data'),
        Output(y2_dropdown, 'data'),
        Output(color_dropdown, 'data'),
        Input(store_id, 'data')
    )
    def populate_dropdowns(df_data):
        if not df_data:
            return [no_update] * 6

        df = pd.DataFrame(df_data)
        options = [{'label': col, 'value': col} for col in df.columns]
        return [options] * 6
