import streamlit as st
import pandas as pd
import sys, os
import plotly.express as px

# Bảo đảm Python nhận diện thư mục utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
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
        import os
        if os.path.exists("data/interest_rates.xlsx"):
         df_rates = pd.read_excel("data/interest_rates.xlsx")
        else:
        st.warning("⚠️ Chưa có file lãi suất. Vui lòng upload file Excel để bắt đầu.")
        df_rates = pd.DataFrame(columns=["Ngân hàng", "Sản phẩm vay", "Lãi suất (%)", "Ghi chú"])

        result = recommend_packages(income, expenses, debt, investment_amount, duration, df_rates)
        st.subheader("📊 Gợi ý tài chính & gói vay phù hợp:")
        st.dataframe(result)

        # --- Biểu đồ so sánh lãi suất Big4 ---
        fig = px.bar(df_rates, x="Ngân hàng", y="Lãi suất (%)",
                     color="Ngân hàng", text="Lãi suất (%)",
                     title="So sánh lãi suất giữa Big4 ngân hàng")
        fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
        fig.update_layout(yaxis_title="Lãi suất (%)", xaxis_title="Ngân hàng", showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        advice_text = ai_advice(income, expenses, debt, investment_goal, investment_amount, duration, df_rates)
        st.markdown(f"### 🤖 Lời khuyên AI:\n{advice_text}")

elif role == "🏦 Cán bộ Agribank":
    st.title("🏦 Quản lý lãi suất & gói vay Agribank")

    st.info("Nhập hoặc cập nhật dữ liệu lãi suất để hệ thống AI tư vấn chính xác hơn.")
    uploaded_file = st.file_uploader("Tải file lãi suất mới (Excel)", type=["xlsx", "xls"])
if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        df.to_excel("data/interest_rates.xlsx", index=False)
        st.success("✅ Dữ liệu Excel đã được cập nhật thành công.")
    except Exception as e:
        st.error(f"❌ Lỗi khi đọc file Excel: {e}")

        
        # Ghi đè lại file trong thư mục data
        df.to_csv("data/interest_rates.xlsx", index=False)
        st.success(f"✅ Dữ liệu đã được cập nhật (mã hóa: {encoding_used}).")
    
    st.subheader("📈 Lãi suất hiện tại:")
    df_rates = pd.read_csv("data/interest_rates.xlsx")
    st.dataframe(df_rates)

    # Biểu đồ trực quan lãi suất Big4
    import plotly.express as px
    fig = px.bar(df_rates, x="Ngân hàng", y="Lãi suất (%)",
                 color="Ngân hàng", text="Lãi suất (%)",
                 title="Biểu đồ lãi suất các ngân hàng")
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

