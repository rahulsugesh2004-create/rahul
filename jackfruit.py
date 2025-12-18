import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import time

# ---------------- Page Config ---------------- #
st.set_page_config(page_title="BMI Health Analyzer", layout="centered")


# ---------------- Title ---------------- #
st.title("BMI Health Analyzer")
st.caption("Personalized BMI analysis with visual indicators")

# ---------------- User Details ---------------- #
st.subheader("👤 User Details")
col1, col2, col3 = st.columns(3)

with col1:
    name = st.text_input("Name")

with col2:
    age = st.number_input("Age", min_value=1, max_value=120, step=1)

with col3:
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

# ---------------- Body Inputs ---------------- #
st.subheader("📏 Body Measurements")
col4, col5 = st.columns(2)

with col4:
    height = st.number_input("Height (meters)", 0.5, 2.5, step=0.01)

with col5:
    weight = st.number_input("Weight (kg)", 1.0, 300.0, step=0.1)

# ---------------- Functions ---------------- #
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Healthy"
    elif bmi < 30:
        return "Overweight"
    else:
        return "High Risk"

def health_tips(status):
    tips = {
        "Underweight": [
            "Eat regular meals with nutritious foods",
            "Include protein-rich foods",
            "Maintain a consistent sleep routine",
            "Light strength activities can help"
        ],
        "Healthy": [
            "Maintain a balanced diet",
            "Stay physically active",
            "Drink enough water",
            "Get proper sleep"
        ],
        "Overweight": [
            "Reduce sugary and junk foods",
            "Increase daily physical activity",
            "Practice portion control",
            "Eat more fruits and vegetables"
        ],
        "High Risk": [
            "Focus on gradual lifestyle changes",
            "Avoid highly processed foods",
            "Include regular physical activity if possible",
            "Consult a healthcare professional"
        ]
    }
    return tips.get(status, [])

def animated_bmi_bar(target_bmi):
    target_bmi = min(max(target_bmi, 0), 40)
    placeholder = st.empty()

    for b in range(0, int(target_bmi) + 1):
        fig, ax = plt.subplots(figsize=(8, 2))

        ax.barh(0, 18.5, left=0, color="#f1c40f")
        ax.barh(0, 6.5, left=18.5, color="#2ecc71")
        ax.barh(0, 5, left=25, color="#e67e22")
        ax.barh(0, 10, left=30, color="#e74c3c")

        ax.annotate("▲", (b, 0), (b, 0.25), ha="center", fontsize=18)

        ax.set_xlim(0, 40)
        ax.set_yticks([])
        ax.set_xlabel("BMI Value")
        ax.set_title("BMI Health Indicator")

        for spine in ["top", "right", "left"]:
            ax.spines[spine].set_visible(False)

        placeholder.pyplot(fig)
        time.sleep(0.03)

def bmi_comparison_chart(user_bmi):
    fig, ax = plt.subplots()
    ax.bar(["Your BMI", "Healthy Max (24.9)"], [user_bmi, 24.9])
    ax.set_ylabel("BMI Value")
    ax.set_title("BMI Comparison Chart")
    st.pyplot(fig)

# ---------------- App Logic ---------------- #
if st.button("Calculate BMI"):

    if name.strip() == "":
        st.error("Please enter your name")
    else:
        bmi = calculate_bmi(weight, height)
        status = bmi_status(bmi)

        st.session_state["bmi_status"] = status
        st.session_state["show_tips"] = False

        df = pd.DataFrame({
            "Name": [name],
            "Age": [age],
            "Gender": [gender],
            "Height (m)": [height],
            "Weight (kg)": [weight],
            "BMI": [bmi],
            "Status": [status]
        })

        st.success("BMI calculated successfully")
        st.table(df)

        animated_bmi_bar(bmi)

        st.subheader("📊 BMI Comparison")
        bmi_comparison_chart(bmi)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download BMI Record (CSV)",
            csv,
            "bmi_record.csv",
            "text/csv"
        )

# ---------------- Health Tips Button ---------------- #
if "bmi_status" in st.session_state:

    if st.button("💡 Get Health Tips"):
        st.session_state["show_tips"] = True

    if st.session_state.get("show_tips"):
        st.subheader("💡 Health Tips")
        for tip in health_tips(st.session_state["bmi_status"]):
            st.markdown(f"- {tip}")

# ---------------- Legend ---------------- #
st.markdown("### 📘 BMI Legend")
st.markdown(
    """
    🟨 **Underweight**: BMI < 18.5  
    🟩 **Healthy**: 18.5 – 24.9  
    🟧 **Overweight**: 25 – 29.9  
    🟥 **High Risk**: BMI ≥ 30  
    """
)