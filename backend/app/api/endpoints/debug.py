from fastapi import APIRouter, UploadFile, File
import pdfplumber
import io

router = APIRouter()

@router.post("/debug-pdf")
async def debug_pdf(file: UploadFile = File(...)):
    """Debug endpoint to see what's in the PDF"""
    content = await file.read()
    
    result = {
        'filename': file.filename,
        'pages': []
    }
    
    with pdfplumber.open(io.BytesIO(content)) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables()
            text = page.extract_text()
            
            page_info = {
                'page_number': page_num,
                'table_count': len(tables),
                'text_preview': text[:1000] if text else None,  # First 1000 chars
                'tables': []
            }
            
            for table_idx, table in enumerate(tables):
                if table:
                    page_info['tables'].append({
                        'table_index': table_idx,
                        'row_count': len(table),
                        'first_5_rows': table[:5]
                    })
            
            result['pages'].append(page_info)
    
    return result
