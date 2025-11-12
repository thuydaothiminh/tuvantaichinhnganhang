import streamlit as st
import pandas as pd
import sys, os
import plotly.express as px
import chardet

# Bảo đảm Python nhận diện thư mục utils
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils.financial_calc import recommend_packages
from utils.ai_advisor import ai_advice

st.set_page_config(page_title="AI Tư vấn tài chính gia đình", layout="wide")

# --- Sidebar lựa chọn vai trò ---
role = st.sidebar.radio("Bạn là:", ["👨‍👩‍👧‍👦 Khách hàng", "🏦 Cán bộ Agribank"])

# ==========================================
# 1️⃣ Vai trò KHÁCH HÀNG
# ==========================================
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

    # --- Nút bấm phân tích ---
    if st.button("🔍 Phân tích & Gợi ý bằng AI"):
        st.subheader("📊 Kết quả phân tích tài chính cá nhân")

        savings_rate = round(((income - expenses) / income) * 100, 2) if income > 0 else 0
        debt_ratio = round((debt / income) * 100, 2) if income > 0 else 0

        # Gợi ý
        if savings_rate < 10:
            suggestion = "💡 Mức tiết kiệm còn thấp. Hãy xem xét cắt giảm chi tiêu hoặc tăng thu nhập phụ."
        elif savings_rate < 25:
            suggestion = "✅ Mức tiết kiệm khá ổn. Nên bắt đầu gửi tiết kiệm có kỳ hạn hoặc đầu tư an toàn."
        else:
            suggestion = "🏆 Tuyệt vời! Bạn có thể xem xét các gói đầu tư dài hạn hoặc trái phiếu Agribank."

        # Gợi ý sản phẩm
        if investment_goal == "Tích lũy":
            product = "🎁 Gói tiết kiệm linh hoạt Agribank – Lãi suất ~5.5%/năm."
        elif investment_goal == "Đầu tư":
            product = "📈 Gói đầu tư Agribank – Cổ phiếu ngân hàng & trái phiếu doanh nghiệp uy tín."
        elif investment_goal == "Mua nhà":
            product = "🏠 Gói vay mua nhà Agribank – Lãi suất ưu đãi chỉ từ 6.5%/năm."
        elif investment_goal == "Trả nợ":
            product = "🧾 Gói tái cấu trúc nợ – Gia hạn 6–12 tháng, lãi suất hỗ trợ thấp hơn 1.2%."
        else:
            product = "🌱 Gói tiết kiệm hưu trí thông minh – tích lũy an toàn, lãi suất hấp dẫn."

        st.write(f"**Tỷ lệ tiết kiệm hiện tại:** {savings_rate}%")
        st.write(f"**Tỷ lệ nợ trên thu nhập:** {debt_ratio}%")
        st.success(suggestion)
        st.info(product)

# ==========================================
# 2️⃣ Vai trò CÁN BỘ AGRIBANK
# ==========================================
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

        st.subheader("📈 Lãi suất hiện tại:")
        df_rates = pd.read_excel("data/interest_rates.xlsx")
        st.dataframe(df_rates)

    # Biểu đồ trực quan lãi suất Big4
    import plotly.express as px
    fig = px.bar(df_rates, x="Ngân hàng", y="Lãi suất (%)",
                 color="Ngân hàng", text="Lãi suất (%)",
                 title="Biểu đồ lãi suất các ngân hàng")
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

