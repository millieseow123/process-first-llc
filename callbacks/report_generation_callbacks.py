import os
import json
from dash import Input, Output, dcc, ctx
import dash
from dotenv import load_dotenv
import openai
from components.report_generator import generate_report


# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def register_report_generation_callbacks(app):
    
    # Function to get text summary from OpenAI
    def get_llm_output(json_data):
        # prompt = f"""
        # You are a data analyst. Based on the following JSON data, generate a report that includes the following:
        # 1. A textual summary of the key insights.
        # 2. A table summarizing the most impactful variables and their values.
        # 3. Instructions for creating a plot that visualizes the top impacts on the Key Performance Indicator (KPI).

        # Return your response as a structured JSON object with the following format:

        # {{
        #     "text_summary": "Your text summary here...",
        #     "table_data": [
        #         {{"Equipment": "HEX-100", "Variable": "Cold Fluid Temperature", "Initial Value": 300, "Tuned Value": 330, "Impact on KPI": 2.5}},
        #         {{"Equipment": "Fuel Tank", "Variable": "Temperature", "Initial Value": 350, "Tuned Value": 365, "Impact on KPI": 3.0}}
        #     ],
        #     "plot_data": {{
        #         "Cold Fluid Temperature": 2.5,
        #         "Temperature (Fuel Tank)": 3.0,
        #         "Temperature (Air Intake)": 1.8
        #     }}
        # }}

        # JSON data:
        # {json_data}
        # """
        
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[
        #         {"role": "system", "content": "You are a data analyst."},
        #         {"role": "user", "content": prompt},
        #     ],
        #     max_tokens=1500,
        # )
        # output = response["choices"][0]["message"]["content"].strip()

        #-----> Hardcoded the LLM response cus i was unable to get a response from openai. I think need to pay <-----#
        output = {
            "text_summary": """
            The process simulation results indicate that temperature and pressure variables have the most significant impact on the Key Performance Indicator (KPI). 
            Adjustments to the cold fluid temperature of HEX-100 and the temperature of the Fuel Tank show the highest potential for improvement.
            Further tuning of the Air Intake's temperature can optimize the overall system performance.
            """,
            "table_data": [
                {"Equipment": "HEX-100", "Variable": "Cold Fluid Temperature", "Initial Value": 300, "Tuned Value": 330, "Impact on KPI": 2.5},
                {"Equipment": "Fuel Tank", "Variable": "Temperature", "Initial Value": 350, "Tuned Value": 365, "Impact on KPI": 3.0},
                {"Equipment": "Air Intake", "Variable": "Temperature", "Initial Value": 295, "Tuned Value": 305, "Impact on KPI": 1.8},
            ],
            "plot_data": {
                "Cold Fluid Temperature": 2.5,
                "Temperature (Fuel Tank)": 3.0,
                "Temperature (Air Intake)": 1.8,
            }
        }
        try:
            text_summary = output["text_summary"]
            table_data = output["table_data"]
            plot_data = output["plot_data"]
            return text_summary, table_data, plot_data
        except json.JSONDecodeError as e:
            print("Error parsing LLM output:", e)
            return None

    # Callback to generate and download the report
    @app.callback(
        [
            Output("download-pdf", "data"),
            Output("error-message", "children"),
            Output("error-interval", "disabled"),
        ],
        [Input("generate-report-btn", "n_clicks"), 
         Input("error-interval", "n_intervals")],
    )
    def generate_and_download_report(n_clicks, n_intervals):
        # Clear the error message if the interval has been triggered
        if ctx.triggered_id == "error-interval":
            return dash.no_update, "", True
        
        if n_clicks:
            try:
                root_dir = os.path.dirname(os.path.dirname(__file__))
                file_path = os.path.join(root_dir, "mock_results.json")

                # Load the mock results JSON
                with open(file_path) as f:
                    data = json.load(f)

                json_data = json.dumps(data)

                # Get the LLM-generated summary
                text_summary, table_data, plot_data = get_llm_output(json_data)
                
                generate_report(text_summary, table_data, plot_data)

                # Return the file for download
                return dcc.send_file("kpi_report.pdf"), "", True
            except Exception as e:
                return dash.no_update, f"Error generating report: {str(e)}", False
        return dash.no_update, "", True
