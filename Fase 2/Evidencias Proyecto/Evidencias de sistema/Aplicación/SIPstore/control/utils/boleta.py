from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Image
from django.conf import settings
import os

def generar_boleta_pdf(pedido, detalles):
    """
    Genera un PDF de boleta con la información del pedido y sus detalles.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Ruta de la imagen del logo (puede ser estática o dinámica)
    logo_path = os.path.join(settings.BASE_DIR, "static", "img", "logoMin2.png")

    # Agregar logo
    try:
        logo = Image(logo_path, width=2*inch, height=2*inch)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 12))
    except Exception as e:
        print(f"No se pudo cargar la imagen del logo: {e}")

    # Encabezado
    elements.append(Paragraph("<b>BOLETA DE VENTA</b>", styles["Title"]))
    elements.append(Spacer(1, 12))

    # Datos del pedido
    datos_pedido = [
        f"<b>N° Boleta:</b> {pedido.id}",
        f"<b>Fecha Pedido:</b> {pedido.fecha_pedido.strftime('%d-%m-%Y')}",
        f"<b>Fecha Retiro:</b> {pedido.fecha_retiro.strftime('%d-%m-%Y') if pedido.fecha_retiro else 'N/A'}",
        f"<b>Estado:</b> {pedido.estado.title()}",
        f"<b>Método de Pago:</b> {pedido.get_metodo_pago_display()}",
        f"<b>Centro de Retiro:</b> {pedido.local.nombre if pedido.local else 'N/A'}",
    ]
    for d in datos_pedido:
        elements.append(Paragraph(d, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Datos del cliente
    elements.append(Paragraph("<b>Datos del Cliente</b>", styles["Heading2"]))
    datos_cliente = [
        f"<b>Nombre:</b> {pedido.comprador}",
        f"<b>RUT/ID:</b> {pedido.rut_cli}",
        f"<b>Correo:</b> {pedido.correo_cli}",
        f"<b>Teléfono:</b> +{pedido.celular_cli}",
        f"<b>Dirección:</b> {pedido.ubicacion_cli}",
    ]
    for d in datos_cliente:
        elements.append(Paragraph(d, styles["Normal"]))
    elements.append(Spacer(1, 12))

    # Tabla de productos
    elements.append(Paragraph("<b>Detalle de Venta</b>", styles["Heading2"]))
    data = [["Producto", "Precio Unitario", "Cantidad", "Subtotal"]]

    # Estilo para las celdas de producto (soporta texto largo)
    producto_style = ParagraphStyle(
        name='ProductoStyle',
        fontSize=10,
        leading=12,  # altura de línea
    )

    for item in detalles:
        # Fallback seguro para nombre del producto
        nombre = item.nombre_producto or (getattr(item.producto, "nombre", "Producto Desconocido") if item.producto else "Producto Desconocido")
        data.append([
            Paragraph(nombre, producto_style),  # <- Ajuste de texto automático
            f"${item.precio_unitario:,.0f}",
            str(item.cantidad),
            f"${item.subtotal:,.0f}",
        ])

    data.append(["", "", "Total", f"${pedido.monto_total:,.0f}"])

    # Tabla con anchos ajustados
    table = Table(data, colWidths=[4*inch, 1.2*inch, 0.8*inch, 1.5*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#003366")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BACKGROUND", (0, 1), (-1, -2), colors.whitesmoke),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),  # Centrar verticalmente
    ]))
    elements.append(table)

    # Renderizar PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer