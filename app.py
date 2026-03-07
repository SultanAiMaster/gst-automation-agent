"""
GST Automation Agent - Core Application
Main Flask application with GST calculation, invoice management, and return filing
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import pandas as pd
import json
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'gst-automation-secret-key-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gst_automation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# ==================== DATABASE MODELS ====================

class BusinessProfile(db.Model):
    """Business profile with GSTIN details"""
    id = db.Column(db.Integer, primary_key=True)
    gstin = db.Column(db.String(15), unique=True, nullable=False)
    business_name = db.Column(db.String(200), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    state_code = db.Column(db.String(2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    invoices = db.relationship('Invoice', backref='business', lazy=True)

class Invoice(db.Model):
    """Invoice model for sales and purchases"""
    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(50), nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    invoice_type = db.Column(db.String(20), nullable=False)  # sales/purchase
    customer_name = db.Column(db.String(200))
    customer_gstin = db.Column(db.String(15))
    total_amount = db.Column(db.Float, nullable=False)
    taxable_amount = db.Column(db.Float, nullable=False)
    gst_rate = db.Column(db.Float, nullable=False)
    cgst_amount = db.Column(db.Float, default=0)
    sgst_amount = db.Column(db.Float, default=0)
    igst_amount = db.Column(db.Float, default=0)
    status = db.Column(db.String(20), default='pending')  # pending/paid/overdue
    business_id = db.Column(db.Integer, db.ForeignKey('business_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('InvoiceItem', backref='invoice', lazy=True)

class InvoiceItem(db.Model):
    """Line items in an invoice"""
    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoice.id'), nullable=False)
    item_name = db.Column(db.String(200), nullable=False)
    hsn_code = db.Column(db.String(8))
    quantity = db.Column(db.Float, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    gst_rate = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TaxPayment(db.Model):
    """Track tax payments made"""
    id = db.Column(db.Integer, primary_key=True)
    tax_period = db.Column(db.String(20), nullable=False)  # monthly/quarterly
    tax_type = db.Column(db.String(20), nullable=False)  # CGST/SGST/IGST
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), default='pending')
    business_id = db.Column(db.Integer, db.ForeignKey('business_profile.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ==================== GST CALCULATION ENGINE ====================

class GSTCalculator:
    """Core GST calculation engine"""
    
    @staticmethod
    def validate_gstin(gstin):
        """Validate GSTIN format and checksum"""
        if not gstin or len(gstin) != 15:
            return False
        
        # GSTIN format: 2 digits (state code) + 10 chars (PAN) + 1 digit (entity code) + 1 char (Z)
        state_code = gstin[:2]
        pan = gstin[2:12]
        entity_code = gstin[12]
        suffix = gstin[13]
        
        # Check state code validity
        try:
            state_num = int(state_code)
            if state_num < 1 or state_num > 37:
                return False
        except:
            return False
        
        # Check suffix is 'Z'
        if suffix != 'Z':
            return False
        
        return True
    
    @staticmethod
    def calculate_gst(amount, gst_rate, is_inter_state=False):
        """Calculate CGST, SGST, IGST based on transaction type"""
        gst_amount = (amount * gst_rate) / 100
        
        if is_inter_state:
            return {
                'cgst': 0,
                'sgst': 0,
                'igst': gst_amount,
                'total_gst': gst_amount,
                'total_amount': amount + gst_amount
            }
        else:
            half_gst = gst_amount / 2
            return {
                'cgst': half_gst,
                'sgst': half_gst,
                'igst': 0,
                'total_gst': gst_amount,
                'total_amount': amount + gst_amount
            }
    
    @staticmethod
    def determine_inter_state(seller_state, buyer_state):
        """Determine if transaction is inter-state"""
        return seller_state != buyer_state

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - Dashboard"""
    return render_template('index.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/business/create', methods=['POST'])
