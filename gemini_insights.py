import json
import google.generativeai as genai
from scripts.analytics_dashboard import PharmaAnalytics
import config

class GeminiInsights:
    """Generate AI-powered business insights using Google Gemini"""
    
    def __init__(self, api_key=None):
        if api_key is None:
            api_key = config.GEMINI_API_KEY
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize analytics
        self.analytics = PharmaAnalytics()
    
    def generate_executive_summary(self):
        """Generate executive summary using Gemini AI"""
        # Get data insights
        data_summary = self.analytics.export_insights_for_gemini()
        
        prompt = f"""
        You are a senior pharmaceutical industry analyst. Based on the following sales data, provide a comprehensive executive summary:

        PERFORMANCE OVERVIEW:
        - Total Sales: ${data_summary['performance_overview']['total_sales']:,}
        - Best Performing Drug: {data_summary['performance_overview']['best_drug']}
        - Market Leader Share: {data_summary['performance_overview']['market_leader_share']}%

        YEARLY PERFORMANCE:
        {json.dumps(data_summary['yearly_performance'], indent=2)}

        GROWTH METRICS:
        {json.dumps(data_summary['growth_metrics'], indent=2)}

        ANOMALIES DETECTED: {data_summary['anomalies_detected']} unusual patterns identified

        Please provide:
        1. Key business insights and trends
        2. Strategic recommendations for portfolio optimization
        3. Risk assessment and opportunities
        4. Market positioning analysis

        Format as a professional business report suitable for C-suite executives.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def answer_business_question(self, question):
        """Answer specific business questions about the pharma data"""
        data_summary = self.analytics.export_insights_for_gemini()
        
        prompt = f"""
        You are a pharmaceutical business analyst. Based on the following sales data:

        {json.dumps(data_summary, indent=2)}

        Business Question: {question}

        Provide a data-driven answer with specific insights and actionable recommendations.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error answering question: {str(e)}"
    
    def generate_forecast_insights(self):
        """Generate AI-powered forecasting insights"""
        stats = self.analytics.generate_summary_stats()
        
        prompt = f"""
        Based on the pharmaceutical sales data showing:
        
        Best performing drug: {stats['best_performing_drug']}
        YoY growth patterns: {stats.get('yoy_growth', 'Data insufficient').to_dict() if 'yoy_growth' in stats else 'Data insufficient'}
        
        Provide strategic forecasting insights for the next 6-12 months, including:
        1. Expected market trends
        2. Risk factors to monitor
        3. Opportunity areas for growth
        4. Resource allocation recommendations
        
        Focus on actionable business intelligence suitable for pharmaceutical executives.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating forecast insights: {str(e)}"

# Example usage
if __name__ == "__main__":
    # Initialize Gemini insights
    gemini = GeminiInsights()
    
    # Generate executive summary
    print("=== EXECUTIVE SUMMARY ===")
    summary = gemini.generate_executive_summary()
    print(summary)
    
    print("\n" + "="*50 + "\n")
    
    # Answer business questions
    questions = [
        "Which drug should we prioritize for increased marketing investment?",
        "What are the main risks facing our product portfolio?",
        "How can we optimize our quarterly sales performance?"
    ]
    
    for question in questions:
        print(f"Q: {question}")
        answer = gemini.answer_business_question(question)
        print(f"A: {answer}")
        print("\n" + "-"*30 + "\n")
