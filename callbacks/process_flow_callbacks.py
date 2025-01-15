from dash import ctx, Input, Output, State

def register_process_flow_callbacks(app):
    
    # Callback to add or delete a new node
    @app.callback(
        Output("node-table", "rowData"),
        Input("add-node-btn", "n_clicks"),
        Input("delete-node-btn", "n_clicks"),
        State("node-table", "rowData"),
        State("node-table", "selectedRows"),
    )
    def modify_node_table(add_clicks, delete_clicks, nodes, selected_rows):
        if ctx.triggered_id == "add-node-btn" and add_clicks:
            # Add a new node
            nodes.append({"Name": f"Node {len(nodes) + 1}", "Type": "type1"})
        elif ctx.triggered_id == "delete-node-btn" and delete_clicks and selected_rows:
            # Delete selected nodes
            selected_names = {row["Name"] for row in selected_rows}
            nodes = [node for node in nodes if node["Name"] not in selected_names]
        return nodes
    
    # Callback to add or delete a new edge
    @app.callback(
        Output("edge-table", "rowData"),
        Input("add-edge-btn", "n_clicks"),
        Input("delete-edge-btn", "n_clicks"),
        State("edge-table", "rowData"),
        State("node-table", "rowData"),
        State("edge-table", "selectedRows"),
    )
    def modify_edge_table(add_clicks, delete_clicks, edges, nodes, selected_rows):
        if ctx.triggered_id == "add-edge-btn" and add_clicks and nodes:
            # Add a new edge with the first node as both Upstream and Downstream
            first_node = nodes[0]["Name"]
            edges.append({"Upstream Node": first_node, "Downstream Node": first_node})
        elif ctx.triggered_id == "delete-edge-btn" and delete_clicks and selected_rows:
            # Delete selected edges
            edges = [edge for edge in edges if edge not in selected_rows]
        return edges
    
    # Callback to disable the delete button when no rows are selected
    @app.callback(
        [Output("delete-node-btn", "disabled"), Output("delete-edge-btn", "disabled")],
        [Input("node-table", "selectedRows"), Input("edge-table", "selectedRows")],
    )
    def toggle_delete_buttons(node_selected_rows, edge_selected_rows):
        # Disable the button if no rows are selected
        disable_node_btn = len(node_selected_rows) == 0 if node_selected_rows else True
        disable_edge_btn = len(edge_selected_rows) == 0 if edge_selected_rows else True
        return disable_node_btn, disable_edge_btn
    
    # Callback to update the stores when tables are edited
    @app.callback(
        Output("node-store", "data"),
        Output("edge-store", "data"),
        Input("node-table", "rowData"),
        Input("edge-table", "rowData"),
    )
    def update_stores(nodes, edges):
        return nodes, edges
    
    # Callback to update the graph based on Node and Edge tables
    @app.callback(
        Output("process-flow-canvas", "elements"),
        Input("node-table", "rowData"),
        Input("edge-table", "rowData"),
    )
    def update_canvas(nodes, edges):
        elements = [{"data": {"id": node["Name"], "label": node["Name"]}} for node in nodes]
        elements += [{"data": {"source": edge["Upstream Node"], "target": edge["Downstream Node"]}} for edge in edges]
        return elements
