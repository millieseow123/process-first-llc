from dash import html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc

# Reusable Paginated Table Component
def PaginatedTable(data, rows_per_page_options=[10, 15, 20]):

    # Layout
    return html.Div(
        [
            html.H2("Process Equipment Variables and Measurements", style={"marginBottom": "20px"}),
            # Table
            dag.AgGrid(
                id="table",
                rowData=data,
                columnDefs=[
                    {"headerName": "Equipment", "field": "Equipment"},
                    {"headerName": "Variable", "field": "Variable"},
                    {"headerName": "Value", "field": "Value"},
                    {"headerName": "Unit", "field": "Unit"},
                ],
                defaultColDef={"flex": 1}, 
                className="ag-theme-alpine",
                style={"height": "400px", "width": "100%"}
            ),
            html.Div(
                [
                # Pagination Controls
                dbc.Pagination(
                    id="pagination",
                    max_value=1,
                    active_page=1,
                    fully_expanded=False,
                    first_last=True,
                ),
                # Dropdown to select rows per page
                html.Div([html.Span("Rows per page:", style={"marginRight": "10px"}),
                dcc.Dropdown(
                    id="rows-per-page-dropdown",
                    options=[{"label": str(option), "value": option} for option in rows_per_page_options],
                    value=rows_per_page_options[0],  # Default to first option
                    clearable=False,
                    style={"width": "200px"},
                ),],
                style={"display": "flex", "alignItems": "center"},
                ),
            ],
            style={ "display": "flex",
                "justifyContent": "space-between",
                "gap": "20px",
                "marginTop": "10px",
                "marginBottom": "10px",},
            ),
            dcc.Store(id="rows_per_page_store", data=rows_per_page_options[0]),
        ]
    )
