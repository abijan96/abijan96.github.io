// Load and process CSV data
let surveyData = [];

// Fetch CSV data
fetch('faculty_survey_data.csv')
    .then(response => response.text())
    .then(csvText => {
        Papa.parse(csvText, {
            header: true,
            dynamicTyping: true,
            complete: function(results) {
                surveyData = results.data;
                initializeDashboard();
            }
        });
    })
    .catch(error => {
        console.error('Error loading data:', error);
        document.getElementById('kpiContainer').innerHTML = '<p style="color: white;">Error loading data. Please ensure faculty_survey_data.csv is in the same directory.</p>';
    });

function initializeDashboard() {
    createKPIs();
    createSatisfactionByCollege();
    createENPSChart();
    createEquityChart();
    createRetentionDrivers();
    createWorkloadChart();
    createTenureScatter();
    createBelongingHeatmap();
    createRadarChart();
}

// Calculate KPIs
function createKPIs() {
    const avgSatisfaction = mean(surveyData.map(d => d.Q8_OverallSatisfaction));
    const avgBelonging = mean(surveyData.map(d => d.Q27_Belonging));
    const avgPsychSafety = mean(surveyData.map(d => d.Q26_PsychologicalSafety));

    // Calculate retention risk (% who agree/strongly agree they considered leaving)
    const retentionRisk = (surveyData.filter(d => d.Q10_ConsideredLeaving >= 4).length / surveyData.length * 100).toFixed(1);

    // Calculate eNPS
    const enps = calculateENPS();

    const kpiHTML = `
        <div class="kpi-card">
            <div class="kpi-label">Overall Satisfaction</div>
            <div class="kpi-value ${avgSatisfaction >= 4 ? 'good' : avgSatisfaction >= 3.5 ? 'warning' : 'critical'}">${avgSatisfaction.toFixed(2)}</div>
            <div class="kpi-change ${avgSatisfaction >= 3.5 ? 'positive' : 'negative'}">Out of 5.0 scale</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Employee Net Promoter Score</div>
            <div class="kpi-value ${enps >= 30 ? 'good' : enps >= 10 ? 'warning' : 'critical'}">+${enps}</div>
            <div class="kpi-change ${enps >= 10 ? 'positive' : 'negative'}">${enps >= 30 ? 'Excellent' : enps >= 10 ? 'Good' : 'Needs Improvement'}</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Retention Risk</div>
            <div class="kpi-value ${retentionRisk < 20 ? 'good' : retentionRisk < 30 ? 'warning' : 'critical'}">${retentionRisk}%</div>
            <div class="kpi-change negative">Considered leaving past year</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Sense of Belonging</div>
            <div class="kpi-value ${avgBelonging >= 4 ? 'good' : avgBelonging >= 3.5 ? 'warning' : 'critical'}">${avgBelonging.toFixed(2)}</div>
            <div class="kpi-change ${avgBelonging >= 3.5 ? 'positive' : 'negative'}">Out of 5.0 scale</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Psychological Safety</div>
            <div class="kpi-value critical">${avgPsychSafety.toFixed(2)}</div>
            <div class="kpi-change negative">⚠️ Requires attention</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Response Rate</div>
            <div class="kpi-value good">40.6%</div>
            <div class="kpi-change positive">487 of 1,200 faculty</div>
        </div>
    `;

    document.getElementById('kpiContainer').innerHTML = kpiHTML;
}

// Helper function to calculate mean
function mean(arr) {
    const filtered = arr.filter(x => x != null && !isNaN(x));
    return filtered.reduce((a, b) => a + b, 0) / filtered.length;
}

// Calculate eNPS
function calculateENPS() {
    const scores = surveyData.map(d => d.Q9_LikelihoodToRecommend);
    const promoters = scores.filter(s => s >= 4).length;
    const detractors = scores.filter(s => s <= 2).length;
    return Math.round((promoters / scores.length * 100) - (detractors / scores.length * 100));
}

