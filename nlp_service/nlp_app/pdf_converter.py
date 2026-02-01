# FILE: python-nlp-service/app/pdf_converter.py
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
import tempfile
import re
from typing import Dict, List, Optional
import PyPDF2
import pdfplumber

bp = Blueprint('pdf', __name__, url_prefix='/api/pdf')

class PdfToHtmlConverter:
    """Convert PDF to HTML while preserving structure, TOC, and footnotes"""
    
    def __init__(self):
        self.footnote_pattern = re.compile(r'\[(\d+)\]|\((\d+)\)|^(\d+)\.')
        self.heading_patterns = [
            re.compile(r'^[A-Z\s]{10,}$'),  # All caps headings
            re.compile(r'^\d+\.\s+[A-Z]'),  # Numbered sections
            re.compile(r'^[IVXLCDM]+\.\s+'),  # Roman numerals
        ]
    
    def convert(self, pdf_path: str, preserve_toc: bool = True, 
                preserve_footnotes: bool = True) -> Dict:
        """Main conversion method"""
        try:
            # Extract text and structure from PDF
            with pdfplumber.open(pdf_path) as pdf:
                pages = []
                toc_items = []
                footnotes = []
                
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    
                    # Detect headings
                    lines = text.split('\n')
                    page_content = []
                    
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        
                        # Check if line is a heading
                        if self._is_heading(line):
                            heading_id = self._generate_id(line)
                            page_content.append({
                                'type': 'heading',
                                'text': line,
                                'id': heading_id,
                                'page': page_num
                            })
                            if preserve_toc:
                                toc_items.append({
                                    'text': line,
                                    'id': heading_id,
                                    'page': page_num
                                })
                        
                        # Check for footnotes
                        elif preserve_footnotes and self._is_footnote(line):
                            footnote_num = self._extract_footnote_number(line)
                            if footnote_num:
                                footnotes.append({
                                    'number': footnote_num,
                                    'text': line,
                                    'page': page_num
                                })
                            page_content.append({
                                'type': 'footnote',
                                'text': line,
                                'number': footnote_num
                            })
                        
                        # Regular paragraph
                        else:
                            page_content.append({
                                'type': 'paragraph',
                                'text': line
                            })
                    
                    pages.append(page_content)
                
                # Build HTML
                html = self._build_html(pages, toc_items if preserve_toc else [], 
                                       footnotes if preserve_footnotes else [])
                
                return {
                    'html': html,
                    'page_count': len(pdf.pages),
                    'has_toc': len(toc_items) > 0,
                    'has_footnotes': len(footnotes) > 0,
                    'footnote_count': len(footnotes)
                }
                
        except Exception as e:
            raise Exception(f"PDF conversion failed: {str(e)}")
    
    def _is_heading(self, line: str) -> bool:
        """Determine if a line is a heading"""
        if len(line) < 3:
            return False
        
        for pattern in self.heading_patterns:
            if pattern.match(line):
                return True
        
        # Check if line is short, all caps, and bold-looking
        if len(line) < 100 and line.isupper() and len(line.split()) <= 10:
            return True
        
        return False
    
    def _is_footnote(self, line: str) -> bool:
        """Determine if a line is a footnote"""
        return bool(self.footnote_pattern.match(line))
    
    def _extract_footnote_number(self, line: str) -> Optional[int]:
        """Extract footnote number from line"""
        match = self.footnote_pattern.match(line)
        if match:
            for group in match.groups():
                if group:
                    try:
                        return int(group)
                    except ValueError:
                        continue
        return None
    
    def _generate_id(self, text: str) -> str:
        """Generate HTML ID from text"""
        # Convert to lowercase and replace spaces with hyphens
        id_text = re.sub(r'[^\w\s-]', '', text.lower())
        id_text = re.sub(r'[-\s]+', '-', id_text).strip('-')
        return id_text[:50]  # Limit length
    
    def _build_html(self, pages: List, toc_items: List, footnotes: List) -> str:
        """Build complete HTML document"""
        html_parts = []
        
        # HTML header
        html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Judgment Document</title>
    <style>
        body {
            font-family: 'Times New Roman', Times, serif;
            line-height: 1.8;
            max-width: 900px;
            margin: 0 auto;
            padding: 40px 20px;
            color: #333;
        }
        .toc {
            background: #f8f9fa;
            padding: 30px;
            margin: 30px 0;
            border-left: 4px solid #007bff;
            border-radius: 4px;
        }
        .toc h2 {
            margin-top: 0;
            color: #007bff;
            font-size: 1.5em;
        }
        .toc ol {
            padding-left: 25px;
            counter-reset: item;
        }
        .toc li {
            margin: 8px 0;
            list-style: none;
        }
        .toc li:before {
            content: counter(item) ". ";
            counter-increment: item;
            font-weight: bold;
            color: #007bff;
        }
        .toc a {
            color: #0056b3;
            text-decoration: none;
            transition: color 0.2s;
        }
        .toc a:hover {
            color: #007bff;
            text-decoration: underline;
        }
        .heading {
            font-weight: bold;
            font-size: 1.3em;
            margin: 30px 0 15px;
            color: #2c3e50;
            padding-bottom: 8px;
            border-bottom: 2px solid #e9ecef;
        }
        .paragraph {
            text-align: justify;
            margin: 15px 0;
            line-height: 1.8;
        }
        .footnotes {
            margin-top: 50px;
            padding-top: 30px;
            border-top: 3px solid #dee2e6;
        }
        .footnotes h2 {
            color: #495057;
            font-size: 1.4em;
            margin-bottom: 20px;
        }
        .footnote {
            margin: 12px 0;
            padding-left: 30px;
            position: relative;
            font-size: 0.95em;
            color: #555;
        }
        .footnote-number {
            position: absolute;
            left: 0;
            font-weight: bold;
            color: #007bff;
        }
        .footnote-ref {
            vertical-align: super;
            font-size: 0.8em;
            color: #007bff;
            text-decoration: none;
            padding: 0 2px;
        }
        .footnote-ref:hover {
            text-decoration: underline;
        }
        .page-break {
            page-break-after: always;
            margin: 40px 0;
            border-bottom: 1px dashed #ccc;
        }
    </style>
