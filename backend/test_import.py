try:
    from app.services.categorizer import TransactionCategorizer
    from app.services.transaction_analyzer import TransactionAnalyzer
    print("Import successful!")
    analyzer = TransactionAnalyzer()
    print("TransactionAnalyzer created successfully!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
