"""
Staff Development Day 2025 - Comprehensive Survey Analytics
Survey & People Analytics Analyst Approach
"""

import pandas as pd
import numpy as np
import json
import re
from collections import Counter, defaultdict

# ============================================================================
# CONFIGURATION & MAPPINGS
# ============================================================================

# Likert Agreement Scale Mapping
AGREEMENT_MAP = {
    'strongly agree': 5,
    'agree': 4,
    'tend to agree': 4,
    'neither': 3,
    'neutral': 3,
    'tend to disagree': 2,
    'disagree': 2,
    'strongly disagree': 1
}

# Quality Scale Mapping
QUALITY_MAP = {
    'excellent': 5,
    'very good': 4,
    'good': 4,
    'fair': 3,
    'poor': 2,
    'very poor': 1
}

# Theme Taxonomy
THEME_TAXONOMY = [
    'Session Timing & Duration',
    'Speaker/Facilitator Quality',
    'Content Relevance & Applicability',
    'Networking/Peer Interaction',
    'Venue & Logistics',
    'Organization & Flow',
    'Keynotes',
    'Breakouts',
    'Lunch/Fireside',
    'Suggestions/Requests',
    'Other'
]

# Theme Keywords (for detection)
THEME_KEYWORDS = {
    'Session Timing & Duration': ['time', 'timing', 'duration', 'long', 'short', 'rushed', 'downtime', 'pacing', 'schedule', 'transition', 'break'],
    'Speaker/Facilitator Quality': ['speaker', 'facilitator', 'presenter', 'engaging', 'informative', 'disjointed', 'hard to follow'],
    'Content Relevance & Applicability': ['relevant', 'practical', 'applicable', 'useful', 'content', 'topic', 'training', 'skill'],
    'Networking/Peer Interaction': ['network', 'colleague', 'interact', 'peer', 'conversation', 'connect'],
    'Venue & Logistics': ['venue', 'room', 'location', 'food', 'lunch', 'breakfast', 'catering', 'setup'],
    'Organization & Flow': ['organization', 'flow', 'organized', 'structure', 'coordination'],
    'Keynotes': ['keynote', 'katie', 'dewulf', 'stuart', 'macdonald', 'magic'],
    'Breakouts': ['breakout', 'session', 'workshop', 'claudia', 'anna', 'amy', 'maureen', 'scott', 'chris', 'ashley', 'josh', 'matt'],
    'Lunch/Fireside': ['fireside', 'ai', 'panel', 'lunch'],
    'Suggestions/Requests': ['future', 'would like', 'suggest', 'recommend', 'next year', 'more', 'advanced', '201', '301', 'deeper']
}

# Sentiment Keywords
POSITIVE_WORDS = ['great', 'excellent', 'fantastic', 'loved', 'appreciate', 'helpful', 'valuable', 'enjoyed', 'wonderful', 'amazing', 'best', 'insightful']
NEGATIVE_WORDS = ['disappointed', 'poor', 'rushed', 'boring', 'irrelevant', 'waste', 'frustrat', 'annoying', 'confusing', 'disjointed', 'ignored', 'refused']
NEGATION_WORDS = ['not', 'no', 'never', 'nothing', 'neither', 'nobody', 'nowhere', "n't", 'barely', 'hardly', 'scarcely']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def clean_text(text):
    """Clean and normalize text"""
    if pd.isna(text):
        return ''
    return str(text).strip().lower()

def normalize_likert_to_5(value):
    """Normalize Likert agreement scale to 1-5"""
    if pd.isna(value):
        return np.nan

    # If already numeric and in range 1-5
    try:
        num = float(value)
        if 1 <= num <= 5:
            return num
    except (ValueError, TypeError):
        pass

    # Map text responses
    cleaned = clean_text(value)
    return AGREEMENT_MAP.get(cleaned, np.nan)