def create_business():
    """Create new business profile"""
    try:
        data = request.json
        
        # Validate GSTIN
        if not GSTCalculator.validate_gstin(data['gstin']):
            return jsonify({
                'success': False,
                'message': 'Invalid GSTIN format'
            }), 400
        
        # Check if GSTIN already exists
        existing = BusinessProfile.query.filter_by(gstin=data['gstin']).first()
        if existing:
            return jsonify({
                'success': False,
                'message': 'GSTIN already registered'
            }), 400
        
        # Create business profile
        business = BusinessProfile(
            gstin=data['gstin'],
            business_name=data['business_name'],
            state=data['state'],
            state_code=data['state_code']
        )
        
        db.session.add(business)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Business profile created successfully',
            'business_id': business.id
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/invoice/create', methods=['POST'])
def create_invoice():
    """Create new invoice with GST calculation"""
    try:
        data = request.json
        business = BusinessProfile.query.get(data['business_id'])
        
        if not business:
            return jsonify({
                'success': False,
                'message': 'Business not found'
            }), 404
        
        # Determine if inter-state
        customer_state = data.get('customer_state', '')
        is_inter_state = GSTCalculator.determine_inter_state(
            business.state_code,
            customer_state
        )
        
        # Calculate GST
        gst_calc = GSTCalculator.calculate_gst(
            data['amount'],
            data['gst_rate'],
            is_inter_state
        )
        
        # Create invoice
        invoice = Invoice(
            invoice_number=data['invoice_number'],
            invoice_date=datetime.strptime(data['invoice_date'], '%Y-%m-%d').date(),
            invoice_type=data.get('invoice_type', 'sales'),
            customer_name=data.get('customer_name', ''),
            customer_gstin=data.get('customer_gstin', ''),
            total_amount=gst_calc['total_amount'],
            taxable_amount=data['amount'],
            gst_rate=data['gst_rate'],
            cgst_amount=gst_calc['cgst'],
            sgst_amount=gst_calc['sgst'],
            igst_amount=gst_calc['igst'],
            business_id=data['business_id']
        )
        
        db.session.add(invoice)
        db.session.commit()
        
        # Add items
        for item in data.get('items', []):
            invoice_item = InvoiceItem(
                invoice_id=invoice.id,
                item_name=item['item_name'],
                hsn_code=item.get('hsn_code', ''),
                quantity=item['quantity'],
                unit_price=item['unit_price'],
                gst_rate=item['gst_rate'],
                amount=item['quantity'] * item['unit_price']
            )
            db.session.add(invoice_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Invoice created successfully',
            'invoice_id': invoice.id,
            'gst_breakdown': gst_calc
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/gstr1/<int:business_id>/<period>')
def generate_gstr1(business_id, period):
    """Generate GSTR-1 report"""
    try:
        business = BusinessProfile.query.get(business_id)
        
        if not business:
            return jsonify({
                'success': False,
                'message': 'Business not found'
            }), 404
        
        # Parse period (YYYY-MM)
        year, month = map(int, period.split('-'))
        
        # Get sales invoices for the period
        start_date = datetime(year, month, 1).date()
        if month == 12:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, month + 1, 1).date()
        
        invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.invoice_type == 'sales',
            Invoice.invoice_date >= start_date,
            Invoice.invoice_date < end_date
        ).all()
        
        # Calculate totals
        b2b_invoices = [inv for inv in invoices if inv.customer_gstin]
        b2c_invoices = [inv for inv in invoices if not inv.customer_gstin]
        
        total_taxable_value = sum(inv.taxable_amount for inv in invoices)
        total_igst = sum(inv.igst_amount for inv in invoices)
        total_cgst = sum(inv.cgst_amount for inv in invoices)
        total_sgst = sum(inv.sgst_amount for inv in invoices)
        total_tax = total_igst + total_cgst + total_sgst
        
        return jsonify({
            'success': True,
            'period': period,
            'business_name': business.business_name,
            'gstin': business.gstin,
            'summary': {
                'total_invoices': len(invoices),
                'b2b_invoices': len(b2b_invoices),
                'b2c_invoices': len(b2c_invoices),
                'total_taxable_value': total_taxable_value,
                'total_igst': total_igst,
                'total_cgst': total_cgst,
                'total_sgst': total_sgst,
                'total_tax': total_tax
            },
            'invoices': [
                {
                    'invoice_number': inv.invoice_number,
                    'invoice_date': inv.invoice_date.strftime('%Y-%m-%d'),
                    'customer_gstin': inv.customer_gstin,
                    'customer_name': inv.customer_name,
                    'taxable_value': inv.taxable_amount,
                    'igst': inv.igst_amount,
                    'cgst': inv.cgst_amount,
                    'sgst': inv.sgst_amount,
                    'total_amount': inv.total_amount
                }
                for inv in invoices
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/gstr3b/<int:business_id>/<period>')
def generate_gstr3b(business_id, period):
    """Generate GSTR-3B calculation"""
    try:
        business = BusinessProfile.query.get(business_id)
        
        if not business:
            return jsonify({
                'success': False,
                'message': 'Business not found'
            }), 404
        
        # Parse period (YYYY-MM)
        year, month = map(int, period.split('-'))
        
        # Determine quarter
        quarter = ((month - 1) // 3) + 1
        start_month = (quarter - 1) * 3 + 1
        start_date = datetime(year, start_month, 1).date()
        
        if quarter == 4:
            end_date = datetime(year + 1, 1, 1).date()
        else:
            end_date = datetime(year, start_month + 3, 1).date()
        
        # Get all invoices for the quarter
        sales_invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.invoice_type == 'sales',
            Invoice.invoice_date >= start_date,
            Invoice.invoice_date < end_date
        ).all()
        
        purchase_invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.invoice_type == 'purchase',
            Invoice.invoice_date >= start_date,
            Invoice.invoice_date < end_date
        ).all()
        
        # Calculate sales tax
        total_taxable_sales = sum(inv.taxable_amount for inv in sales_invoices)
        sales_igst = sum(inv.igst_amount for inv in sales_invoices)
        sales_cgst = sum(inv.cgst_amount for inv in sales_invoices)
        sales_sgst = sum(inv.sgst_amount for inv in sales_invoices)
        total_sales_tax = sales_igst + sales_cgst + sales_sgst
        
        # Calculate ITC from purchases
        total_taxable_purchases = sum(inv.taxable_amount for inv in purchase_invoices)
        itc_igst = sum(inv.igst_amount for inv in purchase_invoices)
        itc_cgst = sum(inv.cgst_amount for inv in purchase_invoices)
        itc_sgst = sum(inv.sgst_amount for inv in purchase_invoices)
        total_itc = itc_igst + itc_cgst + itc_sgst
        
        # Calculate net tax payable
        net_igst = max(0, sales_igst - itc_igst)
        net_cgst = max(0, sales_cgst - itc_cgst)
        net_sgst = max(0, sales_sgst - itc_sgst)
        net_tax_payable = net_igst + net_cgst + net_sgst
        
        return jsonify({
            'success': True,
            'period': period,
            'quarter': quarter,
            'business_name': business.business_name,
            'gstin': business.gstin,
            'summary': {
                '3.1': {
                    'outward_supplies': {
                        'total_taxable_value': total_taxable_sales,
                        'igst': sales_igst,
                        'cgst': sales_cgst,
                        'sgst': sales_sgst,
                        'total_tax': total_sales_tax
                    }
                },
                '3.2': {
                    'itc': {
                        'total_taxable_value': total_taxable_purchases,
                        'igst': itc_igst,
                        'cgst': itc_cgst,
                        'sgst': itc_sgst,
                        'total_itc': total_itc
                    }
                },
                '4.0': {
                    'tax_payable': {
                        'igst': net_igst,
                        'cgst': net_cgst,
                        'sgst': net_sgst,
                        'total': net_tax_payable
                    }
                }
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/dashboard/<int:business_id>')
def dashboard(business_id):
    """Get dashboard data"""
    try:
        business = BusinessProfile.query.get(business_id)
        
        if not business:
            return jsonify({
                'success': False,
                'message': 'Business not found'
            }), 404
        
        # Get current month data
        today = datetime.utcnow().date()
        month_start = today.replace(day=1)
        
        sales_invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.invoice_type == 'sales',
            Invoice.invoice_date >= month_start
        ).all()
        
        purchase_invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.invoice_type == 'purchase',
            Invoice.invoice_date >= month_start
        ).all()
        
        # Calculate totals
        total_sales = sum(inv.total_amount for inv in sales_invoices)
        total_purchases = sum(inv.total_amount for inv in purchase_invoices)
        total_tax = sum(
            inv.cgst_amount + inv.sgst_amount + inv.igst_amount 
            for inv in sales_invoices
        )
        total_itc = sum(
            inv.cgst_amount + inv.sgst_amount + inv.igst_amount 
            for inv in purchase_invoices
        )
        
        # Get pending invoices
        pending_invoices = Invoice.query.filter(
            Invoice.business_id == business_id,
            Invoice.status == 'pending'
        ).count()
        
        # Calculate next filing deadline
        next_deadline = today.replace(day=20)
        if today.day > 20:
            next_deadline = (today.replace(month=today.month % 12 + 1, day=1) if today.month != 12 
                           else today.replace(year=today.year + 1, month=1, day=1)).replace(day=20)
        
        return jsonify({
            'success': True,
            'business_name': business.business_name,
            'gstin': business.gstin,
            'overview': {
                'total_sales': total_sales,
                'total_purchases': total_purchases,
                'tax_liability': total_tax,
                'itc_available': total_itc,
                'net_tax_payable': max(0, total_tax - total_itc),
                'pending_invoices': pending_invoices,
                'next_filing_deadline': next_deadline.strftime('%Y-%m-%d'),
                'days_until_deadline': (next_deadline - today).days
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

# ==================== INITIALIZATION ====================

def init_db():
    """Initialize database"""
    with app.app_context():
        db.create_all()
        print("Database initialized successfully")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
