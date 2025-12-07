"""
Prepare comprehensive JSON data for D3.js dashboard
"""

import pandas as pd
import json
import numpy as np

# Load all the output files
kpi_overall = pd.read_csv('output_kpi_overall.csv')
kpi_by_dept = pd.read_csv('output_kpi_by_department.csv')
themes_overall = pd.read_csv('output_themes_overall.csv')
themes_by_dept = pd.read_csv('output_themes_by_department.csv')
buckets_detail = pd.read_csv('output_buckets_detail.csv')

# Load original data for additional details
file_path = r'C:\Users\USER\Downloads\Staff Development Day Survey 2025 (Responses).xlsx'
df_raw = pd.read_excel(file_path)

dept_col = 'Please indicate your department.'
morning_breakout_col = 'Please select which morning breakout session you attended:'
afternoon_breakout_col = 'Please select which afternoon breakout session you attended:'

def safe_float(val):
    """Convert to float, handling NaN"""
    if pd.isna(val):
        return None
    return float(val)

# Prepare comprehensive dashboard data
dashboard_data = {
    'metadata': {
        'title': 'Staff Development Day 2025 Survey Results',
        'total_responses': int(len(df_raw)),
        'survey_start': str(df_raw['Timestamp'].min()),
        'survey_end': str(df_raw['Timestamp'].max()),
        'departments': {k: int(v) for k, v in df_raw[dept_col].value_counts().to_dict().items()}
    },

    'overall_metrics': {
        'nps': {
            'overall_score': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['mean_0_10'].iloc[0]),
            'nps_value': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['nps_score'].iloc[0]),
            'promoters': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['promoter_pct'].iloc[0]),
            'passives': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['passive_pct'].iloc[0]),
            'detractors': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['detractor_pct'].iloc[0]),
            'top2_box': safe_float(kpi_overall[kpi_overall['metric'] == 'Overall_NPS']['top2_box_pct'].iloc[0])
        },
        'venue_score': safe_float(kpi_overall[kpi_overall['metric'] == 'Venue']['mean_0_10'].iloc[0]),
        'organization_score': safe_float(kpi_overall[kpi_overall['metric'] == 'Organization_Flow']['mean_0_10'].iloc[0]),
        'duration_score': safe_float(kpi_overall[kpi_overall['metric'] == 'Duration']['mean_0_10'].iloc[0])
    },

    'session_performance': [],

    'department_comparison': [],

    'themes': {
        'overall': themes_overall.to_dict(orient='records'),
        'by_department': themes_by_dept.to_dict(orient='records')
    },

    'kpi_by_department': [],  # Will populate after cleaning

    'breakout_sessions': {
        'morning': {k: int(v) for k, v in df_raw[morning_breakout_col].value_counts().to_dict().items()} if morning_breakout_col in df_raw.columns else {},
        'afternoon': {k: int(v) for k, v in df_raw[afternoon_breakout_col].value_counts().to_dict().items()} if afternoon_breakout_col in df_raw.columns else {}
    },

    'all_metrics': [],  # Will populate after cleaning

    'sentiment_distribution': {
        'positive': int(buckets_detail['sentiment_overall'].value_counts().get('Positive', 0)),
        'neutral': int(buckets_detail['sentiment_overall'].value_counts().get('Neutral', 0)),
        'negative': int(buckets_detail['sentiment_overall'].value_counts().get('Negative', 0))
    }
}

# Session Performance (all NPS metrics)
nps_sessions = [
    {'name': 'Morning Keynote', 'metric': 'Morning_Keynote_NPS', 'speaker': 'Katie DeWulf'},
    {'name': 'Fireside Chat (AI)', 'metric': 'Fireside_NPS', 'speaker': 'AI Panel'},
    {'name': 'Afternoon Keynote', 'metric': 'Afternoon_Keynote_NPS', 'speaker': 'Stuart MacDonald'},
    {'name': 'Morning Breakout', 'metric': 'Morning_Breakout_NPS', 'speaker': 'Various'},
    {'name': 'Afternoon Breakout', 'metric': 'Afternoon_Breakout_NPS', 'speaker': 'Various'}
]

