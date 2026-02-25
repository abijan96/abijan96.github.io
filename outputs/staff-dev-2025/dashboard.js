// Staff Development Day 2025 Dashboard - D3.js Visualizations

let dashboardData = null;
let currentDepartment = 'all';

// Color palette - Notre Dame colors
const colors = {
    primary: '#0C2340',
    gold: '#C99700',
    green: '#27ae60',
    orange: '#f39c12',
    red: '#e74c3c',
    blue: '#3498db',
    lightGray: '#ecf0f1',
    darkGray: '#95a5a6'
};

// Load data and initialize dashboard
d3.json('dashboard_data.json').then(data => {
    dashboardData = data;
    initializeDashboard();
}).catch(error => {
    console.error('Error loading data:', error);
    document.querySelector('.container').innerHTML = '<div style="padding: 50px; text-align: center;"><h2>Error loading dashboard data</h2><p>Please ensure dashboard_data.json is in the same directory.</p></div>';
});

function initializeDashboard() {
    renderStatsOverview();
    renderNPSOverview();
    renderSessionPerformance();
    renderDepartmentComparison();
    renderSentimentChart();
    renderThemesChart();
    renderSessionDetails();
    renderInsights();
    setupFilters();
}

function renderStatsOverview() {
    const stats = [
        {
            label: 'Overall Satisfaction',
            value: dashboardData.overall_metrics.nps.overall_score.toFixed(1),
            sublabel: 'out of 10',
            class: 'positive'
        },
        {
            label: 'Net Promoter Score',
            value: dashboardData.overall_metrics.nps.nps_value.toFixed(0),
            sublabel: `${dashboardData.overall_metrics.nps.promoters.toFixed(0)}% promoters`,
            class: 'positive'
        },
        {
            label: 'Venue Rating',
            value: dashboardData.overall_metrics.venue_score.toFixed(1),
            sublabel: 'out of 10',
            class: 'excellent'
        },
        {
            label: 'Total Responses',
            value: dashboardData.metadata.total_responses,
            sublabel: `${Object.keys(dashboardData.metadata.departments).length} departments`,
            class: ''
        }
    ];

    const container = d3.select('#stats-overview');

    const cards = container.selectAll('.stat-card')
        .data(stats)
        .join('div')
        .attr('class', d => `stat-card ${d.class}`);

    cards.append('h3').text(d => d.label);
    cards.append('div').attr('class', 'value').text(d => d.value);
    cards.append('div').attr('class', 'label').text(d => d.sublabel);
}

function renderNPSOverview() {
    const nps = dashboardData.overall_metrics.nps;
    const container = d3.select('#nps-overview');

    // NPS Score display
    container.append('div')
        .attr('class', 'nps-gauge')
        .html(`
            <div style="font-size: 4em; font-weight: 700; color: ${colors.primary}; margin: 20px 0;">
                ${nps.nps_value.toFixed(0)}
            </div>
            <div style="font-size: 1.2em; color: ${colors.darkGray}; margin-bottom: 30px;">
                Net Promoter Score
            </div>
        `);

    // NPS Segments
    const segments = container.append('div')
        .attr('class', 'nps-segments');

    [
        { type: 'detractor', label: 'Detractors', value: nps.detractors, range: '0-6' },
        { type: 'passive', label: 'Passives', value: nps.passives, range: '7-8' },
        { type: 'promoter', label: 'Promoters', value: nps.promoters, range: '9-10' }
    ].forEach(seg => {
        segments.append('div')
            .attr('class', `nps-segment ${seg.type}`)
            .html(`
                <div class="percentage">${seg.value.toFixed(0)}%</div>
                <div class="label">${seg.label}</div>
                <div style="font-size: 0.8em; opacity: 0.8;">(${seg.range})</div>
            `);
    });
}

