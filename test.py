import streamlit as st

# App Title
st.title("Simple Calculator")

# 1. Number inputs for two values
num1 = st.number_input("Enter first number:", value=0.0, format="%.2f")
num2 = st.number_input("Enter second number:", value=0.0, format="%.2f")

# 2. Operation selector (Add, Subtract, Multiply, Divide)
operation = st.selectbox(
    "Choose operation:",
    ["Add", "Subtract", "Multiply", "Divide"]
)

# 3. Display the result when button is clicked
if st.button("Calculate"):
    if operation == "Add":
        result = num1 + num2
        st.success(f"Result: {num1} + {num2} = {result}")

    elif operation == "Subtract":
        result = num1 - num2
        st.success(f"Result: {num1} - {num2} = {result}")

    elif operation == "Multiply":
        result = num1 * num2
        st.success(f"Result: {num1} * {num2} = {result}")

    elif operation == "Divide":
        if num2 != 0:
            result = num1 / num2
            st.success(f"Result: {num1} / {num2} = {result}")
        else:
            st.error("Error: Cannot divide by zero!")
