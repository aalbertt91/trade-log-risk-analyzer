import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
import logging
from datetime import datetime
import os

# --- LOGGING CONFIGURATION ---
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


# --- DATA LOADING ---
try:
    df = pd.read_excel("data/trades.xlsx")
    logging.info("Excel file loaded successfully")
except FileNotFoundError:
    logging.error("File not found, please check the data folder")
    exit()
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
    exit()

# --- DATA VALIDATION AND CONVERSION ---
required_columns = ["close_date", "entry_price", "exit_price", "quantity", "fees"]

try:
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns in Excel: {missing_columns}")

    df["close_date"] = pd.to_datetime(df["close_date"], errors="coerce")
    df["entry_price"] = pd.to_numeric(df["entry_price"], errors="coerce")
    df["exit_price"] = pd.to_numeric(df["exit_price"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    df["fees"] = pd.to_numeric(df["fees"], errors="coerce")
    logging.info("Data types converted successfully.")
except Exception as e:
    logging.error(f"Data cleaning error: {e}")

# --- DATA CLEANUP AND PNL CALCULATION ---
before = len(df)
df = df.dropna().copy() 
after = len(df)

logging.info(f"Rows before cleanup: {before}, after cleanup: {after}")

df = df.sort_values("close_date").reset_index(drop=True)
df["pnl"] = (df["exit_price"] - df["entry_price"]) * df["quantity"] - df["fees"]

# --- AGGREGATING DAILY RETURNS ---
newdf = df.groupby("close_date")["pnl"].sum().to_frame().reset_index()
newdf["cumulative_pnl"] = newdf["pnl"].cumsum()
newdf["daily_returns"] = newdf["cumulative_pnl"].pct_change()

# --- RISK METRICS CALCULATION ---
volatility = newdf["daily_returns"].std()
rolling_max = newdf["cumulative_pnl"].cummax()
drawdown = newdf["cumulative_pnl"] - rolling_max
max_drawdown = drawdown.min()
total_pnl = newdf["pnl"].sum()

if volatility > 0:
    sharpe_ratio = (newdf["daily_returns"].mean() / volatility) * np.sqrt(252)
    logging.info(f"Sharpe Ratio calculated: {sharpe_ratio:.2f}")
else:
    sharpe_ratio = 0.0
    logging.warning(
        "Volatility is 0, Sharpe Ratio set to 0.0 to avoid division by zero."
    )


# --- REPORTING AND GRAPH SAVING ---
report_path = "reports"

# Check if directory exists, if not, create it
if not os.path.exists(report_path):
    os.makedirs(report_path)
    logging.info(f"Created missing directory: {report_path}")

try:
    # 1. Equity Curve Generation
    plt.figure(figsize=(10, 6))
    plt.plot(newdf["close_date"], newdf["cumulative_pnl"], color="blue", linewidth=2)
    plt.title("Equity Curve - Strategy Performance")
    plt.xlabel("Date")
    plt.ylabel("Cumulative PnL ($)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{report_path}/equity_curve.png")
    plt.clf()
    logging.info("Equity curve graph generated and saved.")

    # 2. Drawdown Analysis Generation
    plt.figure(figsize=(10, 6))
    plt.plot(newdf["close_date"], drawdown, color="red", linewidth=2)
    plt.title("Drawdown Analysis")
    plt.xlabel("Date")
    plt.ylabel("Drawdown ($)")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{report_path}/drawdown.png")
    plt.clf()
    logging.info("Drawdown graph generated and saved.")

    # 3. PDF Report Generation
    today = datetime.now().strftime("%Y-%m-%d")
    pdf_file = f"{report_path}/risk_report.pdf"
    c = canvas.Canvas(pdf_file)

    # PDF Header
    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, "Strategy Performance Analysis")
    c.setFont("Helvetica", 10)
    c.drawString(100, 780, f"Date: {today}")

    # Summary Metrics Section
    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 750, "Summary Metrics")
    c.setFont("Helvetica", 12)
    c.drawString(110, 730, f"Total PnL: ${total_pnl:.2f}")
    c.drawString(110, 710, f"Annualized Sharpe Ratio: {sharpe_ratio:.2f}")
    c.drawString(110, 690, f"Max Drawdown: ${max_drawdown:.2f}")
    c.drawString(110, 670, f"Volatility (Daily): {volatility:.4f}")

    # Add Graphs to PDF
    c.drawImage(f"{report_path}/equity_curve.png", 50, 380, width=500, height=280)
    c.drawImage(f"{report_path}/drawdown.png", 50, 80, width=500, height=280)

    # PDF Footer
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(
        100,
        30,
        "Disclaimer: This report is generated automatically for backtesting purposes.",
    )

    c.save()
    logging.info(f"PDF report successfully saved at: {pdf_file}")

except Exception as e:
    logging.error(f"An error occurred while saving reports or graphs: {e}")

    