import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import config

class PharmaAnalytics:
    """Comprehensive pharma sales analytics"""
    
    def __init__(self, data_path=None):
        if data_path is None:
            data_path = config.DATA_PATH + 'pharma_sales_data.csv'
        self.df = pd.read_csv(data_path)
        self.df['Date'] = pd.to_datetime(self.df['Date'])
        self.drug_cols = ['Lipitor', 'Humira', 'Keytruda', 'Revlimid']
        
    def generate_summary_stats(self):
        """Generate comprehensive summary statistics"""
        stats = {}
        
        # Overall performance
        stats['total_sales'] = self.df[self.drug_cols].sum().sum()
        stats['avg_monthly_sales'] = self.df[self.drug_cols].sum(axis=1).mean()
        stats['best_performing_drug'] = self.df[self.drug_cols].sum().idxmax()
        stats['market_leader_share'] = self.df[self.drug_cols].sum().max() / self.df[self.drug_cols].sum().sum() * 100
        
        # Yearly breakdown
        yearly_data = self.df.groupby('Year')[self.drug_cols].sum()
        stats['yearly_totals'] = yearly_data
        
        # Growth trends
        latest_year = self.df['Year'].max()
        prev_year = latest_year - 1
        
        if prev_year in yearly_data.index:
            yoy_growth = ((yearly_data.loc[latest_year] - yearly_data.loc[prev_year]) / 
                         yearly_data.loc[prev_year] * 100)
            stats['yoy_growth'] = yoy_growth
        
        return stats
    
    def detect_anomalies(self, z_threshold=2.5):
        """Detect sales anomalies using Z-score method"""
        anomalies = {}
        
        for drug in self.drug_cols:
            # Calculate Z-scores
            z_scores = np.abs((self.df[drug] - self.df[drug].mean()) / self.df[drug].std())
            
            # Find anomalies
            anomaly_indices = z_scores > z_threshold
            anomaly_data = self.df.loc[anomaly_indices, ['Date', drug, 'Year', 'Quarter']]
            
            if not anomaly_data.empty:
                anomalies[drug] = anomaly_data.to_dict('records')
        
        return anomalies
    
    def create_sales_trend_chart(self):
        """Create interactive sales trend visualization"""
        fig = go.Figure()
        
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        for i, drug in enumerate(self.drug_cols):
            fig.add_trace(go.Scatter(
                x=self.df['Date'],
                y=self.df[drug],
                mode='lines+markers',
                name=drug,
                line=dict(color=colors[i], width=3),
                marker=dict(size=6)
            ))
        
        fig.update_layout(
            title='Pharma Sales Trends (2022-2024)',
            xaxis_title='Date',
            yaxis_title='Sales Volume',
            hovermode='x unified',
            template='plotly_white',
            height=500
        )
        
        return fig
    
    def create_market_share_chart(self):
        """Create market share pie chart for latest year"""
        latest_year_data = self.df[self.df['Year'] == self.df['Year'].max()]
        market_shares = latest_year_data[self.drug_cols].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=self.drug_cols,
            values=market_shares,
            hole=0.4,
            textinfo='label+percent'
        )])
        
        fig.update_layout(
            title=f'Market Share Distribution ({self.df["Year"].max()})',
            template='plotly_white'
        )
        
        return fig
    
    def create_quarterly_performance(self):
        """Create quarterly performance comparison"""
        quarterly_data = self.df.groupby(['Year', 'Quarter'])[self.drug_cols].sum().reset_index()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=self.drug_cols,
            vertical_spacing=0.1
        )
        
        for i, drug in enumerate(self.drug_cols):
            row = (i // 2) + 1
            col = (i % 2) + 1
            
            for year in sorted(quarterly_data['Year'].unique()):
                year_data = quarterly_data[quarterly_data['Year'] == year]
                fig.add_trace(
                    go.Scatter(
                        x=year_data['Quarter'],
                        y=year_data[drug],
                        mode='lines+markers',
                        name=f'{drug} {year}',
                        showlegend=(i == 0)
                    ),
                    row=row, col=col
                )
        
        fig.update_layout(
            title='Quarterly Sales Performance by Drug',
            height=600,
            template='plotly_white'
        )
        
        return fig
    
    def export_insights_for_gemini(self):
        """Export structured data for Gemini AI analysis"""
        stats = self.generate_summary_stats()
        anomalies = self.detect_anomalies()
        
        # Prepare data summary for AI
        summary = {
            'performance_overview': {
                'total_sales': int(stats['total_sales']),
                'best_drug': stats['best_performing_drug'],
                'market_leader_share': round(stats['market_leader_share'], 2)
            },
            'yearly_performance': stats['yearly_totals'].to_dict(),
            'growth_metrics': stats.get('yoy_growth', {}).to_dict() if 'yoy_growth' in stats else {},
            'anomalies_detected': len(anomalies),
            'anomaly_details': anomalies
        }
        
        return summary

# Example usage
if __name__ == "__main__":
    analytics = PharmaAnalytics()
    
    # Generate visualizations
    trend_chart = analytics.create_sales_trend_chart()
    trend_chart.show()
    
    # Print summary stats
    stats = analytics.generate_summary_stats()
    print("=== Pharma Sales Analytics Summary ===")
    print(f"Total Sales: ${stats['total_sales']:,}")
    print(f"Best Performing Drug: {stats['best_performing_drug']}")
    print(f"Market Leader Share: {stats['market_leader_share']:.2f}%")
