import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple

class PropertyAnalyzer:
    """
    A class for analyzing real estate properties and providing insights.
    """
    
    def __init__(self, market_data: Optional[pd.DataFrame] = None):
        """
        Initialize the PropertyAnalyzer with optional market data.
        
        Args:
            market_data: DataFrame containing market comparison data (optional)
        """
        self.market_data = market_data
        self.feature_weights = {
            "location": 0.25,
            "condition": 0.15,
            "size": 0.15,
            "age": 0.10,
            "amenities": 0.10,
            "schools": 0.10,
            "crime_rate": 0.08,
            "future_development": 0.07
        }
    
    def analyze_property(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a property.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            Dictionary with analysis results
        """
        results = {}
        
        # Basic property metrics
        results["basic_metrics"] = self.calculate_basic_metrics(property_data)
        
        # Evaluate features
        results["feature_scores"] = self.evaluate_features(property_data)
        
        # Calculate overall score
        results["overall_score"] = self.calculate_property_score(results["feature_scores"])
        
        # Market comparison
        if self.market_data is not None:
            results["market_comparison"] = self.compare_to_market(property_data)
        
        return results
    
    def calculate_basic_metrics(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate basic property metrics.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            Dictionary with calculated metrics
        """
        metrics = {}
        
        # Price per square foot
        if "price" in property_data and "square_footage" in property_data:
            if property_data["square_footage"] > 0:
                metrics["price_per_sqft"] = property_data["price"] / property_data["square_footage"]
            else:
                metrics["price_per_sqft"] = 0
        
        # Estimated property value appreciation
        if "location_growth_rate" in property_data:
            metrics["estimated_5yr_appreciation"] = property_data["price"] * (
                (1 + property_data["location_growth_rate"]) ** 5 - 1
            )
        
        # Property age factors
        if "year_built" in property_data:
            import datetime
            current_year = datetime.datetime.now().year
            age = current_year - property_data["year_built"]
            metrics["age"] = age
            
            # Estimated remaining life (assuming 75-year average lifespan for a building)
            metrics["estimated_remaining_life"] = max(0, 75 - age)
            
            # Age-based depreciation factor
            metrics["age_depreciation_factor"] = min(1.0, max(0.25, 1 - (age / 100)))
        
        return metrics
    
    def evaluate_features(self, property_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Evaluate and score different property features.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            Dictionary with feature scores (0-10 scale)
        """
        feature_scores = {}
        
        # Location score (0-10)
        if "location_rating" in property_data:
            feature_scores["location"] = property_data["location_rating"]
        else:
            feature_scores["location"] = self._calculate_location_score(property_data)
        
        # Condition score (0-10)
        if "condition" in property_data:
            feature_scores["condition"] = property_data["condition"]
        
        # Size score (0-10)
        if "square_footage" in property_data:
            # Normalize square footage to a 0-10 scale
            # Assuming 3000+ sq ft is a 10, and 500 sq ft is a 1
            size_score = (property_data["square_footage"] - 500) / 250
            feature_scores["size"] = max(0, min(10, size_score))
        
        # Age score (0-10, newer is better)
        if "year_built" in property_data:
            import datetime
            current_year = datetime.datetime.now().year
            age = current_year - property_data["year_built"]
            # Age score: 0 years = 10 points, 100+ years = 0 points
            age_score = 10 - (age / 10)
            feature_scores["age"] = max(0, min(10, age_score))
        
        # Amenities score (0-10)
        if "amenities" in property_data:
            feature_scores["amenities"] = property_data["amenities"]
        
        # Schools score (0-10)
        if "school_rating" in property_data:
            feature_scores["schools"] = property_data["school_rating"]
        
        # Crime rate score (0-10, lower crime rate is better)
        if "crime_rate" in property_data:
            # Assuming 0 crime rate is 10 points, and 10% or higher is 0 points
            crime_score = 10 - (property_data["crime_rate"] * 100)
            feature_scores["crime_rate"] = max(0, min(10, crime_score))
        
        # Future development score (0-10)
        if "future_development_rating" in property_data:
            feature_scores["future_development"] = property_data["future_development_rating"]
        
        return feature_scores
    
    def _calculate_location_score(self, property_data: Dict[str, Any]) -> float:
        """
        Calculate location score based on various location factors.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            Location score (0-10 scale)
        """
        location_score = 5.0  # Default mid-range score
        
        # Factors that could adjust the score
        factors = [
            ("proximity_to_downtown", 1.5),
            ("proximity_to_public_transport", 1.0),
            ("proximity_to_schools", 0.7),
            ("proximity_to_shopping", 0.7),
            ("proximity_to_parks", 0.5),
            ("neighborhood_rating", 1.5),
            ("walkability_score", 1.0),
        ]
        
        factor_count = 0
        for factor, weight in factors:
            if factor in property_data:
                # Assume all factors are scored 0-10
                location_score += (property_data[factor] - 5) * weight / 5
                factor_count += 1
        
        # Normalize score to 0-10 range
        location_score = max(0, min(10, location_score))
        
        return location_score
    
    def calculate_property_score(self, feature_scores: Dict[str, float]) -> float:
        """
        Calculate overall property score based on feature scores and weights.
        
        Args:
            feature_scores: Dictionary with feature scores
            
        Returns:
            Overall property score (0-10 scale)
        """
        overall_score = 0.0
        total_weight = 0.0
        
        for feature, score in feature_scores.items():
            if feature in self.feature_weights:
                weight = self.feature_weights[feature]
                overall_score += score * weight
                total_weight += weight
        
        # Normalize if not all features were scored
        if total_weight > 0:
            overall_score /= total_weight
            # Adjust to ensure we use the full weight
            overall_score *= sum(self.feature_weights.values()) / total_weight
        
        return round(overall_score, 2)
    
    def compare_to_market(self, property_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Compare property metrics against market averages.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            Dictionary with comparison results
        """
        if self.market_data is None:
            return {"error": "No market data available for comparison"}
        
        comparison = {}
        
        # Filter market data to comparable properties
        comparable_properties = self._get_comparable_properties(property_data)
        
        if len(comparable_properties) == 0:
            return {"error": "No comparable properties found in market data"}
        
        # Price comparison
        if "price" in property_data:
            avg_market_price = comparable_properties["price"].mean()
            comparison["price_vs_market"] = {
                "property_value": property_data["price"],
                "market_average": avg_market_price,
                "difference": property_data["price"] - avg_market_price,
                "percentage": ((property_data["price"] / avg_market_price) - 1) * 100 if avg_market_price > 0 else 0
            }
        
        # Price per square foot comparison
        if "price" in property_data and "square_footage" in property_data:
            property_price_psf = property_data["price"] / property_data["square_footage"] if property_data["square_footage"] > 0 else 0
            comparable_price_psf = comparable_properties["price"].sum() / comparable_properties["square_footage"].sum() if comparable_properties["square_footage"].sum() > 0 else 0
            
            comparison["price_per_sqft_vs_market"] = {
                "property_value": property_price_psf,
                "market_average": comparable_price_psf,
                "difference": property_price_psf - comparable_price_psf,
                "percentage": ((property_price_psf / comparable_price_psf) - 1) * 100 if comparable_price_psf > 0 else 0
            }
        
        return comparison
    
    def _get_comparable_properties(self, property_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Filter market data to find comparable properties.
        
        Args:
            property_data: Dictionary containing property details
            
        Returns:
            DataFrame with comparable properties
        """
        if self.market_data is None:
            return pd.DataFrame()
        
        comparable = self.market_data.copy()
        
        # Filter by location if available
        if "zip_code" in property_data and "zip_code" in comparable.columns:
            comparable = comparable[comparable["zip_code"] == property_data["zip_code"]]
        
        # Filter by property type
        if "property_type" in property_data and "property_type" in comparable.columns:
            comparable = comparable[comparable["property_type"] == property_data["property_type"]]
        
        # Filter by size (±20% of the property's square footage)
        if "square_footage" in property_data and "square_footage" in comparable.columns:
            min_size = property_data["square_footage"] * 0.8
            max_size = property_data["square_footage"] * 1.2
            comparable = comparable[(comparable["square_footage"] >= min_size) & 
                                (comparable["square_footage"] <= max_size)]
        
        # If too few properties, relax constraints
        if len(comparable) < 5 and "zip_code" in property_data:
            # Try expanding to neighboring areas
            if "neighborhood" in property_data and "neighborhood" in self.market_data.columns:
                comparable = self.market_data[self.market_data["neighborhood"] == property_data["neighborhood"]]
        
        return comparable
    
    def update_market_data(self, new_market_data: pd.DataFrame) -> None:
        """
        Update the market comparison data.
        
        Args:
            new_market_data: DataFrame containing updated market data
        """
        self.market_data = new_market_data
    
    def set_feature_weights(self, new_weights: Dict[str, float]) -> None:
        """
        Update the feature weights used for property scoring.
        
        Args:
            new_weights: Dictionary with new feature weights
        """
        # Validate weights
        total = sum(new_weights.values())
        if abs(total - 1.0) > 0.01:
            normalized_weights = {k: v/total for k, v in new_weights.items()}
            self.feature_weights = normalized_weights
        else:
            self.feature_weights = new_weights

