from flask import Flask, render_template, request, redirect, url_for, send_file
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Mock family member list and provision data
family_members = ["John Doe", "Jane Doe", "Mark Doe", "Lucy Doe"]
provisions = ["Rice (kg)", "Wheat (kg)", "Sugar (kg)", "Oil (liters)"]

@app.route('/')
def family_members_page():
    return render_template('family_members.html', members=family_members)

@app.route('/provision_selection/<member>')
def provision_selection(member):
    return render_template('provision_selection.html', member=member, provisions=provisions)

@app.route('/generate_bill', methods=['POST'])
def generate_bill():
    member = request.form['member']
    selected_provisions = request.form.getlist('provision')
    quantities = request.form.getlist('quantity')

    # Generate PDF bill
    pdf_file = io.BytesIO()
    c = canvas.Canvas(pdf_file)
    c.setFont("Helvetica", 14)
    c.drawString(100, 800, "Tamil Nadu Government Ration Bill")
    c.drawString(100, 780, f"Family Member: {member}")
    c.drawString(100, 760, "Provisions:")
    
    y = 740
    for provision, quantity in zip(selected_provisions, quantities):
        c.drawString(120, y, f"- {provision}: {quantity}")
        y -= 20
    
    c.drawString(100, y-20, "Thank you for using the Public Distribution System.")
    c.save()
    pdf_file.seek(0)
    
    return send_file(pdf_file, download_name="ration_bill.pdf", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=false, host='0.0.0.0')
