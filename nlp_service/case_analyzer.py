"""
AI-Powered Case Analysis
Extracts arguments, citations, and provides strategic insights
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import re
import logging
from datetime import datetime

case_analysis_bp = Blueprint('case_analysis', __name__)
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['solvelitigation']

def extract_citations(text):
    """
    Extract case citations from text
    Returns list of case numbers
    """
    # Pattern for Indian case citations
    patterns = [
        r'\b\d{4}\s+\(\d+\)\s+[A-Z]+\s+\d+\b',  # 2023 (1) SCC 123
        r'\b[A-Z]+\s*\([A-Z]\)\s*\d+/\d{4}\b',  # WP(C) 123/2023
        r'\bAIR\s+\d{4}\s+[A-Z]+\s+\d+\b',      # AIR 2023 SC 123
    ]
    
    citations = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        citations.extend(matches)
    
    return list(set(citations))

def extract_legal_principles(text):
    """
    Extract legal principles and maxims
    """
    # Common legal principle indicators
    indicators = [
        'held that', 'observed that', 'principle', 'maxim',
        'doctrine', 'established that', 'rule of law',
        'legal position', 'settled law'
    ]
    
    principles = []
    sentences = text.split('.')
    
    for sentence in sentences:
        sentence_lower = sentence.lower()
        if any(indicator in sentence_lower for indicator in indicators):
            if len(sentence.strip()) > 50:  # Avoid too short sentences
                principles.append(sentence.strip())
    
    return principles[:10]  # Return top 10

def extract_arguments(text, argument_type='for'):
    """
    Extract arguments FOR or AGAINST from text
    """
    # Keywords for different types of arguments
    for_keywords = [
        'in favor of', 'supports', 'establishes', 'proves',
        'clearly shows', 'demonstrates', 'substantiates',
        'petitioner submits', 'it is submitted', 'contention',
        'grounds', 'basis', 'entitled to'
    ]
    
    against_keywords = [
        'against', 'contrary to', 'refutes', 'disputes',
        'challenge', 'oppose', 'respondent submits',
        'counter', 'rebuttal', 'objection', 'denial'
    ]
    
    keywords = for_keywords if argument_type == 'for' else against_keywords
    
    arguments = []
    sentences = text.split('.')
    
    for i, sentence in enumerate(sentences):
        sentence_lower = sentence.lower()
        
        # Check if sentence contains argument keywords
        if any(keyword in sentence_lower for keyword in keywords):
            # Get context (current + next sentence)
            context = sentence
            if i + 1 < len(sentences):
                context += '. ' + sentences[i + 1]
            
            if len(context.strip()) > 100:
                arguments.append(context.strip())
    
    return arguments[:15]  # Return top 15

def analyze_strength(argument_text, citations_count, keywords_found):
    """
    Determine argument strength based on multiple factors
    """
    score = 0
    
    # Citation weight
    if citations_count > 3:
        score += 40
    elif citations_count > 1:
        score += 25
    elif citations_count > 0:
        score += 10
    
    # Length weight (comprehensive arguments)
    if len(argument_text) > 300:
        score += 20
    elif len(argument_text) > 150:
        score += 10
    
    # Strong language weight
    strong_words = ['clearly', 'established', 'settled', 'binding', 'mandatory']
    if any(word in argument_text.lower() for word in strong_words):
        score += 20
    
    # Keyword weight
    score += min(keywords_found * 5, 20)
    
    if score >= 70:
        return 'strong'
    elif score >= 40:
        return 'moderate'
    else:
        return 'weak'

@case_analysis_bp.route('/analyze-case/<case_id>', methods=['POST'])
def analyze_case(case_id):
    """
    Comprehensive AI analysis of a case
    """
    try:
        # Get case and all its documents
        cases_collection = db['user_cases']
        documents_collection = db['user_documents']
        notes_collection = db['user_notes']
        judgments_collection = db['judgments']
        
        case = cases_collection.find_one({'_id': ObjectId(case_id)})
        if not case:
            return jsonify({
                'success': False,
                'message': 'Case not found'
            }), 404
        
        # Get all documents in this case
        documents = list(documents_collection.find({
            'caseId': ObjectId(case_id),
            'status': 'processed'
        }))
        
        if len(documents) == 0:
            return jsonify({
                'success': False,
                'message': 'No processed documents found in case'
            }), 400
        
        # Combine all document texts
        all_text = ""
        document_sources = {}
        
        for doc in documents:
            if doc.get('extractedText'):
                all_text += doc['extractedText'] + "\n\n"
                document_sources[doc['_id']] = doc['fileName']
        
        if not all_text.strip():
            return jsonify({
                'success': False,
                'message': 'No text extracted from documents'
            }), 400
        
        logger.info(f"Analyzing case {case_id} with {len(all_text)} characters of text")
        
        # Extract citations
        citations = extract_citations(all_text)
        
        # Extract legal principles
        principles = extract_legal_principles(all_text)
        
        # Extract FOR arguments
        for_arguments = extract_arguments(all_text, 'for')
        
        # Extract AGAINST arguments  
        against_arguments = extract_arguments(all_text, 'against')
        
        # Build structured FOR points
        for_points = []
        for arg in for_arguments[:10]:  # Top 10
            # Count citations in this argument
            arg_citations = len([c for c in citations if c in arg])
            
            # Determine strength
            strength = analyze_strength(arg, arg_citations, 1)
            
            for_points.append({
                'text': arg[:500],  # Limit length
                'source': 'User Documents',
                'sourceType': 'user_document',
                'strength': strength,
            })
        
        # Build structured AGAINST points
        against_points = []
        for arg in against_arguments[:10]:
            arg_citations = len([c for c in citations if c in arg])
            strength = analyze_strength(arg, arg_citations, 1)
            
            against_points.append({
                'text': arg[:500],
                'source': 'User Documents',
                'sourceType': 'user_document',
                'strength': strength,
            })
        
        # Calculate overall strength
        strong_for = len([p for p in for_points if p['strength'] == 'strong'])
        moderate_for = len([p for p in for_points if p['strength'] == 'moderate'])
        weak_for = len([p for p in for_points if p['strength'] == 'weak'])
        
        strong_against = len([p for p in against_points if p['strength'] == 'strong'])
        moderate_against = len([p for p in against_points if p['strength'] == 'moderate'])
        weak_against = len([p for p in against_points if p['strength'] == 'weak'])
        
        # Weighted scoring
        for_score = (strong_for * 3) + (moderate_for * 2) + (weak_for * 1)
        against_score = (strong_against * 3) + (moderate_against * 2) + (weak_against * 1)
        
        total_score = for_score + against_score
        if total_score == 0:
            for_percentage = 50
            against_percentage = 50
        else:
            for_percentage = int((for_score / total_score) * 100)
            against_percentage = 100 - for_percentage
        
        # Find related judgments based on citations
        related_judgments = []
        if citations:
            # Try to find judgments matching citations
            for citation in citations[:5]:  # Check top 5 citations
                matching = judgments_collection.find_one({
                    '$or': [
                        {'caseNumber': {'$regex': citation, '$options': 'i'}},
                        {'fullText': {'$regex': citation, '$options': 'i'}}
                    ]
                })
                if matching:
                    related_judgments.append({
                        'caseNumber': matching.get('caseNumber', 'Unknown'),
                        'courtType': matching.get('courtType', 'Unknown'),
                        'year': matching.get('year', 0),
                        'relevance': f"Cited in case documents"
                    })
        
        # Generate recommendations
        recommendations = []
        
        if for_percentage > 65:
            recommendations.append("Your case has strong supporting arguments. Focus on emphasizing precedents cited.")
        elif for_percentage < 35:
            recommendations.append("Opposition has stronger arguments. Consider addressing their key points proactively.")
        else:
            recommendations.append("Case is balanced. Strengthen evidence and cite more supporting precedents.")
        
        if len(citations) < 3:
            recommendations.append("Add more case law citations to strengthen legal arguments.")
        
        if strong_against > 0:
            recommendations.append("Prepare robust counter-arguments to opposition's strong points.")
        
        if len(related_judgments) > 0:
            recommendations.append(f"Review {len(related_judgments)} related judgments cited in your documents.")
        
        # Prepare neutral points (legal principles)
        neutral_points = [
            {
                'text': principle[:500],
                'source': 'Legal Principles',
                'sourceType': 'note'
            }
            for principle in principles[:5]
        ]
        
        # Save analysis
        analysis = {
            'caseId': ObjectId(case_id),
            'userId': case['userId'],
            'forPoints': for_points,
            'againstPoints': against_points,
            'neutralPoints': neutral_points,
            'overallStrength': {
                'for': for_percentage,
                'against': against_percentage
            },
            'recommendations': recommendations,
            'relatedJudgments': related_judgments,
            'citationsFound': len(citations),
            'generatedAt': datetime.utcnow()
        }
        
        analysis_collection = db['case_analysis']
        analysis_collection.update_one(
            {'caseId': ObjectId(case_id)},
            {'$set': analysis},
            upsert=True
        )
        
        logger.info(f"Analysis complete for case {case_id}")
        
        return jsonify({
            'success': True,
            'data': analysis
        })
        
    except Exception as e:
        logger.error(f"Error analyzing case: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Analysis failed',
            'error': str(e)
        }), 500

@case_analysis_bp.route('/extract-citations/<document_id>', methods=['POST'])
def extract_document_citations(document_id):
    """
    Extract citations from a specific document
    """
    try:
        documents_collection = db['user_documents']
        document = documents_collection.find_one({'_id': ObjectId(document_id)})
        
        if not document or not document.get('extractedText'):
            return jsonify({
                'success': False,
                'message': 'Document or text not found'
            }), 404
        
        citations = extract_citations(document['extractedText'])
        
        return jsonify({
            'success': True,
            'data': {
                'citations': citations,
                'count': len(citations)
            }
        })
        
    except Exception as e:
        logger.error(f"Error extracting citations: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Citation extraction failed',
            'error': str(e)
        }), 500

