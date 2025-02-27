import numpy as np
import pandas as pd
from datetime import datetime
from typing import Dict, List, Tuple, Optional, Union

class FinancialCalculator:
    """
    A class that handles all financial calculations related to real estate investments.
    
    This calculator provides methods for:
    - ROI calculation
    - Cap rate calculation
    - Cash flow analysis
    - Mortgage analysis
    - Property value estimation
    - Investment return analysis
    """
    
    def __init__(self):
        """Initialize the FinancialCalculator with default values."""
        self.inflation_rate = 0.02  # Default annual inflation rate (2%)
        self.property_appreciation_rate = 0.03  # Default annual appreciation rate (3%)
    
    def set_economic_assumptions(self, inflation_rate: float = None, appreciation_rate: float = None) -> None:
        """
        Set global economic assumptions for calculations.
        
        Args:
            inflation_rate: Annual inflation rate as a decimal (e.g., 0.02 for 2%)
            appreciation_rate: Annual property appreciation rate as a decimal
        """
        if inflation_rate is not None:
            self.inflation_rate = inflation_rate
        if appreciation_rate is not None:
            self.property_appreciation_rate = appreciation_rate
    
    # === ROI and Return Calculations ===
    
    def calculate_roi(self, total_investment: float, annual_return: float) -> float:
        """
        Calculate the Return on Investment (ROI).
        
        Args:
            total_investment: Total amount invested in the property
            annual_return: Annual return from the property
            
        Returns:
            ROI as a decimal
        """
        if total_investment <= 0:
            raise ValueError("Total investment must be greater than zero")
        
        return annual_return / total_investment
    
    def calculate_cash_on_cash_return(self, annual_cash_flow: float, total_cash_invested: float) -> float:
        """
        Calculate the Cash-on-Cash Return.
        
        Args:
            annual_cash_flow: Annual cash flow from the property
            total_cash_invested: Total cash invested (down payment, closing costs, etc.)
            
        Returns:
            Cash-on-Cash Return as a decimal
        """
        if total_cash_invested <= 0:
            raise ValueError("Total cash invested must be greater than zero")
        
        return annual_cash_flow / total_cash_invested
    
    def calculate_cap_rate(self, noi: float, property_value: float) -> float:
        """
        Calculate the Capitalization Rate (Cap Rate).
        
        Args:
            noi: Annual Net Operating Income
            property_value: Current market value of the property
            
        Returns:
            Cap Rate as a decimal
        """
        if property_value <= 0:
            raise ValueError("Property value must be greater than zero")
        
        return noi / property_value
    
    # === Cash Flow Analysis ===
    
    def calculate_noi(self, annual_income: float, annual_expenses: float) -> float:
        """
        Calculate Net Operating Income (NOI).
        
        Args:
            annual_income: Total annual income from the property
            annual_expenses: Total annual operating expenses (excluding mortgage)
            
        Returns:
            Net Operating Income
        """
        return annual_income - annual_expenses
    
    def calculate_cash_flow(self, noi: float, annual_debt_service: float) -> float:
        """
        Calculate annual cash flow.
        
        Args:
            noi: Net Operating Income
            annual_debt_service: Annual mortgage payments
            
        Returns:
            Annual cash flow
        """
        return noi - annual_debt_service
    
    def calculate_monthly_cash_flow(self, monthly_income: float, monthly_expenses: float, 
                                monthly_mortgage: float) -> float:
        """
        Calculate monthly cash flow.
        
        Args:
            monthly_income: Monthly rental income
            monthly_expenses: Monthly expenses
            monthly_mortgage: Monthly mortgage payment
            
        Returns:
            Monthly cash flow
        """
        return monthly_income - monthly_expenses - monthly_mortgage
    
    # === Mortgage Analysis ===
    
    def calculate_mortgage_payment(self, loan_amount: float, interest_rate: float, 
                                loan_term_years: int) -> float:
        """
        Calculate monthly mortgage payment.
        
        Args:
            loan_amount: Total loan amount
            interest_rate: Annual interest rate as a decimal
            loan_term_years: Loan term in years
            
        Returns:
            Monthly mortgage payment
        """
        monthly_rate = interest_rate / 12
        num_payments = loan_term_years * 12
        
        if monthly_rate == 0:
            return loan_amount / num_payments
        
        return loan_amount * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
    
    def calculate_amortization_schedule(self, loan_amount: float, interest_rate: float, 
                                    loan_term_years: int) -> pd.DataFrame:
        """
        Generate an amortization schedule for a mortgage.
        
        Args:
            loan_amount: Total loan amount
            interest_rate: Annual interest rate as a decimal
            loan_term_years: Loan term in years
            
        Returns:
            DataFrame containing the amortization schedule
        """
        monthly_rate = interest_rate / 12
        num_payments = loan_term_years * 12
        monthly_payment = self.calculate_mortgage_payment(loan_amount, interest_rate, loan_term_years)
        
        schedule = []
        remaining_balance = loan_amount
        
        for payment_num in range(1, num_payments + 1):
            interest_payment = remaining_balance * monthly_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            
            schedule.append({
                'Payment': payment_num,
                'Payment Amount': monthly_payment,
                'Principal': principal_payment,
                'Interest': interest_payment,
                'Remaining Balance': max(0, remaining_balance)
            })
        
        return pd.DataFrame(schedule)
    
    def calculate_loan_to_value(self, loan_amount: float, property_value: float) -> float:
        """
        Calculate the Loan-to-Value (LTV) ratio.
        
        Args:
            loan_amount: Total loan amount
            property_value: Current property value
            
        Returns:
            LTV ratio as a decimal
        """
        if property_value <= 0:
            raise ValueError("Property value must be greater than zero")
        
        return loan_amount / property_value
    
    # === Property Value Estimation ===
    
    def estimate_future_value(self, current_value: float, years: int, 
                        appreciation_rate: float = None) -> float:
        """
        Estimate the future value of a property.
        
        Args:
            current_value: Current property value
            years: Number of years in the future
            appreciation_rate: Annual appreciation rate as a decimal (defaults to class value)
            
        Returns:
            Estimated future property value
        """
        if appreciation_rate is None:
            appreciation_rate = self.property_appreciation_rate
        
        return current_value * ((1 + appreciation_rate) ** years)
    
    def calculate_value_by_comps(self, comp_properties: List[Dict], 
                            subject_property: Dict) -> float:
        """
        Estimate property value based on comparable properties.
        
        Args:
            comp_properties: List of comparable properties with their details and prices
            subject_property: Details of the subject property
            
        Returns:
            Estimated value of the subject property
        """
        if not comp_properties:
            raise ValueError("At least one comparable property is required")
        
        # Simple average of comparable properties (in a real application, this would be more sophisticated)
        total_value = sum(prop['price'] for prop in comp_properties)
        return total_value / len(comp_properties)
    
    # === Investment Analysis ===
    
    def calculate_irr(self, initial_investment: float, cash_flows: List[float]) -> float:
        """
        Calculate the Internal Rate of Return (IRR) for an investment.
        
        Args:
            initial_investment: Initial cash outlay
            cash_flows: List of future cash flows (positive or negative)
            
        Returns:
            IRR as a decimal
        """
        # Convert to numpy array and add initial investment as negative cash flow
        all_cash_flows = np.array([-initial_investment] + cash_flows)
        
        # Calculate IRR
        try:
            irr = np.irr(all_cash_flows)
            return irr
        except Exception:
            return None  # Return None if IRR cannot be calculated
    
    def calculate_break_even_point(self, purchase_price: float, monthly_income: float, 
                                monthly_expenses: float) -> float:
        """
        Calculate the break-even point in months.
        
        Args:
            purchase_price: Total purchase price
            monthly_income: Monthly income from the property
            monthly_expenses: Monthly expenses
            
        Returns:
            Number of months to break even
        """
        monthly_net = monthly_income - monthly_expenses
        
        if monthly_net <= 0:
            return float('inf')  # Will never break even
        
        return purchase_price / monthly_net
    
    def calculate_cash_flow_projection(self, initial_investment: float, annual_income: float, 
                                    annual_expenses: float, mortgage_payment: float, 
                                    years: int) -> pd.DataFrame:
        """
        Project cash flows for a real estate investment over time.
        
        Args:
            initial_investment: Initial cash investment
            annual_income: First year annual income
            annual_expenses: First year annual expenses
            mortgage_payment: Annual mortgage payment (fixed)
            years: Number of years to project
            
        Returns:
            DataFrame with projected cash flows
        """
        projection = []
        
        for year in range(1, years + 1):
            # Apply inflation to income and expenses
            income = annual_income * ((1 + self.inflation_rate) ** (year - 1))
            expenses = annual_expenses * ((1 + self.inflation_rate) ** (year - 1))
            
            noi = income - expenses
            cash_flow = noi - mortgage_payment
            
            projection.append({
                'Year': year,
                'Income': income,
                'Expenses': expenses,
                'NOI': noi,
                'Mortgage Payment': mortgage_payment,
                'Cash Flow': cash_flow,
                'Cumulative Cash Flow': cash_flow if year == 1 else 
                                    projection[-1]['Cumulative Cash Flow'] + cash_flow
            })
        
        return pd.DataFrame(projection)
    
    def calculate_total_return(self, purchase_price: float, sale_price: float, 
                            total_income: float, total_expenses: float) -> float:
        """
        Calculate the total return on investment.
        
        Args:
            purchase_price: Original purchase price
            sale_price: Final sale price
            total_income: Total income over the holding period
            total_expenses: Total expenses over the holding period
            
        Returns:
            Total return as a decimal
        """
        equity_gain = sale_price - purchase_price
        net_income = total_income - total_expenses
        total_return = (equity_gain + net_income) / purchase_price
        
        return total_return
    
    def analyze_investment(self, property_data: Dict) -> Dict:
        """
        Comprehensive analysis of a real estate investment.
        
        Args:
            property_data: Dictionary containing all property information
            
        Returns:
            Dictionary with analysis results
        """
        results = {}
        
        # Extract key values
        purchase_price = property_data.get('purchase_price', 0)
        property_value = property_data.get('current_value', purchase_price)
        down_payment = property_data.get('down_payment', 0)
        loan_amount = purchase_price - down_payment
        interest_rate = property_data.get('interest_rate', 0.04)
        loan_term = property_data.get('loan_term_years', 30)
        annual_income = property_data.get('annual_income', 0)
        annual_expenses = property_data.get('annual_expenses', 0)
        
        # Basic calculations
        monthly_mortgage = self.calculate_mortgage_payment(loan_amount, interest_rate, loan_term)
        annual_mortgage = monthly_mortgage * 12
        noi = self.calculate_noi(annual_income, annual_expenses)
        annual_cash_flow = self.calculate_cash_flow(noi, annual_mortgage)
        cap_rate = self.calculate_cap_rate(noi, property_value)
        cash_on_cash = self.calculate_cash_on_cash_return(annual_cash_flow, down_payment)
        
        # Compile results
        results['monthly_mortgage'] = monthly_mortgage
        results['annual_mortgage'] = annual_mortgage
        results['noi'] = noi
        results['annual_cash_flow'] = annual_cash_flow
        results['monthly_cash_flow'] = annual_cash_flow / 12
        results['cap_rate'] = cap_rate
        results['cash_on_cash_return'] = cash_on_cash
        results['loan_to_value'] = self.calculate_loan_to_value(loan_amount, property_value)
        
        # Future projections
        if property_data.get('holding_period_years'):
            years = property_data['holding_period_years']
            results['future_value'] = self.estimate_future_value(property_value, years)
            
            # Create cash flow projection
            results['cash_flow_projection'] = self.calculate_cash_flow_projection(
                down_payment, annual_income, annual_expenses, annual_mortgage, years
            )
            
            # Calculate projected returns
            projected_cash_flows = results['cash_flow_projection']['Cash Flow'].tolist()
            final_value = results['future_value']
            final_loan_balance = self.calculate_amortization_schedule(
                loan_amount, interest_rate, loan_term
            ).iloc[min(years * 12 - 1, loan_term * 12 - 1)]['Remaining Balance']
            
            # Add sale proceeds to final year cash flow
            equity_at_sale = final_value - final_loan_balance
            projected_cash_flows[-1] += equity_at_sale - down_payment
            
            results['irr'] = self.calculate_irr(down_payment, projected_cash_flows)
        
        return results

