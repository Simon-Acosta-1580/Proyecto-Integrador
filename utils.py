from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import tempfile

def soft_delete(instance, session):
    instance.activo = False
    session.add(instance)
    session.commit()
    return instance

def restore(instance, session):
    instance.activo = True
    session.add(instance)
    session.commit()
    return instance

def generar_pdf_reporte_analisis(analisis_list):
    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, "reporte_analisis.pdf")
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    title = Paragraph("Reporte de Análisis y Beneficios", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 12))

    data = [["ID", "Nombre", "Impacto total", "Alcance medios", "Participación redes", "Beneficios (categoría - ingreso)"]]

    for a in analisis_list:
        beneficios_str = ""
        if a.get("beneficios"):
            beneficios_str = "; ".join(f"{b['categoria']} ${b['ingreso']}" for b in a["beneficios"])
        data.append([
            str(a.get("id","")),
            a.get("nombre",""),
            str(a.get("impacto_total","")),
            str(a.get("alcance_medios","")),
            str(a.get("participacion_redes","")),
            beneficios_str
        ])

    table = Table(data, repeatRows=1)
    elements.append(table)
    doc.build(elements)
    return file_path

def file_response_pdf(path):
    return FileResponse(path, media_type="application/pdf", filename=os.path.basename(path))
