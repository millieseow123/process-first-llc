import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc
from dash import html, dcc
from fpdf import FPDF

# Report generation components
def ReportGeneration():
    return html.Div(
        [
            html.Img(
                src="/assets/images/report.png",
                alt="Report Image",
                style={"width": "100%", "maxWidth": "100px", "margin": "20px 0"},
            ),
            html.P("The system allows you to run experiments with various process variables. "
                   "Click 'Generate Report' to receive a detailed analysis of how these variables affect the Key Performance Indicator (KPI).",
                    style={"maxWidth": "600px"},
            ),
            dcc.Loading(
                dbc.Button("Generate Report", id="generate-report-btn", color="primary"),
                type="circle",
                style={"color": "#007BFF", "width": "100px", "height": "100px"},
            ),
            dcc.Download(id="download-pdf"),
            html.Div(id="error-message", style={"color": "red",
                "marginTop": "10px",
                "fontSize": "14px", 
                "width": "40%",     
                "textAlign": "center",
                "margin": "0 auto",}),
            dcc.Interval(id="error-interval", interval=5000, n_intervals=0, disabled=True),
        ],
        style={
            "textAlign": "center",
            "display": "flex",
            "flexDirection": "column",
            "alignItems": "center",
            "height": "100vh", 
        },
    )

def generate_report(text_summary, table_data, plot_data):
     # Create the PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title Page
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Process Simulation Report", ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 8, "KPI Tuning and Impact Analysis", ln=True, align="C")
    pdf.ln(5)

    # Section 1: Executive Summary
    pdf.set_left_margin(15)  # Ensure consistent left margin
    pdf.set_right_margin(15)    
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 8, "Section 1: Executive Summary", ln=True)
    pdf.set_font("Arial", "", 12)
    clean_text_summary = "\n".join(line.strip() for line in text_summary.splitlines() if line.strip())
    pdf.multi_cell(0, 8, clean_text_summary)
    pdf.ln(6)

    # Section 2: Summary of Experiments
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Section 2: Summary of Experiments", ln=True)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(40, 10, "Equipment", border=1, align="C")
    pdf.cell(55, 10, "Variable", border=1, align="C")
    pdf.cell(30, 10, "Initial Value", border=1, align="C")
    pdf.cell(30, 10, "Tuned Value", border=1, align="C")
    pdf.cell(30, 10, "Impact on KPI", border=1, align="C")
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", "", 12)
    for row in table_data:
        pdf.cell(40, 10, row["Equipment"], border=1)
        pdf.cell(55, 10, row["Variable"], border=1)
        pdf.cell(30, 10, str(row["Initial Value"]), border=1)
        pdf.cell(30, 10, str(row["Tuned Value"]), border=1)
        pdf.cell(30, 10, f"{row['Impact on KPI']}%", border=1)
        pdf.ln()

    # Section 3: KPI Impact Plot
    pdf.ln(10)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Section 3: KPI Impact Plot", ln=True)

    # Generate Plot
    plt.figure(figsize=(6, 4))
    plt.bar(plot_data.keys(), plot_data.values(), color="skyblue")
    plt.title("Top Impact on KPI")
    plt.xlabel("Variable")
    plt.ylabel("Impact Value (%)")
    plt.tight_layout()
    plt.savefig("plot.png")
    pdf.image("plot.png", x=10, y=pdf.get_y(), w=190)
    pdf.ln(20)

    # Save the PDF
    pdf.output("kpi_report.pdf")
