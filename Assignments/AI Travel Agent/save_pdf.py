# --- NEW PDF Generation Function using xhtml2pdf ---

import io
import os
from markdown import markdown
from xhtml2pdf import pisa
import streamlit as st

def create_pdf(content: str) -> bytes:
    """Converts a markdown string to a PDF byte object using xhtml2pdf."""
    st.info("Using xhtml2pdf for PDF generation.")

    # Convert markdown to HTML
    html_content = markdown(content)

    # Add CSS for styling and for embedding the Unicode font
    # This is crucial for making emojis and special characters work.
    styled_html = f"""
    <html>
    <head>
        <style>
            @font-face {{
                font-family: 'DejaVu Sans';
                src: url('DejaVuSans.ttf');
            }}
            body {{
                font-family: 'DejaVu Sans', sans-serif;
                line-height: 1.6;
            }}
            h1, h2, h3 {{
                font-weight: bold;
            }}
            ul {{
                list-style-type: disc;
                margin-left: 20px;
            }}
            li {{
                margin-bottom: 8px;
            }}
            code {{
                background-color: #f1f1f1;
                padding: 2px 5px;
                border-radius: 4px;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    # Create a file-like object in memory to hold the PDF data
    result = io.BytesIO()

    # Generate the PDF
    # The link_callback is necessary to help the library find the local font file
    pdf = pisa.CreatePDF(
        io.StringIO(styled_html),                # source HTML
        dest=result,                             # destination
        link_callback=lambda uri, rel: os.path.join(os.getcwd(), 'DejaVuSans.ttf')
    )

    # Check for errors and return the PDF data
    if not pdf.err:
        return result.getvalue()
    else:
        st.error(f"Error converting to PDF: {pdf.err}")
        return b""