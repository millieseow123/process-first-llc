import dash_cytoscape as cyto
from dash import html, dcc
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
from constants.data import INITIAL_NODES_DATA, INITIAL_EDGES_DATA

def ProcessFlow():
    return html.Div(
        [
            # Node Table
            html.H2("Process Equipment List"),
            dag.AgGrid(
                id="node-table",
                rowData=INITIAL_NODES_DATA,
                columnDefs=[
                    {"headerName": "Name", "field": "Name", "editable": True},
                    {
                        "headerName": "Type",
                        "field": "Type",
                        "editable": True,
                        "sortable": True, 
                        "cellEditor": "agSelectCellEditor",
                        "cellEditorParams": {"values": ["type1", "type2", "type3"]},
                    },
                ],
                defaultColDef={"flex": 1}, 
                style={"height": "400px", "width": "100%"},
                className="ag-theme-alpine",
                dashGridOptions={
                    "rowSelection": "multiple"
                },
            ),
            dbc.Button("Add Equipment", id="add-node-btn", color="primary", style={"margin": "10px 5px 10px 0"}),
            dbc.Button("Delete Selected Equipment", id="delete-node-btn", color="danger", style={"margin": "10px 0"}),

            # Edge Table
            html.H2("System Connections"),
            dag.AgGrid(
                id="edge-table",
                rowData=INITIAL_EDGES_DATA,
                columnDefs=[
                    {
                        "headerName": "Upstream Node",
                        "field": "Upstream Node",
                        "editable": True,
                        "cellEditor": "agSelectCellEditor",
                        "cellEditorParams": {"values": [node["Name"] for node in INITIAL_NODES_DATA]},
                    },
                    {
                        "headerName": "Downstream Node",
                        "field": "Downstream Node",
                        "editable": True,
                        "cellEditor": "agSelectCellEditor",
                        "cellEditorParams": {"values": [node["Name"] for node in INITIAL_NODES_DATA]},
                    },
                ],
                defaultColDef={"flex": 1}, 
                style={"height": "400px", "width": "100%"},
                className="ag-theme-alpine",
                dashGridOptions={
                    "rowSelection": "multiple" 
                },
            ),
            dbc.Button("Add Connection", id="add-edge-btn", color="primary", style={"margin": "10px 5px 10px 0"}),
            dbc.Button("Delete Selected Connection", id="delete-edge-btn", color="danger", style={"margin": "10px 0"}, disabled=True),

            # Store components for shared data
            dcc.Store(id="node-store", data=INITIAL_NODES_DATA),
            dcc.Store(id="edge-store", data=INITIAL_EDGES_DATA),

            # Visualization Canvas
            html.H3("Canvas"),
            cyto.Cytoscape(
                id="process-flow-canvas",
                style={"width": "100%", "height": "500px", "border": "2px solid #007BFF",  "backgroundColor": "#f9f9f9", "marginBottom": "10px"},
                layout={"name": "breadthfirst"},
                elements=[],
                userZoomingEnabled=True,
                zoomingEnabled=True,       
                userPanningEnabled=True,  
            ),
        ]
    )
