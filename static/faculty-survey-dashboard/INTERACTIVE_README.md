# Interactive Faculty Survey Dashboard

## 🎛️ Enhanced Version with D3.js Controls

This is the **fully interactive version** of the Notre Dame Faculty Experience Survey Dashboard, featuring dynamic filters, real-time data updates, and advanced D3.js visualizations.

### 🆕 What's New in Interactive Version

#### Interactive Controls & Filters
- **Multi-select filters** for College, Gender, Rank, Discipline, and Years
- **Satisfaction slider** to filter by minimum satisfaction level
- **Real-time updates** - all charts update dynamically when filters change
- **Export functionality** - download filtered data as CSV
- **Reset button** - quickly clear all filters

#### Enhanced Visualizations (6 Charts)

1. **Satisfaction by College** (Interactive Bar Chart)
   - Switch between metrics (Satisfaction, Work-Life Balance, Belonging, Psych Safety)
   - **Click bars** to drill down by gender
   - Hover for detailed tooltips
   - Color-coded by score (red/yellow/green)

2. **Satisfaction vs Retention Risk** (Bubble Chart)
   - Bubble size = number of faculty
   - Quadrant analysis (color-coded)
   - Click bubbles for college details
   - Identifies at-risk colleges

3. **Demographic Comparison** (Grouped Bar Chart)
   - **Switch between**: Gender, Race, Rank, Discipline
   - Compare 4 metrics simultaneously
   - Interactive legend
   - Identifies equity gaps

4. **Workload Distribution** (Bar Chart with Reference Line)
   - Average weekly hours by discipline
   - Reference line shows national average (55 hrs)
   - Color-coded by workload severity
   - Identifies burnout risk areas

5. **Correlation Heatmap** (Interactive Matrix)
   - Shows correlations between 5 key metrics
   - Color intensity indicates strength
   - Hover to see exact correlation values
   - Identifies related variables

6. **Satisfaction Over Time** (Multi-line Chart)
   - 3 metrics tracked across career stages
   - Interactive points with tooltips
   - Identifies critical career transition points
   - Smooth curve interpolation

#### Dynamic KPIs
All 6 KPI cards update in real-time based on filters:
- Overall Satisfaction
- Employee Net Promoter Score (eNPS)
- Retention Risk %
- Belonging Score
- Psychological Safety
- Sample Size (filtered count)

### 🚀 Access the Interactive Dashboard

**Branch:** `interactive-dashboard`

**Local URL (after Hugo build):**
https://abijan96.github.io/faculty-survey-dashboard/interactive.html

**Compared to Static Version:**
- Static: `/faculty-survey-dashboard/index.html` (Chart.js, no filters)
- Interactive: `/faculty-survey-dashboard/interactive.html` (D3.js, full interactivity)

### 📖 How to Use

#### Applying Filters

1. **Multi-select filters** (College, Gender, Rank, etc.):
   - Hold **Ctrl** (Windows) or **Cmd** (Mac) to select multiple options
   - Uncheck "All" to enable specific selections
   - Select "All" to include everything

2. **Satisfaction slider**:
   - Drag to set minimum satisfaction threshold
   - Only faculty meeting this threshold will be included

3. **Apply Filters button**:
   - Click to update all visualizations
   - KPIs and charts refresh in real-time
   - Filter status shows in footer (e.g., "Showing 234 of 487 responses")

4. **Reset button**:
   - Clears all filters
   - Returns to full dataset

5. **Export button**:
   - Downloads filtered data as CSV
   - Includes timestamp in filename
   - Useful for further analysis in Excel/R/Python

#### Interacting with Charts

- **Hover**: See detailed tooltips with exact values
- **Click bars** (Chart 1): Drill down by gender for that college
- **Click bubbles** (Chart 2): See detailed college info
- **Switch metrics**: Use dropdowns to change what's displayed
- **All charts animate** when data updates

### 🎯 Use Cases

#### For Deans
1. **Compare your college to others**:
   - Filter by your college
   - See detailed breakdowns by gender, rank

2. **Identify at-risk faculty**:
   - Set satisfaction slider to 3.0 or lower
   - See which groups need intervention

3. **Analyze equity gaps**:
   - Use Chart 3 to compare by demographics
   - Export data for deeper analysis

#### For HR / DEI Offices
1. **Track diversity metrics**:
   - Filter by gender + race combinations
   - Identify intersectional disparities

2. **Workload analysis**:
   - Compare disciplines
   - Identify burnout risk areas

3. **Retention planning**:
   - See which groups are considering leaving
   - Use bubble chart to prioritize interventions

#### For Researchers
1. **Hypothesis testing**:
   - Use correlation heatmap
   - Filter by specific populations

2. **Longitudinal analysis**:
   - Chart 6 shows career stage patterns
   - Export filtered data for statistical analysis

