# Trade Performance & Risk Analytics

This repository contains a professional-grade automation tool designed to transform raw trading logs into audit-ready financial risk reports. By calculating institutional metrics like the Sharpe Ratio and Maximum Drawdown, it bridges the gap between raw execution data and portfolio management insights.

# 📌 Problem & Solution
Raw trade logs in Excel format are often difficult to interpret for risk management. Without visualizing the "Equity Curve" or calculating risk-adjusted returns, traders cannot accurately assess if a strategy is truly profitable or simply over-leveraged during volatile periods.

This automation bot:

Eliminates manual data processing by automatically calculating PnL, fees, and cumulative returns from Excel transaction logs.

Enforces data integrity through robust validation and cleanup of missing fees or inconsistent date formats.

Automates quantitative risk assessment by modeling the Annualized Sharpe Ratio and volatility metrics.

Streamlines investor relations and internal audits by generating standardized PDF reports with high-fidelity equity and drawdown visualizations.

# 🛠 Tech Stack
**Python:** Core analytical engine and automation orchestration.

**Pandas:** For advanced time-series aggregation and data manipulation.

**NumPy:** For vectorized numerical operations and risk metric modeling.

**Matplotlib**: To generate high-fidelity Equity Curve and Drawdown charts.

**ReportLab:** For programmatic generation of professional, audit-ready PDF reports.

**Logging:** To track the data processing pipeline and capture execution flow.

# ⚙️ Core Automation Workflow
**Ingestion & Validation:** Loads trade data from Excel and enforces strict numeric/datetime type conversions.

**Quantitative Analysis:** Groups trades by date to calculate daily returns, cumulative PnL, and volatility.

**Risk Modeling:** Computes the Annualized Sharpe Ratio and identifies the Maximum Drawdown (underwater periods).

**Visual Reporting:** Generates performance charts and compiles all metrics into a final, portable PDF report.

# 📊 Example Output
Upon execution, the bot provides real-time logs and generates professional documents in the reports/ directory:

```
INFO - Excel file loaded successfully
INFO - Data types converted successfully.
INFO - Rows before cleanup: 36, after cleanup: 36
INFO - Sharpe Ratio calculated: 4.45
INFO - Equity curve graph generated and saved.
INFO - Drawdown graph generated and saved.
INFO - PDF report successfully saved at: reports/risk_report.pdf
```

# 🚀 How to Run
1. Place your trading log in data/trades.xlsx.

2. Install dependencies:

```
pip install -r requirements.txt
```

3. Run the automation:

```
python src/trade_risk_analyzer.py
```
