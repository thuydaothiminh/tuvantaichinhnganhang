def ai_advice(income, expenses, debt, goal, invest_amt, duration, df_rates):
    agr_rate = df_rates[df_rates["Ngân hàng"] == "Agribank"]["Lãi suất (%)"].min()
    msg = f"""
Khách hàng có thu nhập {income:,} VNĐ/tháng và chi tiêu {expenses:,} VNĐ/tháng. 
Với mục tiêu '{goal}', hệ thống đề xuất:
- Khoản vay: {invest_amt:,} VNĐ trong {duration} tháng.
- Ưu tiên gói Agribank với lãi suất {agr_rate}%/năm.
- Dự kiến trả khoảng {(invest_amt*(1+agr_rate/100)/duration):,.0f} VNĐ/tháng.
So sánh nhanh: Agribank đang cạnh tranh hơn {df_rates['Lãi suất (%)'].mean()-agr_rate:.2f}% so với trung bình Big4.

🎯 Khuyến nghị: Nên chọn gói Agribank Smart Loan để tối ưu chi phí và hưởng ưu đãi KH thân thiết.
"""
    return msg
