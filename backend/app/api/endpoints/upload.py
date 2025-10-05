from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.services.pdf_parser import PDFParser
from app.services.transaction_analyzer import TransactionAnalyzer
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

pdf_parser = PDFParser()
analyzer = TransactionAnalyzer()


@router.post("/analyze")
async def analyze_statements(files: List[UploadFile] = File(...)):
    """
    Upload and analyze one or more bank statement PDFs
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(files) > 10:
        raise HTTPException(
            status_code=400, 
            detail="Maximum 10 files allowed per request"
        )
    
    file_results = []
    
    try:
        for file in files:
            if not file.filename.endswith('.pdf'):
                logger.warning(f"Skipping non-PDF file: {file.filename}")
                continue
            
            content = await file.read()
            
            if len(content) > 20 * 1024 * 1024:
                raise HTTPException(
                    status_code=400,
                    detail=f"File {file.filename} exceeds 20MB limit"
                )
            
            logger.info(f"Processing file: {file.filename}")
            
            # Parse PDF
            transactions = await pdf_parser.parse_pdf(content, file.filename)
            
            if not transactions:
                logger.warning(f"No transactions found in {file.filename}")
                continue
            
            # Analyze transactions
            analysis = analyzer.analyze(transactions)
            
            file_results.append({
                'file_name': file.filename,
                'transaction_count': len(transactions),
                'total_debits': analysis['total_debits'],
                'total_credits': analysis['total_credits'],
                'top_expenses': analysis['top_expenses'],
                'top_revenues': analysis['top_revenues'],
                'chart_data': analysis['chart_data'],
                'spending_by_category': analysis['spending_by_category']
            })
        
        if not file_results:
            raise HTTPException(
                status_code=400,
                detail="No valid transactions found in uploaded files"
            )
        
        logger.info(f"Successfully processed {len(file_results)} files")
        
        return {
            'message': 'Analysis complete',
            'files_processed': len(file_results),
            'results': file_results
        }
    
    except Exception as e:
        logger.error(f"Error processing files: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
