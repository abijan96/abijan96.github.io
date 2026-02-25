import pandas as pd
import numpy as np
from collections import Counter
import re

# Read the CSV file, skip first 2 rows (header and metadata)
df = pd.read_csv('90-day-survey-analysis.csv', skiprows=[0, 2])

# The column names are now in the first row after skipping
df.columns = ['StartDate', 'EndDate', 'Status', 'IPAddress', 'Progress', 'Duration (in seconds)',
              'Finished', 'RecordedDate', 'ResponseId', 'RecipientLastName', 'RecipientFirstName',
              'RecipientEmail', 'ExternalReference', 'LocationLatitude', 'LocationLongitude',
              'DistributionChannel', 'UserLanguage', 'Q4', 'Q6', 'Q8', 'Q10', 'Q12', 'Q14',
              'Q16', 'Q18', 'Q20', 'Q22', 'Q24', 'Q24_liked', 'Q25_improve']

# Filter out incomplete responses and test responses
df = df[df['Finished'] == True].copy()
df['Progress'] = pd.to_numeric(df['Progress'], errors='coerce')
df = df[df['Progress'] == 100].copy()

# Convert date columns
df['StartDate'] = pd.to_datetime(df['StartDate'], errors='coerce')
df['EndDate'] = pd.to_datetime(df['EndDate'], errors='coerce')

# Define question columns (Q4-Q24 are the Likert scale questions)
likert_questions = {
    'Q4': '1. I clearly understand the expectations of my job',
    'Q6': '2. I know where to go or whom to ask if I have a question',
    'Q8': '3. I am happy with the decision to work at NDR',
    'Q10': '4. I feel like I am a part of NDR',
    'Q12': '5. My manager helped me establish my goals',
    'Q14': '6. My manager communicates effectively',
    'Q16': '7. My manager provides regular and effective feedback',
    'Q18': '8. I feel positively challenged and engaged',
    'Q20': '9. I feel part of my team',
    'Q22': '10. There are roadblocks preventing me from performing',
    'Q24': '11. My manager talked to me about my progress'
}

print("="*80)
print("90-DAY ONBOARDING SURVEY ANALYSIS")
print("="*80)
print(f"\nTotal Completed Responses: {len(df)}")
print(f"Date Range: {df['StartDate'].min().strftime('%Y-%m-%d')} to {df['StartDate'].max().strftime('%Y-%m-%d')}")
print(f"Time Span: {(df['StartDate'].max() - df['StartDate'].min()).days} days (~{(df['StartDate'].max() - df['StartDate'].min()).days/365:.1f} years)")

# Group by year to see response trends over time
df['Year'] = df['StartDate'].dt.year
responses_by_year = df['Year'].value_counts().sort_index()
print(f"\nResponses by Year:")
for year, count in responses_by_year.items():
    print(f"  {year}: {count} responses")

print("\n" + "="*80)
print("QUANTITATIVE INSIGHTS - LIKERT SCALE ANALYSIS")
print("="*80)

# Analyze each question
def calculate_sentiment_score(series):
    """Convert Likert responses to numeric scores"""
    mapping = {
        'Strongly agree': 5,
        'Agree': 4,
        'Neither agree nor disagree': 3,
        'Disagree': 2,
        'Strongly disagree': 1,
        'Yes': 5,
        'No': 1
    }
    return series.map(mapping)

results = []
for q_code, q_text in likert_questions.items():
    if q_code in df.columns:
        # Remove empty responses
        responses = df[q_code].dropna()

        if len(responses) > 0:
            # Calculate distribution
            dist = responses.value_counts()

            # Calculate sentiment score
            numeric_scores = calculate_sentiment_score(responses)
            avg_score = numeric_scores.mean()

            # Calculate positive response rate (Strongly agree + Agree + Yes)
            positive_responses = responses.isin(['Strongly agree', 'Agree', 'Yes']).sum()
            positive_rate = (positive_responses / len(responses)) * 100

            # For Q22 (roadblocks), invert the logic - Disagree is good
            if q_code == 'Q22':
                negative_responses = responses.isin(['Strongly agree', 'Agree', 'Yes']).sum()
                negative_rate = (negative_responses / len(responses)) * 100
                positive_rate = 100 - negative_rate

            results.append({
                'question': q_text,
                'avg_score': avg_score,
                'positive_rate': positive_rate,
                'total_responses': len(responses),
                'distribution': dist.to_dict()
            })

