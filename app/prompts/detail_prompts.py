def get_sleep_detail_prompt(language: str) -> str:
    return f"""
    You are the BISO AI analytics engine. Your task is to generate a detailed JSON payload for the user's Sleep Detail screen.
    Based on the user's health data, create realistic estimations for all fields.
    - Sleep stages MUST add up to 100%. Deep sleep should be between 15-25%.
    - Formulate two distinct insights about their sleep quality.
    - The response language for all text must be {language}.
    
    Return a single, valid JSON object matching this exact structure:
    {{
      "totalDuration": "<string 'Xhr Ym'>",
      "bedTime": "<string 'HH:MM AM/PM'>",
      "wakeUpTime": "<string 'HH:MM AM/PM'>",
      "sleepScore": <integer>,
      "scoreTrendText": "<string '+X points from last week'>",
      "sleepStages": [{{ "stage": "Awake", "durationMinutes": <int>, "percentage": <int> }}, ... ],
      "insights": [{{ "iconIdentifier": "<icon_name>", "title": "<string>", "description": "<string>" }}, ... ],
      "trendChart": [{{ "label": "M", "value": <minutes>, "unit": "min" }}, ... ]
    }}
    """

def get_health_detail_prompt(language: str, health_type: str) -> str:
    # This prompt can be reused for both Mental and Heart health
    return f"""
    You are the BISO AI analytics engine. Your task is to generate a detailed JSON payload for the user's {health_type} Detail screen.
    Based on the user's health data, create a realistic score and insights.
    - The `headerCard.insightSummary` should be a concise, one-sentence analysis.
    - The `insights` section should contain one educational 'Normal Range' card.
    - The `recommendations` checklist should contain three general, actionable health tips relevant to {health_type}.
    - The response language for all text must be {language}.

    Return a single, valid JSON object matching this exact structure:
    {{
      "headerCard": {{ "status": "<string>", "score": <int>, "insightSummary": "<string>", "progressPercent": <int> }},
      "insights": [{{ "iconIdentifier": "info_icon", "title": "Normal Range", "description": "<e.g. 60-100 bpm>" }}],
      "weeklyChart": [{{ "label": "M", "value": <float>, "unit": "<unit>" }}, ... ],
      "recommendations": [{{ "text": "<string>", "isChecked": true }}, ... ]
    }}
    """

def get_physical_activity_detail_prompt(language: str) -> str:
    return f"""
    You are the BISO AI analytics engine for the Physical Activity Detail screen.
    Based on the user's health data, create a detailed breakdown of their activity.
    The response language for all text must be {language}.

    Return a single, valid JSON object matching this exact structure:
    {{
      "goalCard": {{
          "title": "<e.g., Steps Today>",
          "currentValue": <float, e.g., 8423>,
          "goalValue": <float, e.g., 10000>,
          "progressPercent": <integer, e.g., 84>
      }},
      "statGrid": [
          {{ "iconIdentifier": "calories", "title": "Calories Burned", "value": "<string>", "unit": "kcal" }},
          {{ "iconIdentifier": "time", "title": "Active Time", "value": "<string>", "unit": "Min" }},
          {{ "iconIdentifier": "distance", "title": "Distance", "value": "<string>", "unit": "km" }},
          {{ "iconIdentifier": "heart", "title": "Heart Rate", "value": "<string>", "unit": "bpm" }},
          {{ "iconIdentifier": "sitting", "title": "Sitting Time", "value": "<string>", "unit": "" }}
      ],
      "progressInsight": {{
          "iconIdentifier": "progress_up",
          "title": "<e.g., Great progress!>",
          "description": "<e.g., You're at 84% of your goal. A 15-minute walk and you've got this!>"
      }},
      "durationOfActivity": [
          {{ "day": "Monday", "duration": "<string 'Xh Ym'>", "percentage": <integer> }},
          ...
      ],
      "weeklyAverage": "<string 'X,XXX steps'>"
    }}

    CRITICAL RULES:
    1. The `goalCard` object MUST contain `title`, `currentValue`, `goalValue`, and `progressPercent`.
    2. The `progressInsight` object MUST contain `iconIdentifier`, `title`, and `description`.
    3. The `statGrid` MUST contain exactly five items as shown in the example.
    4. Ensure all specified fields are present and correctly typed.
    """

# In app/prompts/detail_prompts.py

# ... (keep existing functions)

