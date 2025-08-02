from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import os
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Database Configuration
DATABASE_PATH = 'database/cases.db'

def get_db_connection():
    """Create and return a database connection"""
    if not os.path.exists('database'):
        os.makedirs('database')
    return sqlite3.connect(DATABASE_PATH)

def init_db():
    """Initialize the database with schema and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create cases table with proper schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL,
            case_number INTEGER NOT NULL,
            filing_year INTEGER NOT NULL,
            petitioner TEXT NOT NULL,
            respondent TEXT NOT NULL,
            filing_date TEXT,
            next_hearing TEXT,
            status TEXT,
            judge TEXT,
            latest_order TEXT,
            pdf_link TEXT,
            UNIQUE(case_type, case_number, filing_year)
        )
    ''')
    
    # Insert sample data only if table is empty
    cursor.execute("SELECT COUNT(*) FROM cases")
    if cursor.fetchone()[0] == 0:
        sample_cases = [
            ('WP(C)', 1234, 2023, 'Environmental Action Group', 'Delhi Govt.', 
             '2023-03-15', '2023-09-10', 'Pending', 'Justice Sharma',
             'Notice issued to respondents', '/orders/WPC1234.pdf'),
            ('CRL.A', 567, 2022, 'State of Delhi', 'Rajesh Kumar', 
             '2022-05-20', '2023-08-25', 'Appeal Admitted', 'Justice Verma',
             'Bail granted with conditions', '/orders/CRLA567.pdf'),
            ('CS(OS)', 789, 2021, 'M/S ABC Properties', 'XYZ Developers', 
             '2021-01-10', '2023-08-30', 'Part-Heard', 'Justice Kapoor',
             'Interim injunction granted', '/orders/CSOS789.pdf'),
            ('TEST.CAS.', 12, 2022, 'Priya Malhotra', 'Vikram Malhotra',
             '2022-08-05', None, 'Probate Granted', 'Justice Oberoi',
             'Will validated', '/orders/TESTCAS12.pdf')
        ]
        
        cursor.executemany('''
            INSERT OR IGNORE INTO cases 
            (case_type, case_number, filing_year, petitioner, respondent,
             filing_date, next_hearing, status, judge, latest_order, pdf_link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_cases)
        print("Sample cases inserted into database")
    
    conn.commit()
    conn.close()

# Routes
@app.route('/')
def index():
    """Render the main search page"""
    return render_template('index.html')

@app.route('/search_case', methods=['POST'])
def search_case():
    """Handle case search requests"""
    try:
        # Get form data
        case_type = request.form.get('case_type')
        case_number = request.form.get('case_number')
        filing_year = request.form.get('filing_year')

        # Validate inputs
        if not all([case_type, case_number, filing_year]):
            return jsonify({'status': 'error', 'message': 'Missing required fields'})

        # Query database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM cases 
            WHERE case_type = ? AND case_number = ? AND filing_year = ?
        ''', (case_type, case_number, filing_year))
        
        case = cursor.fetchone()
        conn.close()

        if not case:
            return jsonify({
                'status': 'error', 
                'message': 'Case not found in database'
            })

        # Format the response data
        response_data = {
            'case_type': case[1],
            'case_number': case[2],
            'filing_year': case[3],
            'case_title': f"{case[1]} {case[2]}/{case[3]}",
            'petitioner': case[4],
            'respondent': case[5],
            'filing_date': format_date(case[6]),
            'next_hearing': format_date(case[7]),
            'status': case[8],
            'judge': case[9],
            'latest_order': case[10],
            'pdf_link': case[11],
            'orders': [{
                'date': format_date(case[6]),
                'description': case[10],
                'pdf_link': case[11]
            }]
        }

        return jsonify({
            'status': 'success',
            'data': response_data
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Internal server error',
            'detail': str(e)
        })

def format_date(date_str):
    """Format YYYY-MM-DD date to DD Month YYYY"""
    if not date_str:
        return "Not scheduled"
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.strftime('%d %B %Y')
    except ValueError:
        return date_str  # Return as-is if not in expected format

# Initialize the database when starting the app
init_db()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Proxy to Node.js backend
@app.route('/api/cases/search')
def search_case():
    response = requests.get(
        'http://localhost:5000/api/cases/search',
        params=request.args
    )
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=3000)