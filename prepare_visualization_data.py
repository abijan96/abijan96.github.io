import pandas as pd
import json

# Read the CSV file
df = pd.read_csv('90-day-survey-analysis.csv', skiprows=[0, 2])

df.columns = ['StartDate', 'EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)',
              'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 'RecipientFirstName',
              'RecipientEmail', 'ExternalReference', 'LocationLatitude', 'LocationLongitude',
              'DistributionChannel', 'UserLanguage', 'Q4', 'Q6', 'Q8', 'Q10', 'Q12', 'Q14',
              'Q16', 'Q18', 'Q20', 'Q22', 'Q24', 'Q24_liked', 'Q25_improve']

# Filter completed responses
df = df[df['Finished'] == True].copy()
df['Progress'] = pd.to_numeric(df['Progress'], errors='coerce')
df = df[df['Progress'] == 100].copy()

# Convert dates
df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
df['Year'] = df['StartDate'].dt.year
df['Quarter'] = df['StartDate'].dt.to_period('Q').astype(str)

# Sentiment scoring function
def calculate_sentiment_score(series):
    mapping = {
        'Strongly agree': 5,
        'Agree': 4,
        'Neither agree nor disagree': 3,
        'Disagree': 2,
        'Strongly disagree': 1,
        'Yes': 5,
        'No': 1,
        'Strong disagree': 1
    }
    return series.map(mapping)

# Question labels
questions = {
    'Q4': 'Understand job expectations',
    'Q6': 'Know where to ask questions',
    'Q8': 'Happy with NDR decision',
    'Q10': 'Feel part of NDR',
    'Q12': 'Manager helped set goals',
    'Q14': 'Manager communicates well',
    'Q16': 'Manager provides feedback',
    'Q18': 'Feel challenged & engaged',
    'Q20': 'Feel part of team',
    'Q22': 'No roadblocks (inverted)',
    'Q24': 'Manager discussed progress'
}

# Calculate overall satisfaction scores
satisfaction_data = []
for q_code, q_label in questions.items():
    if q_code in df.columns:
        responses = df[q_code].dropna()
        if len(responses) > 0:
            numeric_scores = calculate_sentiment_score(responses)
            avg_score = numeric_scores.mean()

            # Calculate positive rate
            positive = responses.isin(['Strongly agree', 'Agree', 'Yes']).sum()
            positive_rate = (positive / len(responses)) * 100

            # For Q22, invert the logic
            if q_code == 'Q22':
                negative = responses.isin(['Strongly agree', 'Agree', 'Yes']).sum()
                positive_rate = 100 - ((negative / len(responses)) * 100)

            satisfaction_data.append({
                'question': q_label,
                'score': round(avg_score, 2),
                'positiveRate': round(positive_rate, 1),
                'responses': len(responses)
            })

# Sort by positive rate
satisfaction_data = sorted(satisfaction_data, key=lambda x: x['positiveRate'], reverse=True)

# Trends over time (quarterly)
time_trends = []
key_questions = {
    'Q8': 'Happy with NDR',
    'Q10': 'Feel part of NDR',
    'Q14': 'Manager communication',
    'Q18': 'Feel engaged'
}

for quarter in df['Quarter'].unique():
    quarter_df = df[df['Quarter'] == quarter]
    quarter_data = {'quarter': quarter}

    for q_code, q_label in key_questions.items():
        if q_code in quarter_df.columns:
            responses = quarter_df[q_code].dropna()
            if len(responses) > 0:
                numeric_scores = calculate_sentiment_score(responses)
                quarter_data[q_label] = round(numeric_scores.mean(), 2)

    time_trends.append(quarter_data)

# Sort by quarter
time_trends = sorted(time_trends, key=lambda x: x['quarter'])

# Responses by year
responses_by_year = df['Year'].value_counts().sort_index().to_dict()
year_data = [{'year': int(year), 'count': int(count)} for year, count in responses_by_year.items()]

# Qualitative themes - LIKED
liked_responses = df['Q24_liked'].dropna()
liked_themes = {
    'Team & colleagues': 0,
    'Meetings & introductions': 0,
    'Manager & leadership': 0,
    'Structure & organization': 0,
    'Check-ins & touchpoints': 0,
    'Training & learning': 0,
    'Welcoming & hospitality': 0,
    'Intentional & thoughtful': 0
}

