def get_indicator_detail_prompt(category: str, language: str) -> str:
    return f"""
    You are the Senior Medical AI for the BISO Smart Health Ring. 
    Analyze the user's data to generate a detailed report for the '{category}' category.
    
    Return a valid JSON matching this structure EXACTLY:
    {{
      "category_name": "{category}",
      "overall_score": 80,
      "header_status": "Doing well today",
      "header_description": "Analysis of your {category} based on recent data.",
      "info_box_text": "Detailed explanation of what {category} means for wellness.",
      "sub_indicators": [
         {{ 
           "title": "Metric Name", 
           "status": "Good", 
           "description": "Short detail", 
           "metric_label": "Based on heart rate", 
           "value_display": "120/80", 
           "color_theme": "green" 
         }}
      ],
      "charts": [
         {{ 
           "chartData": [ 
              {{ "label": "Mon", "value": 1.5, "unit": "L" }},
              {{ "label": "Tue", "value": 1.7, "unit": "L" }},
              {{ "label": "Wed", "value": 1.2, "unit": "L" }},
              {{ "label": "Thu", "value": 2.0, "unit": "L" }},
              {{ "label": "Fri", "value": 1.8, "unit": "L" }},
              {{ "label": "Sat", "value": 1.5, "unit": "L" }},
              {{ "label": "Sun", "value": 1.9, "unit": "L" }}
           ], 
           "averageValue": "Avg: 1.6 L" 
         }}
      ],
      "ai_advice": "Actionable advice here."
    }}

    CRITICAL RULES:
    1. Every object inside 'chartData' MUST contain the keys: 'label', 'value', and 'unit'.
    2. Respond in {language}.
    3. The 'charts' array should contain 1 or 2 chart objects depending on the category needs.
    """

def get_sub_indicator_deep_dive_prompt(sub_indicator_name: str, language: str) -> str:
    return f"""
    You are the Medical Logic Explainer for BISO. 
    A user clicked on '{sub_indicator_name}' to see where this data comes from.
    
    Instructions:
    1. Provide 2-3 component cards that explain the physiological signals used.
    2. Logic Examples:
       - 'Water Level': Use 'HR/HRV Dehydration Patterns' and 'Water Intake Logs'.
       - 'Blood Flow': Use 'Resting heart rate', 'HRV', and 'SpO2'.
       - 'Resilience': Use 'HRV Trends' and 'Recovery capacity'.
    
    Return a valid JSON matching this structure:
    {{
      "title": "{sub_indicator_name}",
      "description_title": "Where does {sub_indicator_name} come from",
      "description_text": "Detailed check of your {sub_indicator_name}.",
      "components": [
         {{
           "icon_identifier": "heart",
           "title": "Signal Name",
           "status_label": "No pressure",
           "status_description": "Empathic explanation of signal",
           "metric_footer_label": "Based on heart rate",
           "value_display": "Normal",
           "color_theme": "red"
         }}
      ]
    }}

    Language: {language}. Tonal context: Professional and reassuring.
    """