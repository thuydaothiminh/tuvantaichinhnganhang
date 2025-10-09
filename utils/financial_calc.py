import pandas as pd

def recommend_packages(income, expenses, debt, investment_amount, duration, df_rates):
    capacity = income - expenses - (debt * 0.05)
    if capacity <= 0:
        return pd.DataFrame([{"Khuyến nghị": "Không đủ khả năng vay. Cần giảm chi tiêu hoặc tăng thu nhập."}])
    
    best_rate = df_rates[df_rates["Ngân hàng"] == "Agribank"]["Lãi suất (%)"].min()
    monthly_payment = (investment_amount * (1 + best_rate / 100)) / duration
    return pd.DataFrame({
        "Gói vay đề xuất": ["Agribank Smart Loan"],
        "Số tiền vay": [f"{investment_amount:,.0f} VNĐ"],
        "Kỳ hạn (tháng)": [duration],
        "Lãi suất (%)": [best_rate],
        "Dự kiến trả hàng tháng": [f"{monthly_payment:,.0f} VNĐ"]
    })
