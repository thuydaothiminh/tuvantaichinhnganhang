import streamlit as st
import pandas as pd
from utils.financial_calc import recommend_packages
from utils.ai_advisor import ai_advice

st.set_page_config(page_title="AI Tư vấn tài chính gia đình", layout="wide")

# --- Sidebar lựa chọn vai trò ---
role = st.sidebar.radio("Bạn là:", ["👨‍👩‍👧‍👦 Khách hàng", "🏦 Cán bộ Agribank"])

if role == "👨‍👩‍👧‍👦 Khách hàng":
    st.title("💰 AI Tư vấn tài chính gia đình thông minh")

    col1, col2 = st.columns(2)
    with col1:
        income = st.number_input("Thu nhập hàng tháng (VNĐ)", min_value=0)
        expenses = st.number_input("Chi tiêu hàng tháng (VNĐ)", min_value=0)
        debt = st.number_input("Nợ hiện tại (VNĐ)", min_value=0)
    with col2:
        investment_goal = st.selectbox("Mục tiêu đầu tư", ["Mua nhà", "Mua xe", "Học tập", "Nông nghiệp", "Khác"])
        investment_amount = st.number_input("Số tiền mong muốn đầu tư (VNĐ)", min_value=0)
        duration = st.slider("Thời gian vay dự kiến (tháng)", 6, 60, 12)

    if st.button("🔍 Phân tích & tư vấn"):
        df_rates = pd.read_csv("data/interest_rates.csv")
        result = recommend_packages(income, expenses, debt, investment_amount, duration, df_rates)
        st.subheader("📊 Gợi ý tài chính & gói vay phù hợp:")
        st.dataframe(result)
        advice_text = ai_advice(income, expenses, debt, investment_goal, investment_amount, duration, df_rates)
        st.markdown(f"### 🤖 Lời khuyên AI:\n{advice_text}")

elif role == "🏦 Cán bộ Agribank":
    st.title("🏦 Quản lý lãi suất & gói vay Agribank")

    st.info("Nhập hoặc cập nhật dữ liệu lãi suất để hệ thống AI tư vấn chính xác hơn.")
    uploaded_file = st.file_uploader("Tải file CSV lãi suất mới", type=["csv"])
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        df.to_csv("data/interest_rates.csv", index=False)
        st.success("✅ Dữ liệu đã được cập nhật.")
    
    st.subheader("📈 Lãi suất hiện tại:")
    df_rates = pd.read_csv("data/interest_rates.csv")
    st.dataframe(df_rates)
