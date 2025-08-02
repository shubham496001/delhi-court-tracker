

# Delhi High Court Case Tracker System  



![Delhi High Court Logo](static/images/dhc-logo.png)  
*Digital Case Management Platform with Automated Data Fetching & Analytics*

---

## 🌟 Key Features
- **Smart Case Search** (Type/Number/Year/Petitioner)
- **Real-time Data Sync** with NJDG
- **Interactive Dashboard**
- **Role-Based Access** (Judges/Lawyers/Clerks)

🔗 **Live Website**: [https://delhi-court-tracker.onrender.com]

---

## 📂 Project Structure
```
delhi-court-tracker/
├── backend/               # Node.js API
├── static/               # CSS/JS/Images
├── templates/            # Flask HTML
├── app.py                # Main app
└── requirements.txt      # Python deps
```

---

## 🔍 Common Case Types
| Type  | Full Name               | Example        |
|-------|-------------------------|----------------|
| CRL   | Criminal Appeal         | CRL 789/2022   | 
| WP(C) | Writ Petition (Civil)   | WP(C) 101/2023 |
| ARB   | Arbitration             | ARB 12/2021    |
| CIV   | Civil Suit              | CIV 2056/2020  |
| TAX   | Tax Appeal              | TAX 45/2023    |

---

## 🚀 Quick Start
```bash
# 1. Clone repo
git clone https://github.com/shubham496001/delhi-court-tracker.git

# 2. Install dependencies
pip install -r requirements.txt
npm install --prefix backend

# 3. Configure .env
echo "MONGODB_URI=your_connection_string" > .env

# 4. Run
python app.py & cd backend && node app.js
```

---

## 💻 Usage Examples
### Search Criminal Case
```python
import requests

response = requests.post(
    "https://delhi-court-tracker.onrender.com/search",
    json={"case_type": "CRL", "number": 789, "year": 2022}
)
print(response.json())
```

### Expected Output
```json
{
  "case": "CRL 789/2022",
  "parties": ["State vs. Sharma"],
  "next_hearing": "2023-11-15",
  "status": "Pending"
}
```

---

## 📊 Dashboard Preview
- **Real-time Case Tracking**
- **Hearing Date Calendar**  
- **Judge Performance Metrics**

---

## 📬 Contact
**Shubham Namdeo**  
[shubhamnamdeojso4157@gmail.com](shubhamnamdeojso4157@gmail.com)  
[GitHub Repository](https://github.com/shubham496001/delhi-court-tracker)

---

This version:
✅ Highlights live website link upfront  
✅ Provides clear case type examples  
✅ Includes ready-to-run code snippets  
✅ Maintains professional structure  
