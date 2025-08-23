import streamlit as st
import calendar
import datetime
import os
import io

# Define Expense class
class Expense:
    def __init__(self, name, category, amount):
        self.name = name
        self.category = category
        self.amount = amount

    def __repr__(self):
        return f"<Expense: {self.name}, {self.category}, ₹{self.amount:.2f}>"

# Save expense to file
def save_expense_to_file(expense, file_path):
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")

# Summarize expenses from file
def summarize_expenses(file_path, budget):
    expenses = []

    if not os.path.exists(file_path):
        return expenses

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            name, amount, category = line.strip().split(",")
            expenses.append(Expense(name, category, float(amount)))

    # Category-wise total
    category_totals = {}
    for exp in expenses:
        category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount

    st.subheader("📊 Expenses by Category")
    for category, total in category_totals.items():
        st.write(f"**{category}**: ₹{total:.2f}")

    total_spent = sum(exp.amount for exp in expenses)
    st.success(f"💸 Total Spent: ₹{total_spent:.2f}")
    remaining = budget - total_spent
    st.info(f"✅ Remaining Budget: ₹{remaining:.2f}")

    today = datetime.datetime.now()
    days_in_month = calendar.monthrange(today.year, today.month)[1]
    days_remaining = days_in_month - today.day
    st.info(f"📅 Remaining days in the month: **{days_remaining}**")

    if days_remaining > 0:
        daily_budget = remaining / days_remaining
        st.info(f"📅 Budget per Day: ₹{daily_budget:.2f}")
    else:
        st.warning(f"📅 Last day of the month. Today's budget: ₹{remaining:.2f}")
    
    return expenses

# Generate PDF report
def generate_pdf_report(expenses, budget, file_path):
    if not expenses:
        return None
    
    try:
        buffer = io.BytesIO()
        # ReportLab imports are now local to this function
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import inch

        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1,  # Center alignment
            fontName='Helvetica-Bold'
        )
        
        # Title
        title = Paragraph("Personal Expense Tracker Report", title_style)
        story.append(title)
        story.append(Spacer(1, 20))
        
        # Summary section
        total_spent = sum(exp.amount for exp in expenses)
        remaining = budget - total_spent
        
        summary_data = [
            ["Monthly Budget", f"Rs.{budget:.2f}"],
            ["Total Spent", f"Rs.{total_spent:.2f}"],
            ["Remaining Budget", f"Rs.{remaining:.2f}"],
            ["Generated Date", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 2.5*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11)
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 25))
        
        # Category totals
        category_totals = {}
        for exp in expenses:
            category_totals[exp.category] = category_totals.get(exp.category, 0) + exp.amount
        
        if category_totals:
            cat_title = Paragraph("Expenses by Category", styles['Heading2'])
            story.append(cat_title)
            story.append(Spacer(1, 15))
            
            cat_data = [["Category", "Total Amount"]]
            for category, total in category_totals.items():
                # Clean category name by removing emojis
                clean_category = category.replace('🍔', '').replace('🏡', '').replace('💼', '').replace('🎉', '').replace('✈️', '').replace('✨', '').strip()
                cat_data.append([clean_category, f"Rs.{total:.2f}"])
            
            cat_table = Table(cat_data, colWidths=[3.5*inch, 2*inch])
            cat_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 11)
            ]))
            story.append(cat_table)
            story.append(Spacer(1, 25))
        
        # Individual expenses
        exp_title = Paragraph("Individual Expenses", styles['Heading2'])
        story.append(exp_title)
        story.append(Spacer(1, 15))
        
        exp_data = [["Name", "Category", "Amount"]]
        for exp in expenses:
            # Clean category name by removing emojis
            clean_category = exp.category.replace('🍔', '').replace('🏡', '').replace('💼', '').replace('🎉', '').replace('✈️', '').replace('✨', '').strip()
            exp_data.append([exp.name, clean_category, f"Rs.{exp.amount:.2f}"])
        
        exp_table = Table(exp_data, colWidths=[2.5*inch, 2*inch, 1.5*inch])
        exp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.darkred),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.lightcoral),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 11)
        ]))
        story.append(exp_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer
        
    except ImportError:
        st.error("❌ PDF generation is not available. The 'reportlab' package is required for PDF export.")
        st.info("💡 To enable PDF export, install reportlab: pip install reportlab")
        return None
    except Exception as e:
        st.error(f"❌ Error generating PDF: {str(e)}")
        return None

# Main Streamlit App
def main():
    st.title("💰 Expense Tracker")
    file_path = "expenses.csv"

    budget = st.number_input("Enter your monthly budget (₹)", min_value=0.0, value=2000.0, step=100.0)

    st.header("➕ Add a New Expense")
    name = st.text_input("Expense Name")
    amount = st.number_input("Expense Amount (₹)", min_value=0.0, step=10.0)
    category = st.selectbox("Category", ["🍔 Food", "🏡 Home", "💼 Work", "🎉 Fun", "✈️ Travel", "✨ Miscellaneous"])

    if st.button("Save Expense"):
        if name and amount > 0:
            expense = Expense(name, category, amount)
            save_expense_to_file(expense, file_path)
            st.success(f"✅ Saved: {expense}")
        else:
            st.error("❌ Please enter a valid name and amount!")

    st.header(" Monthly Summary")

    expenses = summarize_expenses(file_path, budget)
    
    # Clear All Expenses Button
    if st.button("🗑️ Clear All Expenses", type="secondary"):
        if os.path.exists(file_path):
            os.remove(file_path)
            st.success("✅ All expenses cleared! The tracker has been reset.")
            st.rerun()
        else:
            st.info("ℹ️ No expenses file found to clear.")
    
    # summarize_expenses(file_path, budget)

    # Generate PDF Report Button
    if st.button("📄 Generate PDF Report"):
        if not expenses:
            st.warning("⚠️ No expenses to generate report for. Please add some expenses first.")
        else:
            pdf_buffer = generate_pdf_report(expenses, budget, file_path)
            if pdf_buffer:
                st.download_button(
                    label="Download PDF Report",
                    data=pdf_buffer,
                    file_name="expense_report.pdf",
                    mime="application/pdf"
                )
            # Error messages are already handled in the generate_pdf_report function

if __name__ == "__main__":
    main()
