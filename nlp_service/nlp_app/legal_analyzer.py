# nlp_service/app/legal_analyzer.py
import re
from typing import List, Dict

def extract_headnotes(text: str) -> List[str]:
    """Extract key legal principles as headnotes"""
    headnotes = []
    
    # Pattern: "Held that..." or "It was held..."
    held_pattern = r'(Held that|It was held that|The Court held that)([^.]+\.)'
    for match in re.finditer(held_pattern, text, re.IGNORECASE):
        headnotes.append(match.group(2).strip())
    
    # Pattern: Numbered holdings
    numbered_pattern = r'^\d+\.\s+([A-Z][^.]+\.)'
    for match in re.finditer(numbered_pattern, text, re.MULTILINE):
        headnotes.append(match.group(1).strip())
    
    return headnotes[:10]  # Top 10 headnotes

def extract_points_of_law(text: str) -> List[Dict]:
    """Extract specific legal points"""
    points = []
    
    # Criminal law patterns
    criminal_patterns = [
        r'(Section\s+\d+[A-Z]*\s+of\s+(?:the\s+)?IPC)',
        r'(under\s+Section\s+\d+\s+CrPC)',
    ]
    
    # Civil law patterns
    civil_patterns = [
        r'(Order\s+\w+\s+Rule\s+\w+\s+CPC)',
        r'(Section\s+\d+\s+of\s+(?:the\s+)?Contract Act)',
    ]
    
    # Constitutional law
    const_patterns = [
        r'(Article\s+\d+\s+of\s+(?:the\s+)?Constitution)',
    ]
    
    for pattern in criminal_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            points.append({
                'principle': match.group(1),
                'category': 'criminal'
            })
    
    # Similar for civil and constitutional...
    
    return points

def extract_acts_involved(text: str) -> List[Dict]:
    """Extract all acts and statutes referenced"""
    acts = {}
    
    patterns = [
        r'(Indian Penal Code|IPC)',
        r'(Code of Criminal Procedure|CrPC)',
        r'(Code of Civil Procedure|CPC)',
        r'(Companies Act,?\s+\d{4})',
        r'(Income[-\s]?tax Act,?\s+\d{4})',
        r'(Constitution of India)',
        r'(Evidence Act)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            act_name = match.group(1)
            if act_name not in acts:
                acts[act_name] = {
                    'actName': act_name,
                    'sections': extract_sections_for_act(text, act_name)
                }
    
    return list(acts.values())

# Add Flask endpoint
@bp.route('/analyze-legal', methods=['POST'])
def analyze_legal():
    data = request.json
    text = data.get('text', '')
    
    return jsonify({
        'headnotes': extract_headnotes(text),
        'pointsOfLaw': extract_points_of_law(text),
        'actsInvolved': extract_acts_involved(text)
    })