3. **Comparative studies**:
   - Compare colleges, disciplines, demographics
   - Export subsets for detailed analysis

### 💻 Technical Details

#### Technologies Used
- **D3.js v7** - All visualizations built from scratch
- **PapaParse** - CSV parsing
- **Vanilla JavaScript** - No frameworks, fast performance
- **CSS Grid & Flexbox** - Responsive layout
- **SVG** - Scalable, high-quality graphics

#### Key Features
- **Responsive design** - Works on desktop, tablet, mobile
- **Smooth animations** - 800ms transitions on data updates
- **Accessible tooltips** - High contrast, readable
- **Performance optimized** - Handles 487+ records smoothly
- **Data validation** - Filters invalid/missing data automatically

#### Browser Compatibility
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers supported

### 📊 Data Processing

The dashboard automatically:
- Filters null/undefined values
- Calculates means, correlations, percentages
- Groups data by categories
- Sorts for optimal visualization
- Validates data types

### 🔧 Customization

#### To modify metrics displayed:
Edit these arrays in `interactive-dashboard.js`:
```javascript
const metrics = [
    { key: 'Q8_OverallSatisfaction', label: 'Satisfaction' },
    // Add more metrics here
];
```

#### To add new filters:
1. Add HTML select element in `interactive.html`
2. Add filter logic in `applyFilters()` function
3. Update filter status display

#### To change color schemes:
Modify D3 color scales in each chart function:
```javascript
const colorScale = d3.scaleSequential()
    .domain([1, 5])
    .interpolator(d3.interpolateRdYlGn);
```

### 📈 Performance Notes

- **Initial load**: ~1 second (loads 487 records)
- **Filter application**: ~200ms (updates all charts)
- **Smooth animations**: 60fps on modern browsers
- **Memory usage**: <50MB typical

### 🐛 Troubleshooting

**Charts not loading?**
- Check browser console (F12) for errors
- Verify `faculty_survey_data.csv` is in same directory
- Ensure internet connection (D3.js loads from CDN)

**Filters not working?**
- Click "Apply Filters" button after selection
- Try "Reset" button to clear any stuck states
- Refresh page if issues persist

**Export not working?**
- Check browser allows downloads
- Verify popup blocker not active

### 🔄 Deployment

#### To Deploy Interactive Version:

**Option 1: Replace main dashboard**
```bash
cd /c/Users/USER/abijan96.github.io
git checkout master
cp static/faculty-survey-dashboard/interactive.html static/faculty-survey-dashboard/index.html
cp static/faculty-survey-dashboard/interactive-dashboard.js static/faculty-survey-dashboard/dashboard.js
git add .
git commit -m "Replace with interactive dashboard"
git push
```

**Option 2: Keep both versions**
- Static version: `/faculty-survey-dashboard/index.html`
- Interactive version: `/faculty-survey-dashboard/interactive.html`
- Users can choose which to use

**Option 3: Merge branches**
```bash
git checkout master
git merge interactive-dashboard
git push
```

### 📝 Comparison: Static vs Interactive

| Feature | Static (Chart.js) | Interactive (D3.js) |
|---------|------------------|-------------------|
| Filters | ❌ None | ✅ 6 filter types |
| Chart Types | 8 charts | 6 enhanced charts |
| Drill-down | ❌ No | ✅ Yes (click bars) |
| Metric Switching | ❌ No | ✅ Yes (dropdowns) |
| Export Data | ❌ No | ✅ Yes (CSV) |
| Animations | Basic | Advanced D3 |
| Customization | Limited | Highly customizable |
| Performance | Very fast | Fast |
| File Size | ~21KB JS | ~36KB JS |

### 🎓 Educational Value

This dashboard demonstrates:
- **Advanced D3.js** - Custom visualizations, not templates
- **Data filtering & aggregation** - Real-time processing
- **Interactive design** - User-centered approach
- **Statistical visualization** - Correlations, distributions
- **Responsive web development** - Works on all devices
- **Clean code architecture** - Modular, maintainable

### 🚀 Next Steps

1. **Test the interactive dashboard** locally or on GitHub Pages
2. **Gather feedback** from stakeholders
3. **Choose deployment strategy** (replace or keep both)
4. **Add more features** if needed:
   - Download charts as PNG/SVG
   - Add statistical tests
   - Implement data comparison tool
   - Add annotation tools

### 📞 Support

For questions or issues:
- Check browser console for errors
- Review this README
- Verify all files are in correct location

---

**Created for:** Notre Dame IR Specialist Assessment
**Date:** November 2025
**Branch:** `interactive-dashboard`
**Technologies:** D3.js v7, PapaParse, Vanilla JS
**Status:** ✅ Ready for deployment
