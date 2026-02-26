import streamlit as st
from datetime import date
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle   # ← Added ParagraphStyle here
from reportlab.lib.units import inch

def generate_checklist_pdf(data, today_str):
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name='ChecklistTitle',
        parent=styles['Heading1'],
        fontSize=16,
        leading=20,
        spaceAfter=12,
        alignment=1
    )

    phase_style = ParagraphStyle(
        name='ChecklistPhase',
        parent=styles['Heading2'],
        fontSize=11,  # Smaller for page 2+
        leading=13,
        spaceBefore=24,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    item_style = ParagraphStyle(
        name='ChecklistItem',
        parent=styles['Normal'],
        fontSize=10,
        leading=12,
        spaceAfter=4,
        splitLongWords=1  # Force break very long words
    )

    date_style = ParagraphStyle(
        name='ChecklistDate',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        spaceAfter=2,
        fontName='Helvetica-Oblique'
    )

    notes_style = ParagraphStyle(
        name='ChecklistNotes',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        spaceAfter=6,
        splitLongWords=1
    )

    reminder_style = ParagraphStyle(
        name='ChecklistReminder',
        parent=styles['Italic'],
        fontSize=9,
        leading=11,
        spaceBefore=12
    )

    flowables = []

    flowables.append(Paragraph("Estate Administration Checklist", title_style))
    flowables.append(Paragraph(f"Prepared: {today_str} | CPA: Alexander - Bel Air, MD", item_style))
    flowables.append(Paragraph("No sensitive data collected. Tracking only. Use secure portal for documents.", item_style))
    flowables.append(Spacer(1, 0.25*inch))

    def add_item(label, date_key, notes_key):
        flowables.append(Paragraph(label, item_style))
        flowables.append(Paragraph(f"Date: {data.get(date_key, '__________')}", date_style))
        notes = data.get(notes_key, '').strip() or '-'
        flowables.append(Paragraph(f"Notes: {notes}", notes_style))
        flowables.append(Spacer(1, 0.1*inch))

    flowables.append(Paragraph("Phase 1: Immediate Steps and State Authority", phase_style))
    add_item("1. Obtain multiple certified Death Certificates", "p1_1", "p1_1_notes")
    add_item("2. Locate Will and File with Probate Court", "p1_2", "p1_2_notes")
    add_item("3. Petition for Appointment", "p1_3", "p1_3_notes")
    add_item("4. Receive Letters Testamentary / Administration", "p1_4", "p1_4_notes")

    flowables.append(Paragraph("Phase 2: Federal Identity and Authorization", phase_style))
    add_item("5. Apply for Estate EIN", "p2_5", "p2_5_notes")
    add_item("6a. Form 56 filed for Decedent", "p2_6a", "p2_6a_notes")
    add_item("6b. Form 56 filed for Estate", "p2_6b", "p2_6b_notes")
    add_item("7. Notice to Creditors published", "p2_7", "p2_7_notes")

    flowables.append(Paragraph("Phase 3: Tax Filing Requirements", phase_style))
    add_item("8. Final Form 1040", "p3_8", "p3_8_notes")
    add_item("9. Form 1041", "p3_9", "p3_9_notes")
    add_item("10. Form 706 (if required)", "p3_10", "p3_10_notes")

    flowables.append(Paragraph("Phase 4: Expediting and Protecting Yourself", phase_style))
    add_item("11. Form 4810 - Prompt Assessment", "p4_11", "p4_11_notes")
    add_item("12. Form 5495 - Discharge from Liability", "p4_12", "p4_12_notes")

    flowables.append(Paragraph("Phase 5: Closing the Estate", phase_style))
    add_item("13. Distribute Assets", "p5_13", "p5_13_notes")
    add_item("14a. Final Form 56 - Decedent", "p5_14a", "p5_14a_notes")
    add_item("14b. Final Form 56 - Estate", "p5_14b", "p5_14b_notes")

    flowables.append(Spacer(1, 0.25*inch))
    flowables.append(Paragraph("Reminder: File separate Form 56 for decedent and estate initially and at termination.", reminder_style))

    doc.build(flowables)
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return BytesIO(pdf_bytes)


st.set_page_config(page_title="Estate Checklist - ReportLab", layout="wide")

st.title("Estate Administration Checklist")
st.markdown("Intake form : Do not place sensitive personal information on intake form. Upload through secure portal provided by Tax Advisor once required")

today_str = date.today().strftime("%B %d, %Y")

with st.form("checklist"):
    st.subheader("Phase 1: Immediate Steps and State Authority")
    st.text_input("1. Obtain multiple certified Death Certificates - Date", key="p1_1")
    st.text_input("Notes", key="p1_1_notes")

    st.text_input("2. Locate Will and File with Probate Court - Date", key="p1_2")
    st.text_input("Notes", key="p1_2_notes")

    st.text_input("3. Petition for Appointment - Date", key="p1_3")
    st.text_input("Notes", key="p1_3_notes")

    st.text_input("4. Receive Letters Testamentary / Administration - Date", key="p1_4")
    st.text_input("Notes", key="p1_4_notes")

    st.subheader("Phase 2: Federal Identity and Authorization")
    st.text_input("5. Apply for Estate EIN - Date", key="p2_5")
    st.text_input("Notes", key="p2_5_notes")

    st.text_input("6a. Form 56 filed for Decedent - Date", key="p2_6a")
    st.text_input("Notes", key="p2_6a_notes")

    st.text_input("6b. Form 56 filed for Estate - Date", key="p2_6b")
    st.text_input("Notes", key="p2_6b_notes")

    st.text_input("7. Notice to Creditors published - Date", key="p2_7")
    st.text_input("Notes", key="p2_7_notes")

    st.subheader("Phase 3: Tax Filing Requirements")
    st.text_input("8. Final Form 1040 - Date", key="p3_8")
    st.text_input("Notes", key="p3_8_notes")

    st.text_input("9. Form 1041 - Date", key="p3_9")
    st.text_input("Notes", key="p3_9_notes")

    st.text_input("10. Form 706 (if required) - Date", key="p3_10")
    st.text_input("Notes", key="p3_10_notes")

    st.subheader("Phase 4: Expediting and Protecting Yourself")
    st.text_input("11. Form 4810 - Prompt Assessment - Date", key="p4_11")
    st.text_input("Notes", key="p4_11_notes")

    st.text_input("12. Form 5495 - Discharge from Liability - Date", key="p4_12")
    st.text_input("Notes", key="p4_12_notes")

    st.subheader("Phase 5: Closing the Estate")
    st.text_input("13. Distribute Assets - Date", key="p5_13")
    st.text_input("Notes", key="p5_13_notes")

    st.text_input("14a. Final Form 56 - Decedent - Date", key="p5_14a")
    st.text_input("Notes", key="p5_14a_notes")

    st.text_input("14b. Final Form 56 - Estate - Date", key="p5_14b")
    st.text_input("Notes", key="p5_14b_notes")

    generate = st.form_submit_button("Create PDF", type="primary")

if generate:
    data = {k: v for k, v in st.session_state.items() if v and not k.startswith("FormSubmit")}

    pdf_buffer = generate_checklist_pdf(data, today_str)

    st.success("PDF generated using ReportLab – flush left, separate lines")
    st.download_button(
        label="Download Checklist PDF",
        data=pdf_buffer,
        file_name=f"estate_checklist_{today_str.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )

    st.info("All lines start flush left. No indentation. No cutoff expected.")