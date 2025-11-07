# Notre Dame Faculty Experience Survey Dashboard

An interactive data visualization dashboard for the Fall 2025 Faculty Experience Survey results.

**Live Demo:** https://abijan96.github.io/faculty-survey-dashboard/

## 📊 Features

- **Key Performance Indicators (KPIs)**: Overall satisfaction, eNPS, retention risk, belonging, psychological safety
- **Interactive Visualizations**: 8 different chart types including bar charts, scatter plots, radar charts, and heatmaps
- **Equity Analysis**: Demographic breakdowns by gender, race/ethnicity, and intersectional identities
- **Actionable Insights**: Each chart includes interpretation and recommendations for Deans

## 🚀 Deployment to GitHub Pages

### Method 1: Using GitHub Web Interface (Easiest)

1. **Go to your GitHub repository**: https://github.com/abijan96/abijan96.github.io

2. **Navigate to the repository** and click "Add file" → "Upload files"

3. **Upload these files**:
   - `index.html`
   - `dashboard.js`
   - `faculty_survey_data.csv`
   - `README.md`

4. **Create a folder structure**:
   - Create a new folder called `faculty-survey-dashboard`
   - Upload all files into this folder

5. **Commit changes**:
   - Scroll down and add commit message: "Add faculty survey dashboard"
   - Click "Commit changes"

6. **Access your dashboard**:
   - Visit: https://abijan96.github.io/faculty-survey-dashboard/

### Method 2: Using Git Command Line

```bash
# Navigate to your local repository
cd path/to/abijan96.github.io

# Create dashboard folder
mkdir faculty-survey-dashboard
cd faculty-survey-dashboard

# Copy all files from C:\Users\USER\Downloads\faculty-survey-dashboard\
# to this folder

# Stage all changes
git add .

# Commit changes
git commit -m "Add interactive faculty survey dashboard with visualizations"

# Push to GitHub
git push origin main
```

### Method 3: Using GitHub Desktop

1. Open GitHub Desktop
2. Select your `abijan96.github.io` repository
3. Create a new folder: `faculty-survey-dashboard`
4. Copy all files from `C:\Users\USER\Downloads\faculty-survey-dashboard\` into this folder
5. Review changes in GitHub Desktop
6. Add commit message: "Add faculty survey dashboard"
7. Click "Commit to main"
8. Click "Push origin"

## 📁 File Structure

```
faculty-survey-dashboard/
├── index.html              # Main dashboard HTML
├── dashboard.js            # JavaScript for charts and data processing
├── faculty_survey_data.csv # Survey response data (487 responses)
└── README.md              # This file
```

## 🎨 Dashboard Sections

### Key Performance Indicators
- Overall Satisfaction: 3.27/5.0
- Employee Net Promoter Score: +17
- Retention Risk: 25.7%
- Sense of Belonging: 3.53/5.0
- Psychological Safety: 2.76/5.0 ⚠️

### Visualizations

1. **Overall Satisfaction by College** - Bar chart showing satisfaction scores across colleges
2. **Employee Net Promoter Score (eNPS)** - Horizontal bar chart with college-level eNPS
3. **Faculty Experience Equity Analysis** - Grouped bar chart comparing metrics by gender
4. **Retention Risk Drivers** - Horizontal bar showing top reasons for considering leaving
5. **Weekly Work Hours by Discipline** - Dual-axis chart showing workload by discipline
6. **Tenure Process: Clarity vs. Fairness** - Scatter plot with quadrant analysis
7. **Belonging by Gender × Race** - Intersectional analysis of belonging scores
8. **Key Metrics Comparison** - Radar chart showing overall performance

## 📊 Data Details

- **Total Responses**: 487 faculty members
- **Response Rate**: 40.6% (487 of 1,200 faculty)
- **Survey Period**: October 15 - November 5, 2025
- **Question Types**: Demographics, Satisfaction, Workload, Support, Belonging, Open-ended

## 🎯 Key Findings

### Critical Issues (Immediate Attention Required)
- **Psychological Safety**: 2.76/5.0 - Lowest rated metric
- **Architecture College**: Negative eNPS (-1), low satisfaction (3.2)
- **Equity Gaps**: Women and faculty of color report significantly lower belonging
- **Intersectional Disadvantage**: Women of color and non-binary faculty experience compounded negative effects

### Areas of Concern
- **Retention Risk**: 25.7% of faculty seriously considered leaving
- **Workload**: STEM faculty average 62 hours/week, 28% work 70+ hours
- **Compensation**: Only 3.31/5.0 satisfaction with competitiveness
- **Science College**: Low tenure clarity (3.0) and fairness (3.1)

### Strengths to Maintain
- **Engineering College**: Highest satisfaction (4.1) and eNPS (+38)
- **Professional Development**: 3.69/5.0 - relatively strong
- **Collaboration**: 3.58/5.0 - good opportunities reported

## 🛠 Technologies Used

- **Chart.js 4.4.0** - Primary charting library
- **D3.js v7** - Data manipulation and advanced visualizations
- **PapaParse 5.4.1** - CSV parsing
- **Vanilla JavaScript** - No frameworks, fast loading
- **Responsive CSS Grid** - Mobile-friendly layout

## 📱 Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

## 📧 Contact

For questions about this dashboard or the survey data:
- **Institutional Research, Innovation & Strategy**
- University of Notre Dame
- Email: [your-email]@nd.edu

## 📄 License

Created for the Fall 2025 IR Specialist Assessment Exercise
Data generated for demonstration purposes

---

**Last Updated**: November 6, 2025
**Version**: 1.0.0
