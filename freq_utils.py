import streamlit as st
import pandas as pd

st.title("BMI Calculator App")

# User input
height = st.number_input("Enter Height (meters):", min_value=0.5, max_value=2.5, step=0.01)
weight = st.number_input("Enter Weight (kg):", min_value=1.0, max_value=300.0, step=0.1)

# Function to calculate BMI
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

# Function to determine status
def bmi_status(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Good"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Function to give improvement tips
def bmi_improvement_tips(status):
    if status == "Underweight":
        return (
            "• Increase calorie intake with nutritious foods\n"
            "• Eat more protein-rich foods\n"
            "• Include strength training exercises\n"
            "• Maintain a regular meal schedule"
        )
    elif status == "Good":
        return (
            "• Maintain a balanced diet\n"
            "• Continue regular physical activity\n"
            "• Stay hydrated\n"
            "• Get adequate sleep"
        )
    elif status == "Overweight":
        return (
            "• Reduce sugary and fried foods\n"
            "• Increase physical activity\n"
            "• Practice portion control\n"
            "• Eat more fruits and vegetables"
        )
    else:
        return (
            "• Follow a calorie-controlled diet\n"
            "• Engage in daily exercise (walking, cardio)\n"
            "• Avoid processed foods\n"
            "• Consult a healthcare professional if needed"
        )

# When user clicks button
if st.button("Calculate BMI"):
    bmi = calculate_bmi(weight, height)
    status = bmi_status(bmi)

    # Create table
    df = pd.DataFrame({
        "Height (m)": [height],
        "Weight (kg)": [weight],
        "BMI": [bmi],
        "Status": [status]
    })

    st.success("BMI Calculated Successfully!")
    st.table(df)

    # Store status for improvement button
    st.session_state["bmi_status"] = status

# Improvement button
if "bmi_status" in st.session_state:
    if st.button("How to Improve BMI"):
        tips = bmi_improvement_tips(st.session_state["bmi_status"])
        st.info("### BMI Improvement Tips")
        st.text(tips)