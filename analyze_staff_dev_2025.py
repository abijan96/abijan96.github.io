import pandas as pd
import numpy as np
from datetime import datetime

# Read the Excel file
file_path = r'C:\Users\USER\Downloads\Staff Development Day Survey 2025 (Responses).xlsx'
df = pd.read_excel(file_path)

print("=" * 80)
print("STAFF DEVELOPMENT DAY 2025 - SURVEY ANALYSIS")
print("=" * 80)
print(f"\nTotal Responses: {len(df)}")
print(f"Survey Period: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
print("\n" + "=" * 80)

# 1. DEPARTMENT BREAKDOWN
print("\n1. DEPARTMENT DISTRIBUTION")
print("-" * 80)
dept_col = 'Please indicate your department.'
if dept_col in df.columns:
    dept_counts = df[dept_col].value_counts()
    print(f"\nTotal departments represented: {dept_counts.count()}")
    print("\nBreakdown:")
    for dept, count in dept_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {dept}: {count} ({pct:.1f}%)")

# 2. NET PROMOTER SCORE (NPS) - Overall Event
print("\n\n2. NET PROMOTER SCORE - OVERALL EVENT")
print("-" * 80)
nps_col = 'On a scale of 0-10, how likely are you to recommend Staff Development Day to a colleague?'
if nps_col in df.columns:
    nps_scores = df[nps_col].dropna()
    promoters = len(nps_scores[nps_scores >= 9])
    passives = len(nps_scores[(nps_scores >= 7) & (nps_scores < 9)])
    detractors = len(nps_scores[nps_scores < 7])
    nps = ((promoters - detractors) / len(nps_scores)) * 100

    print(f"\nAverage Score: {nps_scores.mean():.2f}/10")
    print(f"Promoters (9-10): {promoters} ({(promoters/len(nps_scores)*100):.1f}%)")
    print(f"Passives (7-8): {passives} ({(passives/len(nps_scores)*100):.1f}%)")
    print(f"Detractors (0-6): {detractors} ({(detractors/len(nps_scores)*100):.1f}%)")
    print(f"\nNet Promoter Score: {nps:.1f}")

# 3. EVENT LOGISTICS RATINGS
print("\n\n3. EVENT LOGISTICS")
print("-" * 80)
logistics = {
    'Organization & Flow': 'Regarding the Staff Development Day, how would you rate the following? [The organization and flow of the event?]',
    'Venue': 'Regarding the Staff Development Day, how would you rate the following? [The venue of the event?]',
    'Duration': 'Regarding the Staff Development Day, how would you rate the following? [The duration of the event?]'
}

for aspect, col in logistics.items():
    if col in df.columns:
        ratings = df[col].value_counts().sort_index(ascending=False)
        avg_rating = df[col].dropna().map({'Poor': 1, 'Fair': 2, 'Good': 3, 'Very Good': 4, 'Excellent': 5}).mean()
        print(f"\n{aspect}:")
        print(f"  Average: {avg_rating:.2f}/5")
        for rating, count in ratings.items():
            pct = (count / df[col].notna().sum()) * 100
            print(f"  {rating}: {count} ({pct:.1f}%)")

# 4. MORNING KEYNOTE - Katie DeWulf
print("\n\n4. MORNING KEYNOTE - Katie DeWulf: 'Navigate the Shift'")
print("-" * 80)
morning_keynote = {
    'Informative/Engaging': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [I thought the speaker was informative, engaging, and relatable.]',
    'Time Allotted': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [The time allotted for the keynote speaker was appropriate.]',
    'Relevance': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [The topic covered was relevant and informational.]'
}

for aspect, col in morning_keynote.items():
    if col in df.columns:
        ratings = df[col].value_counts().sort_index(ascending=False)
        avg_rating = df[col].dropna().map({'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly Agree': 5}).mean()
        print(f"\n{aspect}:")
        print(f"  Average: {avg_rating:.2f}/5")
        for rating, count in ratings.items():
            pct = (count / df[col].notna().sum()) * 100
            print(f"  {rating}: {count} ({pct:.1f}%)")

nps_morning = 'MORNING KEYNOTE SPEAKER - On a scale of 0-10, how likely are you to recommend the morning keynote speaker, Katie DeWulf : "Practical Strategies for Thriving Through Change" to a colleague?'
if nps_morning in df.columns:
    scores = df[nps_morning].dropna()
    print(f"\nRecommendation Score: {scores.mean():.2f}/10")

# 5. LUNCH & FIRESIDE CHAT - AI Discussion
print("\n\n5. LUNCH & FIRESIDE CHAT - 'Beyond the Buzz: Real Talk on AI'")
print("-" * 80)
fireside = {
    'Informative/Engaging': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The speakers were informative, engaging, and relatable.]',
    'Time Allotted': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The time allotted for the panel discussion was appropriate.]',
    'Relevance': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The topics covered were relevant and informational.]'
}

