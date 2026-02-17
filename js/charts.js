/**
 * Charts Module
 * Responsible for rendering charts using Plotly.js.
 */

const darkLayout = {
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
        family: 'Inter, sans-serif',
        color: '#e0e0e0'
    },
    xaxis: {
        gridcolor: '#333',
        zerolinecolor: '#333'
    },
    yaxis: {
        gridcolor: '#333',
        zerolinecolor: '#333'
    },
    margin: { t: 40, r: 20, l: 60, b: 40 }
};

export function renderTrendChart(containerId, aggregatedData) {
    const trace = {
        x: aggregatedData.dates,
        y: aggregatedData.values,
        type: 'scatter',
        mode: 'lines',
        line: {
            color: '#00d4ff',
            width: 3
        },
        fill: 'tozeroy', // Gradient fill
        fillcolor: 'rgba(0, 212, 255, 0.2)'
    };

    const layout = {
        ...darkLayout,
        title: 'Daily Bicycle Thefts Trend',
        xaxis: { ...darkLayout.xaxis, title: 'Date' },
        yaxis: { ...darkLayout.yaxis, title: 'Number of Thefts' }
    };

    Plotly.newPlot(containerId, [trace], layout, { responsive: true, displayModeBar: false });
}

export function renderBarChart(containerId, aggregatedData, title = 'Chart', orientation = 'v') {
    const trace = {
        x: orientation === 'v' ? aggregatedData.labels : aggregatedData.values,
        y: orientation === 'v' ? aggregatedData.values : aggregatedData.labels,
        type: 'bar',
        orientation: orientation,
        marker: {
            color: '#ff006e' // Vibrant pink/magenta
        }
    };

    const layout = {
        ...darkLayout,
        title: title,
        xaxis: { ...darkLayout.xaxis },
        yaxis: { ...darkLayout.yaxis }
    };

    // Adjust margins for horizontal bar charts to fit labels
    if (orientation === 'h') {
        layout.margin.l = 150;
    }

    Plotly.newPlot(containerId, [trace], layout, { responsive: true, displayModeBar: false });
}

export function renderPieChart(containerId, aggregatedData, title = 'Distribution') {
    const trace = {
        labels: aggregatedData.labels,
        values: aggregatedData.values,
        type: 'pie',
        textinfo: 'label+percent',
        insidetextorientation: 'radial',
        hole: 0.4, // Donut chart style
        marker: {
            colors: [
                '#00d4ff', '#ff006e', '#8338ec', '#ffbe0b', '#fb5607',
                '#3a86ff', '#e0e0e0', '#9e9e9e'
            ]
        }
    };

    const layout = {
        ...darkLayout,
        title: title,
        showlegend: false
    };

    Plotly.newPlot(containerId, [trace], layout, { responsive: true, displayModeBar: false });
}