def normalize_quality_to_5(value):
    """Normalize quality scale to 1-5"""
    if pd.isna(value):
        return np.nan

    # If already numeric and in range 1-5
    try:
        num = float(value)
        if 1 <= num <= 5:
            return num
    except (ValueError, TypeError):
        pass

    # Map text responses
    cleaned = clean_text(value)
    return QUALITY_MAP.get(cleaned, np.nan)

def convert_5_to_10(value):
    """Convert 1-5 scale to 0-10 scale"""
    if pd.isna(value):
        return np.nan
    return (value - 1) / 4 * 10

def normalize_nps(value):
    """Normalize NPS (0-10) values"""
    if pd.isna(value):
        return np.nan
    try:
        num = float(value)
        if 0 <= num <= 10:
            return num
    except (ValueError, TypeError):
        pass
    return np.nan

def get_nps_bucket(score):
    """Categorize NPS score into Detractor/Passive/Promoter"""
    if pd.isna(score):
        return 'Missing'
    if score <= 6:
        return 'Detractor'
    elif score <= 8:
        return 'Passive'
    else:
        return 'Promoter'

def get_sat_bucket(score):
    """Categorize satisfaction score into Low/Medium/High"""
    if pd.isna(score):
        return 'Missing'
    if score < 5.0:
        return 'Low'
    elif score < 8.0:
        return 'Medium'
    else:
        return 'High'

def is_top2_box(score):
    """Check if score is Top-2 Box (>=8/10)"""
    if pd.isna(score):
        return False
    return score >= 8.0

def detect_sentiment(text):
    """Detect sentiment: Positive/Neutral/Negative"""
    if pd.isna(text) or not text.strip():
        return 'Neutral'

    text_lower = text.lower()
    words = re.findall(r'\b\w+\b', text_lower)

    # Check for negations
    negated_indices = set()
    for i, word in enumerate(words):
        if any(neg in word for neg in NEGATION_WORDS):
            # Mark next 3 words as negated
            for j in range(i+1, min(i+4, len(words))):
                negated_indices.add(j)

    # Count sentiment
    pos_count = 0
    neg_count = 0

    for i, word in enumerate(words):
        is_negated = i in negated_indices

        if any(pos in word for pos in POSITIVE_WORDS):
            if is_negated:
                neg_count += 1
            else:
                pos_count += 1

        if any(neg in word for neg in NEGATIVE_WORDS):
            if is_negated:
                pos_count += 1
            else:
                neg_count += 1

    # Determine overall sentiment
    if pos_count > neg_count:
        return 'Positive'
    elif neg_count > pos_count:
        return 'Negative'
    else:
        return 'Neutral'

def extract_themes(text):
    """Extract themes from text based on keyword matching"""
    if pd.isna(text) or not text.strip():
        return []

    text_lower = text.lower()
    detected_themes = []

    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in text_lower for keyword in keywords):
            detected_themes.append(theme)

    if not detected_themes:
        detected_themes.append('Other')

    return detected_themes

def get_theme_sentiments(text, themes):
    """Get sentiment for each theme mentioned"""
    # For simplicity, apply overall sentiment to all themes
    # In production, would do more granular sentence-level analysis
    overall_sent = detect_sentiment(text)
    return [{'theme': theme, 'sentiment': overall_sent} for theme in themes]

