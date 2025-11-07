// Global variables
let surveyData = [];
let filteredData = [];
let tooltip;

// Load data on page load
document.addEventListener('DOMContentLoaded', function() {
    tooltip = d3.select('#tooltip');
    loadData();
    setupEventListeners();
});

// Load CSV data
function loadData() {
    // Use absolute path from site root for GitHub Pages deployment
    const csvPath = '/faculty-survey-dashboard/faculty_survey_data.csv';

    Papa.parse(csvPath, {
        download: true,
        header: true,
        dynamicTyping: true,
        complete: function(results) {
            surveyData = results.data.filter(d => d.ResponseID); // Remove empty rows
            filteredData = [...surveyData];

            document.getElementById('loadingOverlay').classList.add('hidden');
            updateDashboard();
        },
        error: function(error) {
            console.error('Error loading data:', error);
            console.error('Attempted to load from:', csvPath);
            alert('Error loading survey data. Please check the browser console for details.');
        }
    });
}

// Setup event listeners
function setupEventListeners() {
    // Apply Filters button
    document.getElementById('applyFilters').addEventListener('click', applyFilters);

    // Reset Filters button
    document.getElementById('resetFilters').addEventListener('click', resetFilters);

    // Export Data button
    document.getElementById('exportData').addEventListener('click', exportFilteredData);

    // Satisfaction slider
    const slider = document.getElementById('satisfactionSlider');
    slider.addEventListener('input', function() {
        document.getElementById('satisfactionValue').textContent = this.value;
    });

    // Metric selectors
    document.getElementById('satisfactionMetric').addEventListener('change', () => updateChart1());
    document.getElementById('demoMetric').addEventListener('change', () => updateChart3());

    // Multi-select helpers
    const selects = document.querySelectorAll('select[multiple]');
    selects.forEach(select => {
        select.addEventListener('change', function() {
            const options = Array.from(this.options);
            const allOption = options.find(opt => opt.value === 'all');
            const otherOptions = options.filter(opt => opt.value !== 'all');

            if (allOption && allOption.selected && otherOptions.some(opt => opt.selected)) {
                allOption.selected = false;
            }
            if (!otherOptions.some(opt => opt.selected) && allOption) {
                allOption.selected = true;
            }
        });
    });
}

// Apply filters
function applyFilters() {
    filteredData = surveyData.filter(d => {
        // College filter
        const collegeSelected = getSelectedValues('collegeFilter');
        if (!collegeSelected.includes('all') && !collegeSelected.includes(d.College)) {
            return false;
        }

        // Gender filter
        const genderSelected = getSelectedValues('genderFilter');
        if (!genderSelected.includes('all') && !genderSelected.includes(d.Gender)) {
            return false;
        }

        // Rank filter
        const rankSelected = getSelectedValues('rankFilter');
        if (!rankSelected.includes('all') && !rankSelected.includes(d.Rank)) {
            return false;
        }

        // Discipline filter
        const disciplineSelected = getSelectedValues('disciplineFilter');
        if (!disciplineSelected.includes('all') && !disciplineSelected.includes(d.Discipline)) {
            return false;
        }

        // Years filter
        const yearsSelected = getSelectedValues('yearsFilter');
        if (!yearsSelected.includes('all') && !yearsSelected.includes(d.YearsAtInstitution)) {
            return false;
        }

        // Satisfaction threshold
        const minSatisfaction = parseFloat(document.getElementById('satisfactionSlider').value);
        if (d.Q8_OverallSatisfaction < minSatisfaction) {
            return false;
        }

        return true;
    });

    updateDashboard();
}

// Reset all filters
function resetFilters() {
    // Reset all selects to "all"
    const selects = document.querySelectorAll('select[multiple]');
    selects.forEach(select => {
        Array.from(select.options).forEach(opt => {
            opt.selected = opt.value === 'all';
        });
    });

    // Reset slider
    document.getElementById('satisfactionSlider').value = 1;
    document.getElementById('satisfactionValue').textContent = '1.0';

    filteredData = [...surveyData];
    updateDashboard();
}