function renderSessionPerformance() {
    const sessions = dashboardData.session_performance;
    const margin = { top: 20, right: 30, bottom: 60, left: 200 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select('#session-performance')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const y = d3.scaleBand()
        .domain(sessions.map(d => d.name))
        .range([0, height])
        .padding(0.3);

    const x = d3.scaleLinear()
        .domain([0, 10])
        .range([0, width]);

    // Color scale based on score
    const colorScale = d3.scaleLinear()
        .domain([6, 7.5, 9])
        .range([colors.orange, colors.gold, colors.green]);

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(x.ticks(10))
        .join('line')
        .attr('x1', d => x(d))
        .attr('x2', d => x(d))
        .attr('y1', 0)
        .attr('y2', height)
        .attr('stroke', colors.lightGray)
        .attr('stroke-width', 1);

    // Bars
    svg.selectAll('.bar')
        .data(sessions)
        .join('rect')
        .attr('class', 'bar')
        .attr('y', d => y(d.name))
        .attr('x', 0)
        .attr('height', y.bandwidth())
        .attr('width', d => x(d.score))
        .attr('fill', d => colorScale(d.score))
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.name}</strong>
                Score: ${d.score.toFixed(2)}/10<br>
                NPS: ${d.nps.toFixed(0)}<br>
                Promoters: ${d.promoters.toFixed(0)}%<br>
                Top-2 Box: ${d.top2_box.toFixed(0)}%
            `);
        })
        .on('mouseout', hideTooltip);

    // Score labels
    svg.selectAll('.score-label')
        .data(sessions)
        .join('text')
        .attr('class', 'score-label')
        .attr('y', d => y(d.name) + y.bandwidth() / 2)
        .attr('x', d => x(d.score) + 5)
        .attr('dy', '0.35em')
        .attr('font-size', '13px')
        .attr('font-weight', '600')
        .attr('fill', colors.primary)
        .text(d => d.score.toFixed(2));

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x).ticks(10));

    // X-axis label
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Recommendation Score (0-10)');
}

function renderDepartmentComparison() {
    const departments = dashboardData.department_comparison;
    const margin = { top: 20, right: 30, bottom: 60, left: 50 };
    const width = 600 - margin.left - margin.right;
    const height = 350 - margin.top - margin.bottom;

    const svg = d3.select('#department-comparison')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Scales
    const x = d3.scaleBand()
        .domain(departments.map(d => d.department.substring(0, 20)))
        .range([0, width])
        .padding(0.3);

    const y = d3.scaleLinear()
        .domain([0, 10])
        .range([height, 0]);

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(y.ticks(10))
        .join('line')
        .attr('y1', d => y(d))
        .attr('y2', d => y(d))
        .attr('x1', 0)
        .attr('x2', width)
        .attr('stroke', colors.lightGray);

    // Bars
    svg.selectAll('.bar')
        .data(departments)
        .join('rect')
        .attr('class', 'bar')
        .attr('x', d => x(d.department.substring(0, 20)))
        .attr('y', d => y(d.score))
        .attr('width', x.bandwidth())
        .attr('height', d => height - y(d.score))
        .attr('fill', colors.primary)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.department}</strong>
                Score: ${d.score.toFixed(2)}/10<br>
                NPS: ${d.nps.toFixed(0)}<br>
                Respondents: ${d.respondents}
            `);
        })
        .on('mouseout', hideTooltip);

    // Score labels
    svg.selectAll('.score-label')
        .data(departments)
        .join('text')
        .attr('class', 'score-label')
        .attr('x', d => x(d.department.substring(0, 20)) + x.bandwidth() / 2)
        .attr('y', d => y(d.score) - 5)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .attr('fill', colors.primary)
        .text(d => d.score.toFixed(1));

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .attr('text-anchor', 'end')
        .attr('dx', '-0.5em')
        .attr('dy', '0.5em');

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y).ticks(10));

    // Y-axis label
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -35)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Score (0-10)');
}

