
import subprocess
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "validated_sales.csv"
REPORT_FILE = BASE_DIR / "sales_report.xlsx"
REPORT_SCRIPT = BASE_DIR / "sales_report.py"

st.set_page_config(
    page_title="Sales Report Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Sales Report Assistant")
st.caption("Explore your sales data and generate Excel reports.")

if not DATA_FILE.exists():
    st.error(
        "validated_sales.csv was not found. "
        "Run csv_processor.py first to validate your sales.csv file."
    )
    st.stop()

try:
    df = pd.read_csv(DATA_FILE)
except Exception as exc:
    st.error(f"Could not read the sales data: {exc}")
    st.stop()

required_columns = {"Product", "Quantity", "Price"}

if not required_columns.issubset(df.columns):
    st.error(
        "The CSV must contain these columns: "
        "Product, Quantity, Price."
    )
    st.stop()

df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df = df.dropna(subset=["Product", "Quantity", "Price"]).copy()
df = df[(df["Quantity"] > 0) & (df["Price"] >= 0)].copy()
df["Revenue"] = df["Quantity"] * df["Price"]

if df.empty:
    st.warning("There are no valid sales records to analyze.")
    st.stop()

total_revenue = df["Revenue"].sum()
total_units = df["Quantity"].sum()
record_count = len(df)
product_revenue = df.groupby("Product")["Revenue"].sum()
product_units = df.groupby("Product")["Quantity"].sum()

# Dashboard
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"₹{total_revenue:,.2f}")
col2.metric("Units Sold", f"{total_units:,.0f}")
col3.metric("Valid Records", f"{record_count:,}")

st.subheader("Sales Details")
st.dataframe(df, use_container_width=True, hide_index=True)

st.subheader("Product-wise Revenue")
st.bar_chart(product_revenue.sort_values(ascending=False))

# Generate the Excel report using your existing script.
st.subheader("Excel Report")

if st.button("Generate Excel Report"):
    if not REPORT_SCRIPT.exists():
        st.error("sales_report.py was not found.")
    else:
        try:
            result = subprocess.run(
                [sys.executable, str(REPORT_SCRIPT)],
                cwd=str(BASE_DIR),
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                st.error("The Excel report could not be generated.")
                st.code(result.stderr or result.stdout)
            elif REPORT_FILE.exists():
                st.success("Excel report generated successfully.")
            else:
                st.error(
                    "The script ran but sales_report.xlsx "
                    "was not created."
                )
        except subprocess.TimeoutExpired:
            st.error("Report generation took too long.")
        except Exception as exc:
            st.error(f"Error generating report: {exc}")

if REPORT_FILE.exists():
    with open(REPORT_FILE, "rb") as report:
        st.download_button(
            label="Download Excel Report",
            data=report,
            file_name="sales_report.xlsx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "spreadsheetml.sheet"
            ),
        )

# Rule-based chat assistant
st.subheader("💬 Ask Questions About Your Sales")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input(
    "Try: What is my total revenue?"
)

if question:
    st.session_state.chat_history.append(
        {"role": "user", "content": question}
    )

    q = question.lower()
    answer = None

    if "help" in q or "what can i ask" in q:
        answer = (
            "You can ask about total revenue, total units sold, "
            "number of records, best-selling product, "
            "top revenue product, or a specific product."
        )

    elif "revenue" in q and (
        "total" in q or "overall" in q or "all sales" in q
    ):
        answer = f"Total sales revenue is ₹{total_revenue:,.2f}."

    elif "record" in q or "number of sales" in q:
        answer = f"There are {record_count} valid sales records."

    elif "unit" in q or "quantity" in q or "how many sold" in q:
        answer = f"Total units sold: {total_units:,.0f}."

    elif (
        ("most" in q or "highest" in q or "top" in q
         or "best" in q)
        and ("revenue" in q or "earning" in q or "sales" in q)
    ):
        top_product = product_revenue.idxmax()
        answer = (
            f"**{top_product}** generated the highest revenue: "
            f"₹{product_revenue.max():,.2f}."
        )

    elif "lowest" in q or "least revenue" in q:
        low_product = product_revenue.idxmin()
        answer = (
            f"**{low_product}** generated the lowest revenue: "
            f"₹{product_revenue.min():,.2f}."
        )

    else:
        # Match a product name from the data.
        matched_product = next(
            (
                product for product in product_revenue.index
                if str(product).lower() in q
            ),
            None,
        )

        if matched_product is not None:
            answer = (
                f"**{matched_product}**\n\n"
                f"- Revenue: ₹"
                f"{product_revenue[matched_product]:,.2f}\n"
                f"- Units sold: "
                f"{product_units[matched_product]:,.0f}"
            )
        else:
            answer = (
                "I couldn't identify that question. Try asking "
                "'What is my total revenue?', "
                "'Which product generated the highest revenue?', "
                "'How many units were sold?', or "
                "'What are the sales for Laptop?'"
            )

    st.session_state.chat_history.append(
        {"role": "assistant", "content": answer}
    )

    st.rerun()