for aspect, col in fireside.items():
    if col in df.columns:
        ratings = df[col].value_counts().sort_index(ascending=False)
        avg_rating = df[col].dropna().map({'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly Agree': 5}).mean()
        print(f"\n{aspect}:")
        print(f"  Average: {avg_rating:.2f}/5")
        for rating, count in ratings.items():
            pct = (count / df[col].notna().sum()) * 100
            print(f"  {rating}: {count} ({pct:.1f}%)")

nps_fireside = 'LUNCH AND FIRESIDE CHAT On a scale of 0-10, how likely are you to recommend the lunch and fireside chat: "Beyond the Buzz: Real Talk on AI" to a colleague?'
if nps_fireside in df.columns:
    scores = df[nps_fireside].dropna()
    print(f"\nRecommendation Score: {scores.mean():.2f}/10")

# 6. AFTERNOON KEYNOTE - Stuart MacDonald
print("\n\n6. AFTERNOON KEYNOTE - Stuart MacDonald: 'Continuous Improvement & Magic'")
print("-" * 80)
afternoon_keynote = {
    'Informative/Engaging': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The speaker was informative, engaging, and relatable.]',
    'Time Allotted': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The time allotted for the keynote speaker was appropriate.]',
    'Relevance': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The topic covered was relevant and informational.]'
}

for aspect, col in afternoon_keynote.items():
    if col in df.columns:
        ratings = df[col].value_counts().sort_index(ascending=False)
        avg_rating = df[col].dropna().map({'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly Agree': 5}).mean()
        print(f"\n{aspect}:")
        print(f"  Average: {avg_rating:.2f}/5")
        for rating, count in ratings.items():
            pct = (count / df[col].notna().sum()) * 100
            print(f"  {rating}: {count} ({pct:.1f}%)")

nps_afternoon = 'AFTERNOON KEYNOTE SPEAKER - On a scale of 0-10, how likely would you recommend the afternoon keynote speaker, Stuart MacDonald: "Continuous Improvement & Magic?":'
if nps_afternoon in df.columns:
    scores = df[nps_afternoon].dropna()
    print(f"\nRecommendation Score: {scores.mean():.2f}/10")

# 7. MORNING BREAKOUT SESSIONS
print("\n\n7. MORNING BREAKOUT SESSIONS")
print("-" * 80)
morning_breakout_col = 'Please select which morning breakout session you attended:'
if morning_breakout_col in df.columns:
    breakout_counts = df[morning_breakout_col].value_counts()
    print("\nAttendance:")
    for session, count in breakout_counts.items():
        pct = (count / df[morning_breakout_col].notna().sum()) * 100
        print(f"  {session}: {count} ({pct:.1f}%)")

    morning_breakout_ratings = {
        'Informative/Engaging': 'Regarding the MORNING BREAKOUT SESSION you attended. [The speaker was informative, engaging, and relatable.]',
        'Time Allotted': 'Regarding the MORNING BREAKOUT SESSION you attended. [The time allotted for the speaker was appropriate.]',
        'Relevance': 'Regarding the MORNING BREAKOUT SESSION you attended. [The topic covered was relevant and informational.]'
    }

    print("\nOverall Ratings:")
    for aspect, col in morning_breakout_ratings.items():
        if col in df.columns:
            avg_rating = df[col].dropna().map({'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly Agree': 5}).mean()
            print(f"  {aspect}: {avg_rating:.2f}/5")

    nps_morning_breakout = 'On a scale of 0-10, how likely do you recommend attending the morning breakout session you attended to a friend or colleague?'
    if nps_morning_breakout in df.columns:
        scores = df[nps_morning_breakout].dropna()
        print(f"  Recommendation Score: {scores.mean():.2f}/10")