function renderSentimentChart() {
    const sentiment = dashboardData.sentiment_distribution;
    const data = [
        { label: 'Positive', value: sentiment.positive, color: colors.green },
        { label: 'Neutral', value: sentiment.neutral, color: colors.darkGray },
        { label: 'Negative', value: sentiment.negative, color: colors.red }
    ];

    const width = 300;
    const height = 300;
    const radius = Math.min(width, height) / 2;

    const svg = d3.select('#sentiment-chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height)
        .append('g')
        .attr('transform', `translate(${width / 2},${height / 2})`);

    const pie = d3.pie()
        .value(d => d.value)
        .sort(null);

    const arc = d3.arc()
        .innerRadius(radius * 0.5)
        .outerRadius(radius);

    const arcs = svg.selectAll('.arc')
        .data(pie(data))
        .join('g')
        .attr('class', 'arc');

    arcs.append('path')
        .attr('d', arc)
        .attr('fill', d => d.data.color)
        .attr('stroke', 'white')
        .attr('stroke-width', 2)
        .on('mouseover', function(event, d) {
            const total = sentiment.positive + sentiment.neutral + sentiment.negative;
            const pct = (d.data.value / total * 100).toFixed(1);
            showTooltip(event, `
                <strong>${d.data.label}</strong>
                Count: ${d.data.value}<br>
                Percentage: ${pct}%
            `);
        })
        .on('mouseout', hideTooltip);

    arcs.append('text')
        .attr('transform', d => `translate(${arc.centroid(d)})`)
        .attr('text-anchor', 'middle')
        .attr('fill', 'white')
        .attr('font-weight', '600')
        .attr('font-size', '14px')
        .text(d => d.data.value);

    // Legend
    const legend = d3.select('#sentiment-chart')
        .append('div')
        .attr('class', 'legend')
        .style('margin-top', '20px');

    data.forEach(d => {
        const item = legend.append('div')
            .attr('class', 'legend-item');

        item.append('div')
            .attr('class', 'legend-color')
            .style('background', d.color);

        item.append('span')
            .text(`${d.label} (${d.value})`);
    });
}

function renderThemesChart() {
    const themes = dashboardData.themes.overall
        .sort((a, b) => b.prevalence_pct - a.prevalence_pct)
        .slice(0, 8);

    const margin = { top: 20, right: 30, bottom: 40, left: 250 };
    const width = 900 - margin.left - margin.right;
    const height = 450 - margin.top - margin.bottom;

    const svg = d3.select('#themes-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    const y = d3.scaleBand()
        .domain(themes.map(d => d.theme))
        .range([0, height])
        .padding(0.2);

    const x = d3.scaleLinear()
        .domain([0, d3.max(themes, d => d.prevalence_pct)])
        .range([0, width]);

    // Stacked bars for sentiment
    const stack = d3.stack()
        .keys(['pos_pct', 'neu_pct', 'neg_pct']);

    const stackedData = themes.map(d => ({
        theme: d.theme,
        pos_pct: d.pos_pct,
        neu_pct: d.neu_pct,
        neg_pct: d.neg_pct,
        prevalence_pct: d.prevalence_pct,
        mentions: d.mentions
    }));

    const sentimentColors = {
        pos_pct: colors.green,
        neu_pct: colors.darkGray,
        neg_pct: colors.red
    };

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(x.ticks(10))
        .join('line')
        .attr('x1', d => x(d))
        .attr('x2', d => x(d))
        .attr('y1', 0)
        .attr('y2', height)
        .attr('stroke', colors.lightGray);

    // Main bars (prevalence)
    svg.selectAll('.theme-bar')
        .data(themes)
        .join('rect')
        .attr('class', 'theme-bar')
        .attr('y', d => y(d.theme))
        .attr('x', 0)
        .attr('height', y.bandwidth())
        .attr('width', d => x(d.prevalence_pct))
        .attr('fill', colors.primary)
        .attr('opacity', 0.7)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.theme}</strong>
                Prevalence: ${d.prevalence_pct.toFixed(1)}%<br>
                Mentions: ${d.mentions}<br>
                Positive: ${d.pos_pct.toFixed(0)}%<br>
                Neutral: ${d.neu_pct.toFixed(0)}%<br>
                Negative: ${d.neg_pct.toFixed(0)}%
            `);
        })
        .on('mouseout', hideTooltip);

    // Prevalence labels
    svg.selectAll('.prevalence-label')
        .data(themes)
        .join('text')
        .attr('class', 'prevalence-label')
        .attr('y', d => y(d.theme) + y.bandwidth() / 2)
        .attr('x', d => x(d.prevalence_pct) + 5)
        .attr('dy', '0.35em')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .attr('fill', colors.primary)
        .text(d => `${d.prevalence_pct.toFixed(0)}%`);

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 35)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Percentage of Respondents Mentioning (%)');
}

function renderSessionDetails() {
    const sessions = dashboardData.session_performance.filter(s => s.details.engaging !== null);

    const margin = { top: 20, right: 30, bottom: 80, left: 50 };
    const width = 1100 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select('#session-details')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Prepare data for grouped bars
    const metrics = ['engaging', 'time', 'relevant'];
    const metricLabels = {
        engaging: 'Engaging',
        time: 'Time Allotted',
        relevant: 'Relevance'
    };

    const data = [];
    sessions.forEach(session => {
        metrics.forEach(metric => {
            if (session.details[metric] !== null) {
                data.push({
                    session: session.name,
                    metric: metricLabels[metric],
                    value: session.details[metric]
                });
            }
        });
    });

    // Scales
    const x0 = d3.scaleBand()
        .domain(sessions.map(d => d.name))
        .range([0, width])
        .padding(0.2);

    const x1 = d3.scaleBand()
        .domain(Object.values(metricLabels))
        .range([0, x0.bandwidth()])
        .padding(0.05);

    const y = d3.scaleLinear()
        .domain([0, 10])
        .range([height, 0]);

    const color = d3.scaleOrdinal()
        .domain(Object.values(metricLabels))
        .range([colors.primary, colors.gold, colors.blue]);

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(y.ticks(10))
        .join('line')
        .attr('y1', d => y(d))
        .attr('y2', d => y(d))
        .attr('x1', 0)
        .attr('x2', width)
        .attr('stroke', colors.lightGray);

    // Grouped bars
    const sessionGroups = svg.selectAll('.session-group')
        .data(sessions)
        .join('g')
        .attr('class', 'session-group')
        .attr('transform', d => `translate(${x0(d.name)},0)`);

    sessionGroups.selectAll('.bar')
        .data(d => {
            return Object.values(metricLabels).map(metric => ({
                metric: metric,
                value: d.details[Object.keys(metricLabels).find(k => metricLabels[k] === metric)],
                session: d.name
            }));
        })
        .join('rect')
        .attr('class', 'bar')
        .attr('x', d => x1(d.metric))
        .attr('y', d => y(d.value))
        .attr('width', x1.bandwidth())
        .attr('height', d => height - y(d.value))
        .attr('fill', d => color(d.metric))
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.session}</strong>
                ${d.metric}: ${d.value.toFixed(2)}/10
            `);
        })
        .on('mouseout', hideTooltip);

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x0))
        .selectAll('text')
        .attr('transform', 'rotate(-45)')
        .attr('text-anchor', 'end')
        .attr('dx', '-0.5em')
        .attr('dy', '0.5em');

    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y).ticks(10));

    // Y-axis label
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('x', -height / 2)
        .attr('y', -35)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Score (0-10)');

    // Legend
    const legend = svg.append('g')
        .attr('class', 'legend')
        .attr('transform', `translate(${width - 200}, 0)`);

    Object.values(metricLabels).forEach((metric, i) => {
        const legendRow = legend.append('g')
            .attr('transform', `translate(0, ${i * 20})`);

        legendRow.append('rect')
            .attr('width', 15)
            .attr('height', 15)
            .attr('fill', color(metric));

        legendRow.append('text')
            .attr('x', 20)
            .attr('y', 12)
            .attr('font-size', '12px')
            .text(metric);
    });
}