// Get selected values from multi-select
function getSelectedValues(selectId) {
    const select = document.getElementById(selectId);
    return Array.from(select.selectedOptions).map(opt => opt.value);
}

// Export filtered data
function exportFilteredData() {
    const csv = Papa.unparse(filteredData);
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `faculty_survey_filtered_${new Date().toISOString().split('T')[0]}.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Update entire dashboard
function updateDashboard() {
    document.getElementById('filterStatus').textContent =
        `Showing ${filteredData.length} of ${surveyData.length} responses`;

    updateKPIs();
    updateChart1();
    updateChart2();
    updateChart3();
    updateChart4();
    updateChart5();
    updateChart6();
}

// Helper function to calculate mean
function mean(arr) {
    const filtered = arr.filter(x => x != null && !isNaN(x));
    return filtered.length > 0 ? filtered.reduce((a, b) => a + b, 0) / filtered.length : 0;
}

// Update KPIs
function updateKPIs() {
    const avgSatisfaction = mean(filteredData.map(d => d.Q8_OverallSatisfaction));
    const avgBelonging = mean(filteredData.map(d => d.Q27_Belonging));
    const avgPsychSafety = mean(filteredData.map(d => d.Q26_PsychologicalSafety));
    const retentionRisk = (filteredData.filter(d => d.Q10_ConsideredLeaving >= 4).length / filteredData.length * 100);

    // Calculate eNPS
    const scores = filteredData.map(d => d.Q9_LikelihoodToRecommend);
    const promoters = scores.filter(s => s >= 4).length;
    const detractors = scores.filter(s => s <= 2).length;
    const enps = Math.round((promoters / scores.length * 100) - (detractors / scores.length * 100));

    const html = `
        <div class="kpi-card">
            <div class="kpi-label">Overall Satisfaction</div>
            <div class="kpi-value ${avgSatisfaction >= 4 ? 'good' : avgSatisfaction >= 3.5 ? 'warning' : 'critical'}">
                ${avgSatisfaction.toFixed(2)}
            </div>
            <div class="kpi-subtitle">out of 5.0</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">eNPS Score</div>
            <div class="kpi-value ${enps >= 30 ? 'good' : enps >= 10 ? 'warning' : 'critical'}">
                ${enps > 0 ? '+' : ''}${enps}
            </div>
            <div class="kpi-subtitle">${enps >= 30 ? 'Excellent' : enps >= 10 ? 'Good' : 'Needs Work'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Retention Risk</div>
            <div class="kpi-value ${retentionRisk < 20 ? 'good' : retentionRisk < 30 ? 'warning' : 'critical'}">
                ${retentionRisk.toFixed(1)}%
            </div>
            <div class="kpi-subtitle">${filteredData.filter(d => d.Q10_ConsideredLeaving >= 4).length} faculty at risk</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Belonging Score</div>
            <div class="kpi-value ${avgBelonging >= 4 ? 'good' : avgBelonging >= 3.5 ? 'warning' : 'critical'}">
                ${avgBelonging.toFixed(2)}
            </div>
            <div class="kpi-subtitle">out of 5.0</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Psychological Safety</div>
            <div class="kpi-value ${avgPsychSafety >= 4 ? 'good' : avgPsychSafety >= 3.5 ? 'warning' : 'critical'}">
                ${avgPsychSafety.toFixed(2)}
            </div>
            <div class="kpi-subtitle">⚠️ ${avgPsychSafety < 3 ? 'Critical' : 'Monitor'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Sample Size</div>
            <div class="kpi-value good">${filteredData.length}</div>
            <div class="kpi-subtitle">${((filteredData.length / surveyData.length) * 100).toFixed(1)}% of total</div>
        </div>
    `;

    document.getElementById('kpiContainer').innerHTML = html;
}

// Chart 1: Satisfaction by College (Interactive Bar Chart)
function updateChart1() {
    const metric = document.getElementById('satisfactionMetric').value;
    const metricName = document.getElementById('satisfactionMetric').options[
        document.getElementById('satisfactionMetric').selectedIndex
    ].text;

    // Clear previous chart
    d3.select('#chart1').selectAll('*').remove();

    // Group by college
    const colleges = Array.from(new Set(filteredData.map(d => d.College))).filter(c => c);
    const data = colleges.map(college => {
        const collegeData = filteredData.filter(d => d.College === college);
        return {
            college: college,
            value: mean(collegeData.map(d => d[metric])),
            count: collegeData.length
        };
    }).sort((a, b) => b.value - a.value);

    // Set up dimensions
    const margin = {top: 20, right: 30, bottom: 80, left: 60};
    const width = document.getElementById('chart1').offsetWidth - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;

    // Create SVG
    const svg = d3.select('#chart1')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleBand()
        .domain(data.map(d => d.college))
        .range([0, width])
        .padding(0.2);

    const y = d3.scaleLinear()
        .domain([0, 5])
        .range([height, 0]);

    // Color scale
    const colorScale = d3.scaleSequential()
        .domain([1, 5])
        .interpolator(d3.interpolateRdYlGn);

    // Bars
    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.college))
        .attr('y', height)
        .attr('width', x.bandwidth())
        .attr('height', 0)
        .attr('fill', d => colorScale(d.value))
        .attr('stroke', '#333')
        .attr('stroke-width', 1)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.college}</strong><br/>
                ${metricName}: ${d.value.toFixed(2)}/5.0<br/>
                Faculty Count: ${d.count}
            `);
            d3.select(this).attr('opacity', 0.8);
        })
        .on('mouseout', function() {
            hideTooltip();
            d3.select(this).attr('opacity', 1);
        })
        .on('click', function(event, d) {
            drillDownByGender(d.college, metric);
        })
        .transition()
        .duration(800)
        .attr('y', d => y(d.value))
        .attr('height', d => height - y(d.value));

    // X axis
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end');

    // Y axis
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    // Y axis label
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .text(`${metricName} Score (1-5)`);

    // Update insight
    const topCollege = data[0];
    const bottomCollege = data[data.length - 1];
    document.getElementById('insight1').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p><strong>${topCollege.college}</strong> leads with ${metricName.toLowerCase()} of <strong>${topCollege.value.toFixed(2)}</strong>.
        <strong>${bottomCollege.college}</strong> needs attention at <strong>${bottomCollege.value.toFixed(2)}</strong>.
        Click any bar to see gender breakdown.</p>
    `;
}

// Drill down function
function drillDownByGender(college, metric) {
    const genderData = ['Man', 'Woman', 'Non-binary'].map(gender => {
        const subset = filteredData.filter(d => d.College === college && d.Gender === gender);
        return {
            gender: gender,
            value: mean(subset.map(d => d[metric])),
            count: subset.length
        };
    }).filter(d => d.count > 0);

    alert(`${college} - Gender Breakdown:\n\n${genderData.map(d =>
        `${d.gender}: ${d.value.toFixed(2)} (n=${d.count})`
    ).join('\n')}`);
}

// Chart 2: Satisfaction vs Retention Risk (Scatter Plot)
function updateChart2() {
    d3.select('#chart2').selectAll('*').remove();

    // Group by college
    const colleges = Array.from(new Set(filteredData.map(d => d.College))).filter(c => c);
    const data = colleges.map(college => {
        const collegeData = filteredData.filter(d => d.College === college);
        return {
            college: college,
            satisfaction: mean(collegeData.map(d => d.Q8_OverallSatisfaction)),
            retentionRisk: collegeData.filter(d => d.Q10_ConsideredLeaving >= 4).length / collegeData.length * 100,
            count: collegeData.length
        };
    });

    const margin = {top: 20, right: 30, bottom: 60, left: 60};
    const width = document.getElementById('chart2').offsetWidth - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;

    const svg = d3.select('#chart2')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleLinear()
        .domain([0, 5])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, Math.max(50, d3.max(data, d => d.retentionRisk))])
        .range([height, 0]);

    const size = d3.scaleSqrt()
        .domain([0, d3.max(data, d => d.count)])
        .range([5, 30]);

    // Add quadrant lines
    svg.append('line')
        .attr('x1', x(3.5))
        .attr('x2', x(3.5))
        .attr('y1', 0)
        .attr('y2', height)
        .attr('stroke', '#999')
        .attr('stroke-dasharray', '5,5')
        .attr('stroke-width', 1);

    svg.append('line')
        .attr('x1', 0)
        .attr('x2', width)
        .attr('y1', y(25))
        .attr('y2', y(25))
        .attr('stroke', '#999')
        .attr('stroke-dasharray', '5,5')
        .attr('stroke-width', 1);

    // Bubbles
    svg.selectAll('.bubble')
        .data(data)
        .enter()
        .append('circle')
        .attr('class', 'scatter-point')
        .attr('cx', width / 2)
        .attr('cy', height / 2)
        .attr('r', 0)
        .attr('fill', d => {
            if (d.satisfaction >= 3.5 && d.retentionRisk < 25) return '#10B981';
            if (d.satisfaction < 3.5 && d.retentionRisk >= 25) return '#EF4444';
            return '#F59E0B';
        })
        .attr('stroke', '#333')
        .attr('stroke-width', 2)
        .attr('opacity', 0.7)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.college}</strong><br/>
                Satisfaction: ${d.satisfaction.toFixed(2)}/5.0<br/>
                Retention Risk: ${d.retentionRisk.toFixed(1)}%<br/>
                Faculty Count: ${d.count}
            `);
        })
        .on('mouseout', hideTooltip)
        .transition()
        .duration(1000)
        .attr('cx', d => x(d.satisfaction))
        .attr('cy', d => y(d.retentionRisk))
        .attr('r', d => size(d.count));

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    // Labels
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + margin.bottom - 10)
        .style('text-anchor', 'middle')
        .text('Overall Satisfaction (1-5)');

    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .text('Retention Risk (%)');

    document.getElementById('insight2').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p>Top-right quadrant (high risk + low satisfaction) requires immediate attention.
        Bottom-right quadrant (low risk + high satisfaction) represents healthy colleges.</p>
    `;
}

// Chart 3: Demographic Comparison (Grouped Bar)
function updateChart3() {
    const demoType = document.getElementById('demoMetric').value;
    d3.select('#chart3').selectAll('*').remove();

    const metrics = [
        { key: 'Q8_OverallSatisfaction', label: 'Satisfaction' },
        { key: 'Q27_Belonging', label: 'Belonging' },
        { key: 'Q26_PsychologicalSafety', label: 'Psych Safety' },
        { key: 'Q13_WorkLifeBalance', label: 'Work-Life' }
    ];

    let groups, groupField;
    if (demoType === 'gender') {
        groups = ['Man', 'Woman', 'Non-binary'];
        groupField = 'Gender';
    } else if (demoType === 'race') {
        groups = ['White', 'Asian', 'Black or African American', 'Hispanic or Latino/a/x'];
        groupField = 'Race';
    } else if (demoType === 'rank') {
        groups = ['Professor', 'Associate Professor', 'Assistant Professor'];
        groupField = 'Rank';
    } else {
        groups = ['STEM', 'Social Sciences', 'Humanities', 'Business'];
        groupField = 'Discipline';
    }

    const data = groups.map(group => {
        const subset = filteredData.filter(d => d[groupField] === group);
        const result = { group: group };
        metrics.forEach(m => {
            result[m.label] = mean(subset.map(d => d[m.key]));
        });
        result.count = subset.length;
        return result;
    }).filter(d => d.count > 0);

    const margin = {top: 20, right: 120, bottom: 60, left: 60};
    const width = document.getElementById('chart3').offsetWidth - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select('#chart3')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x0 = d3.scaleBand()
        .domain(data.map(d => d.group))
        .range([0, width])
        .padding(0.2);

    const x1 = d3.scaleBand()
        .domain(metrics.map(m => m.label))
        .range([0, x0.bandwidth()])
        .padding(0.05);

    const y = d3.scaleLinear()
        .domain([0, 5])
        .range([height, 0]);

    const color = d3.scaleOrdinal()
        .domain(metrics.map(m => m.label))
        .range(['#3B82F6', '#10B981', '#F59E0B', '#EC4899']);

    const groupElements = svg.selectAll('.group')
        .data(data)
        .enter()
        .append('g')
        .attr('transform', d => `translate(${x0(d.group)},0)`);

    groupElements.selectAll('rect')
        .data(d => metrics.map(m => ({ metric: m.label, value: d[m.label], group: d.group })))
        .enter()
        .append('rect')
        .attr('x', d => x1(d.metric))
        .attr('y', height)
        .attr('width', x1.bandwidth())
        .attr('height', 0)
        .attr('fill', d => color(d.metric))
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.group}</strong><br/>
                ${d.metric}: ${d.value.toFixed(2)}/5.0
            `);
        })
        .on('mouseout', hideTooltip)
        .transition()
        .duration(800)
        .attr('y', d => y(d.value))
        .attr('height', d => height - y(d.value));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x0))
        .selectAll('text')
        .attr('transform', 'rotate(-20)')
        .style('text-anchor', 'end');

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    // Legend
    const legend = svg.selectAll('.legend')
        .data(metrics.map(m => m.label))
        .enter()
        .append('g')
        .attr('class', 'legend')
        .attr('transform', (d, i) => `translate(${width + 10},${i * 25})`);

    legend.append('rect')
        .attr('width', 18)
        .attr('height', 18)
        .attr('fill', color);

    legend.append('text')
        .attr('x', 24)
        .attr('y', 9)
        .attr('dy', '.35em')
        .text(d => d);

    document.getElementById('insight3').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p>Compare scores across different demographic groups. Lower scores may indicate equity gaps requiring DEI interventions.</p>
    `;
}

// Chart 4: Workload Distribution (Violin Plot simulation with bars)
function updateChart4() {
    d3.select('#chart4').selectAll('*').remove();

    const disciplines = ['STEM', 'Social Sciences', 'Humanities', 'Business'];
    const hoursMap = {
        '40-49 hours': 45,
        '50-59 hours': 55,
        '60-69 hours': 65,
        '70+ hours': 75
    };

    const data = disciplines.map(disc => {
        const subset = filteredData.filter(d => d.Discipline === disc && d.Q14_WeeklyHours);
        const avgHours = mean(subset.map(d => hoursMap[d.Q14_WeeklyHours] || 55));
        const over70 = subset.filter(d => d.Q14_WeeklyHours === '70+ hours').length / subset.length * 100;
        return {
            discipline: disc,
            avgHours: avgHours,
            over70: over70,
            count: subset.length
        };
    }).filter(d => d.count > 0);

    const margin = {top: 20, right: 80, bottom: 60, left: 60};
    const width = document.getElementById('chart4').offsetWidth - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;

    const svg = d3.select('#chart4')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(data.map(d => d.discipline))
        .range([0, width])
        .padding(0.3);

    const y = d3.scaleLinear()
        .domain([0, 80])
        .range([height, 0]);

    // Bars for average hours
    svg.selectAll('.bar')
        .data(data)
        .enter()
        .append('rect')
        .attr('x', d => x(d.discipline))
        .attr('y', height)
        .attr('width', x.bandwidth())
        .attr('height', 0)
        .attr('fill', d => d.avgHours > 60 ? '#EF4444' : d.avgHours > 55 ? '#F59E0B' : '#10B981')
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.discipline}</strong><br/>
                Avg Hours: ${d.avgHours.toFixed(1)}/week<br/>
                Working 70+: ${d.over70.toFixed(1)}%<br/>
                n = ${d.count}
            `);
        })
        .on('mouseout', hideTooltip)
        .transition()
        .duration(800)
        .attr('y', d => y(d.avgHours))
        .attr('height', d => height - y(d.avgHours));

    // Reference line at 55 hours (national avg)
    svg.append('line')
        .attr('x1', 0)
        .attr('x2', width)
        .attr('y1', y(55))
        .attr('y2', y(55))
        .attr('stroke', '#666')
        .attr('stroke-dasharray', '5,5')
        .attr('stroke-width', 2);

    svg.append('text')
        .attr('x', width - 5)
        .attr('y', y(55) - 5)
        .style('text-anchor', 'end')
        .style('font-size', '12px')
        .text('National Avg (55 hrs)');

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('text')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .attr('transform', 'rotate(-90)')
        .style('text-anchor', 'middle')
        .text('Average Hours/Week');

    document.getElementById('insight4').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p>Red bars indicate disciplines with unsustainable workload (>60 hrs/week). Consider workload reduction strategies.</p>
    `;
}

// Chart 5: Correlation Heatmap
function updateChart5() {
    d3.select('#chart5').selectAll('*').remove();

    const variables = [
        { key: 'Q8_OverallSatisfaction', label: 'Satisfaction' },
        { key: 'Q13_WorkLifeBalance', label: 'Work-Life' },
        { key: 'Q22_Compensation', label: 'Compensation' },
        { key: 'Q27_Belonging', label: 'Belonging' },
        { key: 'Q26_PsychologicalSafety', label: 'Psych Safety' }
    ];

    // Calculate correlations
    const correlations = [];
    variables.forEach(v1 => {
        variables.forEach(v2 => {
            const corr = calculateCorrelation(
                filteredData.map(d => d[v1.key]),
                filteredData.map(d => d[v2.key])
            );
            correlations.push({
                x: v1.label,
                y: v2.label,
                value: corr
            });
        });
    });

    const margin = {top: 20, right: 20, bottom: 80, left: 80};
    const width = document.getElementById('chart5').offsetWidth - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;
    const cellSize = Math.min(width, height) / variables.length;

    const svg = d3.select('#chart5')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand()
        .domain(variables.map(v => v.label))
        .range([0, cellSize * variables.length])
        .padding(0.05);

    const y = d3.scaleBand()
        .domain(variables.map(v => v.label))
        .range([0, cellSize * variables.length])
        .padding(0.05);

    const color = d3.scaleSequential()
        .domain([-1, 1])
        .interpolator(d3.interpolateRdBu);

    svg.selectAll('rect')
        .data(correlations)
        .enter()
        .append('rect')
        .attr('x', d => x(d.x))
        .attr('y', d => y(d.y))
        .attr('width', x.bandwidth())
        .attr('height', y.bandwidth())
        .attr('fill', d => color(-d.value))
        .attr('stroke', '#fff')
        .attr('stroke-width', 2)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.x} vs ${d.y}</strong><br/>
                Correlation: ${d.value.toFixed(3)}<br/>
                ${Math.abs(d.value) > 0.7 ? '(Strong)' : Math.abs(d.value) > 0.4 ? '(Moderate)' : '(Weak)'}
            `);
        })
        .on('mouseout', hideTooltip);

    // Add text labels
    svg.selectAll('text')
        .data(correlations)
        .enter()
        .append('text')
        .attr('x', d => x(d.x) + x.bandwidth() / 2)
        .attr('y', d => y(d.y) + y.bandwidth() / 2)
        .attr('dy', '.35em')
        .attr('text-anchor', 'middle')
        .attr('fill', d => Math.abs(d.value) > 0.5 ? 'white' : 'black')
        .style('font-size', '10px')
        .style('font-weight', 'bold')
        .text(d => d.value.toFixed(2));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${cellSize * variables.length})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .style('text-anchor', 'end');

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    document.getElementById('insight5').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p>Darker blue = stronger positive correlation. Strong correlations suggest variables that move together and may have common root causes.</p>
    `;
}

// Helper function to calculate correlation
function calculateCorrelation(x, y) {
    const validPairs = x.map((xi, i) => [xi, y[i]]).filter(([xi, yi]) =>
        xi != null && yi != null && !isNaN(xi) && !isNaN(yi)
    );

    if (validPairs.length < 2) return 0;

    const xVals = validPairs.map(p => p[0]);
    const yVals = validPairs.map(p => p[1]);

    const xMean = mean(xVals);
    const yMean = mean(yVals);

    const n = validPairs.length;
    let num = 0, denX = 0, denY = 0;

    for (let i = 0; i < n; i++) {
        const xDiff = xVals[i] - xMean;
        const yDiff = yVals[i] - yMean;
        num += xDiff * yDiff;
        denX += xDiff * xDiff;
        denY += yDiff * yDiff;
    }

    return denX === 0 || denY === 0 ? 0 : num / Math.sqrt(denX * denY);
}

// Chart 6: Satisfaction by Years at Institution (Line Chart)
function updateChart6() {
    d3.select('#chart6').selectAll('*').remove();

    const yearsOrder = ['0-2 years', '3-5 years', '6-10 years', '11-15 years', '16-20 years', 'More than 20 years'];
    const metrics = [
        { key: 'Q8_OverallSatisfaction', label: 'Overall Satisfaction', color: '#3B82F6' },
        { key: 'Q13_WorkLifeBalance', label: 'Work-Life Balance', color: '#10B981' },
        { key: 'Q27_Belonging', label: 'Belonging', color: '#F59E0B' }
    ];

    const data = yearsOrder.map((year, idx) => {
        const subset = filteredData.filter(d => d.YearsAtInstitution === year);
        const result = { years: year, yearIdx: idx };
        metrics.forEach(m => {
            result[m.label] = mean(subset.map(d => d[m.key]));
        });
        result.count = subset.length;
        return result;
    }).filter(d => d.count > 0);

    const margin = {top: 20, right: 150, bottom: 60, left: 60};
    const width = document.getElementById('chart6').offsetWidth - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;

    const svg = d3.select('#chart6')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear()
        .domain([0, data.length - 1])
        .range([0, width]);

    const y = d3.scaleLinear()
        .domain([0, 5])
        .range([height, 0]);

    // Draw lines for each metric
    metrics.forEach(metric => {
        const line = d3.line()
            .x((d, i) => x(i))
            .y(d => y(d[metric.label]))
            .curve(d3.curveMonotoneX);

        svg.append('path')
            .datum(data)
            .attr('class', 'line-chart-path')
            .attr('d', line)
            .attr('stroke', metric.color)
            .attr('stroke-width', 3)
            .attr('fill', 'none');

        // Add points
        svg.selectAll(`.point-${metric.label}`)
            .data(data)
            .enter()
            .append('circle')
            .attr('class', 'scatter-point')
            .attr('cx', (d, i) => x(i))
            .attr('cy', d => y(d[metric.label]))
            .attr('r', 5)
            .attr('fill', metric.color)
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .on('mouseover', function(event, d) {
                showTooltip(event, `
                    <strong>${d.years}</strong><br/>
                    ${metric.label}: ${d[metric.label].toFixed(2)}<br/>
                    n = ${d.count}
                `);
            })
            .on('mouseout', hideTooltip);
    });

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x)
            .tickValues(d3.range(data.length))
            .tickFormat(i => data[i].years.replace(' years', '')))
        .selectAll('text')
        .attr('transform', 'rotate(-20)')
        .style('text-anchor', 'end');

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('text')
        .attr('y', 0 - margin.left + 10)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .attr('transform', 'rotate(-90)')
        .style('text-anchor', 'middle')
        .text('Score (1-5)');

    // Legend
    const legend = svg.selectAll('.legend')
        .data(metrics)
        .enter()
        .append('g')
        .attr('transform', (d, i) => `translate(${width + 10},${i * 25})`);

    legend.append('line')
        .attr('x1', 0)
        .attr('x2', 20)
        .attr('y1', 10)
        .attr('y2', 10)
        .attr('stroke', d => d.color)
        .attr('stroke-width', 3);

    legend.append('text')
        .attr('x', 25)
        .attr('y', 10)
        .attr('dy', '.35em')
        .text(d => d.label);

    document.getElementById('insight6').innerHTML = `
        <h4>💡 Key Insight</h4>
        <p>Track how faculty experience changes over time. Drops at certain career stages may indicate need for targeted support.</p>
    `;
}

// Tooltip functions
function showTooltip(event, html) {
    tooltip.html(html)
        .classed('show', true)
        .style('left', (event.pageX + 15) + 'px')
        .style('top', (event.pageY - 28) + 'px');
}

function hideTooltip() {
    tooltip.classed('show', false);
}