def extract_quote(text, max_words=25):
    """Extract a representative quote (max 25 words)"""
    if pd.isna(text) or not text.strip():
        return ''

    # Take first sentence or up to max_words
    sentences = re.split(r'[.!?]', text.strip())
    first_sentence = sentences[0].strip()

    words = first_sentence.split()
    if len(words) <= max_words:
        return first_sentence
    else:
        return ' '.join(words[:max_words]) + '...'

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def main():
    print("=" * 80)
    print("STAFF DEVELOPMENT DAY 2025 - COMPREHENSIVE SURVEY ANALYTICS")
    print("=" * 80)

    # Load data
    file_path = r'C:\Users\USER\Downloads\Staff Development Day Survey 2025 (Responses).xlsx'
    df = pd.read_excel(file_path)

    print(f"\nLoaded {len(df)} responses")

    # Add respondent ID
    df['respondent_id'] = range(1, len(df) + 1)

    # ========================================================================
    # A) NORMALIZE ALL SCALES
    # ========================================================================
    print("\n" + "=" * 80)
    print("A) NORMALIZING ALL SCALES TO 0-10")
    print("=" * 80)

    # Column definitions
    dept_col = 'Please indicate your department.'

    # NPS columns (already 0-10)
    nps_cols = {
        'Overall_NPS': 'On a scale of 0-10, how likely are you to recommend Staff Development Day to a colleague?',
        'Morning_Keynote_NPS': 'MORNING KEYNOTE SPEAKER - On a scale of 0-10, how likely are you to recommend the morning keynote speaker, Katie DeWulf : "Practical Strategies for Thriving Through Change" to a colleague?',
        'Fireside_NPS': 'LUNCH AND FIRESIDE CHAT On a scale of 0-10, how likely are you to recommend the lunch and fireside chat: "Beyond the Buzz: Real Talk on AI" to a colleague?',
        'Afternoon_Keynote_NPS': 'AFTERNOON KEYNOTE SPEAKER - On a scale of 0-10, how likely would you recommend the afternoon keynote speaker, Stuart MacDonald: "Continuous Improvement & Magic?":',
        'Morning_Breakout_NPS': 'On a scale of 0-10, how likely do you recommend attending the morning breakout session you attended to a friend or colleague?',
        'Afternoon_Breakout_NPS': 'On a scale of 0-10, how likely do you recommend attending the afternoon breakout session you attended to a friend or colleague?'
    }

    # Quality columns (need mapping to 1-5, then 0-10)
    quality_cols = {
        'Organization_Flow': 'Regarding the Staff Development Day, how would you rate the following? [The organization and flow of the event?]',
        'Venue': 'Regarding the Staff Development Day, how would you rate the following? [The venue of the event?]',
        'Duration': 'Regarding the Staff Development Day, how would you rate the following? [The duration of the event?]'
    }

    # Likert agreement columns (need mapping to 1-5, then 0-10)
    likert_cols = {
        'Morning_Keynote_Engaging': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [I thought the speaker was informative, engaging, and relatable.]',
        'Morning_Keynote_Time': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [The time allotted for the keynote speaker was appropriate.]',
        'Morning_Keynote_Relevant': 'Regarding the MORNING KEYNOTE SPEAKER - Katie DeWulf - The Big Apple Red: "Navigate the Shift: Practical Strategies for Thriving Through Change", please rate the following questions: [The topic covered was relevant and informational.]',
        'Fireside_Engaging': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The speakers were informative, engaging, and relatable.]',
        'Fireside_Time': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The time allotted for the panel discussion was appropriate.]',
        'Fireside_Relevant': 'Regarding the LUNCH AND FIRESIDE CHAT - Beyond the Buzz: "Real Talk on AI", please rate the following questions: [The topics covered were relevant and informational.]',
        'Afternoon_Keynote_Engaging': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The speaker was informative, engaging, and relatable.]',
        'Afternoon_Keynote_Time': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The time allotted for the keynote speaker was appropriate.]',
        'Afternoon_Keynote_Relevant': 'Regarding the AFTERNOON KEYNOTE SPEAKER - Stuart MacDonald: "Continuous Improvement and Magic," please rate the following questions: [The topic covered was relevant and informational.]',
        'Morning_Breakout_Engaging': 'Regarding the MORNING BREAKOUT SESSION you attended. [The speaker was informative, engaging, and relatable.]',
        'Morning_Breakout_Time': 'Regarding the MORNING BREAKOUT SESSION you attended. [The time allotted for the speaker was appropriate.]',
        'Morning_Breakout_Relevant': 'Regarding the MORNING BREAKOUT SESSION you attended. [The topic covered was relevant and informational.]',
        'Afternoon_Breakout_Engaging': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The speaker was informative, engaging, and relatable.]',
        'Afternoon_Breakout_Time': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The time allotted for the speaker was appropriate.]',
        'Afternoon_Breakout_Relevant': 'Regarding the AFTERNOON BREAKOUT SESSION you attended. [The topic covered was relevant and informational.]'
    }

    # Normalize NPS columns (already 0-10)
    for new_col, orig_col in nps_cols.items():
        if orig_col in df.columns:
            df[new_col] = df[orig_col].apply(normalize_nps)
            print(f"[OK] Normalized {new_col}: mean={df[new_col].mean():.2f}/10")

    # Normalize Quality columns (map to 1-5, then convert to 0-10)
    for new_col, orig_col in quality_cols.items():
        if orig_col in df.columns:
            df[f'{new_col}_5pt'] = df[orig_col].apply(normalize_quality_to_5)
            df[new_col] = df[f'{new_col}_5pt'].apply(convert_5_to_10)
            print(f"[OK] Normalized {new_col}: mean={df[new_col].mean():.2f}/10")

    # Normalize Likert columns (map to 1-5, then convert to 0-10)
    for new_col, orig_col in likert_cols.items():
        if orig_col in df.columns:
            df[f'{new_col}_5pt'] = df[orig_col].apply(normalize_likert_to_5)
            df[new_col] = df[f'{new_col}_5pt'].apply(convert_5_to_10)
            print(f"[OK] Normalized {new_col}: mean={df[new_col].mean():.2f}/10")

    # ========================================================================
    # B) BUCKETIZATION
    # ========================================================================
    print("\n" + "=" * 80)
    print("B) APPLYING BUCKETIZATION")
    print("=" * 80)

    # NPS Buckets
    for col in nps_cols.keys():
        bucket_col = f'{col}_Bucket'
        df[bucket_col] = df[col].apply(get_nps_bucket)
        print(f"[OK] Created {bucket_col}")

    # Satisfaction Buckets (for all other normalized columns)
    all_other_cols = list(quality_cols.keys()) + list(likert_cols.keys())
    for col in all_other_cols:
        bucket_col = f'{col}_Bucket'
        df[bucket_col] = df[col].apply(get_sat_bucket)
        print(f"[OK] Created {bucket_col}")

    # Top-2 Box flags
    all_norm_cols = list(nps_cols.keys()) + all_other_cols
    for col in all_norm_cols:
        top2_col = f'{col}_Top2Box'
        df[top2_col] = df[col].apply(is_top2_box)

    print(f"\n[OK] Created Top-2 Box flags for all {len(all_norm_cols)} normalized columns")

    # ========================================================================
    # C) SENTIMENT & THEMES
    # ========================================================================
    print("\n" + "=" * 80)
    print("C) ANALYZING SENTIMENT & THEMES")
    print("=" * 80)

    # Open-ended columns
    feedback_col = 'Please provide any feedback as it relates to the schedule, content covered, or the overall experience.'
    future_col = 'What other content or sessions would you like to see covered in future Staff Development Day events?'

    # Combine both feedback columns
    df['combined_feedback'] = df[feedback_col].fillna('') + ' ' + df[future_col].fillna('')

    # Apply sentiment & theme analysis
    df['sentiment_overall'] = df['combined_feedback'].apply(detect_sentiment)
    df['themes'] = df['combined_feedback'].apply(extract_themes)
    df['theme_sentiments'] = df.apply(lambda row: get_theme_sentiments(row['combined_feedback'], row['themes']), axis=1)
    df['quote_short'] = df['combined_feedback'].apply(extract_quote)

    sentiment_counts = df['sentiment_overall'].value_counts()
    print(f"\nSentiment Distribution:")
    for sent, count in sentiment_counts.items():
        print(f"  {sent}: {count} ({count/len(df)*100:.1f}%)")

    # Count theme prevalence
    all_themes = [theme for themes_list in df['themes'] for theme in themes_list]
    theme_counts = Counter(all_themes)
    print(f"\nTop Themes:")
    for theme, count in theme_counts.most_common(10):
        print(f"  {theme}: {count} mentions ({count/len(df)*100:.1f}%)")

    # ========================================================================
    # D) AGGREGATIONS
    # ========================================================================
    print("\n" + "=" * 80)
    print("D) GENERATING AGGREGATIONS")
    print("=" * 80)

    # --- KPI Overall ---
    kpi_overall_data = []

    for col in all_norm_cols:
        if col in df.columns:
            mean_score = df[col].mean()
            top2_pct = df[f'{col}_Top2Box'].sum() / df[col].notna().sum() * 100 if df[col].notna().sum() > 0 else 0

            row = {
                'metric': col,
                'mean_0_10': round(mean_score, 2),
                'top2_box_pct': round(top2_pct, 1),
                'n_responses': df[col].notna().sum()
            }

            # Add NPS breakdowns if applicable
            if col in nps_cols.keys():
                bucket_col = f'{col}_Bucket'
                bucket_counts = df[bucket_col].value_counts()
                total_valid = df[col].notna().sum()
                row['detractor_pct'] = round(bucket_counts.get('Detractor', 0) / total_valid * 100, 1) if total_valid > 0 else 0
                row['passive_pct'] = round(bucket_counts.get('Passive', 0) / total_valid * 100, 1) if total_valid > 0 else 0
                row['promoter_pct'] = round(bucket_counts.get('Promoter', 0) / total_valid * 100, 1) if total_valid > 0 else 0
                row['nps_score'] = row['promoter_pct'] - row['detractor_pct']

            kpi_overall_data.append(row)

    kpi_overall_df = pd.DataFrame(kpi_overall_data)
    print(f"\n[OK] Generated overall KPIs for {len(kpi_overall_data)} metrics")

    # --- KPI by Department ---
    kpi_by_dept_data = []

    departments = df[dept_col].dropna().unique()

    for dept in departments:
        dept_df = df[df[dept_col] == dept]

        for col in all_norm_cols:
            if col in dept_df.columns and dept_df[col].notna().sum() > 0:
                mean_score = dept_df[col].mean()
                top2_pct = dept_df[f'{col}_Top2Box'].sum() / dept_df[col].notna().sum() * 100

                row = {
                    'department': dept,
                    'metric': col,
                    'mean_0_10': round(mean_score, 2),
                    'top2_box_pct': round(top2_pct, 1),
                    'n_responses': dept_df[col].notna().sum()
                }

                # Add NPS breakdowns if applicable
                if col in nps_cols.keys():
                    bucket_col = f'{col}_Bucket'
                    bucket_counts = dept_df[bucket_col].value_counts()
                    total_valid = dept_df[col].notna().sum()
                    row['detractor_pct'] = round(bucket_counts.get('Detractor', 0) / total_valid * 100, 1)
                    row['passive_pct'] = round(bucket_counts.get('Passive', 0) / total_valid * 100, 1)
                    row['promoter_pct'] = round(bucket_counts.get('Promoter', 0) / total_valid * 100, 1)
                    row['nps_score'] = row['promoter_pct'] - row['detractor_pct']

                kpi_by_dept_data.append(row)

    kpi_by_dept_df = pd.DataFrame(kpi_by_dept_data)
    print(f"[OK] Generated departmental KPIs: {len(kpi_by_dept_data)} records")

    # --- Themes Overall ---
    themes_overall_data = []

    for theme in THEME_TAXONOMY:
        # Count mentions
        mentions = sum(1 for themes_list in df['themes'] if theme in themes_list)
        if mentions == 0:
            continue

        prevalence_pct = mentions / len(df) * 100

        # Get sentiment breakdown for this theme
        pos_count = 0
        neu_count = 0
        neg_count = 0
        sample_quotes = []

        for idx, row in df.iterrows():
            if theme in row['themes']:
                sent = row['sentiment_overall']
                if sent == 'Positive':
                    pos_count += 1
                elif sent == 'Neutral':
                    neu_count += 1
                elif sent == 'Negative':
                    neg_count += 1

                if row['quote_short'] and len(sample_quotes) < 3:
                    sample_quotes.append(row['quote_short'])

        themes_overall_data.append({
            'theme': theme,
            'prevalence_pct': round(prevalence_pct, 1),
            'mentions': mentions,
            'pos_pct': round(pos_count / mentions * 100, 1) if mentions > 0 else 0,
            'neu_pct': round(neu_count / mentions * 100, 1) if mentions > 0 else 0,
            'neg_pct': round(neg_count / mentions * 100, 1) if mentions > 0 else 0,
            'sample_quote': sample_quotes[0] if sample_quotes else ''
        })

    themes_overall_df = pd.DataFrame(themes_overall_data).sort_values('prevalence_pct', ascending=False)
    print(f"[OK] Generated theme analysis: {len(themes_overall_data)} themes")

    # --- Themes by Department ---
    themes_by_dept_data = []

    for dept in departments:
        dept_df = df[df[dept_col] == dept]

        for theme in THEME_TAXONOMY:
            mentions = sum(1 for themes_list in dept_df['themes'] if theme in themes_list)
            if mentions == 0:
                continue

            prevalence_pct = mentions / len(dept_df) * 100

            pos_count = sum(1 for idx, row in dept_df.iterrows() if theme in row['themes'] and row['sentiment_overall'] == 'Positive')
            neu_count = sum(1 for idx, row in dept_df.iterrows() if theme in row['themes'] and row['sentiment_overall'] == 'Neutral')
            neg_count = sum(1 for idx, row in dept_df.iterrows() if theme in row['themes'] and row['sentiment_overall'] == 'Negative')

            themes_by_dept_data.append({
                'department': dept,
                'theme': theme,
                'prevalence_pct': round(prevalence_pct, 1),
                'mentions': mentions,
                'pos_pct': round(pos_count / mentions * 100, 1) if mentions > 0 else 0,
                'neu_pct': round(neu_count / mentions * 100, 1) if mentions > 0 else 0,
                'neg_pct': round(neg_count / mentions * 100, 1) if mentions > 0 else 0
            })

    themes_by_dept_df = pd.DataFrame(themes_by_dept_data)
    print(f"[OK] Generated departmental theme analysis: {len(themes_by_dept_data)} records")

    # ========================================================================
    # E) OUTPUTS
    # ========================================================================
    print("\n" + "=" * 80)
    print("E) EXPORTING OUTPUTS")
    print("=" * 80)

    # --- Buckets Detail (row-level) ---
    export_cols = ['respondent_id', dept_col, 'sentiment_overall', 'themes', 'theme_sentiments', 'quote_short']
    export_cols += all_norm_cols  # All normalized 0-10 columns
    export_cols += [f'{col}_Bucket' for col in all_norm_cols]  # All bucket columns

    # Filter to only existing columns
    export_cols = [col for col in export_cols if col in df.columns]

    buckets_detail_df = df[export_cols].copy()

    # Convert lists to JSON strings for CSV export
    buckets_detail_df['themes'] = buckets_detail_df['themes'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    buckets_detail_df['theme_sentiments'] = buckets_detail_df['theme_sentiments'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

    # Export to CSV
    buckets_detail_df.to_csv('output_buckets_detail.csv', index=False)
    print("[OK] Exported: output_buckets_detail.csv")

    kpi_overall_df.to_csv('output_kpi_overall.csv', index=False)
    print("[OK] Exported: output_kpi_overall.csv")

    kpi_by_dept_df.to_csv('output_kpi_by_department.csv', index=False)
    print("[OK] Exported: output_kpi_by_department.csv")

    themes_overall_df.to_csv('output_themes_overall.csv', index=False)
    print("[OK] Exported: output_themes_overall.csv")

    themes_by_dept_df.to_csv('output_themes_by_department.csv', index=False)
    print("[OK] Exported: output_themes_by_department.csv")

    # Also export as JSON
    outputs_json = {
        'kpi_overall': kpi_overall_df.to_dict(orient='records'),
        'kpi_by_department': kpi_by_dept_df.to_dict(orient='records'),
        'themes_overall': themes_overall_df.to_dict(orient='records'),
        'themes_by_department': themes_by_dept_df.to_dict(orient='records')
    }

    with open('output_analytics_summary.json', 'w') as f:
        json.dump(outputs_json, f, indent=2)
    print("[OK] Exported: output_analytics_summary.json")

    # ========================================================================
    # F) EXECUTIVE SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("F) EXECUTIVE SUMMARY")
    print("=" * 80)

    summary = []

    # Overall satisfaction
    overall_nps = kpi_overall_df[kpi_overall_df['metric'] == 'Overall_NPS'].iloc[0]
    summary.append(f"Overall event satisfaction: {overall_nps['mean_0_10']}/10 with NPS of {overall_nps['nps_score']:.1f} ({overall_nps['promoter_pct']:.1f}% promoters, {overall_nps['detractor_pct']:.1f}% detractors)")

    # Top-2 Box highlights
    top_metrics = kpi_overall_df.nlargest(3, 'top2_box_pct')
    summary.append(f"Top-rated elements: {top_metrics.iloc[0]['metric']} ({top_metrics.iloc[0]['top2_box_pct']:.1f}% Top-2 Box), {top_metrics.iloc[1]['metric']} ({top_metrics.iloc[1]['top2_box_pct']:.1f}%), {top_metrics.iloc[2]['metric']} ({top_metrics.iloc[2]['top2_box_pct']:.1f}%)")

    # NPS performance by session
    nps_metrics = kpi_overall_df[kpi_overall_df['metric'].str.contains('NPS', na=False)].sort_values('mean_0_10', ascending=False)
    summary.append(f"Session NPS rankings: 1) {nps_metrics.iloc[0]['metric']} ({nps_metrics.iloc[0]['mean_0_10']}/10), 2) {nps_metrics.iloc[1]['metric']} ({nps_metrics.iloc[1]['mean_0_10']}/10), 3) {nps_metrics.iloc[2]['metric']} ({nps_metrics.iloc[2]['mean_0_10']}/10)")

    # Key strengths (from themes)
    pos_themes = themes_overall_df[themes_overall_df['pos_pct'] > 50].nlargest(3, 'prevalence_pct')
    if len(pos_themes) > 0:
        strength_list = ', '.join([f"{row['theme']} ({row['pos_pct']:.0f}% positive)" for _, row in pos_themes.iterrows()])
        summary.append(f"Key strengths from feedback: {strength_list}")

    # Improvement areas (from themes with negative sentiment)
    neg_themes = themes_overall_df[themes_overall_df['neg_pct'] > 30].nlargest(3, 'prevalence_pct')
    if len(neg_themes) > 0:
        improve_list = ', '.join([f"{row['theme']} ({row['neg_pct']:.0f}% negative)" for _, row in neg_themes.iterrows()])
        summary.append(f"Areas for improvement: {improve_list}")

    # Specific improvement insights
    timing_theme = themes_overall_df[themes_overall_df['theme'] == 'Session Timing & Duration']
    if len(timing_theme) > 0 and timing_theme.iloc[0]['prevalence_pct'] > 20:
        summary.append(f"Timing/pacing mentioned by {timing_theme.iloc[0]['prevalence_pct']:.1f}% of respondents ({timing_theme.iloc[0]['neg_pct']:.0f}% negative sentiment) - key concern")

    # Lowest scoring metrics
    bottom_metrics = kpi_overall_df.nsmallest(3, 'mean_0_10')
    summary.append(f"Lowest-rated elements: {bottom_metrics.iloc[0]['metric']} ({bottom_metrics.iloc[0]['mean_0_10']}/10), {bottom_metrics.iloc[1]['metric']} ({bottom_metrics.iloc[1]['mean_0_10']}/10), {bottom_metrics.iloc[2]['metric']} ({bottom_metrics.iloc[2]['mean_0_10']}/10)")

    # Department differences
    dept_variance = kpi_by_dept_df[kpi_by_dept_df['metric'] == 'Overall_NPS'].copy()
    if len(dept_variance) > 1:
        max_dept = dept_variance.loc[dept_variance['mean_0_10'].idxmax()]
        min_dept = dept_variance.loc[dept_variance['mean_0_10'].idxmin()]
        variance = max_dept['mean_0_10'] - min_dept['mean_0_10']
        if variance > 1.0:
            summary.append(f"Department variance: {max_dept['department']} highest ({max_dept['mean_0_10']}/10) vs {min_dept['department']} lowest ({min_dept['mean_0_10']}/10) - {variance:.1f} point gap")
        else:
            summary.append(f"Department satisfaction relatively consistent across units (variance <1.0 point)")

    # Suggestions theme
    suggestions_theme = themes_overall_df[themes_overall_df['theme'] == 'Suggestions/Requests']
    if len(suggestions_theme) > 0:
        summary.append(f"Future content requests from {suggestions_theme.iloc[0]['prevalence_pct']:.1f}% of respondents - review for 2026 planning")

    # Content relevance
    relevance_cols = [col for col in kpi_overall_df['metric'] if 'Relevant' in col]
    if relevance_cols:
        relevance_avg = kpi_overall_df[kpi_overall_df['metric'].isin(relevance_cols)]['mean_0_10'].mean()
        summary.append(f"Content relevance average across all sessions: {relevance_avg:.2f}/10")

    # Engagement scores
    engagement_cols = [col for col in kpi_overall_df['metric'] if 'Engaging' in col]
    if engagement_cols:
        engagement_avg = kpi_overall_df[kpi_overall_df['metric'].isin(engagement_cols)]['mean_0_10'].mean()
        summary.append(f"Speaker engagement average across all sessions: {engagement_avg:.2f}/10")

    # Final recommendation
    if overall_nps['nps_score'] > 30:
        summary.append(f"Strong overall performance with healthy NPS - focus on optimizing timing/pacing for 2026")
    elif overall_nps['nps_score'] > 0:
        summary.append(f"Positive overall response - address timing concerns and content depth for improvement")
    else:
        summary.append(f"Event requires significant improvements - review all elements for 2026")

    # Print summary
    print("\nEXECUTIVE SUMMARY (12 Key Points):\n")
    for i, point in enumerate(summary[:12], 1):
        print(f"{i}. {point}\n")

    # Save to file
    with open('output_executive_summary.txt', 'w') as f:
        f.write("STAFF DEVELOPMENT DAY 2025 - EXECUTIVE SUMMARY\n")
        f.write("=" * 80 + "\n\n")
        for i, point in enumerate(summary[:12], 1):
            f.write(f"{i}. {point}\n\n")

    print("[OK] Exported: output_executive_summary.txt")

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    print("\nAssumptions & Notes:")
    print("- Agreement scale mapped: Strongly Agree=5, Agree/Tend to Agree=4, Neither=3, Disagree/Tend to Disagree=2, Strongly Disagree=1")
    print("- Quality scale mapped: Excellent=5, Good/Very Good=4, Fair=3, Poor=2, Very Poor=1")
    print("- All 1-5 scales converted to 0-10 using formula: (x-1)/4*10")
    print("- NPS buckets: Detractor=0-6, Passive=7-8, Promoter=9-10")
    print("- Satisfaction buckets: Low=0-4.9, Medium=5.0-7.9, High=8.0-10")
    print("- Top-2 Box = scores >=8/10")
    print("- Sentiment analysis uses keyword matching with negation handling")
    print("- Theme detection based on predefined taxonomy with keyword matching")
    print("- Combined both open-ended feedback fields for comprehensive analysis")

if __name__ == '__main__':
    main()