function renderInsights() {
    const insights = [
        {
            title: 'Top Strength',
            text: `Venue received the highest rating at ${dashboardData.overall_metrics.venue_score.toFixed(1)}/10. Morning and Afternoon Breakout sessions were highly rated with strong NPS scores.`
        },
        {
            title: 'Critical Improvement Area',
            text: 'Session Timing & Duration mentioned by 52.7% of respondents. Time allotted for sessions consistently scored lowest (6.27-6.50/10). Reduce downtime between sessions and extend breakout session duration.'
        },
        {
            title: 'Morning Keynote Needs Attention',
            text: `Katie DeWulf's morning keynote scored lowest in NPS (7.44/10) with only 42% promoters. Feedback indicates the content was "hard to follow" and "too corporate-focused."`
        },
        {
            title: 'Department Variance',
            text: `${dashboardData.department_comparison[0].department} showed highest satisfaction (${dashboardData.department_comparison[0].score.toFixed(1)}/10) while ${dashboardData.department_comparison[dashboardData.department_comparison.length - 1].department} scored lowest (${dashboardData.department_comparison[dashboardData.department_comparison.length - 1].score.toFixed(1)}/10). Consider department-specific follow-up.`
        },
        {
            title: 'Future Content Requests',
            text: '38.4% of respondents requested advanced/deeper content tracks (201, 301 level sessions), leadership development, and more practical skill-building opportunities.'
        }
    ];

    const container = d3.select('#insights');

    insights.forEach(insight => {
        container.append('div')
            .attr('class', 'insight-box')
            .html(`
                <strong>${insight.title}</strong>
                ${insight.text}
            `);
    });
}