for response in liked_responses:
    response_lower = str(response).lower()
    if any(word in response_lower for word in ['team', 'colleague', 'coworker', 'people']):
        liked_themes['Team & colleagues'] += 1
    if any(word in response_lower for word in ['meeting', 'meet', 'introduction', 'intro']):
        liked_themes['Meetings & introductions'] += 1
    if any(word in response_lower for word in ['manager', 'boss', 'nancy', 'claudia', 'leadership']):
        liked_themes['Manager & leadership'] += 1
    if any(word in response_lower for word in ['structure', 'organized', 'plan']):
        liked_themes['Structure & organization'] += 1
    if any(word in response_lower for word in ['check-in', 'checking', 'touch', 'reaching out']):
        liked_themes['Check-ins & touchpoints'] += 1
    if any(word in response_lower for word in ['training', 'learning', 'education']):
        liked_themes['Training & learning'] += 1
    if any(word in response_lower for word in ['welcome', 'hospitality', 'warm', 'friendly']):
        liked_themes['Welcoming & hospitality'] += 1
    if any(word in response_lower for word in ['intentional', 'thoughtful', 'effort']):
        liked_themes['Intentional & thoughtful'] += 1

liked_theme_data = [
    {'theme': theme, 'count': count, 'percentage': round((count/len(liked_responses))*100, 1)}
    for theme, count in sorted(liked_themes.items(), key=lambda x: x[1], reverse=True)
    if count > 0
]

# Qualitative themes - IMPROVEMENT
improve_responses = df['Q25_improve'].dropna()
improve_themes = {
    'Timeline & wait time': 0,
    'Time management': 0,
    'Connection with new hires': 0,
    'Benefits & HR': 0,
    'Automation & tasks': 0,
    'Overview of NDR teams': 0,
    'Integration & sources': 0
}

for response in improve_responses:
    response_lower = str(response).lower()
    if 'n/a' in response_lower or 'nothing' in response_lower or 'no change' in response_lower:
        continue
    if any(word in response_lower for word in ['wait', 'timeline', 'long', 'months']):
        improve_themes['Timeline & wait time'] += 1
    if any(word in response_lower for word in ['time', 'first week', 'dedicated']):
        improve_themes['Time management'] += 1
    if any(word in response_lower for word in ['new employee', 'new hire', 'cohort']):
        improve_themes['Connection with new hires'] += 1
    if any(word in response_lower for word in ['benefits', 'hr', 'health']):
        improve_themes['Benefits & HR'] += 1
    if any(word in response_lower for word in ['automated', 'task', 'fix']):
        improve_themes['Automation & tasks'] += 1
    if any(word in response_lower for word in ['overview', 'team', 'area']):
        improve_themes['Overview of NDR teams'] += 1
    if any(word in response_lower for word in ['integration', 'overlap', 'confusion']):
        improve_themes['Integration & sources'] += 1

improve_theme_data = [
    {'theme': theme, 'count': count, 'percentage': round((count/len(improve_responses))*100, 1)}
    for theme, count in sorted(improve_themes.items(), key=lambda x: x[1], reverse=True)
    if count > 0
]

# Compile all data
visualization_data = {
    'summary': {
        'totalResponses': len(df),
        'dateRange': {
            'start': df['StartDate'].min().strftime('%Y-%m-%d'),
            'end': df['StartDate'].max().strftime('%Y-%m-%d')
        },
        'overallSatisfaction': round(satisfaction_data[0]['positiveRate'], 1) if satisfaction_data else 0
    },
    'satisfactionScores': satisfaction_data,
    'timeTrends': time_trends,
    'responsesByYear': year_data,
    'likedThemes': liked_theme_data,
    'improvementThemes': improve_theme_data
}

# Save to JSON
with open('onboarding_data.json', 'w') as f:
    json.dump(visualization_data, f, indent=2)

print("Data prepared successfully!")
print(f"Total responses: {len(df)}")
print(f"Satisfaction metrics: {len(satisfaction_data)}")
print(f"Quarterly trends: {len(time_trends)}")
print(f"Liked themes: {len(liked_theme_data)}")
print(f"Improvement themes: {len(improve_theme_data)}")
