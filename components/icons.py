import dash_mantine_components as dmc
from dash_iconify import DashIconify

toggle_icon = dmc.ActionIcon(
    DashIconify(icon="clarity:settings-line"),
    color="blue",
    variant='subtle',
    id="toggle-icon",
    style={"cursor": "pointer"},
)
