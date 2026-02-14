"""
Judgment Analysis Routes
Handles complete judgment analysis including PDF extraction and NLP processing
"""

from flask import request, jsonify
from datetime import datetime
import os
import traceback

def register_judgment_routes(app):
    """Register judgment analysis routes with the Flask app"""
    
    @app.route('/analyze/<judgment_id>', methods=['POST'])
    def analyze_judgment(judgment_id):
        """
        Analyze a judgment by fetching it from MongoDB,
        extracting points of law, generating headnotes,
        and saving results back to the database.
        """
        try:
            from pymongo import MongoClient
            from bson import ObjectId
            import gridfs
            import io
            
            # Connect to MongoDB
            mongo_uri = "mongodb://localhost/solvelitigation"  # Use default socket connection
            client = MongoClient(mongo_uri)
            db = client.solvelitigation
            fs = gridfs.GridFS(db, collection="uploads")
            
            # Fetch judgment from database
            try:
                from bson.errors import InvalidId
                oid = ObjectId(judgment_id)
                judgment = db.judgments.find_one({"_id": oid})
            except (InvalidId, Exception) as e:
                return jsonify({"success": False, "message": f"Invalid judgment ID: {str(e)}"}), 400
            
            if not judgment:
                return jsonify({"success": False, "message": "Judgment not found"}), 404
            
            # Get text from judgment
            text = None
            
            # Try to get text from judgmentText field
            if judgment.get("judgmentText"):
                text = judgment["judgmentText"]
            # Or extract from PDF file
            elif judgment.get("fileId"):
                try:
                    # Try to import PyPDF2
                    try:
                        from PyPDF2 import PdfReader
                    except ImportError:
                        return jsonify({"success": False, "message": "PyPDF2 not installed"}), 500
                    
                    try:
                        file_oid = ObjectId(str(judgment["fileId"]))
                        pdf_file = fs.get(file_oid)
                    except Exception as fid_error:
                        return jsonify({"success": False, "message": f"File ID error: {str(fid_error)}"}), 500
                    pdf_bytes = pdf_file.read()
                    pdf_reader = PdfReader(io.BytesIO(pdf_bytes))
                    
                    # Extract text from all pages
                    text = ""
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                    
                except Exception as e:
                    return jsonify({"success": False, "message": f"Error extracting PDF: {str(e)}"}), 500
            
            if not text or len(text.strip()) < 100:
                return jsonify({"success": False, "message": "Insufficient text for analysis"}), 400
            
            # Analyze the text
            results = {
                "judgment_id": judgment_id,
                "case_number": judgment.get("caseNumber", "Unknown"),
                "status": "processing"
            }
            
            # Extract points of law
            try:
                from ai.extract_points_wrapper import extract_points
                points_result = extract_points(text[:5000])  # First 5000 chars
                results["points_of_law"] = points_result
            except Exception as e:
                results["points_of_law_error"] = str(e)
                results["points_of_law"] = []
            
            # Generate headnotes
            try:
                from ai.headnote_wrapper import generate_headnotes
                headnote_result = generate_headnotes(text[:3000])  # First 3000 chars
                results["headnotes"] = headnote_result
            except Exception as e:
                results["headnotes_error"] = str(e)
                results["headnotes"] = []
            
            # Update judgment in database
            update_data = {
                "analysisStatus": "completed",
                "analysisCompletedAt": datetime.utcnow(),
                "nlpAnalysis": {
                    "pointsOfLaw": results.get("points_of_law", []),
                    "headnotes": results.get("headnotes", []),
                    "processedAt": datetime.utcnow().isoformat()
                }
            }
            
            db.judgments.update_one(
                {"_id": ObjectId(judgment_id)},
                {"$set": update_data}
            )
            
            results["status"] = "completed"
            results["success"] = True
            
            return jsonify(results), 200
            
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Analysis failed: {str(e)}",
                "traceback": traceback.format_exc()
            }), 500
