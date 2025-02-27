import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

from property_analyzer import PropertyAnalyzer
from financial_calculator import FinancialCalculator
from risk_assessment import RiskAssessor
from utils import load_data, save_data

# Set page configuration
st.set_page_config(
    page_title="Real Estate Investment Analyzer",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS for better styling
st.markdown("""
<style>
.main-header {
    font-size: 2.5rem;
    color: #1E88E5;
    text-align: center;
}
.section-header {
    font-size: 1.5rem;
    color: #0D47A1;
    margin-top: 1rem;
}
.metric-card {
    background-color: #f0f2f6;
    border-radius: 10px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.recommendation {
    background-color: #e3f2fd;
    border-left: 5px solid #1E88E5;
    padding: 1rem;
    margin: 1rem 0;
}
.risk-high {color: #d32f2f;}
.risk-medium {color: #f57c00;}
.risk-low {color: #388e3c;}
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">Real Estate Investment Analyzer</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    
    # Load saved properties
    saved_properties = load_data()
    
    page = st.sidebar.selectbox(
        "Choose a section",
        ["Property Input", "Financial Analysis", "Risk Assessment", "Investment Summary"]
    )
    
    # Initialize session state for property data
    if 'property_data' not in st.session_state:
        st.session_state.property_data = {
            'purchase_price': 0,
            'property_type': '',
            'location': '',
            'square_footage': 0,
            'year_built': 0,
            'bedrooms': 0,
            'bathrooms': 0,
            'rental_income': 0,
            'property_tax': 0,
            'insurance': 0,
            'maintenance': 0,
            'utilities': 0,
            'vacancy_rate': 5.0,
            'property_management': 0,
            'loan_amount': 0,
            'interest_rate': 0.0,
            'loan_term': 30,
            'closing_costs': 0,
            'renovation_costs': 0,
            'appreciation_rate': 3.0,
            'neighborhood_growth': 'moderate',
            'job_market': 'stable',
            'crime_rate': 'low',
            'school_quality': 'good',
        }
    
    # Load property if selected
    property_names = list(saved_properties.keys())
    if property_names:
        st.sidebar.markdown("---")
        st.sidebar.subheader("Saved Properties")
        selected_property = st.sidebar.selectbox("Select a property", property_names)
        
        if st.sidebar.button("Load Property"):
            st.session_state.property_data = saved_properties[selected_property]
            st.success(f"Loaded property: {selected_property}")
    
    if page == "Property Input":
        display_property_input()
    elif page == "Financial Analysis":
        display_financial_analysis()
    elif page == "Risk Assessment":
        display_risk_assessment()
    elif page == "Investment Summary":
        display_investment_summary()

def display_property_input():
    st.markdown('<h2 class="section-header">Property Details</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Information")
        st.session_state.property_data['property_name'] = st.text_input("Property Name (for saving)", 
                                                                        st.session_state.property_data.get('property_name', ''))
        st.session_state.property_data['purchase_price'] = st.number_input("Purchase Price ($)", 
                                                                        value=float(st.session_state.property_data['purchase_price']), 
                                                                        min_value=0.0, step=1000.0)
        st.session_state.property_data['property_type'] = st.selectbox("Property Type", 
                                                                    ["Single Family", "Multi-Family", "Condo", "Townhouse", "Commercial"], 
                                                                    index=["Single Family", "Multi-Family", "Condo", "Townhouse", "Commercial"].index(st.session_state.property_data['property_type']) if st.session_state.property_data['property_type'] in ["Single Family", "Multi-Family", "Condo", "Townhouse", "Commercial"] else 0)
        st.session_state.property_data['location'] = st.text_input("Location (City, State)", st.session_state.property_data['location'])
        st.session_state.property_data['square_footage'] = st.number_input("Square Footage", 
                                                                        value=int(st.session_state.property_data['square_footage']), 
                                                                        min_value=0, step=100)
        st.session_state.property_data['year_built'] = st.number_input("Year Built", 
                                                                    value=int(st.session_state.property_data['year_built']) if st.session_state.property_data['year_built'] > 0 else 2000, 
                                                                    min_value=1800, max_value=datetime.now().year)
        st.session_state.property_data['bedrooms'] = st.number_input("Number of Bedrooms", 
                                                                    value=int(st.session_state.property_data['bedrooms']), 
                                                                    min_value=0, step=1)
        st.session_state.property_data['bathrooms'] = st.number_input("Number of Bathrooms", 
                                                                    value=float(st.session_state.property_data['bathrooms']), 
                                                                    min_value=0.0, step=0.5)
    
    with col2:
        st.subheader("Financial Information")
        st.session_state.property_data['rental_income'] = st.number_input("Monthly Rental Income ($)", 
                                                                        value=float(st.session_state.property_data['rental_income']), 
                                                                        min_value=0.0, step=100.0)
        st.session_state.property_data['property_tax'] = st.number_input("Annual Property Tax ($)", 
                                                                        value=float(st.session_state.property_data['property_tax']), 
                                                                        min_value=0.0, step=100.0)
        st.session_state.property_data['insurance'] = st.number_input("Annual Insurance ($)", 
                                                                    value=float(st.session_state.property_data['insurance']), 
                                                                    min_value=0.0, step=100.0)
        st.session_state.property_data['maintenance'] = st.number_input("Monthly Maintenance ($)", 
                                                                    value=float(st.session_state.property_data['maintenance']), 
                                                                    min_value=0.0, step=50.0)
        st.session_state.property_data['utilities'] = st.number_input("Monthly Utilities ($)", 
                                                                    value=float(st.session_state.property_data['utilities']), 
                                                                    min_value=0.0, step=50.0)
        st.session_state.property_data['vacancy_rate'] = st.slider("Vacancy Rate (%)", 
                                                                value=float(st.session_state.property_data['vacancy_rate']), 
                                                                min_value=0.0, max_value=20.0, step=0.5)
        st.session_state.property_data['property_management'] = st.number_input("Monthly Property Management ($)", 
                                                                            value=float(st.session_state.property_data['property_management']), 
                                                                            min_value=0.0, step=50.0)
    
    st.markdown('<h2 class="section-header">Financing Details</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.property_data['loan_amount'] = st.number_input("Loan Amount ($)", 
                                                                    value=float(st.session_state.property_data['loan_amount']), 
                                                                    min_value=0.0, step=1000.0)
        st.session_state.property_data['interest_rate'] = st.slider("Interest Rate (%)", 
                                                                value=float(st.session_state.property_data['interest_rate']), 
                                                                min_value=0.0, max_value=15.0, step=0.125)
        st.session_state.property_data['loan_term'] = st.selectbox("Loan Term (Years)", 
                                                                [15, 20, 30], 
                                                                index=[15, 20, 30].index(st.session_state.property_data['loan_term']) if st.session_state.property_data['loan_term'] in [15, 20, 30] else 2)
    
    with col2:
        st.session_state.property_data['closing_costs'] = st.number_input("Closing Costs ($)", 
                                                                        value=float(st.session_state.property_data['closing_costs']), 
                                                                        min_value=0.0, step=100.0)
        st.session_state.property_data['renovation_costs'] = st.number_input("Renovation Costs ($)", 
                                                                            value=float(st.session_state.property_data['renovation_costs']), 
                                                                            min_value=0.0, step=100.0)
        st.session_state.property_data['appreciation_rate'] = st.slider("Expected Annual Appreciation Rate (%)", 
                                                                    value=float(st.session_state.property_data['appreciation_rate']), 
                                                                    min_value=0.0, max_value=10.0, step=0.1)
    
    st.markdown('<h2 class="section-header">Location Factors</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.property_data['neighborhood_growth'] = st.selectbox("Neighborhood Growth", 
                                                                        ["declining", "stable", "moderate", "high"], 
                                                                        index=["declining", "stable", "moderate", "high"].index(st.session_state.property_data['neighborhood_growth']) if st.session_state.property_data['neighborhood_growth'] in ["declining", "stable", "moderate", "high"] else 2)
        st.session_state.property_data['job_market'] = st.selectbox("Job Market", 
                                                                ["poor", "fair", "stable", "excellent"], 
                                                                index=["poor", "fair", "stable", "excellent"].index(st.session_state.property_data['job_market']) if st.session_state.property_data['job_market'] in ["poor", "fair", "stable", "excellent"] else 2)
    
    with col2:
        st.session_state.property_data['crime_rate'] = st.selectbox("Crime Rate", 
                                                                ["high", "moderate", "low", "very low"], 
                                                                index=["high", "moderate", "low", "very low"].index(st.session_state.property_data['crime_rate']) if st.session_state.property_data['crime_rate'] in ["high", "moderate", "low", "very low"] else 2)
        st.session_state.property_data['school_quality'] = st.selectbox("School Quality", 
                                                                    ["poor", "fair", "good", "excellent"], 
                                                                    index=["poor", "fair", "good", "excellent"].index(st.session_state.property_data['school_quality']) if st.session_state.property_data['school_quality'] in ["poor", "fair", "good", "excellent"] else 2)
    
    st.markdown("---")
    
    if st.button("Save Property Data"):
        if 'property_name' in st.session_state.property_data and st.session_state.property_data['property_name']:
            save_data(st.session_state.property_data)
            st.success(f"Property data saved as: {st.session_state.property_data['property_name']}")
        else:
            st.error("Please enter a property name to save the data")

def display_financial_analysis():
    st.markdown('<h2 class="section-header">Financial Analysis</h2>', unsafe_allow_html=True)
    
    if not st.session_state.property_data['purchase_price']:
        st.warning("Please enter property details in the Property Input section first.")
        return
    
    # Create financial calculator instance
    calculator = FinancialCalculator(st.session_state.property_data)
    
    # Calculate financial metrics
    monthly_cash_flow = calculator.calculate_monthly_cash_flow()
    annual_cash_flow = calculator.calculate_annual_cash_flow()
    cap_rate = calculator.calculate_cap_rate()
    cash_on_cash_return = calculator.calculate_cash_on_cash_return()
    total_roi_5year = calculator.calculate_roi(5)
    total_roi_10year = calculator.calculate_roi(10)
    monthly_mortgage = calculator.calculate_mortgage_payment()
    break_even_point = calculator.calculate_break_even_point()
    