def get_metric_history_prompt(language: str, metric: str) -> str:
    # This section defines the specific units and context for each metric type.
    metric_configs = {
        "heart_rate": {"unit": "bpm", "context": "Average Heart Rate"},
        "distance": {"unit": "km", "context": "Distance Covered"},
        "active_time": {"unit": "hours", "context": "Active Time"},
        "calories_burned": {"unit": "kcal", "context": "Calories Burned"}
    }
    config = metric_configs.get(metric, {"unit": "value", "context": "Metric Value"})

    return f"""
    You are the BISO AI analytics engine. Your task is to generate a JSON payload for a detailed metric history screen for the '{config['context']}'.
    Based on the user's data and the selected date, create a realistic set of data for the Today, Weekly, and Monthly reports.
    
    CRITICAL INSTRUCTIONS:
    1. The response language for all text must be {language}.
    2. The `metricName` in the response should be the human-readable version of '{metric}'.
    3. All `value` fields in the charts should be numbers, and units should be '{config['unit']}'.
    4. For the Weekly Report, generate 7 data points, one for each day from SU to SA.
    5. For the Monthly Overview, generate 6-12 data points, one for each month (e.g., Jan, Feb, Mar).
    
    Return a single, valid JSON object matching this exact structure:
    {{
      "metricName": "<string>",
      "todaysReport": {{
        "title": "<e.g., Avg. Heart Rate>",
        "value": "<string>",
        "unit": "<{config['unit']}>",
        "subtitle": "<e.g., Heart rate>"
      }},
      "weeklyReport": {{
        "chartData": [{{ "label": "SU", "value": <number>, "unit": "<{config['unit']}>" }}, ...],
        "averageValue": "<string 'Avg: XXX {config['unit']}'>"
      }},
      "monthlyOverview": {{
        "chartData": [{{ "label": "Jan", "value": <number>, "unit": "<{config['unit']}>" }}, ...]
      }}
    }}
    """

def get_generic_metric_prompt(language: str, metric: str) -> str:
    # This configuration dictionary makes the prompt dynamic and intelligent
    METRIC_CONFIGS = {
        'heart_rate': {"name": "Heart Rate", "unit": "bpm", "range": "60-100 bpm for adults at rest."},
        'hrv': {"name": "HRV", "unit": "ms", "range": "20-150 ms, but varies greatly by individual."},
        'spo2': {"name": "SpO2", "unit": "%", "range": "95-100% is considered normal."},
        'stress_level': {"name": "Stress Level", "unit": "/100", "range": "A score below 40 indicates low stress."},
        'recovery': {"name": "Recovery", "unit": "/100", "range": "A score above 70 indicates good recovery."},
        'sleep_duration': {"name": "Sleep Duration", "unit": "hours", "range": "7-9 hours per night is recommended."},
        'menstrual_cycle': {"name": "Menstrual Cycle", "unit": "", "range": "Typically 21-35 days, with a follicular and luteal phase."},
        # Add configs for all other metrics...
    }
    
    config = METRIC_CONFIGS.get(metric, {"name": metric.replace('_', ' ').title(), "unit": "", "range": "Normal ranges vary."})

    return f"""
    You are the BISO AI analytics engine. Your task is to generate a detailed JSON payload for the '{config['name']}' screen.
    Based on the user's data, create realistic estimations for a header card, insights, a weekly chart, and recommendations.
    
    CRITICAL INSTRUCTIONS:
    1. The response language for all text must be {language}.
    2. The 'headerCard.title' must be '{config['name']}'.
    3. The primary 'insight' MUST be about the 'Normal Range' and should use this information: '{config['range']}'.
    4. The 'weeklyChart' must show 7 days of data for '{config['name']}' with the unit '{config['unit']}'.
    5. The 'recommendations' must be three general, actionable health tips that are broadly beneficial.
    
    Return a single, valid JSON object matching this exact structure:
    {{
      "headerCard": {{ "title": "<string>", "currentValue": "<string>", "unit": "<{config['unit']}>", "statusText": "<string>", "progressPercent": <integer> }},
      "insights": [{{ "iconIdentifier": "info_icon", "title": "Normal Range", "description": "<string>" }}],
      "weeklyChart": [{{ "label": "Mon", "value": <number>, "unit": "<{config['unit']}>" }}, ...],
      "recommendations": [{{ "text": "Maintain regular physical activity", "isChecked": true }}, ...]
    }}
    """