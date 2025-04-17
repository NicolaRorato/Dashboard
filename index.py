from app import app
from components.layout import main_layout, blocks
# from callbacks import chart_callbacks, toggle_callbacks, dropdown_callbacks
from callbacks.chart_callbacks import register_chart_callbacks
from callbacks.toggle_callbacks import register_toggle_callbacks
from callbacks.dropdown_callbacks import register_dropdown_callbacks

app.layout = main_layout

# Register callbacks
# chart_callbacks.register_callbacks(app)
# toggle_callbacks.register_callbacks(app)
# dropdown_callbacks.register_callbacks(app)
for i in range(blocks):
    register_chart_callbacks(app, f"block-{i + 1}")
    register_toggle_callbacks(app, f"block-{i + 1}")
    register_dropdown_callbacks(app, f"block-{i + 1}")

if __name__ == "__main__":
    app.run(debug=True)