import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

class HeadnoteGenerator:
    """
    AI-powered headnote generator that reads entire judgments
    and creates comprehensive, professional legal headnotes
    """
    
    def __init__(self):
        api_key = os.getenv('ANTHROPIC_API_KEY') or os.getenv('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = anthropic.Anthropic(api_key=api_key)
    
    def generate_headnotes(self, judgment_text: str) -> dict:
        """
        Read entire judgment and generate comprehensive headnotes
        
        Returns a structured headnote with:
        - Case title and citation
        - Brief facts
        - Issues framed
        - Held (decision)
        - Ratio decidendi (legal reasoning)
        - Key legal principles
        - Statutes and provisions
        """
        
        prompt = f"""You are a legal expert tasked with creating comprehensive HEADNOTES for a court judgment.

Read the ENTIRE judgment below carefully and prepare detailed headnotes following the standard legal format.

HEADNOTE FORMAT:
1. **Case Title & Citation** - Extract case name, court, date, judges
2. **Brief Facts** - Summarize the factual background (3-5 sentences)
3. **Issues** - List the key legal questions/issues raised (numbered list)
4. **Held** - State the court's decision clearly
5. **Ratio Decidendi** - Explain the legal reasoning and principles applied
6. **Key Legal Principles** - Extract important legal propositions
7. **Statutes & Provisions** - List all Acts, sections, and provisions discussed
8. **Disposition** - Final order/direction of the court

IMPORTANT GUIDELINES:
- Read the COMPLETE judgment, not just excerpts
- Be precise and legally accurate
- Use clear, professional legal language
- Include all relevant details
- Number each section clearly
- Extract exact statute names and section numbers

JUDGMENT TEXT:
{judgment_text}

Generate the headnotes now in the format specified above."""

        try:
            print("🔍 Sending judgment to AI for headnote generation...")
            
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=4000,  # Allow for comprehensive headnotes
                temperature=0.2,  # Lower temperature for factual accuracy
                messages=[{
                    "role": "user",
                    "content": prompt
                }]
            )
            
            headnotes_text = message.content[0].text
            
            print("✅ Headnotes generated successfully")
            
            # Parse into structured format
            structured = self._parse_headnotes_structured(headnotes_text)
            
            return {
                "success": True,
                "headnotes": headnotes_text,
                "structured": structured,
                "model": "claude-sonnet-4"
            }
            
        except Exception as e:
            print(f"❌ Error generating headnotes: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate headnotes"
            }
    
    def _parse_headnotes_structured(self, text: str) -> dict:
        """
        Parse the AI-generated headnotes into structured JSON format
        """
        structured = {
            "caseTitle": "",
            "citation": "",
            "court": "",
            "date": "",
            "judges": [],
            "briefFacts": "",
            "issues": [],
            "held": "",
            "ratio": [],
            "legalPrinciples": [],
            "statutes": [],
            "disposition": ""
        }
        
        current_section = None
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect sections
            lower_line = line.lower()
            
            if 'case title' in lower_line or 'citation' in lower_line:
                current_section = 'citation'
            elif 'brief facts' in lower_line or 'facts' in lower_line:
                current_section = 'facts'
            elif 'issues' in lower_line:
                current_section = 'issues'
            elif 'held' in lower_line:
                current_section = 'held'
            elif 'ratio decidendi' in lower_line or 'reasoning' in lower_line:
                current_section = 'ratio'
            elif 'legal principles' in lower_line or 'principles' in lower_line:
                current_section = 'principles'
            elif 'statutes' in lower_line or 'provisions' in lower_line:
                current_section = 'statutes'
            elif 'disposition' in lower_line:
                current_section = 'disposition'
            elif current_section:
                # Add content to current section
                if current_section == 'citation':
                    if 'vs' in line or 'v.' in line:
                        structured['caseTitle'] = line
                    elif 'court' in line.lower():
                        structured['court'] = line
                    elif any(month in line for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']):
                        structured['date'] = line
                
                elif current_section == 'facts':
                    structured['briefFacts'] += line + " "
                
                elif current_section == 'issues':
                    if line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '•')):
                        structured['issues'].append(line.lstrip('1234567890.-• '))
                
                elif current_section == 'held':
                    structured['held'] += line + " "
                
                elif current_section == 'ratio':
                    if line.startswith(('1.', '2.', '3.', '-', '•')) or len(line) > 50:
                        structured['ratio'].append(line.lstrip('1234567890.-• '))
                
                elif current_section == 'principles':
                    if line.startswith(('1.', '2.', '3.', '-', '•')):
                        structured['legalPrinciples'].append(line.lstrip('1234567890.-• '))
                
                elif current_section == 'statutes':
                    if 'act' in line.lower() or 'section' in line.lower():
                        structured['statutes'].append(line)
                
                elif current_section == 'disposition':
                    structured['disposition'] += line + " "
        
        # Clean up
        structured['briefFacts'] = structured['briefFacts'].strip()
        structured['held'] = structured['held'].strip()
        structured['disposition'] = structured['disposition'].strip()
        
        return structured