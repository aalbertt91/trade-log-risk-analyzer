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