# 8. AFTERNOON BREAKOUT SESSIONS
print("\n\n8. AFTERNOON BREAKOUT SESSIONS")
print("-" * 80)
afternoon_breakout_col = 'Please select which afternoon breakout session you attended:'
if afternoon_breakout_col in df.columns:
    breakout_counts = df[afternoon_breakout_col].value_counts()
    print("\nAttendance:")
    for session, count in breakout_counts.items():
        pct = (count / df[afternoon_breakout_col].notna().sum()) * 100
        print(f"  {session}: {count} ({pct:.1f}%)")

    afternoon_breakout_ratings = {
        'Informative/Engaging': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The speaker was informative, engaging, and relatable.]',
        'Time Allotted': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The time allotted for the speaker was appropriate.]',
        'Relevance': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The topic covered was relevant and informational.]'
    }

    print("\nOverall Ratings:")
    for aspect, col in afternoon_breakout_ratings.items():
        if col in df.columns:
            avg_rating = df[col].dropna().map({'Strongly Disagree': 1, 'Disagree': 2, 'Neutral': 3, 'Agree': 4, 'Strongly Agree': 5}).mean()
            print(f"  {aspect}: {avg_rating:.2f}/5")

    nps_afternoon_breakout = 'On a scale of 0-10, how likely do you recommend attending the afternoon breakout session you attended to a friend or colleague?'
    if nps_afternoon_breakout in df.columns:
        scores = df[nps_afternoon_breakout].dropna()
        print(f"  Recommendation Score: {scores.mean():.2f}/10")

# 9. OPEN-ENDED FEEDBACK
print("\n\n9. QUALITATIVE FEEDBACK")
print("-" * 80)

feedback_col = 'Please provide any feedback as it relates to the schedule, content covered, or the overall experience.'
if feedback_col in df.columns:
    feedback = df[feedback_col].dropna()
    print(f"\nTotal feedback comments: {len(feedback)}")
    print("\nSample feedback:")
    for i, comment in enumerate(feedback.head(10), 1):
        print(f"\n{i}. {comment}")

future_content_col = 'What other content or sessions would you like to see covered in future Staff Development Day events?'
if future_content_col in df.columns:
    suggestions = df[future_content_col].dropna()
    print(f"\n\nFuture content suggestions: {len(suggestions)}")
    print("\nSample suggestions:")
    for i, suggestion in enumerate(suggestions.head(10), 1):
        print(f"\n{i}. {suggestion}")

# 10. SUMMARY & KEY INSIGHTS
print("\n\n" + "=" * 80)
print("10. KEY INSIGHTS & SUMMARY")
print("=" * 80)

# Calculate overall satisfaction
overall_nps = df[nps_col].dropna().mean() if nps_col in df.columns else None
morning_keynote_nps = df[nps_morning].dropna().mean() if nps_morning in df.columns else None
fireside_nps = df[nps_fireside].dropna().mean() if nps_fireside in df.columns else None
afternoon_keynote_nps = df[nps_afternoon].dropna().mean() if nps_afternoon in df.columns else None

print(f"\nOverall Event Satisfaction: {overall_nps:.2f}/10" if overall_nps else "N/A")
print(f"\nSession Performance (Recommendation Scores):")
print(f"  Morning Keynote (Katie DeWulf): {morning_keynote_nps:.2f}/10" if morning_keynote_nps else "N/A")
print(f"  Fireside Chat (AI): {fireside_nps:.2f}/10" if fireside_nps else "N/A")
print(f"  Afternoon Keynote (Stuart MacDonald): {afternoon_keynote_nps:.2f}/10" if afternoon_keynote_nps else "N/A")

print("\n" + "=" * 80)
print("Analysis complete!")
print("=" * 80)
