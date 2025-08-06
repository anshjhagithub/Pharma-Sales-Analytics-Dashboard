import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import config

class PharmaDataGenerator:
    """Generate realistic pharma sales data for dashboard"""
    
    def __init__(self):
        np.random.seed(42)  # For reproducible results
        
    def create_pharma_dataset(self, start_date='2022-01-01', periods=36):
        """
        Create realistic pharma sales dataset
        Args:
            start_date: Starting date for sales data
            periods: Number of months to generate
        """
        # Generate monthly date range
        dates = pd.date_range(start=start_date, periods=periods, freq='M')
        
        # Define drug characteristics (base sales, trend, seasonality)
        drug_configs = {
            'Lipitor': {'base': 850, 'trend': 0.5, 'seasonality': 50, 'volatility': 25},
            'Humira': {'base': 1200, 'trend': 2.0, 'seasonality': 80, 'volatility': 40},
            'Keytruda': {'base': 950, 'trend': 5.0, 'seasonality': 30, 'volatility': 60},
            'Revlimid': {'base': 720, 'trend': -1.0, 'seasonality': 40, 'volatility': 35}
        }
        
        # Create sales data
        sales_data = {'Date': dates}
        
        for drug, config in drug_configs.items():
            # Base trend
            trend = np.linspace(0, config['trend'] * periods, periods)
            
            # Seasonal pattern (peaks in Q4, dips in Q2)
            seasonal = config['seasonality'] * np.sin(np.linspace(0, 2*np.pi*3, periods) + np.pi/2)
            
            # Random volatility
            noise = np.random.normal(0, config['volatility'], periods)
            
            # Combine all factors
            sales = config['base'] + trend + seasonal + noise
            
            # Ensure no negative sales
            sales = np.maximum(sales, config['base'] * 0.3)
            
            sales_data[drug] = np.round(sales).astype(int)
        
        # Create DataFrame
        df = pd.DataFrame(sales_data)
        
        # Add additional columns for analysis
        df['Month'] = df['Date'].dt.month
        df['Quarter'] = df['Date'].dt.quarter
        df['Year'] = df['Date'].dt.year
        
        return df
    
    def add_market_metrics(self, df):
        """Add market share and growth metrics"""
        # Calculate total market per month
        drug_cols = ['Lipitor', 'Humira', 'Keytruda', 'Revlimid']
        df['Total_Market'] = df[drug_cols].sum(axis=1)
        
        # Calculate market share for each drug
        for drug in drug_cols:
            df[f'{drug}_Market_Share'] = (df[drug] / df['Total_Market'] * 100).round(2)
        
        # Calculate year-over-year growth
        for drug in drug_cols:
            df[f'{drug}_YoY_Growth'] = df[drug].pct_change(12) * 100
        
        return df
    
    def save_dataset(self, df, filename='pharma_sales_data.csv'):
        """Save dataset to CSV"""
        filepath = config.DATA_PATH + filename
        df.to_csv(filepath, index=False)
        print(f"Dataset saved to: {filepath}")
        return filepath

# Generate and save the dataset
if __name__ == "__main__":
    generator = PharmaDataGenerator()
    pharma_df = generator.create_pharma_dataset()
    pharma_df = generator.add_market_metrics(pharma_df)
    generator.save_dataset(pharma_df)
