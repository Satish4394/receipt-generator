from datetime import date
import io
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import streamlit as st

st.set_page_config(
    page_title="Eicher Receipt Generator", page_icon="📄", layout="centered"
)


def create_receipt_pdf(
    receipt_no,
    customer_id,
    customer_name,
    customer_address,
    model_name,
    amount_numeric,
    amount_in_words,
    upi_ref_no,
    receipt_date,
):
  buffer = io.BytesIO()
  c = canvas.Canvas(buffer, pagesize=A4)
  width, height = A4

  # बॉर्डर
  c.setLineWidth(1)
  c.rect(30, 30, width - 60, height - 60)

  # लोगो (इमेज या टेक्स्ट)
  logo_found = False
  for logo_name in ["eicher_logo.png", "eicher_logo.jpg"]:
    if os.path.exists(logo_name):
      try:
        c.drawImage(
            logo_name,
            45,
            height - 75,
            width=130,
            height=35,
            preserveAspectRatio=True,
            mask="auto",
        )
        logo_found = True
        break
      except Exception:
        pass

  if not logo_found:
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.HexColor("#C8102E"))
    c.drawString(45, height - 65, "EICHER")
    c.setFillColor(colors.black)

  # हेडर राइट साइड
  c.setFont("Helvetica-Bold", 10)
  c.drawRightString(width - 45, height - 65, "Receipt")
  c.drawRightString(
      width - 45, height - 80, f"Date  {receipt_date.strftime('%d.%m.%Y')}"
  )

  # रसीद विवरण
  c.setFont("Helvetica", 9)
  c.drawString(45, height - 90, f"Receipt no  {receipt_no}")
  c.drawString(45, height - 103, f"Customer id  {customer_id}")
  c.drawString(45, height - 116, "Invoice No")

  # कंपनी विवरण
  c.setFont("Helvetica-Bold", 9)
  c.drawString(45, height - 138, "VE Commercial Vehicles Limited")
  c.setFont("Helvetica", 8.5)
  c.drawString(
      45,
      height - 151,
      "S.No.3/1, Rajwade Commercial Complex Katraj - Bypass Road,",
  )
  c.drawString(45, height - 164, "Above SBI")
  c.drawString(45, height - 177, "Pune 411046")
  c.drawString(45, height - 190, "(08600145540)")

  c.setLineWidth(0.5)
  c.line(40, height - 204, width - 40, height - 204)

  # कस्टमर विवरण
  y = height - 230
  c.setFont("Helvetica-Bold", 9)
  c.drawString(45, y, "Received with thanks from Mr./Ms")
  c.setFont("Helvetica-Bold", 9.5)
  c.drawString(210, y, str(customer_name).upper())

  y -= 18
  c.setFont("Helvetica", 8.5)
  c.drawString(45, y, customer_address)

  y -= 25
  c.setFont("Helvetica", 9)
  c.drawString(45, y, f"The Sum Of {amount_in_words}")

  y -= 25
  c.drawString(45, y, "Bank Transfer Ref No.:")
  c.drawString(45, y - 16, "Bank:")
  c.drawString(45, y - 32, "Payment Type:  UPI Online Paym")
  c.drawString(45, y - 48, f"Header text:   {upi_ref_no}")

  y -= 80
  c.setFont("Helvetica-Bold", 9)
  c.drawString(45, y, f"MODEL-{model_name}")

  c.setFont("Helvetica", 9)
  c.drawString(45, y - 20, "By Draft/Cheque, Date:")

  c.setFont("Helvetica-Bold", 11)
  c.drawString(width - 150, y - 20, f"Rs {amount_numeric}")

  # फुटर
  c.setFont("Helvetica-Bold", 8.5)
  c.drawString(45, 120, "Terms & Conditions")
  c.setFont("Helvetica", 7.5)
  c.drawString(
      45, 108, "The receipt is issued subject to realization of cheque."
  )
  c.drawString(45, 96, "Subject to Pune jurisdiction only.")
  c.drawString(
      45, 84, "Prices prevailing at time of delievery will be applicable."
  )

  c.setFont("Helvetica-Bold", 8.5)
  c.drawString(45, 60, "TRUCKS AND BUSES")

  c.drawRightString(width - 45, 110, "For")
  c.drawRightString(width - 45, 60, "Authorised Signatory")

  c.save()
  buffer.seek(0)
  return buffer


# --- मोबाइल UI डिज़ाइन ---
st.title("🚛 Eicher Receipt Generator")
st.caption("नीचे दिए गए विवरण भरें और सीधे PDF डाउनलोड करें:")

with st.form("receipt_form"):
  col1, col2 = st.columns(2)
  with col1:
    r_no = st.text_input("Receipt No", value="1580571557")
    r_date = st.date_input("Date", value=date.today())
  with col2:
    c_id = st.text_input("Customer ID", value="10790882")

  cust_name = st.text_input(
      "Customer Name", placeholder="उदा. SURAJ PARSHURAM TAKALKAR"
  )
  cust_address = st.text_area(
      "Customer Address",
      value=(
          "Ground FI Manjarewadi Dharm Nimgaon Road nearhanumantempal Tal -Khed"
          " KHED KHED, KHED, 410505"
      ),
  )

  model_val = st.text_input(
      "Model Name", value="Pro 2119 H CBC 20FT BSVI NGB 7S AC"
  )

  col3, col4 = st.columns(2)
  with col3:
    amt_num = st.text_input("Amount (Rs)", value="11,000.00")
  with col4:
    amt_words = st.text_input(
      "Amount in Words", value="Eleven Thousand Rupees"
  )

  upi_text = st.text_input("UPI / Ref No", value="UPI/625882577397")

  submitted = st.form_submit_button("PDF तैयार करें 🚀", use_container_width=True)

if submitted:
  if not cust_name.strip():
    st.error("कृपया कस्टमर का नाम दर्ज करें!")
  else:
    pdf_bytes = create_receipt_pdf(
        r_no,
        c_id,
        cust_name,
        cust_address,
        model_val,
        amt_num,
        amt_words,
        upi_text,
        r_date,
    )

    clean_name = "".join(
        c for c in cust_name if c.isalnum() or c in (" ", "_")
    ).strip()
    download_filename = f"Receipt_{clean_name.replace(' ', '_')}.pdf"

    st.success("✅ रसीद तैयार हो गई है!")
    st.download_button(
        label="📥 PDF डाउनलोड करें",
        data=pdf_bytes,
        file_name=download_filename,
        mime="application/pdf",
        use_container_width=True,
    )