import sqlite3
import os
from datetime import datetime

def create_database():
    """Ensure database directory and file exist with proper schema"""
    if not os.path.exists('database'):
        os.makedirs('database')
    
    conn = sqlite3.connect('database/cases.db')
    c = conn.cursor()
    
    # Improved table schema with better constraints
    c.execute('''
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            case_type TEXT NOT NULL CHECK(length(case_type) > 0),
            case_number INTEGER NOT NULL CHECK(case_number > 0),
            filing_year INTEGER NOT NULL CHECK(filing_year BETWEEN 2000 AND 2030),
            petitioner TEXT NOT NULL CHECK(length(petitioner) > 0),
            respondent TEXT NOT NULL CHECK(length(respondent) > 0),
            filing_date TEXT CHECK(filing_date IS NULL OR date(filing_date)),
            next_hearing TEXT CHECK(next_hearing IS NULL OR date(next_hearing)),
            status TEXT,
            judge TEXT,
            latest_order TEXT,
            pdf_link TEXT,
            UNIQUE(case_type, case_number, filing_year)
        )
    ''')
    conn.commit()
    conn.close()

def get_sample_cases():
    """Return a comprehensive list of diverse sample cases"""
    return [
        # Writ Petitions (Civil)
        ('WP(C)', 1234, 2023, 'Environmental Action Group', 'Delhi Govt.', 
         '2023-03-15', '2023-09-10', 'Pending', 'Justice Sharma',
         'Notice issued to respondents', '/orders/WPC1234.pdf'),
        
        ('WP(C)', 4567, 2023, 'Clean Air Initiative', 'Central Pollution Control Board', 
         '2023-04-01', '2023-09-15', 'Pending', 'Justice Singh',
         'CPCB to submit air quality report', '/orders/WPC4567.pdf'),
        
        # Criminal Appeals
        ('CRL.A', 567, 2022, 'State of NCT Delhi', 'Rajesh Kumar @ Monty', 
         '2022-05-20', '2023-08-25', 'Appeal Admitted', 'Justice Verma',
         'Bail granted with ₹50,000 bond', '/orders/CRLA567.pdf'),
         
        ('CRL.A', 1289, 2021, 'State vs. Sanjay Verma', 'Convicted Appellant', 
         '2021-11-15', '2023-09-20', 'Appeal Admitted', 'Justice Reddy',
         'Sentence suspended pending appeal', '/orders/CRLA1289.pdf'),
         
        # Commercial Suits
        ('CS(OS)', 789, 2021, 'M/s ABC Properties Pvt. Ltd.', 'XYZ Developers Ltd.', 
         '2021-01-10', '2023-08-30', 'Part-Heard', 'Justice Kapoor',
         'Interim injunction granted on property', '/orders/CSOS789.pdf'),
         
        ('CS(OS)', 1024, 2022, 'Amazon Seller Services', 'Future Retail Ltd.', 
         '2022-02-28', '2023-08-22', 'Part-Heard', 'Justice Khanna',
         'Arbitration clause upheld', '/orders/CSOS1024.pdf'),
         
        # Arbitration Cases
        ('ARB.P.', 75, 2023, 'National Highways Authority', 'Reliance Infrastructure Ltd.', 
         '2023-03-10', None, 'Arbitrator Appointed', 'Justice (Retd.) A.K. Sikri',
         'Tribunal formation ordered', '/orders/ARBP75.pdf'),
         
        # Testamentary Cases
        ('TEST.CAS.', 12, 2022, 'Ms. Priya Malhotra', 'Mr. Vikram Malhotra', 
         '2022-08-05', None, 'Probate Granted', 'Justice Oberoi',
         'Will validated after objections', '/orders/TESTCAS12.pdf'),
         
        # Tax Appeals
        ('ITA', 330, 2022, 'Commissioner of Income Tax', 'M/s Sunrise Enterprises', 
         '2022-07-15', '2023-10-05', 'Pending', 'Justice Gupta',
         'Stay granted on tax demand', '/orders/ITA330.pdf'),
         
        # Service Matters
        ('W.P.(C)', 7890, 2023, 'Delhi Police Constable Union', 'GNCTD', 
         '2023-05-20', '2023-11-15', 'Pending', 'Justice Malhotra',
         'Notice issued on promotion policy', '/orders/WPC7890.pdf'),
        
        # Additional cases to ensure variety
        ('FAO', 221, 2021, 'DDA', 'Landowners Association', 
         '2021-04-12', '2023-09-18', 'Pending', 'Justice Kohli',
         'Compensation enhanced by 20%', '/orders/FAO221.pdf'),
         
        ('CO.PET.', 45, 2023, 'M/s XYZ Traders', 'Creditors Committee', 
         '2023-02-15', '2023-10-30', 'Under Consideration', 'Justice Joshi',
         'Interim moratorium granted', '/orders/COPET45.pdf')
    ]

def add_sample_cases():
    """Add sample cases to database with duplicate prevention and validation"""
    conn = None
    try:
        conn = sqlite3.connect('database/cases.db')
        c = conn.cursor()
        
        # First verify table structure
        c.execute("PRAGMA table_info(cases)")
        columns = [col[1] for col in c.fetchall()]
        if not columns:
            raise sqlite3.Error("Cases table does not exist")
        
        # Get existing cases to avoid duplicates
        c.execute("SELECT case_type, case_number, filing_year FROM cases")
        existing_cases = set(c.fetchall())
        
        cases_to_add = [
            case for case in get_sample_cases()
            if (case[0], case[1], case[2]) not in existing_cases
        ]
        
        if cases_to_add:
            c.executemany('''
                INSERT INTO cases 
                (case_type, case_number, filing_year, petitioner, respondent,
                 filing_date, next_hearing, status, judge, latest_order, pdf_link)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', cases_to_add)
            
            print(f"✅ Added {len(cases_to_add)} new cases at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"📊 Database now contains {len(existing_cases) + len(cases_to_add)} total cases")
        else:
            print(f"ℹ️ All sample cases already exist in database ({len(existing_cases)} cases)")
        
        conn.commit()
        
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def verify_database_integrity():
    """Verify that database contains expected data"""
    try:
        conn = sqlite3.connect('database/cases.db')
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM cases")
        count = c.fetchone()[0]
        
        c.execute('''
            SELECT case_type, COUNT(*) 
            FROM cases 
            GROUP BY case_type 
            ORDER BY COUNT(*) DESC
        ''')
        type_distribution = c.fetchall()
        
        print(f"🔍 Database verification:")
        print(f"Total cases: {count}")
        print("Case type distribution:")
        for case_type, type_count in type_distribution:
            print(f"- {case_type}: {type_count}")
            
    except sqlite3.Error as e:
        print(f"Verification failed: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_database()
    add_sample_cases()
    verify_database_integrity()