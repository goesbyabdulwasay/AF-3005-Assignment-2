import streamlit as st
import pandas as pd
import plotly.express as px

# Initialize session state for storing subscriptions
if "subscriptions" not in st.session_state:
    st.session_state.subscriptions = []

# Title of the app
st.title("📊 Monthly Subscription Expense Tracker")

# User input form
with st.form("subscription_form"):
    col1, col2, col3 = st.columns([2, 1, 1])
    
    name = col1.text_input("Subscription Name", placeholder="Netflix, Spotify, Gym...")
    cost = col2.number_input("Cost (USD)", min_value=0.0, step=0.01)
    frequency = col3.selectbox("Billing Cycle", ["Monthly", "Yearly"])

    submitted = st.form_submit_button("Add Subscription")
    if submitted and name and cost > 0:
        st.session_state.subscriptions.append({"Name": name, "Cost": cost, "Frequency": frequency})

# Display the list of subscriptions
if st.session_state.subscriptions:
    df = pd.DataFrame(st.session_state.subscriptions)

    # Convert yearly costs to monthly
    df["Monthly Cost"] = df.apply(lambda x: x["Cost"] if x["Frequency"] == "Monthly" else x["Cost"] / 12, axis=1)
    
    # Display the table
    st.subheader("Your Subscriptions")
    st.dataframe(df[["Name", "Cost", "Frequency"]])

    # Calculate total expenses
    total_monthly = df["Monthly Cost"].sum()
    total_yearly = total_monthly * 12
    st.metric("💰 Total Monthly Expense", f"${total_monthly:.2f}")
    st.metric("💵 Total Yearly Expense", f"${total_yearly:.2f}")

    # Pie chart visualization
    fig = px.pie(df, values="Monthly Cost", names="Name", title="Subscription Cost Breakdown")
    st.plotly_chart(fig, use_container_width=True)

    # Remove subscription option
    to_remove = st.selectbox("Remove a subscription", ["None"] + df["Name"].tolist())
    if st.button("Remove"):
        st.session_state.subscriptions = [sub for sub in st.session_state.subscriptions if sub["Name"] != to_remove]
        st.experimental_rerun()
else:
    st.info("No subscriptions added yet. Start by adding one above!")
