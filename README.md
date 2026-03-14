# Trade Performance & Risk Analytics (Excel → PDF)

## Project Objective
This project automates the end-to-end analysis of trading logs, transforming raw Excel transaction data into professional, audit-ready financial performance reports. By calculating institutional-grade risk metrics such as the Sharpe Ratio and Maximum Drawdown, the tool provides a comprehensive overview of a strategy's risk-adjusted returns. It aims to bridge the gap between raw execution data and high-level portfolio management insights through automated visualization and PDF reporting.

## Technologies Used

**Python:** Core programming language used for the analytical engine and automation.

**Pandas:** For advanced data manipulation, time-series aggregation, and PnL calculation.

**NumPy:** Used for vectorized numerical operations and risk metric modeling.

**Matplotlib:** For generating high-fidelity Equity Curve and Drawdown charts.

**ReportLab:** For programmatic generation of professional PDF performance reports.

**Logging:** To ensure transparency in the data processing pipeline and capture runtime execution flow.

## How to Run

1. Ensure the required Python libraries are installed:

pip install -r requirements.txt

2. Prepare Data: Place your trading log in data/trades.xlsx.

3. Run the script:

python src/trade_risk_analyzer.py

4. Review Output: After execution, check the reports/ directory for the generated equity_curve.png, drawdown.png, and the final risk_report.pdf.

## Why This Is Valuable for a Hedge Fund

- Quantitative Risk Assessment: Automatically calculates the Annualized Sharpe Ratio, allowing portfolio managers to evaluate returns relative to volatility.

- Drawdown Management: Visualizes "Underwater" periods (Drawdowns) to identify the strategy's worst-case historical loss scenarios and recovery times.

- Automated Reporting Cycle: Eliminates manual reporting tasks by generating standardized PDF summaries, essential for daily internal audits or investor relations.

- Data Integrity: Includes robust validation and cleanup logic to handle missing fees or inconsistent date formats, ensuring that risk metrics are based on high-quality, sanitized data.