function setupFilters() {
    const select = d3.select('#dept-filter');

    // Add department options
    Object.keys(dashboardData.metadata.departments).forEach(dept => {
        select.append('option')
            .attr('value', dept)
            .text(dept);
    });

    // Filter change handler
    select.on('change', function() {
        currentDepartment = this.value;
        console.log('Filter changed to:', currentDepartment);
        console.log('Dashboard data available:', !!dashboardData);
        console.log('kpi_by_department available:', !!dashboardData.kpi_by_department);
        console.log('kpi_by_department count:', dashboardData.kpi_by_department ? dashboardData.kpi_by_department.length : 0);

        // Clear existing charts
        d3.select('#session-performance').html('');
        d3.select('#department-comparison').html('');
        d3.select('#themes-chart').html('');

        // Re-render charts with filtered data
        if (currentDepartment === 'all') {
            renderSessionPerformance();
            renderDepartmentComparison();
            renderThemesChart();
        } else {
            console.log('Rendering filtered view for:', currentDepartment);
            renderSessionPerformanceByDept(currentDepartment);
            renderDepartmentComparison(); // Keep this to show context
            renderThemesChartByDept(currentDepartment);
        }
    });
}

function renderSessionPerformanceByDept(dept) {
    console.log('renderSessionPerformanceByDept called with:', dept);
    console.log('kpi_by_department:', dashboardData.kpi_by_department ? dashboardData.kpi_by_department.length + ' records' : 'undefined');

    // Get department-specific data
    const sessions = [
        {name: 'Morning Keynote', metric: 'Morning_Keynote_NPS'},
        {name: 'Fireside Chat (AI)', metric: 'Fireside_NPS'},
        {name: 'Afternoon Keynote', metric: 'Afternoon_Keynote_NPS'},
        {name: 'Morning Breakout', metric: 'Morning_Breakout_NPS'},
        {name: 'Afternoon Breakout', metric: 'Afternoon_Breakout_NPS'}
    ].map(s => {
        const deptData = dashboardData.kpi_by_department.find(d =>
            d.department === dept && d.metric === s.metric
        );
        console.log(`Looking for ${s.metric} for ${dept}:`, deptData ? 'found' : 'not found');
        return {
            name: s.name,
            score: deptData ? deptData.mean_0_10 : 0,
            nps: deptData ? deptData.nps_score : 0,
            promoters: deptData ? deptData.promoter_pct : 0,
            passives: deptData ? deptData.passive_pct : 0,
            detractors: deptData ? deptData.detractor_pct : 0,
            top2_box: deptData ? deptData.top2_box_pct : 0
        };
    }).filter(s => s.score > 0);

    console.log('Filtered sessions:', sessions.length, sessions);

    const margin = { top: 20, right: 30, bottom: 60, left: 200 };
    const width = 800 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    const svg = d3.select('#session-performance')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add title showing filtered department
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', -5)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .attr('fill', colors.gold)
        .text(`Filtered by: ${dept}`);

    // Scales
    const y = d3.scaleBand()
        .domain(sessions.map(d => d.name))
        .range([0, height])
        .padding(0.3);

    const x = d3.scaleLinear()
        .domain([0, 10])
        .range([0, width]);

    const colorScale = d3.scaleLinear()
        .domain([6, 7.5, 9])
        .range([colors.orange, colors.gold, colors.green]);

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(x.ticks(10))
        .join('line')
        .attr('x1', d => x(d))
        .attr('x2', d => x(d))
        .attr('y1', 0)
        .attr('y2', height)
        .attr('stroke', colors.lightGray);

    // Bars
    svg.selectAll('.bar')
        .data(sessions)
        .join('rect')
        .attr('class', 'bar')
        .attr('y', d => y(d.name))
        .attr('x', 0)
        .attr('height', y.bandwidth())
        .attr('width', d => x(d.score))
        .attr('fill', d => colorScale(d.score))
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.name}</strong>
                Score: ${d.score.toFixed(2)}/10<br>
                NPS: ${d.nps.toFixed(0)}<br>
                Promoters: ${d.promoters.toFixed(0)}%<br>
                Top-2 Box: ${d.top2_box.toFixed(0)}%
            `);
        })
        .on('mouseout', hideTooltip);

    // Score labels
    svg.selectAll('.score-label')
        .data(sessions)
        .join('text')
        .attr('y', d => y(d.name) + y.bandwidth() / 2)
        .attr('x', d => x(d.score) + 5)
        .attr('dy', '0.35em')
        .attr('font-size', '13px')
        .attr('font-weight', '600')
        .attr('fill', colors.primary)
        .text(d => d.score.toFixed(2));

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x).ticks(10));

    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 40)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Recommendation Score (0-10)');
}

function renderThemesChartByDept(dept) {
    const deptThemes = dashboardData.themes.by_department
        .filter(t => t.department === dept)
        .sort((a, b) => b.prevalence_pct - a.prevalence_pct)
        .slice(0, 8);

    if (deptThemes.length === 0) {
        d3.select('#themes-chart').append('p')
            .style('text-align', 'center')
            .style('padding', '50px')
            .style('color', colors.darkGray)
            .text('No theme data available for this department');
        return;
    }

    const margin = { top: 20, right: 30, bottom: 40, left: 250 };
    const width = 900 - margin.left - margin.right;
    const height = 450 - margin.top - margin.bottom;

    const svg = d3.select('#themes-chart')
        .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
        .append('g')
        .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add title
    svg.append('text')
        .attr('x', width / 2)
        .attr('y', -5)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .attr('fill', colors.gold)
        .text(`Filtered by: ${dept}`);

    const y = d3.scaleBand()
        .domain(deptThemes.map(d => d.theme))
        .range([0, height])
        .padding(0.2);

    const x = d3.scaleLinear()
        .domain([0, d3.max(deptThemes, d => d.prevalence_pct)])
        .range([0, width]);

    // Grid lines
    svg.append('g')
        .attr('class', 'grid')
        .selectAll('line')
        .data(x.ticks(10))
        .join('line')
        .attr('x1', d => x(d))
        .attr('x2', d => x(d))
        .attr('y1', 0)
        .attr('y2', height)
        .attr('stroke', colors.lightGray);

    // Bars
    svg.selectAll('.theme-bar')
        .data(deptThemes)
        .join('rect')
        .attr('class', 'theme-bar')
        .attr('y', d => y(d.theme))
        .attr('x', 0)
        .attr('height', y.bandwidth())
        .attr('width', d => x(d.prevalence_pct))
        .attr('fill', colors.primary)
        .attr('opacity', 0.7)
        .on('mouseover', function(event, d) {
            showTooltip(event, `
                <strong>${d.theme}</strong>
                Prevalence: ${d.prevalence_pct.toFixed(1)}%<br>
                Mentions: ${d.mentions}<br>
                Positive: ${d.pos_pct.toFixed(0)}%<br>
                Neutral: ${d.neu_pct.toFixed(0)}%<br>
                Negative: ${d.neg_pct.toFixed(0)}%
            `);
        })
        .on('mouseout', hideTooltip);

    // Labels
    svg.selectAll('.prevalence-label')
        .data(deptThemes)
        .join('text')
        .attr('y', d => y(d.theme) + y.bandwidth() / 2)
        .attr('x', d => x(d.prevalence_pct) + 5)
        .attr('dy', '0.35em')
        .attr('font-size', '12px')
        .attr('font-weight', '600')
        .attr('fill', colors.primary)
        .text(d => `${d.prevalence_pct.toFixed(0)}%`);

    // Axes
    svg.append('g')
        .attr('class', 'axis')
        .call(d3.axisLeft(y));

    svg.append('g')
        .attr('class', 'axis')
        .attr('transform', `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 35)
        .attr('text-anchor', 'middle')
        .attr('font-size', '12px')
        .attr('fill', colors.darkGray)
        .text('Percentage of Respondents Mentioning (%)');
}

function showTooltip(event, html) {
    const tooltip = d3.select('#tooltip');
    tooltip.html(html)
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 10) + 'px')
        .classed('visible', true);
}

function hideTooltip() {
    d3.select('#tooltip').classed('visible', false);
}
