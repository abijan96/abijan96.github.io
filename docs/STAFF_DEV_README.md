# Staff Development Day 2025 - Survey Analytics Project

## Overview
Comprehensive survey analytics and interactive dashboard for Staff Development Day 2025 survey results (112 responses across 5 departments).

## Files Generated

### Analytics Scripts
- **survey_analytics_comprehensive.py** - Main analytics engine with:
  - Scale normalization (Likert, Quality, NPS → 0-10)
  - Bucketization (NPS buckets, Satisfaction buckets, Top-2 Box)
  - Sentiment analysis & theme extraction
  - Departmental aggregations

- **prepare_dashboard_data.py** - Prepares JSON data for D3.js dashboard

### Data Outputs (CSV)
- **output_buckets_detail.csv** - Row-level data with all buckets & sentiment
- **output_kpi_overall.csv** - Overall metrics with NPS breakdowns
- **output_kpi_by_department.csv** - Departmental comparisons
- **output_themes_overall.csv** - Theme prevalence & sentiment
- **output_themes_by_department.csv** - Themes by department
- **output_analytics_summary.json** - All KPIs/themes in JSON format
- **output_executive_summary.txt** - 11-point executive summary
- **dashboard_data.json** - Data formatted for D3.js visualization

### Interactive Dashboard
- **staff-dev-dashboard.html** - Main dashboard page
- **dashboard.js** - D3.js visualization logic
  - Overall NPS gauge with promoter/passive/detractor breakdown
  - Session performance comparison (horizontal bar chart)
  - Department comparison (vertical bar chart)
  - Sentiment distribution (donut chart)
  - Key themes analysis (horizontal bar with prevalence %)
  - Session deep dive (grouped bar chart: Engaging, Time, Relevance)
  - Interactive tooltips on hover
  - Department filter dropdown

## Key Findings

### Overall Performance
- **Overall Satisfaction:** 8.29/10
- **NPS:** 37.5 (49% promoters, 12% detractors)
- **Top-rated:** Venue (9.38/10), Morning Breakouts (8.53/10)

### Critical Insights
1. **Session Timing Issues:** 52.7% mentioned timing/pacing concerns
2. **Morning Keynote:** Lowest NPS (7.44/10) - needs improvement
3. **Time Allocation:** Consistently lowest scores (6.27-6.50/10)
4. **Department Variance:** 1.2-point gap between highest and lowest
5. **Future Requests:** 38.4% want advanced/deeper content (201/301 level)

### Recommendations
1. Reduce downtime between sessions
2. Extend breakout session duration
3. Improve morning keynote content relevance
4. Develop advanced content tracks for repeat attendees
5. Address Keough School of Global Affairs concerns

## Technical Details

### Scale Normalization
- **Agreement Scale:** Strongly Agree=5 → Agree/Tend to Agree=4 → Neither=3 → Disagree/Tend to Disagree=2 → Strongly Disagree=1
- **Quality Scale:** Excellent=5 → Good/Very Good=4 → Fair=3 → Poor=2 → Very Poor=1
- **Conversion Formula:** (x-1)/4*10 to normalize 1-5 scales to 0-10
- **NPS:** Already 0-10, normalized directly

### Bucketization
- **NPS Buckets:** Detractor (0-6), Passive (7-8), Promoter (9-10)
- **Satisfaction Buckets:** Low (0-4.9), Medium (5.0-7.9), High (8.0-10)
- **Top-2 Box:** Scores ≥8/10

### Theme Taxonomy
11 themes identified:
1. Session Timing & Duration (52.7% prevalence)
2. Breakouts (42.0%)
3. Suggestions/Requests (38.4%)
4. Content Relevance & Applicability (33.9%)
5. Lunch/Fireside (33.0%)
6. Speaker/Facilitator Quality (24.1%)
7. Networking/Peer Interaction (21.4%)
8. Keynotes (21.4%)
9. Venue & Logistics (15.2%)
10. Organization & Flow (4.5%)
11. Other (2.7%)

## How to Use

### Running Analytics
```bash
python survey_analytics_comprehensive.py
```

### Viewing Dashboard
1. Open `staff-dev-dashboard.html` in a web browser
2. Ensure `dashboard_data.json` is in the same directory
3. Use department filter to view specific departments (feature ready for expansion)

### Requirements
- Python 3.x with pandas, numpy, openpyxl
- Modern web browser with JavaScript enabled
- D3.js v7 (loaded via CDN)

## Color Scheme
- Primary: Notre Dame Navy (#0C2340)
- Gold: Notre Dame Gold (#C99700)
- Success: Green (#27ae60)
- Warning: Orange (#f39c12)
- Danger: Red (#e74c3c)

## Source Data
- **Original File:** Staff Development Day Survey 2025 (Responses).xlsx
- **Responses:** 112
- **Survey Period:** November 12-18, 2025
- **Departments:** 5 (ND Research, College of Science, Mendoza, Arts & Letters, Keough)
