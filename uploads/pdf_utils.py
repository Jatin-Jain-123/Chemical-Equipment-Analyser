from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from django.conf import settings


def generate_pdf_report(dataset):
    file_name = f"report_{dataset.id}.pdf"
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 50
    summary = dataset.summary

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Chemical Equipment Report")
    y -= 40

    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"Uploaded at: {dataset.uploaded_at}")
    y -= 30

    c.drawString(50, y, f"Total Equipment: {summary['total_equipment']}")
    y -= 20

    c.drawString(50, y, "Averages:")
    y -= 20

    c.drawString(70, y, f"Flowrate: {summary['average_flowrate']}")
    y -= 20
    c.drawString(70, y, f"Pressure: {summary['average_pressure']}")
    y -= 20
    c.drawString(70, y, f"Temperature: {summary['average_temperature']}")
    y -= 30

    c.drawString(50, y, "Equipment Type Distribution:")
    y -= 20

    for eq_type, count in summary["equipment_type_distribution"].items():
        c.drawString(70, y, f"{eq_type}: {count}")
        y -= 20

    c.save()

    return file_name