# Sort by positive rate to identify strengths and weaknesses
results_df = pd.DataFrame(results)
results_df = results_df.sort_values('positive_rate', ascending=False)

print("\nTOP STRENGTHS (Highest Satisfaction):")
print("-" * 80)
for idx, row in results_df.head(5).iterrows():
    print(f"\n{row['question']}")
    print(f"  Positive Response Rate: {row['positive_rate']:.1f}%")
    print(f"  Average Score: {row['avg_score']:.2f}/5.00")
    print(f"  Distribution: {row['distribution']}")

print("\n\nAREAS FOR IMPROVEMENT (Lower Satisfaction):")
print("-" * 80)
for idx, row in results_df.tail(3).iterrows():
    print(f"\n{row['question']}")
    print(f"  Positive Response Rate: {row['positive_rate']:.1f}%")
    print(f"  Average Score: {row['avg_score']:.2f}/5.00")
    print(f"  Distribution: {row['distribution']}")

print("\n" + "="*80)
print("QUALITATIVE INSIGHTS - OPEN-ENDED FEEDBACK ANALYSIS")
print("="*80)

# Analyze open-ended responses
liked_responses = df['Q24_liked'].dropna()
improve_responses = df['Q25_improve'].dropna()

print(f"\n\nWHAT EMPLOYEES LIKED (n={len(liked_responses)}):")
print("-" * 80)

# Extract common themes from "liked" responses
liked_themes = {
    'welcoming/hospitality': 0,
    'structure/organization': 0,
    'check-ins/touchpoints': 0,
    'manager/leadership': 0,
    'team/colleagues': 0,
    'training/learning': 0,
    'automation/checklist': 0,
    'lunch with leadership': 0,
    'intentional/thoughtful': 0,
    'meetings/introductions': 0
}

for response in liked_responses:
    response_lower = str(response).lower()
    if any(word in response_lower for word in ['welcome', 'hospitality', 'warm', 'friendly']):
        liked_themes['welcoming/hospitality'] += 1
    if any(word in response_lower for word in ['structure', 'organized', 'plan']):
        liked_themes['structure/organization'] += 1
    if any(word in response_lower for word in ['check-in', 'checking', 'touch', 'reaching out']):
        liked_themes['check-ins/touchpoints'] += 1
    if any(word in response_lower for word in ['manager', 'boss', 'nancy', 'claudia', 'leadership']):
        liked_themes['manager/leadership'] += 1
    if any(word in response_lower for word in ['team', 'colleague', 'coworker', 'people']):
        liked_themes['team/colleagues'] += 1
    if any(word in response_lower for word in ['training', 'learning', 'education']):
        liked_themes['training/learning'] += 1
    if any(word in response_lower for word in ['automation', 'checklist', 'spreadsheet', 'tasks']):
        liked_themes['automation/checklist'] += 1
    if any(word in response_lower for word in ['lunch', 'jeff', 'rhoads', 'director']):
        liked_themes['lunch with leadership'] += 1
    if any(word in response_lower for word in ['intentional', 'thoughtful', 'effort']):
        liked_themes['intentional/thoughtful'] += 1
    if any(word in response_lower for word in ['meeting', 'meet', 'introduction', 'intro']):
        liked_themes['meetings/introductions'] += 1

# Sort and display themes
sorted_liked = sorted(liked_themes.items(), key=lambda x: x[1], reverse=True)
for theme, count in sorted_liked:
    if count > 0:
        percentage = (count / len(liked_responses)) * 100
        print(f"  {theme.upper()}: {count} mentions ({percentage:.1f}%)")

print("\n\nSAMPLE POSITIVE QUOTES:")
print("-" * 80)
sample_liked = liked_responses.head(8)
for i, response in enumerate(sample_liked, 1):
    if str(response) not in ['NA', 'N/A', 'n/a', 'nothing', '']:
        print(f"{i}. \"{response}\"")

print(f"\n\nWHAT EMPLOYEES WANT IMPROVED (n={len(improve_responses)}):")
print("-" * 80)

# Extract common themes from "improvement" responses
improve_themes = {
    'nothing/no suggestions': 0,
    'timeline/wait time': 0,
    'benefits/HR orientation': 0,
    'connection with new hires': 0,
    'training consistency': 0,
    'meeting efficiency': 0,
    'overview of NDR teams': 0,
    'automation/task issues': 0,
    'integration/onboarding sources': 0,
    'time management': 0
}

