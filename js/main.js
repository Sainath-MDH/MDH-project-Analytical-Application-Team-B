/**
 * Main Application Module
 * Orchestrates data loading, transformation, and visualization.
 */

import { loadData } from './dataLoader.js';
import { processData, aggregateByDate, aggregateByCategory, calculateMetrics } from './dataTransform.js';
import { renderTrendChart, renderBarChart, renderPieChart } from './charts.js';

const DATA_URL = 'data/bike_thefts.csv'; // Relative path to data

async function initDashboard() {
    try {
        console.log("Initializing Dashboard...");

        // 1. Load Data
        const rawData = await loadData(DATA_URL);

        // 2. Transform Data
        const cleanData = processData(rawData);
        console.log(`Processed ${cleanData.length} valid rows.`);

        // 3. Calculate Metrics
        const metrics = calculateMetrics(cleanData);
        updateKPIs(metrics);

        // 4. Prepare Chart Data
        const trendData = aggregateByDate(cleanData);
        const typeData = aggregateByCategory(cleanData, 'bicycleType');
        const offenceData = aggregateByCategory(cleanData, 'offenceType');

        // 5. Render Charts
        renderTrendChart('trendChart', trendData);
        renderBarChart('categoryChart', typeData, 'Thefts by Bicycle Type', 'h');
        renderPieChart('offenceChart', offenceData, 'Thefts by Offence Type');

        // Remove loading spinner
        document.getElementById('loading').style.display = 'none';

    } catch (error) {
        console.error("Dashboard Error:", error);
        document.getElementById('loading').innerHTML = `<p style="color:red">Error loading data: ${error.message}</p>`;
    }
}

function updateKPIs(metrics) {
    document.getElementById('kpi-incidents').textContent = metrics.totalIncidents;
    document.getElementById('kpi-damage').textContent = metrics.totalDamage;
    document.getElementById('kpi-avg').textContent = metrics.avgDamage;
}

// Start the app when DOM is ready
document.addEventListener('DOMContentLoaded', initDashboard);
