import streamlit as st

def calculate_updated_tax(income, exemption=100_000_000):
    taxable_income = max(0, income - exemption)
    tax = 0
    breakdown = []

    brackets = [
        (200_000_000, 0.15),
        (400_000_000, 0.20),
        (float('inf'), 0.25)
    ]

    remaining_income = taxable_income
    previous_cap = 0

    for cap, rate in brackets:
        bracket_amount = min(cap - previous_cap, remaining_income)
        if bracket_amount <= 0:
            break
        bracket_tax = bracket_amount * rate
        tax += bracket_tax
        breakdown.append({
            "درآمد مشمول در این پله": f"{bracket_amount:,.0f} تومان",
            "نرخ": f"{int(rate*100)}٪",
            "مالیات این پله": f"{bracket_tax:,.0f} تومان"
        })
        remaining_income -= bracket_amount
        previous_cap = cap

    return tax, taxable_income, breakdown

def main():
    st.set_page_config(page_title="محاسبه‌گر مالیات اشخاص حقیقی", layout="centered")
    st.title("محاسبه‌گر مالیات اشخاص حقیقی (ماده ۱۳۱)")
    st.markdown("**بر اساس اصلاحیه اخیر قانون مالیات‌های مستقیم**")

    income = st.number_input("درآمد سالانه (تومان):", min_value=0, step=1_000_000)

    if st.button("محاسبه"):
        tax, taxable_income, breakdown = calculate_updated_tax(income)
        st.success(f"درآمد مشمول مالیات: {taxable_income:,.0f} تومان")
        st.success(f"مالیات قابل پرداخت: {tax:,.0f} تومان")

        st.subheader("جزئیات پله‌ای:")
        for row in breakdown:
            st.write(f"{row['درآمد مشمول در این پله']} × {row['نرخ']} = {row['مالیات این پله']}")

if __name__ == "__main__":
    main()
