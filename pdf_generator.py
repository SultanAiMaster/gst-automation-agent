"""
PDF Generator Module for GST Automation Agent
Generates GST-compliant tax invoices in PDF format
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
from io import BytesIO
import os

class InvoicePDFGenerator:
    """Generate professional GST-compliant invoices"""

    def __init__(self):
        self.page_size = A4
        self.margin = 0.5 * inch
        self.styles = getSampleStyleSheet()

        # Custom styles
        self.title_style = ParagraphStyle(
            'Title',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1a1a2e'),
            alignment=TA_CENTER,
            spaceAfter=20
        )

        self.normal_style = ParagraphStyle(
            'Normal',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#333333'),
            leading=14
        )

        self.bold_style = ParagraphStyle(
            'Bold',
            parent=self.styles['Normal'],
            fontSize=10,
            fontName='Helvetica-Bold',
            textColor=colors.HexColor('#333333'),
            leading=14
        )

        self.header_style = ParagraphStyle(
            'Header',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#1a1a2e'),
            spaceAfter=10
        )

    def generate_invoice(self, invoice_data, output_file=None):
        """
        Generate GST invoice PDF

        Args:
            invoice_data: Dictionary containing invoice details
            output_file: Optional file path to save PDF

        Returns:
            BytesIO object with PDF data
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.page_size,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )

        elements = []

        # Header section
        elements.extend(self._create_header(invoice_data))

        # Invoice details
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_invoice_info(invoice_data))

        # Bill to & Ship to
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_party_details(invoice_data))

        # Items table
        elements.append(Spacer(1, 0.3 * inch))
        elements.extend(self._create_items_table(invoice_data))

        # Tax summary
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_tax_summary(invoice_data))

        # Amount in words
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_amount_words(invoice_data))

        # Bank details
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_bank_details(invoice_data))

        # Terms & conditions
        elements.append(Spacer(1, 0.2 * inch))
        elements.extend(self._create_terms())

        # Signature section
        elements.append(Spacer(1, 0.5 * inch))
        elements.extend(self._create_signature(invoice_data))

        # Footer
        elements.append(Spacer(1, 0.3 * inch))
        elements.extend(self._create_footer(invoice_data))

        # Build PDF
        doc.build(elements)

        # Save to file if path provided
        if output_file:
            with open(output_file, 'wb') as f:
                f.write(buffer.getvalue())

        buffer.seek(0)
        return buffer

    def _create_header(self, data):
        """Create company header"""
        elements = []

        # Company name and logo placeholder
        company_name = data.get('business_name', 'Your Company Name')
        company_data = [
            [Paragraph(f"<b>{company_name}</b>", self.bold_style), ''],
            [Paragraph(data.get('address', 'Business Address'), self.normal_style), ''],
            [Paragraph(f"GSTIN: {data.get('gstin', 'N/A')}", self.bold_style),
             Paragraph(f"Phone: {data.get('phone', 'N/A')}", self.normal_style)],
            [Paragraph(f"State: {data.get('state', 'N/A')}", self.normal_style),
             Paragraph(f"Email: {data.get('email', 'N/A')}", self.normal_style)]
        ]

        company_table = Table(company_data, colWidths=[4*inch, 2*inch])
        company_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (0, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (0, 0), 16),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.HexColor('#1a1a2e')),
        ]))

        elements.append(company_table)
        return elements

    def _create_invoice_info(self, data):
        """Create invoice number, date, and type info"""
        elements = []

        billing_table_data = [
            [Paragraph("<b>Invoice Details</b>", self.bold_style), ''],
            [Paragraph(f"Invoice No: {data.get('invoice_number', 'N/A')}", self.normal_style),
             Paragraph(f"Invoice Date: {data.get('invoice_date', 'N/A')}", self.normal_style)],
            [Paragraph(f"Invoice Type: {data.get('invoice_type', 'SALES').upper()}", self.normal_style),
             Paragraph(f"GST Supply Type: {data.get('supply_type', 'Intra-State')}", self.normal_style)],
        ]

        billing_table = Table(billing_table_data, colWidths=[3.5*inch, 2.5*inch])
        billing_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 1), (1, 1), 'RIGHT'),
            ('ALIGN', (1, 2), (1, 2), 'RIGHT'),
        ]))

        elements.append(billing_table)
        return elements

    def _create_party_details(self, data):
        """Create Bill To and Ship To sections"""
        elements = []

        party_data = [
            [Paragraph("<b>Bill To:</b>", self.bold_style), Paragraph("<b>Ship To:</b>", self.bold_style)],
            [Paragraph(data.get('customer_name', 'Customer Name'), self.normal_style),
             Paragraph(data.get('customer_name', 'Customer Name'), self.normal_style)],
            [Paragraph(data.get('customer_gstin', f"GSTIN: N/A"), self.normal_style),
             Paragraph(data.get('customer_gstin', f"GSTIN: N/A"), self.normal_style)],
            [Paragraph(data.get('customer_address', 'Customer Address'), self.normal_style),
             Paragraph(data.get('customer_address', 'Customer Address'), self.normal_style)],
            [Paragraph(f"State: {data.get('customer_state', 'N/A')}", self.normal_style),
             Paragraph(f"State: {data.get('customer_state', 'N/A')}", self.normal_style)],
        ]

        party_table = Table(party_data, colWidths=[3*inch, 3*inch])
        party_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('FONTNAME', (0, 0), (1, 0), 'Helvetica-Bold'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
            ('LINEABOVE', (0, 0), (-1, 0), 1, colors.black),
            ('LINEBELOW', (0, 0), (-1, 0), 1, colors.black),
        ]))

        elements.append(party_table)
        return elements

    def _create_items_table(self, data):
        """Create items table with GST breakdown"""
        elements = []

        # Table headers
        header_data = [
            [Paragraph("<b>#</b>", self.bold_style),
             Paragraph("<b>Item Description</b>", self.bold_style),
             Paragraph("<b>HSN/SAC</b>", self.bold_style),
             Paragraph("<b>Qty</b>", self.bold_style),
             Paragraph("<b>Rate</b>", self.bold_style),
             Paragraph("<b>Amount</b>", self.bold_style),
             Paragraph("<b>GST</b>", self.bold_style)]
        ]

        # Items data
        items = data.get('items', [])
        for idx, item in enumerate(items, 1):
            row = [
                Paragraph(str(idx), self.normal_style),
                Paragraph(item.get('item_name', 'N/A'), self.normal_style),
                Paragraph(item.get('hsn_code', 'N/A'), self.normal_style),
                Paragraph(str(item.get('quantity', 0)), self.normal_style),
                Paragraph(f"₹{item.get('unit_price', 0):.2f}", self.normal_style),
                Paragraph(f"₹{item.get('amount', 0):.2f}", self.normal_style),
                Paragraph(f"{item.get('gst_rate', 0)}%", self.normal_style)
            ]
            header_data.append(row)

        # Column widths
        col_widths = [0.4*inch, 2.5*inch, 1*inch, 0.5*inch, 1*inch, 1*inch, 0.5*inch]

        items_table = Table(header_data, colWidths=col_widths, repeatRows=1)
        items_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cccccc')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(items_table)
        return elements

    def _create_tax_summary(self, data):
        """Create tax summary with CGST/SGST/IGST breakdown"""
        elements = []

        tax_data = [
            ['', '', '', ''],
            ['', '', Paragraph("<b>Tax Summary</b>", self.bold_style), ''],
            [Paragraph('Taxable Amount:', self.normal_style), '', '',
             Paragraph(f"₹{data.get('taxable_amount', 0):.2f}", self.bold_style)],
        ]

        # Add CGST/SGST or IGST based on supply type
        if data.get('igst_amount', 0) > 0:
            tax_data.append([Paragraph('IGST:', self.normal_style), '', '',
                            Paragraph(f"₹{data.get('igst_amount', 0):.2f}", self.normal_style)])
        else:
            tax_data.append([Paragraph('CGST:', self.normal_style), '', '',
                            Paragraph(f"₹{data.get('cgst_amount', 0):.2f}", self.normal_style)])
            tax_data.append([Paragraph('SGST:', self.normal_style), '', '',
                            Paragraph(f"₹{data.get('sgst_amount', 0):.2f}", self.normal_style)])

        # Total
        tax_data.append([Paragraph('<b>Total Amount:</b>', self.bold_style), '', '',
                        Paragraph(f"<b>₹{data.get('total_amount', 0):.2f}</b>", self.bold_style)])

        tax_table = Table(tax_data, colWidths=[2*inch, 1*inch, 1*inch, 2*inch])
        tax_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (-1, 2), (-1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (2, 1), (3, -1), 1, colors.black),
            ('FONTNAME', (0, 4), (0, 4), 'Helvetica-Bold'),
            ('FONTNAME', (3, 4), (3, 4), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]))

        elements.append(tax_table)
        return elements

    def _create_amount_words(self, data):
        """Create amount in words"""
        elements = []

        total = data.get('total_amount', 0)
        words = self._number_to_words(total)

        amount_words_data = [
            [Paragraph("<b>Amount in Words:</b>", self.bold_style)],
            [Paragraph(words, self.normal_style)]
        ]

        amount_words_table = Table(amount_words_data, colWidths=[6*inch])
        amount_words_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))

        elements.append(amount_words_table)
        return elements

    def _number_to_words(self, num):
        """Convert number to words (simplified version)"""
        # This is a basic implementation
        # For production, use num2words library
        if num == 0:
            return "Zero Rupees Only"

        units = ['', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
        teens = ['Ten', 'Eleven', 'Twelve', 'Thirteen', 'Fourteen', 'Fifteen', 'Sixteen',
                'Seventeen', 'Eighteen', 'Nineteen']
        tens = ['', '', 'Twenty', 'Thirty', 'Forty', 'Fifty', 'Sixty', 'Seventy', 'Eighty', 'Ninety']

        def convert_hundreds(n):
            if n < 10:
                return units[n]
            elif n < 20:
                return teens[n - 10]
            elif n < 100:
                return tens[n // 10] + (' ' + units[n % 10] if n % 10 != 0 else '')
            elif n < 1000:
                return units[n // 100] + ' Hundred' + (' and ' + convert_hundreds(n % 100) if n % 100 != 0 else '')

        def convert_thousands(n):
            if n < 1000:
                return convert_hundreds(n)
            elif n < 100000:
                return convert_hundreds(n // 1000) + ' Thousand' + (' ' + convert_hundreds(n % 1000) if n % 1000 != 0 else '')
            elif n < 10000000:
                return convert_hundreds(n // 100000) + ' Lakh' + (' ' + convert_thousands(n % 100000) if n % 100000 != 0 else '')
            else:
                return convert_hundreds(n // 10000000) + ' Crore' + (' ' + convert_thousands(n % 10000000) if n % 10000000 != 0 else '')

        # Handle decimal part (paisa)
        integer_part = int(num)
        decimal_part = int(round((num - integer_part) * 100))

        words = convert_thousands(integer_part) + ' Rupees'
        if decimal_part > 0:
            words += ' and ' + convert_hundreds(decimal_part) + ' Paise'

        return words + ' Only'

    def _create_bank_details(self, data):
        """Create bank details section"""
        elements = []

        bank_data = [
            [Paragraph("<b>Bank Details:</b>", self.bold_style), ''],
            [Paragraph(f"Bank Name: {data.get('bank_name', 'Your Bank Name')}", self.normal_style),
             Paragraph(f"Account No: {data.get('account_number', 'N/A')}", self.normal_style)],
            [Paragraph(f"IFSC Code: {data.get('ifsc_code', 'N/A')}", self.normal_style),
             Paragraph(f"Branch: {data.get('bank_branch', 'N/A')}", self.normal_style)],
        ]

        bank_table = Table(bank_data, colWidths=[4*inch, 2*inch])
        bank_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(bank_table)
        return elements

    def _create_terms(self):
        """Create terms and conditions"""
        elements = []

        terms_data = [
            [Paragraph("<b>Terms & Conditions:</b>", self.bold_style)],
            [Paragraph("1. Goods once sold will not be taken back.", self.normal_style)],
            [Paragraph("2. Interest @ 18% p.a. will be charged on overdue payments.", self.normal_style)],
            [Paragraph("3. Subject to local jurisdiction only.", self.normal_style)],
        ]

        terms_table = Table(terms_data, colWidths=[6*inch])
        terms_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        elements.append(terms_table)
        return elements

    def _create_signature(self, data):
        """Create signature section"""
        elements = []

        signature_data = [
            ['', '', Paragraph(f"<b>For {data.get('business_name', 'Your Company Name')}</b>", self.bold_style)],
            ['', '', ''],
            ['', '', ''],
            ['', '', Paragraph('<b>Authorized Signatory</b>', self.bold_style)],
        ]

        signature_table = Table(signature_data, colWidths=[2*inch, 2*inch, 2*inch])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
        ]))

        elements.append(signature_table)
        return elements

    def _create_footer(self, data):
        """Create footer with GST registration details"""
        elements = []

        footer_data = [
            [Paragraph("<b>GST Registration Details:</b>", self.bold_style)],
            [Paragraph(f"GSTIN: {data.get('gstin', 'N/A')} | State: {data.get('state', 'N/A')} | State Code: {data.get('state_code', 'N/A')} | "
                       f"Legal Name: {data.get('business_name', 'N/A')}", self.normal_style)]
        ]

        footer_table = Table(footer_data, colWidths=[6*inch])
        footer_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#666666')),
        ]))

        elements.append(footer_table)
        return elements
