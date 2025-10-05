from typing import List, Dict
from collections import defaultdict
from datetime import datetime
from app.services.categorizer import TransactionCategorizer
import logging

logger = logging.getLogger(__name__)


class TransactionAnalyzer:
    def __init__(self):
        self.categorizer = TransactionCategorizer()
    
    def analyze(self, transactions: List[Dict]) -> Dict:
        """
        Analyze transactions to calculate totals and top items
        """
        if not transactions:
            return {
                'total_debits': 0,
                'total_credits': 0,
                'top_expenses': [],
                'top_revenues': [],
                'chart_data': [],
                'spending_by_category': []
            }
        
        total_debits = sum(t.get('debit', 0) for t in transactions)
        total_credits = sum(t.get('credit', 0) for t in transactions)
        
        # Get top expenses (debits)
        debits = [
            {
                'description': t['description'],
                'amount': t['debit'],
                'date': t['date']
            }
            for t in transactions if t.get('debit', 0) > 0
        ]
        top_expenses = sorted(debits, key=lambda x: x['amount'], reverse=True)[:3]
        
        # Get top revenues (credits)
        credits = [
            {
                'description': t['description'],
                'amount': t['credit'],
                'date': t['date']
            }
            for t in transactions if t.get('credit', 0) > 0
        ]
        top_revenues = sorted(credits, key=lambda x: x['amount'], reverse=True)[:3]
        
        # Generate cumulative chart data
        chart_data = self._generate_cumulative_chart_data(transactions)
        
        # Categorize spending
        spending_by_category = self.categorizer.categorize_transactions(transactions)
        
        return {
            'total_debits': round(total_debits, 2),
            'total_credits': round(total_credits, 2),
            'top_expenses': top_expenses,
            'top_revenues': top_revenues,
            'chart_data': chart_data,
            'spending_by_category': spending_by_category
        }
    
    def _generate_cumulative_chart_data(self, transactions: List[Dict]) -> List[Dict]:
        """
        Generate cumulative totals by date for chart visualization
        """
        # Aggregate daily amounts
        daily_data = defaultdict(lambda: {'debits': 0.0, 'credits': 0.0})
        
        for transaction in transactions:
            date = transaction.get('date', '')
            if not date:
                continue
            
            daily_data[date]['debits'] += transaction.get('debit', 0)
            daily_data[date]['credits'] += transaction.get('credit', 0)
        
        # Sort by date
        sorted_dates = sorted(daily_data.keys())
        
        # Calculate cumulative totals
        cumulative_debits = 0.0
        cumulative_credits = 0.0
        chart_data = []
        
        for date in sorted_dates:
            cumulative_debits += daily_data[date]['debits']
            cumulative_credits += daily_data[date]['credits']
            
            chart_data.append({
                'date': date,
                'debits': round(cumulative_debits, 2),
                'credits': round(cumulative_credits, 2)
            })
        
        return chart_data