for session in nps_sessions:
    session_data = kpi_overall[kpi_overall['metric'] == session['metric']].iloc[0]

    # Get detail metrics with proper NaN handling
    engaging_metric = session['metric'].replace('_NPS', '_Engaging')
    time_metric = session['metric'].replace('_NPS', '_Time')
    relevant_metric = session['metric'].replace('_NPS', '_Relevant')

    engaging_val = None
    time_val = None
    relevant_val = None

    if engaging_metric in kpi_overall['metric'].values:
        val = kpi_overall[kpi_overall['metric'] == engaging_metric]['mean_0_10'].iloc[0]
        engaging_val = safe_float(val)

    if time_metric in kpi_overall['metric'].values:
        val = kpi_overall[kpi_overall['metric'] == time_metric]['mean_0_10'].iloc[0]
        time_val = safe_float(val)

    if relevant_metric in kpi_overall['metric'].values:
        val = kpi_overall[kpi_overall['metric'] == relevant_metric]['mean_0_10'].iloc[0]
        relevant_val = safe_float(val)

    dashboard_data['session_performance'].append({
        'name': session['name'],
        'speaker': session['speaker'],
        'score': safe_float(session_data['mean_0_10']),
        'nps': safe_float(session_data['nps_score']),
        'promoters': safe_float(session_data['promoter_pct']),
        'passives': safe_float(session_data['passive_pct']),
        'detractors': safe_float(session_data['detractor_pct']),
        'top2_box': safe_float(session_data['top2_box_pct']),
        'details': {
            'engaging': engaging_val,
            'time': time_val,
            'relevant': relevant_val
        }
    })

# Department Comparison (Overall NPS by department)
departments = kpi_by_dept['department'].unique()
for dept in departments:
    dept_data = kpi_by_dept[(kpi_by_dept['department'] == dept) & (kpi_by_dept['metric'] == 'Overall_NPS')]
    if len(dept_data) > 0:
        dept_row = dept_data.iloc[0]
        dashboard_data['department_comparison'].append({
            'department': str(dept),
            'score': safe_float(dept_row['mean_0_10']),
            'nps': safe_float(dept_row['nps_score']),
            'promoters': safe_float(dept_row['promoter_pct']),
            'passives': safe_float(dept_row['passive_pct']),
            'detractors': safe_float(dept_row['detractor_pct']),
            'respondents': int(dept_row['n_responses'])
        })

# Sort department comparison by score
dashboard_data['department_comparison'].sort(key=lambda x: x['score'] if x['score'] is not None else 0, reverse=True)

# Clean up NaN values in themes
for theme in dashboard_data['themes']['overall']:
    for key in theme:
        if isinstance(theme[key], float) and np.isnan(theme[key]):
            theme[key] = None

for theme in dashboard_data['themes']['by_department']:
    for key in theme:
        if isinstance(theme[key], float) and np.isnan(theme[key]):
            theme[key] = None

# Clean and populate all_metrics
for metric_dict in kpi_overall.to_dict(orient='records'):
    cleaned_metric = {}
    for key, value in metric_dict.items():
        if isinstance(value, float) and np.isnan(value):
            cleaned_metric[key] = None
        else:
            cleaned_metric[key] = value
    dashboard_data['all_metrics'].append(cleaned_metric)

# Clean and populate kpi_by_department
for metric_dict in kpi_by_dept.to_dict(orient='records'):
    cleaned_metric = {}
    for key, value in metric_dict.items():
        if isinstance(value, float) and np.isnan(value):
            cleaned_metric[key] = None
        else:
            cleaned_metric[key] = value
    dashboard_data['kpi_by_department'].append(cleaned_metric)

# Save to JSON
with open('dashboard_data.json', 'w') as f:
    json.dump(dashboard_data, f, indent=2)

print("Dashboard data prepared successfully!")
print(f"Total responses: {dashboard_data['metadata']['total_responses']}")
print(f"Sessions tracked: {len(dashboard_data['session_performance'])}")
print(f"Departments: {len(dashboard_data['department_comparison'])}")
print(f"Themes: {len(dashboard_data['themes']['overall'])}")
