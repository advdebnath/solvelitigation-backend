from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import re

class LocalHeadnoteGenerator:
    """
    Self-hosted AI headnote generator using open-source models
    No external API calls - runs on your own infrastructure
    """
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initialize with a summarization model
        Options:
        - facebook/bart-large-cnn (default, good for summaries)
        - google/pegasus-large (better for long documents)
        - t5-large (versatile)
        """
        print(f"🔄 Loading AI model: {model_name}...")
        
        try:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"💻 Using device: {self.device}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(self.device)
            
            print("✅ AI model loaded successfully")
            
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            raise
    
    def generate_headnotes(self, judgment_text: str) -> dict:
        """
        Generate headnotes from full judgment text using self-hosted AI
        """
        try:
            print(f"\n📄 Processing judgment ({len(judgment_text)} chars)...")
            print(f"First 100 chars: {judgment_text[:100]}")
            
            # Split judgment into sections for better processing
            print("🔍 Splitting judgment into sections...")
            sections = self._split_judgment(judgment_text)
            print(f"✅ Sections found: {list(sections.keys())}")
            
            print("🔍 Extracting structured information...")
            headnotes = {
                "caseTitle": self._extract_case_title(judgment_text),
                "court": self._extract_court(judgment_text),
                "date": self._extract_date(judgment_text),
                "briefFacts": self._generate_facts_summary(sections.get('facts', judgment_text[:1000])),
                "issues": self._extract_issues(sections.get('issues', judgment_text)),
                "held": self._extract_held(sections.get('held', judgment_text)),
                "ratio": self._generate_ratio_summary(sections.get('reasoning', judgment_text[1000:3000])),
                "statutes": self._extract_statutes(judgment_text),
                "disposition": self._extract_disposition(judgment_text)
            }
            
            print("✅ Extraction complete")
            print(f"   - Case Title: {headnotes['caseTitle'][:50]}...")
            print(f"   - Court: {headnotes['court']}")
            print(f"   - Issues found: {len(headnotes['issues'])}")
            print(f"   - Statutes found: {len(headnotes['statutes'])}")
            
            # Generate formatted headnotes text
            print("📝 Formatting headnotes...")
            formatted_headnotes = self._format_headnotes(headnotes)
            
            print("✅ Headnotes generated successfully\n")
            
            return {
                "success": True,
                "headnotes": formatted_headnotes,
                "structured": headnotes,
                "model": "self-hosted-ai"
            }
            
        except Exception as e:
            print(f"❌ Error in generate_headnotes: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "error": str(e),
                "message": "Failed to generate headnotes"
            }
    
    def _split_judgment(self, text: str) -> dict:
        """Split judgment into logical sections"""
        sections = {}
        
        try:
            # Extract facts section
            facts_patterns = [
                r'(?:facts?|background)[\s\S]{0,100}?([\s\S]{200,2000}?)(?=held|issue|ratio|judgment)',
                r'(\d+\.\s+.{100,2000}?)(?=\d+\.\s+(?:issue|held))'
            ]
            for pattern in facts_patterns:
                facts_match = re.search(pattern, text[:3000], re.IGNORECASE)
                if facts_match:
                    sections['facts'] = facts_match.group(1)
                    break
            
            # Extract issues section
            issues_match = re.search(r'(?:issues?|questions?)[\s\S]{0,100}?([\s\S]{100,1000}?)(?=held|ratio|discussion)', text, re.IGNORECASE)
            if issues_match:
                sections['issues'] = issues_match.group(1)
            
            # Extract held/decision
            held_match = re.search(r'(?:held|decision|conclusion)[\s\S]{0,100}?([\s\S]{100,1000}?)(?=ratio|disposed|order)', text, re.IGNORECASE)
            if held_match:
                sections['held'] = held_match.group(1)
            
            # Extract reasoning
            ratio_match = re.search(r'(?:ratio|reasoning|analysis)[\s\S]{0,100}?([\s\S]{200,3000}?)', text, re.IGNORECASE)
            if ratio_match:
                sections['reasoning'] = ratio_match.group(1)
                
        except Exception as e:
            print(f"Warning: Error splitting sections: {e}")
        
        return sections
    
    def _extract_case_title(self, text: str) -> str:
        """Extract case title"""
        try:
            # Look for pattern: NAME vs/v. NAME
            patterns = [
                r'([A-Z][a-zA-Z\s\.]+)\s+(?:vs\.?|v\.?)\s+([A-Z][a-zA-Z\s\.]+)',
                r'([A-Z][a-zA-Z\s]+)\s+…Appellant\s+Versus\s+([A-Z][a-zA-Z\s]+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, text[:1500])
                if match:
                    return match.group(0).strip()
            return ""
        except:
            return ""
    
    def _extract_court(self, text: str) -> str:
        """Extract court name"""
        try:
            court_patterns = [
                r'((?:SUPREME|HIGH|DISTRICT)\s+COURT[A-Z\s]+)',
                r'(IN THE [A-Z\s]+COURT[A-Z\s]*)',
            ]
            for pattern in court_patterns:
                match = re.search(pattern, text[:800], re.IGNORECASE)
                if match:
                    court = match.group(1).strip()
                    # Clean up
                    court = re.sub(r'\s+', ' ', court)
                    return court[:100]  # Limit length
            return ""
        except:
            return ""
    
    def _extract_date(self, text: str) -> str:
        """Extract judgment date"""
        try:
            # Look for date patterns
            date_patterns = [
                r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b',
                r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
                r'Date:\s*([^\n]+)'
            ]
            for pattern in date_patterns:
                match = re.search(pattern, text[:1500], re.IGNORECASE)
                if match:
                    return match.group(0).strip()
            return ""
        except:
            return ""
    
    def _generate_facts_summary(self, facts_text: str) -> str:
        """Generate summary of facts using AI"""
        if not facts_text or len(facts_text) < 50:
            return ""
        
        try:
            print("  → Summarizing facts...")
            # Truncate if too long
            facts_text = facts_text[:1024]
            
            inputs = self.tokenizer(facts_text, max_length=1024, truncation=True, return_tensors="pt").to(self.device)
            summary_ids = self.model.generate(
                inputs["input_ids"], 
                max_length=200, 
                min_length=50, 
                length_penalty=2.0, 
                num_beams=4,
                early_stopping=True
            )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary
        except Exception as e:
            print(f"  ⚠️ Facts summary failed: {e}")
            return facts_text[:300] + "..."
    
    def _extract_issues(self, issues_text: str) -> list:
        """Extract legal issues"""
        issues = []
        
        try:
            if not issues_text:
                return []
            
            # Look for numbered points or questions
            lines = issues_text.split('\n')
            for line in lines:
                line = line.strip()
                # Match numbered items or questions
                if re.match(r'^\d+[\.)]\s+', line) or '?' in line:
                    # Clean the line
                    clean_line = re.sub(r'^\d+[\.)]\s+', '', line)
                    if len(clean_line) > 20:  # Must be substantial
                        issues.append(clean_line[:200])  # Limit length
                
                if len(issues) >= 5:  # Max 5 issues
                    break
            
            # If no issues found by pattern, extract from text
            if not issues and issues_text:
                sentences = re.split(r'[.!?]', issues_text)
                for sentence in sentences[:3]:
                    if len(sentence.strip()) > 30:
                        issues.append(sentence.strip())
                        
        except Exception as e:
            print(f"  ⚠️ Issue extraction failed: {e}")
        
        return issues
    
    def _extract_held(self, held_text: str) -> str:
        """Extract what was held"""
        try:
            if not held_text:
                return ""
            
            # Look for decision keywords
            decision_keywords = ['allowed', 'dismissed', 'directed', 'ordered', 'held', 'set aside', 'granted', 'rejected']
            
            sentences = re.split(r'[.!?]', held_text)
            for sentence in sentences:
                sentence = sentence.strip()
                if any(keyword in sentence.lower() for keyword in decision_keywords):
                    if len(sentence) > 30:
                        return sentence[:300]
            
            # Return first substantial sentence
            for sentence in sentences:
                if len(sentence.strip()) > 50:
                    return sentence.strip()[:300]
                    
            return held_text[:300]
        except:
            return ""
    
    def _generate_ratio_summary(self, ratio_text: str) -> list:
        """Generate summary of legal reasoning"""
        if not ratio_text or len(ratio_text) < 100:
            return []
        
        try:
            print("  → Summarizing reasoning...")
            # Truncate if too long
            ratio_text = ratio_text[:1024]
            
            inputs = self.tokenizer(ratio_text, max_length=1024, truncation=True, return_tensors="pt").to(self.device)
            summary_ids = self.model.generate(
                inputs["input_ids"], 
                max_length=300, 
                min_length=100, 
                length_penalty=2.0, 
                num_beams=4,
                early_stopping=True
            )
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            # Split into points
            points = re.split(r'\.\s+', summary)
            return [p.strip() + '.' for p in points if len(p.strip()) > 20][:3]
        except Exception as e:
            print(f"  ⚠️ Ratio summary failed: {e}")
            # Fallback: extract key sentences
            sentences = re.split(r'[.!?]', ratio_text)
            return [s.strip() + '.' for s in sentences if len(s.strip()) > 50][:3]
    
    def _extract_statutes(self, text: str) -> list:
        """Extract statute references"""
        statutes = []
        
        try:
            # Pattern for Act names
            act_pattern = r'([A-Z][a-zA-Z\s,&]+Act,?\s+\d{4})'
            acts = re.findall(act_pattern, text)
            
            # Clean and deduplicate
            seen = set()
            for act in acts:
                act_clean = re.sub(r'\s+', ' ', act.strip())
                if act_clean not in seen and len(act_clean) > 10:
                    statutes.append(act_clean)
                    seen.add(act_clean)
                if len(statutes) >= 10:
                    break
            
            # Pattern for sections
            section_pattern = r'Section\s+\d+[A-Z]?(?:\(\d+\))?'
            sections = re.findall(section_pattern, text, re.IGNORECASE)
            
            # Add unique sections
            for section in sections:
                if section not in seen:
                    statutes.append(section)
                    seen.add(section)
                if len(statutes) >= 15:
                    break
                    
        except Exception as e:
            print(f"  ⚠️ Statute extraction failed: {e}")
        
        return statutes[:15]  # Max 15 statutes
    
    def _extract_disposition(self, text: str) -> str:
        """Extract final disposition/order"""
        try:
            # Look for final order section (usually at the end)
            order_patterns = [
                r'(?:order|disposed?|directed?)[\s\S]{0,100}?([\s\S]{100,500}?)(?:\(|JUDGE|$)',
                r'(\d+\.\s+(?:The appeal|Appeal|Petition)[^.]{50,300}\.)',
            ]
            
            for pattern in order_patterns:
                match = re.search(pattern, text[-2000:], re.IGNORECASE)
                if match:
                    return match.group(1).strip()[:500]
            
            return ""
        except:
            return ""
    
    def _format_headnotes(self, data: dict) -> str:
        """Format structured data into readable headnotes"""
        formatted = []
        
        try:
            if data.get('caseTitle'):
                formatted.append(f"**{data['caseTitle']}**\n")
            
            if data.get('court'):
                formatted.append(f"**Court:** {data['court']}")
            
            if data.get('date'):
                formatted.append(f"**Date:** {data['date']}\n")
            
            if data.get('briefFacts'):
                formatted.append(f"**Brief Facts:**\n{data['briefFacts']}\n")
            
            if data.get('issues'):
                formatted.append("**Issues:**")
                for i, issue in enumerate(data['issues'], 1):
                    formatted.append(f"{i}. {issue}")
                formatted.append("")
            
            if data.get('held'):
                formatted.append(f"**Held:**\n{data['held']}\n")
            
            if data.get('ratio'):
                formatted.append("**Ratio Decidendi:**")
                for point in data['ratio']:
                    formatted.append(f"• {point}")
                formatted.append("")
            
            if data.get('statutes'):
                formatted.append("**Statutes & Provisions:**")
                formatted.append(", ".join(data['statutes'][:10]))
                formatted.append("")
            
            if data.get('disposition'):
                formatted.append(f"**Disposition:**\n{data['disposition']}")
                
        except Exception as e:
            print(f"  ⚠️ Formatting failed: {e}")
            formatted = [f"Error formatting headnotes: {e}"]
        
        return "\n".join(formatted)


# For backward compatibility
HeadnoteGenerator = LocalHeadnoteGenerator