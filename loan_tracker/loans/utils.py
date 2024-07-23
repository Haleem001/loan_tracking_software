from django.core.mail import send_mail
from django.conf import settings
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.colors import HexColor
from django.conf import settings
import os

# Inside generate_loan_pdf function
logo_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'logo.png')
logo = Image(logo_path, width=2*inch, height=1*inch)

class SignatureLine(Flowable):
    def __init__(self, width):
        Flowable.__init__(self)
        self.width = width

    def draw(self):
        self.canv.line(0, 0, self.width, 0)

def generate_loan_pdf(loan_request):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=1*inch, bottomMargin=1*inch)
    elements = []
    
    # Add your logo
    
    elements.append(logo)
    elements.append(Spacer(1, 0.5*inch))
    
    styles = getSampleStyleSheet()
    teal_500 = HexColor('#319795')  # Chakra UI's teal 500
    
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        textColor=teal_500,
        alignment=TA_CENTER
    )
    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=18,
        leading=22,
        alignment=TA_CENTER,
        textColor=teal_500
    )
    normal_style = ParagraphStyle(
        'Normal',
        parent=styles['BodyText'],
        fontSize=12,
        leading=14,
        spaceBefore=6,
        spaceAfter=6,
        textColor=teal_500
    )
    
    elements.append(Paragraph("Loan Approval Certificate", title_style))
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph("This certifies that", subtitle_style))
    elements.append(Spacer(1, 0.25*inch))
    
    full_name = f"{loan_request.user.first_name} {loan_request.user.last_name}"
    elements.append(Paragraph(full_name, subtitle_style))
    elements.append(Spacer(1, 0.5*inch))
    
    elements.append(Paragraph("has been approved for a loan with the following details:", normal_style))
    elements.append(Spacer(1, 0.25*inch))
    
    details = [
        f"Approved Amount: {loan_request.total_amount}",
        f"Reference Number: {loan_request.reference_number}",
        f"Date of Approval: {loan_request.status_date.strftime('%B %d, %Y')}"
    ]
    
    for detail in details:
        elements.append(Paragraph(detail, normal_style))
    
    elements.append(Spacer(1, 0.5*inch))
    elements.append(SignatureLine(6*inch))
    elements.append(Paragraph("Authorized Signature", normal_style))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def send_approval_email(loan_request):
    pdf_buffer = generate_loan_pdf(loan_request)
    full_name = f"{loan_request.user.first_name} {loan_request.user.last_name}"
    email = EmailMessage(
    'Loan Approval Certificate',
    f'Dear {full_name},\n\nCongratulations! Your loan request for ₦{loan_request.total_amount} has been approved. Your reference number is {loan_request.reference_number}. Please find attached the loan approval certificate.',
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
