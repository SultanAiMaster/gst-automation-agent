# GST Return Automation Agent

**The Ultimate GST Automation Tool for Indian Businesses**

---

## 🎯 Overview

Automation agent that simplifies GST return filing for every GSTIN holder in India. Calculate taxes, generate GSTR-1/3B, manage invoices, and file returns automatically.

---

## ✨ Features

### Core Features
- ✅ GSTIN Validation
- ✅ Multi-GSTIN Support
- ✅ Invoice Generation (PDF)
- ✅ GST Calculation (CGST, SGST, IGST)
- ✅ GSTR-1 Auto-Generation
- ✅ GSTR-3B Auto-Calculation
- ✅ ITC Tracking & Reconciliation
- ✅ Filing Deadline Reminders
- ✅ Compliance Dashboard
- ✅ JSON Export for GST Portal

### Advanced Features
- ✅ Invoice Upload (PDF/Image to Data)
- ✅ HSN Code Auto-Detection
- ✅ Reverse Charge Mechanism
- ✅ Tax Liability Summary
- ✅ Sales & Purchase Reports
- ✅ Multi-User Access (CA Suite)
- ✅ API for Integration

---

## 💻 Tech Stack

**Backend:**
- Python 3.10+
- Flask/FastAPI (Web Server)
- Pandas (Data Processing)
- ReportLab (PDF Generation)
- SQLAlchemy (Database ORM)
- PostgreSQL (Database)

**Frontend:**
- HTML5/CSS3/JavaScript
- Bootstrap 5 (Responsive UI)
- Chart.js (Analytics Dashboard)
- SweetAlert2 (Notifications)

**Utilities:**
- PyPDF2 (PDF Processing)
- Pillow (Image Processing)
- Schedule (Cron Jobs)
- Celery (Background Tasks)

---

## 🔧 Installation

```bash
# Clone repository
git clone https://github.com/SultanAiMaster/gst-automation-agent.git
cd gst-automation-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python setup_db.py

# Run server
python app.py
```

---

## 📖 Usage

### Basic Workflow

1. **Register Your Business:**
   - Add GSTIN
   - Configure business details

2. **Manage Invoices:**
   - Create sales invoices
   - Upload purchase invoices
   - Auto-calculate GST

3. **Generate Reports:**
   - GSTR-1 report
   - GSTR-3B calculation
   - Download JSON for filing

4. **Track Compliance:**
   - View dashboard
   - Check deadlines
   - Monitor tax liability

---

## 📊 GST Calculation Logic

### GST Rates
- **0%:** Essential goods
- **5%:** Some food items
- **12%:** Standard items
- **18%:** Most goods & services
- **28%:** Luxury goods

### Inter-State vs Intra-State
- **Intra-State (Same State):** CGST + SGST (GST/2 each)
- **Inter-State (Different State):** IGST (Full GST)

### Example Calculation:
```
Invoice Amount: ₹10,000
GST Rate: 18%
Tax Amount: ₹10,000 × 18% = ₹1,800

Intra-State:
  CGST: ₹900
  SGST: ₹900

Inter-State:
  IGST: ₹1,800
```

---

## 📄 Report Types

### GSTR-1
- Summary of outward supplies
- Taxable sales & purchases
- Tax collected on sales
- B2B, B2C, and export details

### GSTR-3B
- Summary of tax liability
- Input tax credit (ITC)
- Net tax payable
- Quarterly/Annual filing

### GSTR-9
- Annual return summary
- Consolidated data from all returns
- Required for all registered businesses

---

## 🎨 Dashboard Features

- **Overview Cards:**
  - Total Sales
  - Total Purchases
  - Tax Liability
  - ITC Available

- **Charts:**
  - Monthly Sales Trend
  - Tax Payment History
  - Top Products (by Revenue)
  - State-wise Distribution

- **Quick Actions:**
  - Create Invoice
  - Generate Report
  - Upload Invoice
  - Export Data

---

## 🔐 Security

- Data encrypted at rest
- Secure authentication
- Role-based access control
- API rate limiting
- GDPR compliant

---

## 📞 Support

- **Email:** workchainofficial@gmail.com
- **Phone:** +91 86385 56847
- **Custom Development:** Available

---

## 💰 Pricing

**Personal:** ₹999/Lifetime
- Single GSTIN
- Basic Reports
- Invoice Generation

**Professional:** ₹1999/Lifetime
- 5 GSTINs
- All Reports
- Dashboard & Analytics
- Priority Support

**Enterprise:** ₹4999/Lifetime
- Unlimited GSTINs
- API Access
- CA Suite
- White-label Option

---

## 📝 License

MIT License - Free to use, modify, and distribute

---

**Note:** This is a GST compliance tool, not a legal advisor. Consult a Chartered Accountant for complex tax matters.

---

*Building intelligent systems that work while you sleep* 🤖
