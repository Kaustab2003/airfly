#!/usr/bin/env python3
"""
Markdown to PDF Converter for AirFly Insights Presentation
"""

import markdown
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import re
import os

def markdown_to_pdf(markdown_file, pdf_file):
    """Convert markdown file to PDF with proper formatting for presentation slides"""

    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=A4)
    styles = getSampleStyleSheet()

    # Create custom styles for presentation
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor='navy'
    )

    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=20,
        alignment=TA_LEFT,
        textColor='darkblue'
    )

    content_style = styles['Normal']
    content_style.fontSize = 12
    content_style.leading = 16

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=12,
        leftIndent=20,
        leading=16
    )

    # Split content into slides
    slides = re.split(r'^---$', md_content, flags=re.MULTILINE)

    story = []

    for slide in slides:
        if not slide.strip():
            continue

        lines = slide.strip().split('\n')
        slide_content = []

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            if line.startswith('# '):
                # Main title
                title = line[2:].strip()
                story.append(Paragraph(title, title_style))
                story.append(Spacer(1, 0.3*inch))

            elif line.startswith('## Slide'):
                # Slide header
                slide_title = line.split(':', 1)[1].strip() if ':' in line else line[2:].strip()
                story.append(Paragraph(slide_title, slide_title_style))
                story.append(Spacer(1, 0.2*inch))

            elif line.startswith('## '):
                # Section header
                header = line[2:].strip()
                story.append(Paragraph(header, styles['Heading3']))
                story.append(Spacer(1, 0.1*inch))

            elif line.startswith('- ') or line.startswith('* '):
                # Bullet points
                bullets = []
                while i < len(lines) and (lines[i].strip().startswith('- ') or lines[i].strip().startswith('* ')):
                    bullet_text = lines[i].strip()[2:].strip()
                    bullets.append(f"• {bullet_text}")
                    i += 1
                i -= 1  # Adjust for the outer loop

                for bullet in bullets:
                    story.append(Paragraph(bullet, bullet_style))

            elif line.startswith('|') and i + 1 < len(lines) and '|' in lines[i+1]:
                # Table (simplified - just show as text)
                table_lines = []
                while i < len(lines) and lines[i].strip().startswith('|'):
                    table_lines.append(lines[i].strip())
                    i += 1
                i -= 1  # Adjust for the outer loop

                for table_line in table_lines:
                    story.append(Paragraph(table_line.replace('|', ' | '), content_style))

            elif line and not line.startswith('#') and not line.startswith('-') and not line.startswith('*'):
                # Regular content
                content_lines = []
                while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') and not lines[i].strip().startswith('-') and not lines[i].strip().startswith('*'):
                    content_lines.append(lines[i].strip())
                    i += 1
                i -= 1  # Adjust for the outer loop

                content = ' '.join(content_lines)
                if content:
                    story.append(Paragraph(content, content_style))

            i += 1

        # Add page break between slides (except for the last slide)
        if slide != slides[-1]:
            story.append(PageBreak())

    # Build the PDF
    doc.build(story)
    print(f"PDF created successfully: {pdf_file}")

if __name__ == "__main__":
    markdown_file = "presentation_slides.md"
    pdf_file = "AirFly_Insights_Presentation.pdf"

    if os.path.exists(markdown_file):
        try:
            markdown_to_pdf(markdown_file, pdf_file)
            print(f"✅ PDF generated successfully: {pdf_file}")
        except Exception as e:
            print(f"❌ Error generating PDF: {e}")
            print("Note: Ensure reportlab is installed: pip install reportlab markdown")
    else:
        print(f"❌ Error: {markdown_file} not found!")