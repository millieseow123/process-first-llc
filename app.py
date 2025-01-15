from dash import Dash, dash, html, dcc
import dash_bootstrap_components as dbc
from components.paginated_table import PaginatedTable
from components.process_flow import ProcessFlow
from components.report_generator import ReportGeneration
from callbacks.paginated_table_callbacks import register_paginated_table_callbacks
from callbacks.process_flow_callbacks import register_process_flow_callbacks
from callbacks.report_generation_callbacks import register_report_generation_callbacks
from constants.data import PAGINATED_TABLE_DATA

# Initialize the Dash app
app = Dash(__name__, title="Process First LLC", external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

# App layout
app.layout = html.Div(
    [
        html.H1("Process First LLC - Process Visualization Tool",
                style={"padding": "10px 0"}
        ),
        dcc.Tabs(
            id="tabs",
            value="tab-1",
            children=[
                dcc.Tab(label="Paginated Table", value="tab-1"),
                dcc.Tab(label="Process Flow Visualization", value="tab-2"),
                dcc.Tab(label="Report Generation", value="tab-3"),
            ],
        ),
        html.Div(id="tab-content",
        style={"padding": "10px 20px 0"}
        ),
    ]
)

# Callback to render content based on selected tab
@app.callback(
    dash.Output("tab-content", "children"),
    dash.Input("tabs", "value"),
)
def render_tab_content(tab_name):
    if tab_name == "tab-1":
        return PaginatedTable(PAGINATED_TABLE_DATA)
    elif tab_name == "tab-2":
        return ProcessFlow()
    elif tab_name == "tab-3":
        return ReportGeneration()
    
# Register callbacks
register_paginated_table_callbacks(app, PAGINATED_TABLE_DATA)
register_process_flow_callbacks(app)
register_report_generation_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
