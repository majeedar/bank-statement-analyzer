import pdfplumber
import io
import re
from datetime import datetime
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)


class PDFParser:
    async def parse_pdf(self, content: bytes, filename: str) -> List[Dict]:
        transactions = []
        
        try:
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text()
                    if not text:
                        continue
                    
                    page_transactions = self._parse_text(text)
                    transactions.extend(page_transactions)
            
            logger.info(f"Extracted {len(transactions)} transactions from {filename}")
            return transactions
        
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}", exc_info=True)
            raise
    
    def _parse_text(self, text: str) -> List[Dict]:
        """Parse transactions from German Postbank statement text"""
        transactions = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for date pattern: "01.07. 01.07."
            date_match = re.match(r'^(\d{2}\.\d{2}\.) (\d{2}\.\d{2}\.) (.+)$', line)
            
            if date_match:
                buchung = date_match.group(1)
                valuta = date_match.group(2)
                rest_of_line = date_match.group(3)
                
                # Next line should have the year
                if i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    year_match = re.match(r'^(\d{4}) (\d{4}) (.*)$', next_line)
                    
                    if year_match:
                        year = year_match.group(1)
                        
                        # Build full description including all following lines until next transaction
                        description_parts = [rest_of_line]
                        if year_match.group(3):
                            description_parts.append(year_match.group(3))
                        
                        # Read ahead to capture multi-line descriptions
                        j = i + 2
                        while j < len(lines) and not re.match(r'^\d{2}\.\d{2}\. \d{2}\.\d{2}\.', lines[j]):
                            extra_line = lines[j].strip()
                            if extra_line and not extra_line.startswith('Auszug'):
                                description_parts.append(extra_line)
                            j += 1
                            if j - i > 10:  # Limit lookahead
                                break
                        
                        # Join all description parts
                        full_description = ' '.join(description_parts)
                        
                        # Parse amount from the first line (rest_of_line)
                        amount_match = re.search(r'([+-]?)(\d{1,3}(?:\.\d{3})*,\d{2})', rest_of_line)
                        debit = 0.0
                        credit = 0.0
                        
                        if amount_match:
                            sign = amount_match.group(1)
                            amount_str = amount_match.group(2)
                            amount_str = amount_str.replace('.', '').replace(',', '.')
                            amount = float(amount_str)
                            
                            if sign == '-':
                                debit = amount
                            elif sign == '+':
                                credit = amount
                            else:
                                debit = amount
                            
                            # Remove amount from description
                            full_description = re.sub(r'[+-]?\d{1,3}(?:\.\d{3})*,\d{2}', '', full_description).strip()
                        
                        date_str = f"{year}-{buchung[3:5]}-{buchung[0:2]}"
                        
                        if full_description and (debit > 0 or credit > 0):
                            logger.debug(f"Parsed transaction: {full_description[:80]}")
                            transactions.append({
                                'date': date_str,
                                'description': full_description,
                                'debit': debit,
                                'credit': credit,
                                'balance': 0.0
                            })
                        
                        i = j
                        continue
            
            i += 1
        
        return transactions


pdf_parser = PDFParser()
