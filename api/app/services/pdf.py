import io
import re
import barcode
from barcode.writer import ImageWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from app.models.item import Item

def generate_item_label(item: Item) -> io.BytesIO:
    """Generates a PDF label for a given item."""
    # Validate SKU
    if not re.match(r"^[A-Za-z0-9-]{1,50}$", item.sku):
        raise ValueError("Invalid SKU format")
        
    # Create an in-memory buffer for the PDF
    pdf_buffer = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(pdf_buffer, pagesize=(2.625 * inch, 1 * inch))

    # --- Barcode --- #
    code128 = barcode.get('code128', item.sku, writer=ImageWriter())
    barcode_buffer = io.BytesIO()
    code128.write(barcode_buffer, options={"module_height": 10.0, "font_size": 10, "text_distance": 3.0})
    barcode_buffer.seek(0)

    # --- Draw to PDF --- #
    # Draw item name (top)
    c.drawString(0.1 * inch, 0.75 * inch, item.name[:30]) # Truncate name if too long

    # Draw barcode (middle)
    c.drawImage(barcode_buffer, 0.1 * inch, 0.2 * inch, width=2.4 * inch, height=0.4 * inch)

    c.showPage()
    c.save()

    pdf_buffer.seek(0)
    return pdf_buffer
