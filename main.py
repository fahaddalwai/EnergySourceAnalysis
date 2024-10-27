import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.title("Electricity Carbon Intensity and Power Breakdown Analysis")
st.sidebar.header("API Key and Region")

api_key = st.sidebar.text_input("ElectricityMap API Key", type="password")
region = st.sidebar.text_input("Region (e.g., FR)")

def fetch_data(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch data.")
        return None

if api_key and region:
    headers = {"auth-token": api_key}

    # Fetch Latest Carbon Intensity Data
    carbon_intensity_url = f"https://api.electricitymap.org/v3/carbon-intensity/latest?zone={region}"
    carbon_intensity_data = fetch_data(carbon_intensity_url, headers)

    if carbon_intensity_data:
        st.write("### Latest Carbon Intensity")
        st.write(f"Carbon Intensity: {carbon_intensity_data.get('carbonIntensity', 'N/A')} gCO₂/kWh")
        st.write(f"Date and Time: {carbon_intensity_data.get('datetime', 'N/A')}")
        st.write(f"Emission Factor Type: {carbon_intensity_data.get('emissionFactorType', 'N/A')}")

    # Fetch Latest Power Breakdown Data
    power_breakdown_url = f"https://api.electricitymap.org/v3/power-breakdown/latest?zone={region}"
    power_breakdown_data = fetch_data(power_breakdown_url, headers)

    if power_breakdown_data:
        st.write("### Latest Power Breakdown")

        # Extract and display power consumption breakdown
        consumption_breakdown = power_breakdown_data.get('powerConsumptionBreakdown', {})
        consumption_df = pd.DataFrame(consumption_breakdown.items(), columns=['Source', 'Power Consumption (MW)'])
        st.write(consumption_df)

        # Plot Power Consumption Breakdown
        fig, ax = plt.subplots()
        consumption_df.set_index('Source').plot(kind='bar', ax=ax)
        ax.set_ylabel("Power Consumption (MW)")
        ax.set_title("Power Consumption Breakdown")
        st.pyplot(fig)

        # Extract and display power production breakdown
        production_breakdown = power_breakdown_data.get('powerProductionBreakdown', {})
        production_df = pd.DataFrame(production_breakdown.items(), columns=['Source', 'Power Production (MW)'])
        st.write(production_df)

        # Plot Power Production Breakdown
        fig, ax = plt.subplots()
        production_df.set_index('Source').plot(kind='bar', ax=ax)
        ax.set_ylabel("Power Production (MW)")
        ax.set_title("Power Production Breakdown")
        st.pyplot(fig)

        # Display Total Power Consumption and Production
        st.write(f"Total Power Consumption: {power_breakdown_data.get('powerConsumptionTotal', 'N/A')} MW")
        st.write(f"Total Power Production: {power_breakdown_data.get('powerProductionTotal', 'N/A')} MW")
else:
    st.info("Enter your API key and region code to fetch data.")
