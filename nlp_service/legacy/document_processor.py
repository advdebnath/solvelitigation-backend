"""
Document Text Extraction Service
Extracts text from user-uploaded PDFs
"""

from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import PyPDF2
import io
import logging

document_bp = Blueprint('document', __name__)
logger = logging.getLogger(__name__)

# MongoDB connection
client = MongoClient('mongodb://127.0.0.1:27017/')
db = client['solvelitigation']

@document_bp.route('/extract-document/<document_id>', methods=['POST'])
def extract_document_text(document_id):
    """
    Extract text from a user-uploaded document
    """
    try:
        # Get document from database
        documents_collection = db['user_documents']
        document = documents_collection.find_one({'_id': ObjectId(document_id)})
        
        if not document:
            return jsonify({
                'success': False,
                'message': 'Document not found'
            }), 404
        
        # Update status to processing
        documents_collection.update_one(
            {'_id': ObjectId(document_id)},
            {'$set': {'status': 'processing'}}
        )
        
        # Get file from GridFS
        from gridfs import GridFSBucket
        bucket = GridFSBucket(db, bucket_name='user_docs')
        
        try:
            file_stream = bucket.open_download_stream(document['fileId'])
            pdf_bytes = file_stream.read()
        except Exception as e:
            logger.error(f"Error reading file from GridFS: {str(e)}")
            documents_collection.update_one(
                {'_id': ObjectId(document_id)},
                {'$set': {'status': 'failed', 'error': 'File not found in storage'}}
            )
            return jsonify({
                'success': False,
                'message': 'File not found in storage'
            }), 404
        
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        
        extracted_text = ""
        page_count = len(pdf_reader.pages)
        
        for page_num in range(page_count):
            page = pdf_reader.pages[page_num]
            extracted_text += page.extract_text() + "\n\n"
        
        # Update document with extracted text
        documents_collection.update_one(
            {'_id': ObjectId(document_id)},
            {
                '$set': {
                    'extractedText': extracted_text.strip(),
                    'pageCount': page_count,
                    'status': 'processed',
                    'processedAt': None  # Will be set by MongoDB
                }
            }
        )
        
        logger.info(f"Successfully extracted text from document {document_id}")
        
        return jsonify({
            'success': True,
            'message': 'Text extracted successfully',
            'data': {
                'pageCount': page_count,
                'textLength': len(extracted_text)
            }
        })
        
    except Exception as e:
        logger.error(f"Error extracting document text: {str(e)}")
        
        # Update status to failed
        try:
            documents_collection.update_one(
                {'_id': ObjectId(document_id)},
                {'$set': {'status': 'failed', 'error': str(e)}}
            )
        except:
            pass
        
        return jsonify({
            'success': False,
            'message': 'Text extraction failed',
            'error': str(e)
        }), 500

@document_bp.route('/process-pending', methods=['POST'])
def process_pending_documents():
    """
    Process all pending documents
    """
    try:
        documents_collection = db['user_documents']
        
        # Find all documents with 'uploaded' status
        pending_docs = documents_collection.find({
            'status': 'uploaded'
        }).limit(100)  # Process 100 at a time
        
        processed = 0
        failed = 0
        
        for doc in pending_docs:
            try:
                # Process this document
                result = extract_document_text(str(doc['_id']))
                if result[1] == 200:  # Success
                    processed += 1
                else:
                    failed += 1
            except Exception as e:
                logger.error(f"Error processing document {doc['_id']}: {str(e)}")
                failed += 1
        
        return jsonify({
            'success': True,
            'message': f'Processed {processed} documents, {failed} failed'
        })
        
    except Exception as e:
        logger.error(f"Error in batch processing: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Batch processing failed',
            'error': str(e)
        }), 500

