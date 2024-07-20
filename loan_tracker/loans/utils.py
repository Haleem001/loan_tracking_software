
from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import EmailMessage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from io import BytesIO

def generate_loan_pdf(loan_request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=42,
        textColor=colors.darkblue,
        alignment=1  # Center alignment
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=12,
        leading=15,
        spaceAfter=15
    )
    
    elements.append(Spacer(1, 12))
    
    title = Paragraph("Adoption Approval Certificate", title_style)
    elements.append(title)
    elements.append(Spacer(1, 24))
    
    full_name = f"{loan_request.user.first_name} {loan_request.user.last_name}"
    requester_name = f"Requested by: {full_name}"
    approval_date = f"Date of Approval: {loan_request.status_date.strftime('%Y-%m-%d')}"
    thank_you_note = "Thank you "
    
    elements.append(Paragraph(requester_name, normal_style))
    elements.append(Paragraph(approval_date, normal_style))
    elements.append(Paragraph(thank_you_note, normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer




def send_approval_email(loan_request):
    pdf_buffer = generate_loan_pdf(loan_request)
    full_name = f"{loan_request.user.first_name} {loan_request.user.last_name}"
    email = EmailMessage(
        'Loan Approval Certificate',
        f'Dear {full_name},\n\nCongratulations! Your loan request has been approved. Please find attached the loan approval certificate.',
        'your_email@gmail.com',
        [loan_request.user.email],
    )
    email.attach('Loan_Approval_Certificate.pdf', pdf_buffer.getvalue(), 'application/pdf')
    email.send()

def send_rejection_email(loan_request):
    full_name = f"{loan_request.user.first_name} {loan_request.user.last_name}"
    email = EmailMessage(
        'Loan Request Update',
        f'Dear {full_name},\n\nWe regret to inform you that your Loan request has been rejected. Please contact us for further details.',
        'your_email@gmail.com',
        [loan_request.user.email],
    )
    email.send()