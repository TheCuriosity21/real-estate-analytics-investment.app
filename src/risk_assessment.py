"""
Risk Assessment Module for Real Estate Analytics Application.

This module provides functionality to assess various types of risks associated
with real estate investments, including market risks, location risks, and
financial risks. It generates risk scores and investment recommendations.
"""

import numpy as np
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional


class RiskAssessor:
    """Class for assessing various risks in real estate investments."""
    
    def __init__(self):
        # Risk weighting factors (can be adjusted based on market conditions)
        self.risk_weights = {
            'market_risk': 0.3,
            'location_risk': 0.3,
            'financial_risk': 0.25,
            'property_risk': 0.15,
        }
        
        # Risk threshold levels
        self.risk_thresholds = {
            'low': 3.0,
            'medium': 6.0,
            'high': 8.0
        }
    
    def assess_market_risk(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess market-related risk factors.
        
        Args:
            market_data: Dictionary containing market indicators
            
        Returns:
            Dictionary with market risk assessment and score
        """
        risk_score = 0
        risk_factors = []
        
        # Check for market volatility
        if market_data.get('price_volatility', 0) > 0.15:
            risk_score += 2
            risk_factors.append("High market price volatility")
        
        # Check for market trend
        if market_data.get('price_trend', 0) < 0:
            risk_score += market_data.get('price_trend', 0) * -10
            risk_factors.append("Negative price trend in the market")
        
        # Check for supply vs demand
        if market_data.get('inventory_months', 0) > 6:
            risk_score += (market_data.get('inventory_months', 0) - 6) * 0.5
            risk_factors.append("High inventory levels")
        
        # Check for economic indicators
        if market_data.get('unemployment_rate', 0) > 5:
            risk_score += (market_data.get('unemployment_rate', 0) - 5) * 0.3
            risk_factors.append("Elevated unemployment rate")
        
        # Normalize the score to 0-10 range
        risk_score = min(max(risk_score, 0), 10)
        
        return {
            'score': risk_score,
            'factors': risk_factors,
            'assessment': self._get_risk_level(risk_score)
        }
    
    def assess_location_risk(self, location_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess location-related risk factors.
        
        Args:
            location_data: Dictionary containing location information
            
        Returns:
            Dictionary with location risk assessment and score
        """
        risk_score = 0
        risk_factors = []
        
        # Crime rate assessment
        if location_data.get('crime_rate', 0) > location_data.get('avg_city_crime_rate', 0):
            factor = location_data.get('crime_rate', 0) / location_data.get('avg_city_crime_rate', 1)
            risk_score += min(factor * 2, 3)
            risk_factors.append("Above average crime rate")
        
        # Flood zone risk
        if location_data.get('flood_risk', 'low') != 'low':
            flood_risk_map = {'medium': 2, 'high': 4, 'very high': 5}
            risk_score += flood_risk_map.get(location_data.get('flood_risk', 'low'), 0)
            risk_factors.append(f"{location_data.get('flood_risk', 'low').capitalize()} flood risk")
        
        # School quality
        if location_data.get('school_rating', 7) < 5:
            risk_score += (5 - location_data.get('school_rating', 7)) * 0.5
            risk_factors.append("Below average school ratings")
        
        # Employment opportunities
        if location_data.get('job_growth', 0) < 0:
            risk_score += abs(location_data.get('job_growth', 0) * 3)
            risk_factors.append("Declining job market")
        
        # Property tax trends
        if location_data.get('property_tax_trend', 0) > 0.05:
            risk_score += (location_data.get('property_tax_trend', 0) - 0.05) * 20
            risk_factors.append("Rapidly increasing property taxes")
        
        # Normalize the score to 0-10 range
        risk_score = min(max(risk_score, 0), 10)
        
        return {
            'score': risk_score,
            'factors': risk_factors,
            'assessment': self._get_risk_level(risk_score)
        }
    
    def assess_financial_risk(self, financial_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess financial risk factors for the investment.
        
        Args:
            financial_data: Dictionary containing financial information
            
        Returns:
            Dictionary with financial risk assessment and score
        """
        risk_score = 0
        risk_factors = []
        
        # Cash flow assessment
        monthly_cash_flow = financial_data.get('monthly_cash_flow', 0)
        if monthly_cash_flow < 0:
            risk_score += min(abs(monthly_cash_flow) / 200, 4)
            risk_factors.append("Negative cash flow")
        elif monthly_cash_flow < 200:
            risk_score += 2
            risk_factors.append("Low cash flow margin")
        
        # Cap rate assessment
        cap_rate = financial_data.get('cap_rate', 0.07)
        if cap_rate < 0.05:
            risk_score += (0.05 - cap_rate) * 60
            risk_factors.append("Below average capitalization rate")
        
        # Debt service coverage ratio
        dscr = financial_data.get('dscr', 1.2)
        if dscr < 1.2:
            risk_score += (1.2 - dscr) * 10
            risk_factors.append("Low debt service coverage ratio")
        
        # Loan to value ratio
        ltv = financial_data.get('loan_to_value', 0.7)
        if ltv > 0.8:
            risk_score += (ltv - 0.8) * 15
            risk_factors.append("High loan-to-value ratio")
        
        # Vacancy rate concerns
        vacancy_rate = financial_data.get('vacancy_rate', 0.05)
        if vacancy_rate > 0.08:
            risk_score += (vacancy_rate - 0.08) * 20
            risk_factors.append("Above average vacancy rate")
        
        # Normalize the score to 0-10 range
        risk_score = min(max(risk_score, 0), 10)
        
        return {
            'score': risk_score,
            'factors': risk_factors,
            'assessment': self._get_risk_level(risk_score)
        }
    
    def assess_property_risk(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess property-specific risk factors.
        
        Args:
            property_data: Dictionary containing property information
            
        Returns:
            Dictionary with property risk assessment and score
        """
        risk_score = 0
        risk_factors = []
        
        # Age of property
        property_age = property_data.get('age', 0)
        if property_age > 30:
            risk_score += min((property_age - 30) * 0.1, 3)
            risk_factors.append("Older property may require more maintenance")
        
        # Property condition
        condition = property_data.get('condition', 'good').lower()
        condition_score_map = {'excellent': 0, 'good': 1, 'fair': 2.5, 'poor': 5, 'very poor': 7}
        risk_score += condition_score_map.get(condition, 0)
        if condition in ['fair', 'poor', 'very poor']:
            risk_factors.append(f"Property in {condition} condition")
        
        # Special property types
        if property_data.get('is_special_use', False):
            risk_score += 2
            risk_factors.append("Special use property may have limited buyer pool")
        
        # Recent major repairs
        recent_repairs = property_data.get('recent_major_repairs', [])
        if not recent_repairs and property_age > 15:
            risk_score += 1.5
            risk_factors.append("No recent major repairs for aging property")
        
        # Property layout and features
        if property_data.get('has_obsolete_features', False):
            risk_score += 1
            risk_factors.append("Property has obsolete features")
        
        # Normalize the score to 0-10 range
        risk_score = min(max(risk_score, 0), 10)
        
        return {
            'score': risk_score,
            'factors': risk_factors,
            'assessment': self._get_risk_level(risk_score)
        }
    
    def get_overall_risk_assessment(self, property_data: Dict[str, Any],
                                    financial_data: Dict[str, Any],
                                    location_data: Dict[str, Any],
                                    market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate overall risk assessment by combining all risk types.
        
        Args:
            property_data: Property-specific information
            financial_data: Financial metrics and projections
            location_data: Location-related information
            market_data: Market metrics and trends
            
        Returns:
            Dictionary with comprehensive risk assessment
        """
        # Assess individual risk categories
        market_risk = self.assess_market_risk(market_data)
        location_risk = self.assess_location_risk(location_data)
        financial_risk = self.assess_financial_risk(financial_data)
        property_risk = self.assess_property_risk(property_data)
        
        # Calculate weighted risk score
        weighted_score = (
            market_risk['score'] * self.risk_weights['market_risk'] +
            location_risk['score'] * self.risk_weights['location_risk'] +
            financial_risk['score'] * self.risk_weights['financial_risk'] +
            property_risk['score'] * self.risk_weights['property_risk']
        )
        
        # Compile all risk factors
        all_risk_factors = []
        all_risk_factors.extend(market_risk['factors'])
        all_risk_factors.extend(location_risk['factors'])
        all_risk_factors.extend(financial_risk['factors'])
        all_risk_factors.extend(property_risk['factors'])
        
        # Generate overall assessment and recommendations
        recommendations = self._generate_recommendations(
            property_data, financial_data, location_data, market_data,
            market_risk, location_risk, financial_risk, property_risk,
            weighted_score
        )
        
        return {
            'overall_score': weighted_score,
            'risk_level': self._get_risk_level(weighted_score),
            'risk_breakdown': {
                'market_risk': market_risk,
                'location_risk': location_risk,
                'financial_risk': financial_risk,
                'property_risk': property_risk
            },
            'risk_factors': all_risk_factors,
            'recommendations': recommendations,
            'assessment_date': datetime.now().strftime('%Y-%m-%d')
        }
    
    def _get_risk_level(self, score: float) -> str:
        """
        Determine risk level based on score.
        
        Args:
            score: Risk score (0-10)
            
        Returns:
            Risk level as string (low, medium, high, very high)
        """
        if score < self.risk_thresholds['low']:
            return 'low'
        elif score < self.risk_thresholds['medium']:
            return 'medium'
        elif score < self.risk_thresholds['high']:
            return 'high'
        else:
            return 'very high'
    
    def _generate_recommendations(self, property_data: Dict[str, Any],
                                financial_data: Dict[str, Any],
                                location_data: Dict[str, Any],
                                market_data: Dict[str, Any],
                                market_risk: Dict[str, Any],
                                location_risk: Dict[str, Any],
                                financial_risk: Dict[str, Any],
                                property_risk: Dict[str, Any],
                                overall_score: float) -> List[str]:
        """
        Generate recommendations based on risk assessment.
        
        Args:
            Various risk and property data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Overall recommendation based on risk level
        risk_level = self._get_risk_level(overall_score)
        if risk_level == 'low':
            recommendations.append("Overall low risk profile - consider proceeding with investment")
        elif risk_level == 'medium':
            recommendations.append("Medium risk profile - proceed with caution and additional due diligence")
        elif risk_level == 'high':
            recommendations.append("High risk profile - consider negotiating price or terms to offset risk")
        else:
            recommendations.append("Very high risk profile - consider alternative investment opportunities")
        
        # Market risk recommendations
        if market_risk['score'] > self.risk_thresholds['medium']:
            if market_data.get('price_volatility', 0) > 0.15:
                recommendations.append("Consider a longer hold period to offset market volatility")
            if market_data.get('price_trend', 0) < 0:
                recommendations.append("Negotiate purchase price to account for negative market trends")
        
        # Location risk recommendations
        if location_risk['score'] > self.risk_thresholds['medium']:
            if 'crime rate' in ' '.join(location_risk['factors']).lower():
                recommendations.append("Budget for enhanced security measures or property management")
            if 'flood risk' in ' '.join(location_risk['factors']).lower():
                recommendations.append("Obtain comprehensive flood insurance and consider flood mitigation measures")
        
        # Financial risk recommendations
        if financial_risk['score'] > self.risk_thresholds['medium']:
            if 'Negative cash flow' in financial_risk['factors']:
                recommendations.append("Reevaluate rental income potential or consider property improvements to increase rent")
            if 'High loan-to-value ratio' in financial_risk['factors']:
                recommendations.append("Consider increasing down payment to improve debt-to-equity ratio")
        

