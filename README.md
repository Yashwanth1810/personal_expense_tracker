# Personal Expense Tracker

A web app that helps you record daily spending, see totals by category, and stay within a monthly budget. Built with Streamlit so you can use it in the browser without installing a database.

## What it does

You set a monthly budget, add expenses with a name, amount, and category, and the app shows how much you spent, how much is left, and a simple “per day” suggestion for the rest of the month. You can also download a PDF summary and clear all saved expenses when you want a fresh start.

## Features

- **Monthly budget** — Enter how much you plan to spend this month (in ₹).
- **Add expenses** — Name, amount, and category (Food, Home, Work, Fun, Travel, Miscellaneous).
- **Summary** — Totals by category, total spent, money left, days left in the month, and suggested budget per day.
- **PDF report** — Download a printable summary (budget, totals, category breakdown, and line items).
- **Clear data** — Remove all saved expenses from the file when you need to reset.

## Tech stack

| Piece | Role |
|--------|------|
| **Python** | Core language and logic |
| **Streamlit** | Web interface (forms, buttons, and on-screen summary) |
| **CSV file** | Expenses are saved in `expenses.csv` on disk — no separate database app to install |
| **ReportLab** | Creates the downloadable PDF report |

## How it works (simple)

1. When you save an expense, one line is **appended** to `expenses.csv` (name, amount, category).
2. When you open the summary (or after saving), the app **reads** that file, adds up amounts by category and in total, and compares everything to your budget.
3. It uses **today’s date** to figure out how many days are left in the month and divides the remaining budget by that number (or handles the last day of the month in a simple way).
4. The PDF button builds a report from the same data and lets you **download** it in the browser.

Run the app locally:

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Live demo


**Live app:** *[https://personalexpensetrackergit-j5zzfm8rsthjty5atrbfgw.streamlit.app/]*