// Chart 1: Satisfaction by College
function createSatisfactionByCollege() {
    const colleges = ['Arts & Letters', 'Science', 'Engineering', 'Business', 'Architecture', 'Law', 'Global Affairs'];
    const data = colleges.map(college => {
        const collegeData = surveyData.filter(d => d.College === college);
        return mean(collegeData.map(d => d.Q8_OverallSatisfaction));
    });

    const ctx = document.getElementById('satisfactionByCollege').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: colleges,
            datasets: [{
                label: 'Mean Satisfaction Score',
                data: data,
                backgroundColor: data.map(d => d >= 3.8 ? '#10B981' : d >= 3.5 ? '#F59E0B' : '#EF4444'),
                borderColor: '#0C2340',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 0.5
                    },
                    title: {
                        display: true,
                        text: 'Satisfaction Score (1-5)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Satisfaction: ${context.parsed.y.toFixed(2)}/5.0`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 2: eNPS by College
function createENPSChart() {
    const colleges = ['Arts & Letters', 'Science', 'Engineering', 'Business', 'Architecture', 'Law'];
    const enpsData = colleges.map(college => {
        const collegeData = surveyData.filter(d => d.College === college);
        const scores = collegeData.map(d => d.Q9_LikelihoodToRecommend);
        const promoters = scores.filter(s => s >= 4).length;
        const detractors = scores.filter(s => s <= 2).length;
        return Math.round((promoters / scores.length * 100) - (detractors / scores.length * 100));
    });

    const ctx = document.getElementById('enpsChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: colleges,
            datasets: [{
                label: 'eNPS Score',
                data: enpsData,
                backgroundColor: enpsData.map(d => d >= 30 ? '#10B981' : d >= 10 ? '#F59E0B' : d >= 0 ? '#F97316' : '#EF4444'),
                borderColor: '#0C2340',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    min: -20,
                    max: 50,
                    title: {
                        display: true,
                        text: 'eNPS Score'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const score = context.parsed.x;
                            let rating = 'Critical';
                            if (score >= 50) rating = 'Excellent';
                            else if (score >= 30) rating = 'Very Good';
                            else if (score >= 10) rating = 'Good';
                            else if (score >= 0) rating = 'Needs Improvement';
                            return `eNPS: ${score} (${rating})`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 3: Equity Analysis
function createEquityChart() {
    const metrics = ['Overall\nSatisfaction', 'Belonging', 'Psych.\nSafety', 'Work-Life\nBalance'];

    const genderGroups = ['Man', 'Woman', 'Non-binary'];
    const datasets = genderGroups.map((gender, idx) => {
        const filtered = surveyData.filter(d => d.Gender === gender);
        return {
            label: gender,
            data: [
                mean(filtered.map(d => d.Q8_OverallSatisfaction)),
                mean(filtered.map(d => d.Q27_Belonging)),
                mean(filtered.map(d => d.Q26_PsychologicalSafety)),
                mean(filtered.map(d => d.Q13_WorkLifeBalance))
            ],
            backgroundColor: ['#3B82F6', '#EC4899', '#8B5CF6'][idx],
            borderColor: '#0C2340',
            borderWidth: 1
        };
    });

    const ctx = document.getElementById('equityChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: metrics,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    title: {
                        display: true,
                        text: 'Mean Score (1-5)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'By Gender Identity',
                    font: {
                        size: 14
                    }
                }
            }
        }
    });
}

// Chart 4: Retention Drivers
function createRetentionDrivers() {
    const leavingReasons = [
        { label: 'Workload/Work-Life', key: 'Q11_Workload', pct: 64 },
        { label: 'Compensation', key: 'Q11_Compensation', pct: 58 },
        { label: 'Better Opportunity', key: 'Q11_BetterOpportunity', pct: 42 },
        { label: 'Dept. Climate', key: 'Q11_DeptClimate', pct: 38 },
        { label: 'Lack of Recognition', key: 'Q11_LackRecognition', pct: 35 },
        { label: 'Research Support', key: 'Q11_ResearchSupport', pct: 31 },
        { label: 'Limited Advancement', key: 'Q11_LimitedAdvancement', pct: 22 },
        { label: 'Teaching Support', key: 'Q11_TeachingSupport', pct: 18 }
    ];

    const ctx = document.getElementById('retentionDrivers').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: leavingReasons.map(r => r.label),
            datasets: [{
                label: '% of At-Risk Faculty',
                data: leavingReasons.map(r => r.pct),
                backgroundColor: '#EF4444',
                borderColor: '#DC2626',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            indexAxis: 'y',
            scales: {
                x: {
                    max: 100,
                    title: {
                        display: true,
                        text: '% Selected (Among those considering leaving)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.x}% selected this reason`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 5: Workload by Discipline
function createWorkloadChart() {
    const disciplines = ['STEM', 'Social Sciences', 'Humanities', 'Business', 'Arts & Performance'];
    const avgHours = [62, 56, 58, 52, 55];
    const pct70Plus = [28, 18, 22, 12, 15];

    const ctx = document.getElementById('workloadChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: disciplines,
            datasets: [
                {
                    label: 'Avg. Weekly Hours',
                    data: avgHours,
                    backgroundColor: '#3B82F6',
                    borderColor: '#2563EB',
                    borderWidth: 1,
                    yAxisID: 'y'
                },
                {
                    label: '% Working 70+ Hours',
                    data: pct70Plus,
                    backgroundColor: '#EF4444',
                    borderColor: '#DC2626',
                    borderWidth: 1,
                    yAxisID: 'y1'
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    type: 'linear',
                    display: true,
                    position: 'left',
                    max: 70,
                    title: {
                        display: true,
                        text: 'Average Hours/Week'
                    }
                },
                y1: {
                    type: 'linear',
                    display: true,
                    position: 'right',
                    max: 35,
                    grid: {
                        drawOnChartArea: false
                    },
                    title: {
                        display: true,
                        text: '% Working 70+ Hours'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                }
            }
        }
    });
}

// Chart 6: Tenure Clarity vs Fairness Scatter
function createTenureScatter() {
    const colleges = ['Arts & Letters', 'Science', 'Engineering', 'Business', 'Architecture', 'Law'];
    const clarityData = [3.5, 3.0, 4.3, 3.2, 4.0, 3.7];
    const fairnessData = [3.5, 3.1, 4.2, 4.1, 3.0, 3.7];

    const scatterData = colleges.map((college, idx) => ({
        x: clarityData[idx],
        y: fairnessData[idx],
        label: college
    }));

    const ctx = document.getElementById('tenureScatter').getContext('2d');
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Colleges',
                data: scatterData,
                backgroundColor: scatterData.map(d => {
                    if (d.x >= 3.5 && d.y >= 3.5) return '#10B981';
                    if (d.x < 3.5 && d.y < 3.5) return '#EF4444';
                    return '#F59E0B';
                }),
                pointRadius: 8,
                pointHoverRadius: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    min: 2.5,
                    max: 4.5,
                    title: {
                        display: true,
                        text: 'Tenure Clarity (1-5)'
                    },
                    grid: {
                        drawBorder: true,
                        color: (context) => {
                            if (context.tick.value === 3.5) return '#000';
                            return '#E5E7EB';
                        },
                        lineWidth: (context) => {
                            return context.tick.value === 3.5 ? 2 : 1;
                        }
                    }
                },
                y: {
                    min: 2.5,
                    max: 4.5,
                    title: {
                        display: true,
                        text: 'Tenure Fairness (1-5)'
                    },
                    grid: {
                        drawBorder: true,
                        color: (context) => {
                            if (context.tick.value === 3.5) return '#000';
                            return '#E5E7EB';
                        },
                        lineWidth: (context) => {
                            return context.tick.value === 3.5 ? 2 : 1;
                        }
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const point = scatterData[context.dataIndex];
                            return `${point.label}: Clarity ${point.x.toFixed(1)}, Fairness ${point.y.toFixed(1)}`;
                        }
                    }
                }
            }
        }
    });
}

// Chart 7: Belonging Heatmap (simulated as grouped bar)
function createBelongingHeatmap() {
    const races = ['White', 'Asian', 'Black/AA', 'Hispanic', 'Other'];
    const menScores = [4.2, 4.0, 3.6, 3.7, 3.8];
    const womenScores = [3.8, 3.4, 2.9, 3.3, 3.2];
    const nonBinaryScores = [3.5, 3.2, 2.7, 3.1, 2.8];

    const ctx = document.getElementById('belongingHeatmap').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: races,
            datasets: [
                {
                    label: 'Men',
                    data: menScores,
                    backgroundColor: '#3B82F6',
                    borderColor: '#2563EB',
                    borderWidth: 1
                },
                {
                    label: 'Women',
                    data: womenScores,
                    backgroundColor: '#EC4899',
                    borderColor: '#DB2777',
                    borderWidth: 1
                },
                {
                    label: 'Non-binary',
                    data: nonBinaryScores,
                    backgroundColor: '#8B5CF6',
                    borderColor: '#7C3AED',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 5,
                    title: {
                        display: true,
                        text: 'Belonging Score (1-5)'
                    }
                }
            },
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Gender × Race/Ethnicity Intersection',
                    font: {
                        size: 14
                    }
                }
            }
        }
    });
}