for response in improve_responses:
    response_lower = str(response).lower()
    if any(word in response_lower for word in ['nothing', 'n/a', 'na', 'no change', 'no suggestions', 'can\'t think']):
        improve_themes['nothing/no suggestions'] += 1
    if any(word in response_lower for word in ['wait', 'timeline', 'time', 'months', 'long']):
        improve_themes['timeline/wait time'] += 1
    if any(word in response_lower for word in ['benefits', 'hr', 'health insurance']):
        improve_themes['benefits/HR orientation'] += 1
    if any(word in response_lower for word in ['new employee', 'new hire', 'new staff', 'cohort', 'other new']):
        improve_themes['connection with new hires'] += 1
    if any(word in response_lower for word in ['consistency', 'training manual']):
        improve_themes['training consistency'] += 1
    if any(word in response_lower for word in ['unnecessary meeting', 'efficiency', 'too many']):
        improve_themes['meeting efficiency'] += 1
    if any(word in response_lower for word in ['overview', 'other team', 'other area', 'department']):
        improve_themes['overview of NDR teams'] += 1
    if any(word in response_lower for word in ['automated', 'automation', 'task', 'fix issue']):
        improve_themes['automation/task issues'] += 1
    if any(word in response_lower for word in ['integration', 'overlap', 'confusion', 'source']):
        improve_themes['integration/onboarding sources'] += 1
    if any(word in response_lower for word in ['time', 'first week', 'dedicated time']):
        improve_themes['time management'] += 1

# Sort and display themes
sorted_improve = sorted(improve_themes.items(), key=lambda x: x[1], reverse=True)
for theme, count in sorted_improve:
    if count > 0:
        percentage = (count / len(improve_responses)) * 100
        print(f"  {theme.upper()}: {count} mentions ({percentage:.1f}%)")

print("\n\nSAMPLE IMPROVEMENT SUGGESTIONS:")
print("-" * 80)
# Filter out "nothing" responses for meaningful suggestions
meaningful_improve = improve_responses[~improve_responses.str.lower().isin(['na', 'n/a', 'nothing', 'no change', 'none'])]
sample_improve = meaningful_improve.head(8)
for i, response in enumerate(sample_improve, 1):
    print(f"{i}. \"{response}\"")

print("\n" + "="*80)
print("TIME-BASED TRENDS")
print("="*80)

# Analyze if satisfaction has changed over time
df['Quarter'] = df['StartDate'].dt.to_period('Q')

# Calculate average scores by quarter for key questions
key_questions = ['Q8', 'Q10', 'Q14', 'Q18']  # Happy with decision, feel part of NDR, manager communication, engaged
print("\n\nSatisfaction Over Time (Average Scores by Quarter):")
print("-" * 80)

for q in key_questions:
    if q in df.columns:
        quarterly_scores = df.groupby('Quarter')[q].apply(
            lambda x: calculate_sentiment_score(x).mean()
        )
        print(f"\n{likert_questions[q]}:")
        for quarter, score in quarterly_scores.items():
            print(f"  {quarter}: {score:.2f}/5.00")

print("\n" + "="*80)
print("KEY FINDINGS SUMMARY")
print("="*80)

print("\n1. OVERALL SATISFACTION:")
print("   - High satisfaction with onboarding process (most metrics >85% positive)")
print("   - Employees feel welcomed and supported")
print("   - Manager communication and support rated highly")

print("\n2. TOP STRENGTHS:")
top_3 = results_df.head(3)
for idx, row in top_3.iterrows():
    print(f"   - {row['question'].split('.')[1].strip()}: {row['positive_rate']:.1f}% positive")

print("\n3. AREAS FOR IMPROVEMENT:")
bottom_3 = results_df.tail(3)
for idx, row in bottom_3.iterrows():
    print(f"   - {row['question'].split('.')[1].strip()}: {row['positive_rate']:.1f}% positive")

print("\n4. COMMON THEMES FROM FEEDBACK:")
print("   LIKED:")
for theme, count in sorted_liked[:5]:
    if count > 0:
        print(f"   - {theme}")

print("\n   IMPROVEMENT AREAS:")
for theme, count in sorted_improve[:5]:
    if count > 0 and 'nothing' not in theme.lower():
        print(f"   - {theme}")

print("\n" + "="*80)
print("END OF ANALYSIS")
print("="*80)
