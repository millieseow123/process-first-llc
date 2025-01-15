from dash import Input, Output, State

def register_paginated_table_callbacks(app, data):
    @app.callback(
        Output("table", "rowData"),
        Output("pagination", "max_value"),
        Input("pagination", "active_page"),
        Input("rows-per-page-dropdown", "value"),
        State("rows_per_page_store", "data"),
    )
    def update_table(active_page, rows_per_page, stored_rows_per_page):
        if not rows_per_page:
            rows_per_page = stored_rows_per_page

        start_row = (active_page - 1) * rows_per_page
        end_row = start_row + rows_per_page
        total_pages = (len(data) // rows_per_page) + (1 if len(data) % rows_per_page > 0 else 0)

        paginated_data = data[start_row:end_row]

        return paginated_data, total_pages
