from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(file_path, summary, insights, charts):

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path)

    elements = []

    elements.append(Paragraph("Data Analysis Report", styles["Title"]))

    elements.append(Paragraph(str(summary), styles["Normal"]))

    elements.append(Paragraph("AI Insights:", styles["Heading2"]))
    elements.append(Paragraph(insights, styles["Normal"]))

    for chart in charts:
        elements.append(Image(chart))

    doc.build(elements)