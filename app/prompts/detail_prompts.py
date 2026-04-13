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