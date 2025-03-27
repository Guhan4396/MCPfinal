import pandas as pd
import os

class MCPRiskCalculator:
    def __init__(self, risk_db_path):
        # Use absolute path for the risk database
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.risk_db_path = os.path.join(current_dir, '..', risk_db_path)
        self.risk_data = pd.read_csv(self.risk_db_path)
    
    def process_supplier_list(self, suppliers):
        results = []
        for supplier_name, country in suppliers:
            # Calculate risk scores
            risk_scores = {
                'Supplier Name': supplier_name,
                'Country': country,
                'Overall Risk Score': self._calculate_overall_risk(country),
                'Environmental Risk': self._calculate_environmental_risk(country),
                'Social Risk': self._calculate_social_risk(country),
                'Governance Risk': self._calculate_governance_risk(country)
            }
            results.append(risk_scores)
        return results
    
    def format_risk_table(self, results):
        return pd.DataFrame(results)
    
    def _get_country_risk_data(self, country):
        # Try to find the country in the risk database
        country_data = self.risk_data[self.risk_data['Country'].str.lower() == country.lower()]
        if country_data.empty:
            # If country not found, return None
            return None
        return country_data.iloc[0]
    
    def _calculate_overall_risk(self, country):
        country_data = self._get_country_risk_data(country)
        if country_data is None:
            return None
        return country_data['Overall_Risk_Score']
    
    def _calculate_environmental_risk(self, country):
        country_data = self._get_country_risk_data(country)
        if country_data is None:
            return None
        # Average of GHG_Emissions, Water, and Biodiversity
        return (country_data['GHG_Emissions'] + country_data['Water'] + country_data['Biodiversity']) / 3
    
    def _calculate_social_risk(self, country):
        country_data = self._get_country_risk_data(country)
        if country_data is None:
            return None
        # Average of Trade_Unions, Wages, Working_Time, Gender_Based_Violence, Health_and_Safety, Forced_Labor, and Child_Labor
        return (country_data['Trade_Unions'] + country_data['Wages'] + country_data['Working_Time'] + 
                country_data['Gender_Based_Violence'] + country_data['Health_and_Safety'] + 
                country_data['Forced_Labor'] + country_data['Child_Labor']) / 7
    
    def _calculate_governance_risk(self, country):
        country_data = self._get_country_risk_data(country)
        if country_data is None:
            return None
        # Average of Hazardous_Chemicals and Bribery_and_Corruption
        return (country_data['Hazardous_Chemicals'] + country_data['Bribery_and_Corruption']) / 2 