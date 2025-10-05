from typing import List, Dict
from collections import defaultdict
import re
import logging

logger = logging.getLogger(__name__)


class TransactionCategorizer:
    def categorize_transactions(self, transactions: List[Dict]) -> Dict:
        """
        Categorize transactions by type and merchant
        """
        categories = defaultdict(lambda: {'total': 0.0, 'merchants': defaultdict(float), 'count': 0})
        
        for transaction in transactions:
            if transaction.get('debit', 0) == 0:
                continue
            
            description = transaction.get('description', '')
            amount = transaction.get('debit', 0)
            
            # Log the description for debugging
            logger.debug(f"Processing: {description[:100]}")
            
            category = self._determine_category(description)
            merchant = self._extract_merchant(description, category)
            
            logger.debug(f"Category: {category}, Merchant: {merchant}")
            
            categories[category]['total'] += amount
            categories[category]['merchants'][merchant] += amount
            categories[category]['count'] += 1
        
        result = []
        for category_name, data in categories.items():
            top_merchants = sorted(
                [{'name': merchant, 'amount': amount} 
                 for merchant, amount in data['merchants'].items()],
                key=lambda x: x['amount'],
                reverse=True
            )[:5]
            
            result.append({
                'category': category_name,
                'total_amount': round(data['total'], 2),
                'transaction_count': data['count'],
                'top_merchants': top_merchants
            })
        
        result.sort(key=lambda x: x['total_amount'], reverse=True)
        return result[:5]
    
    def _determine_category(self, description: str) -> str:
        """Determine transaction category"""
        desc_lower = description.lower()
        
        if 'kartenzahlung' in desc_lower:
            return 'Card Payments (Kartenzahlung)'
        elif 'lastschrift' in desc_lower:
            return 'Direct Debit (SEPA Lastschrift)'
        elif 'überweisung' in desc_lower:
            return 'Bank Transfer (SEPA Überweisung)'
        else:
            return 'Other Transactions'
    
    def _extract_merchant(self, description: str, category: str) -> str:
        """Extract merchant name from description"""
        
        if 'Kartenzahlung' not in category:
            # For non-card payments, extract company name
            for company in ['Klarna', 'Netflix', 'Badenova', 'Zurich', 'OTTO', 'HTW', 'Bundesagentur']:
                if company.lower() in description.lower():
                    return company
            return description.split()[0] if description else 'Unknown'
        
        # For card payments, look for merchant patterns
        desc_upper = description.upper()
        
        # Check for known merchants
        merchants = {
            'LIDL': 'LIDL',
            'KAUFLAND': 'Kaufland',
            'DM ': 'DM Drogerie',
            'EDEKA': 'EDEKA',
            'REWE': 'REWE',
            'ALDI': 'ALDI',
            'ARIANA': 'Ariana Orient House',
            'KANNA': "Kanna's Asia Shop",
            'WOOLWORTH': 'Woolworth',
            'DEICHMANN': 'Deichmann',
            'BASAK': 'Basak Döner',
        }
        
        for key, name in merchants.items():
            if key in desc_upper:
                return name
        
        # Try to extract first word after common prefixes
        patterns = [
            r'Kartenzahlung\s+Verwendungszweck/Kundenreferenz\s+([A-Z][A-Za-z0-9\s-]+?)(?://|/|\s+\d)',
            r'Verwendungszweck/Kundenreferenz\s+([A-Z][A-Za-z0-9\s-]+?)(?://|/|\s+\d)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, description)
            if match:
                merchant_name = match.group(1).strip()
                # Take first word
                first_word = merchant_name.split()[0]
                return first_word
        
        # Fallback
        return 'Other Merchant'
