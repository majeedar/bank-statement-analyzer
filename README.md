# Bank Statement Analyzer

A modern web application for analyzing bank statements with automatic transaction categorization, merchant extraction, and visual spending insights.

![Screenshot](https://via.placeholder.com/800x400?text=Bank+Statement+Analyzer)

## Features

- 📄 **PDF Upload & Parsing** - Drag-and-drop German Postbank PDF statements
- 🔍 **Transaction Extraction** - Automatic parsing of dates, amounts, and descriptions
- 📊 **Smart Categorization** - Groups transactions by type (Card Payments, Direct Debit, Bank Transfers)
- 🏪 **Merchant Recognition** - Identifies and aggregates spending by store/vendor
- 📈 **Visual Analytics** - Cumulative line charts showing debits and credits over time
- 💡 **Spending Insights** - Top 3 expenses, top 3 revenues, and top 5 merchants per category

## Quick Start

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker (optional)

### Installation

1. Clone repository
```bash
git clone https://github.com/majeedar/bank-statement-analyzer.git
cd bank-statement-analyzer
2. Start backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

3 Start frontend (new terminal)
cd frontend
npm install
npm run dev

4. Open http://localhost:5173

Usage

Drag and drop a PDF bank statement
Wait for analysis
View spending insights and charts

Tech Stack
Frontend: React, TypeScript, Vite, Tailwind CSS, Recharts
Backend: FastAPI, Python, pdfplumber
Infrastructure: Docker, PostgreSQL, Redis
API Documentation
Swagger UI: http://localhost:8000/docs
Contributing
Contributions welcome! Please open an issue or submit a PR.
License
MIT License - see LICENSE file
Author
Majeed Abdul-Razak (@majeedar)
