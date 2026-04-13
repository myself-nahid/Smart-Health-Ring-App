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
    - The `statGrid` must include items for 'Calories Burned', 'Active Time', 'Distance', 'Heart Rate', and 'Sitting Time'. Estimate realistic values.
    - The `progressInsight` should be a motivational message.
    - The `durationOfActivity` percentages must add up to roughly 100%.
    - The response language for all text must be {language}.

    Return a single, valid JSON object matching this exact structure:
    {{
      "goalCard": {{...}},
      "statGrid": [{{ "iconIdentifier": "calories", "title": "Calories Burned", "value": "<string>", "unit": "kcal" }}, ...],
      "progressInsight": {{...}},
      "durationOfActivity": [{{ "day": "Monday", "duration": "Xh Ym", "percentage": <int> }}, ...],
      "weeklyAverage": "<string 'X,XXX steps'>"
    }}
    """