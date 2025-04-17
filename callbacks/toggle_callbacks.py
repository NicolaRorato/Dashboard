from dash import Input, Output, State


def register_callbacks(app):
    @app.callback(
        Output("grid-container", "style"),
        Input("toggle-icon", "n_clicks"),
        State("store-dropdown-visible", "data")
    )
    def toggle_dropdowns_visibility(n_clicks, store_data):
        if n_clicks is None:
            return {"display": "block"}
        return {"display": "none" if store_data["visible"] else "block"}

    @app.callback(
        Output("store-dropdown-visible", "data"),
        Input("toggle-icon", "n_clicks"),
        State("store-dropdown-visible", "data")
    )
    def update_visibility_state(n_clicks, store_data):
        if n_clicks is None:
            return store_data
        store_data["visible"] = not store_data["visible"]
        return store_data


def register_toggle_callbacks(app, block_id):
    @app.callback(
        Output(f'grid-container-{block_id}', 'style'),
        Input(f'toggle-icon-{block_id}', 'n_clicks'),
        State(f'store-dropdown-visible-{block_id}', 'data')
    )
    def toggle_dropdowns_visibility(n_clicks, store_data):
        if n_clicks is None:
            return {"display": "block"}
        return {"display": "none" if store_data["visible"] else "block"}

    @app.callback(
        Output(f'store-dropdown-visible-{block_id}', 'data'),
        Input(f'toggle-icon-{block_id}', 'n_clicks'),
        State(f'store-dropdown-visible-{block_id}', 'data')
    )
    def update_visibility_state(n_clicks, store_data):
        if n_clicks is None:
            return store_data
        store_data["visible"] = not store_data["visible"]
        return store_data
