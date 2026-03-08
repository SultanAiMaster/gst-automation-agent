"""
Test script for PDF Invoice Generation
"""

from pdf_generator import InvoicePDFGenerator
from io import BytesIO

# Create test invoice data
test_invoice = {
    # Business details
    'business_name': 'Sultan Tech Solutions Pvt Ltd',
    'gstin': '27ABCDE1234F1Z5',
    'state': 'Maharashtra',
    'state_code': '27',
    'address': '123, Tech Park, Andheri West, Mumbai - 400058',
    'phone': '+91 8638556847',
    'email': 'contact@sultantech.com',

    # Invoice details
    'invoice_number': 'INV-2026-001',
    'invoice_date': '2026-03-08',
    'invoice_type': 'sales',
    'supply_type': 'Intra-State',

    # Customer details
    'customer_name': 'ABC Industries Ltd',
    'customer_gstin': '27XYZEF5678G2Z9',
    'customer_address': '456, Industrial Area, Pune - 411045',
    'customer_state': 'Maharashtra',

    # Items
    'items': [
        {
            'item_name': 'Web Development Services',
            'hsn_code': '998311',
            'quantity': 1,
            'unit_price': 50000.00,
            'amount': 50000.00,
            'gst_rate': 18
        },
        {
            'item_name': 'Server Maintenance (Annual)',
            'hsn_code': '998313',
            'quantity': 1,
            'unit_price': 12000.00,
            'amount': 12000.00,
            'gst_rate': 18
        }
    ],

    # Tax details
    'taxable_amount': 62000.00,
    'cgst_amount': 5580.00,
    'sgst_amount': 5580.00,
    'igst_amount': 0.00,
    'total_amount': 73160.00,
    'gst_rate': 18,

    # Bank details
    'bank_name': 'HDFC Bank',
    'account_number': '50123456789012',
    'ifsc_code': 'HDFC0001234',
    'bank_branch': 'Andheri West, Mumbai'
}

# Generate PDF
print("Generating test invoice PDF...")
generator = InvoicePDFGenerator()

# Generate to file
output_file = 'test_invoice.pdf'
pdf_buffer = generator.generate_invoice(test_invoice, output_file)

print(f"✅ PDF generated successfully!")
print(f"📄 Saved to: {output_file}")
print(f"📊 Invoice details:")
print(f"   - Invoice Number: {test_invoice['invoice_number']}")
print(f"   - Customer: {test_invoice['customer_name']}")
print(f"   - Total Amount: ₹{test_invoice['total_amount']:,.2f}")
print(f"   - CGST: ₹{test_invoice['cgst_amount']:,.2f}")
print(f"   - SGST: ₹{test_invoice['sgst_amount']:,.2f}")
print(f"   - Total Items: {len(test_invoice['items'])}")

print("\n🎉 Phase 2: PDF Invoice Generation - SUCCESS!")