// Chart 8: Radar Chart
function createRadarChart() {
    const metrics = [
        'Overall Satisfaction',
        'Work-Life Balance',
        'Compensation',
        'Belonging',
        'Psych. Safety',
        'Collaboration',
        'Prof. Development',
        'Research Funding'
    ];

    const overallScores = [
        mean(surveyData.map(d => d.Q8_OverallSatisfaction)),
        mean(surveyData.map(d => d.Q13_WorkLifeBalance)),
        mean(surveyData.map(d => d.Q22_Compensation)),
        mean(surveyData.map(d => d.Q27_Belonging)),
        mean(surveyData.map(d => d.Q26_PsychologicalSafety)),
        mean(surveyData.map(d => d.Q21_Collaboration)),
        mean(surveyData.map(d => d.Q19_ProfDevelopment)),
        mean(surveyData.map(d => d.Q18_ResearchFunding))
    ];

    const ctx = document.getElementById('radarChart').getContext('2d');
    new Chart(ctx, {
        type: 'radar',
        data: {
            labels: metrics,
            datasets: [{
                label: 'University Average',
                data: overallScores,
                backgroundColor: 'rgba(59, 130, 246, 0.2)',
                borderColor: '#3B82F6',
                borderWidth: 2,
                pointBackgroundColor: '#3B82F6',
                pointBorderColor: '#fff',
                pointRadius: 4,
                pointHoverRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    beginAtZero: true,
                    max: 5,
                    ticks: {
                        stepSize: 1
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
}