</head>
<body>''')
        
        # Table of Contents
        if toc_items:
            html_parts.append('<nav class="toc">')
            html_parts.append('<h2>Table of Contents</h2>')
            html_parts.append('<ol>')
            for item in toc_items:
                html_parts.append(
                    f'<li><a href="#{item["id"]}">{self._escape_html(item["text"])}</a></li>'
                )
            html_parts.append('</ol>')
            html_parts.append('</nav>')
        
        # Main content
        html_parts.append('<div class="judgment-content">')
        
        for page_num, page_content in enumerate(pages, 1):
            for item in page_content:
                if item['type'] == 'heading':
                    html_parts.append(
                        f'<h3 class="heading" id="{item["id"]}">{self._escape_html(item["text"])}</h3>'
                    )
                elif item['type'] == 'paragraph':
                    # Add footnote references
                    text = self._add_footnote_refs(item['text'])
                    html_parts.append(f'<p class="paragraph">{text}</p>')
                elif item['type'] == 'footnote':
                    # Footnotes will be added in separate section
                    pass
            
            if page_num < len(pages):
                html_parts.append('<div class="page-break"></div>')
        
        html_parts.append('</div>')
        
        # Footnotes section
        if footnotes:
            html_parts.append('<section class="footnotes">')
            html_parts.append('<h2>Footnotes</h2>')
            for fn in footnotes:
                html_parts.append(
                    f'<div class="footnote" id="fn-{fn["number"]}">'
                    f'<span class="footnote-number">{fn["number"]}.</span>'
                    f'{self._escape_html(fn["text"])}'
                    f'</div>'
                )
            html_parts.append('</section>')
        
        # Close HTML
        html_parts.append('</body></html>')
        
        return '\n'.join(html_parts)
    
    def _add_footnote_refs(self, text: str) -> str:
        """Add hyperlinks for footnote references"""
        def replace_fn(match):
            num = match.group(1) or match.group(2) or match.group(3)
            if num:
                return f'<a href="#fn-{num}" class="footnote-ref">[{num}]</a>'
            return match.group(0)
        
        return self.footnote_pattern.sub(replace_fn, self._escape_html(text))
    
    def _escape_html(self, text: str) -> str:
        """Escape HTML special characters"""
        return (text
                .replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


# API Routes
converter = PdfToHtmlConverter()

@bp.route('/convert-to-html', methods=['POST'])
def convert_to_html():
    """Convert PDF to HTML"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.endswith('.pdf'):
            return jsonify({'error': 'File must be a PDF'}), 400
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            # Get options
            preserve_toc = request.form.get('preserve_toc', 'true').lower() == 'true'
            preserve_footnotes = request.form.get('preserve_footnotes', 'true').lower() == 'true'
            
            # Convert
            result = converter.convert(tmp_path, preserve_toc, preserve_footnotes)
            
            return jsonify(result), 200
            
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/extract-metadata', methods=['POST'])
def extract_metadata():
    """Extract metadata from PDF"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name
        
        try:
            with open(tmp_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                metadata = pdf_reader.metadata
                
                # Extract basic info
                result = {
                    'title': metadata.get('/Title', ''),
                    'author': metadata.get('/Author', ''),
                    'subject': metadata.get('/Subject', ''),
                    'creator': metadata.get('/Creator', ''),
                    'page_count': len(pdf_reader.pages),
                }
                
                # Try to extract Indian court-specific metadata
                with pdfplumber.open(tmp_path) as pdf:
                    first_page_text = pdf.pages[0].extract_text() if pdf.pages else ''
                    
                    # Try to find court name
                    court_match = re.search(r'(?:IN THE|BEFORE THE)\s+(.+?(?:COURT|TRIBUNAL))', 
                                          first_page_text, re.IGNORECASE)
                    if court_match:
                        result['court'] = court_match.group(1).strip()
                    
                    # Try to find case number
                    case_match = re.search(r'(?:Case No\.|W\.P\.|C\.A\.|Crl\. A\.|S\.L\.P\.)\s*:?\s*(\d+[/\-]\d+)', 
                                         first_page_text, re.IGNORECASE)
                    if case_match:
                        result['case_number'] = case_match.group(0).strip()
                
                return jsonify(result), 200
                
        finally:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Register blueprint in main app
def register_pdf_routes(app):
    app.register_blueprint(bp)