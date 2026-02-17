/**
 * Data Transform Module
 * Responsible for cleaning, normalizing, and aggregating data for visualization.
 */

/**
 * Clean and normalize raw data.
 * @param {Array} rawData - The raw data array from PapaParse.
 * @returns {Array} - Cleaned data.
 */
export function processData(rawData) {
    return rawData.map(row => {
        // Create a proper Date object from 'Start date'
        // Assuming format is YYYY-MM-DD based on CSV inspection
        const dateStr = row['Start date'];
        const dateObj = dateStr ? new Date(dateStr) : null;

        return {
            ...row,
            dateObj: dateObj,
            year: dateObj ? dateObj.getFullYear() : null,
            month: dateObj ? dateObj.getMonth() + 1 : null, // 1-12
            financialDamage: parseFloat(row['Financial damage']) || 0,
            bicycleType: row['Type of bicycle'] || 'Unknown',
            offenceType: row['Offence type'] || 'Unknown'
        };
    }).filter(row => row.dateObj !== null); // Remove rows with invalid dates
}

/**
 * Aggregate data by date for trend analysis.
 * @param {Array} data - Processed data.
 * @returns {Object} - { dates: [], counts: [] }
 */
export function aggregateByDate(data) {
    const counts = {};

    data.forEach(row => {
        const dateKey = row['Start date']; // Using string format YYYY-MM-DD
        counts[dateKey] = (counts[dateKey] || 0) + 1;
    });

    const sortedDates = Object.keys(counts).sort();

    return {
        dates: sortedDates,
        values: sortedDates.map(date => counts[date])
    };
}

/**
 * Aggregate data by a categorical field (e.g., 'Type of bicycle').
 * @param {Array} data - Processed data.
 * @param {string} field - Field name to group by.
 * @returns {Object} - { labels: [], values: [] }
 */
export function aggregateByCategory(data, field) {
    const counts = {};

    data.forEach(row => {
        const key = row[field] || 'Unknown';
        counts[key] = (counts[key] || 0) + 1;
    });

    // Sort by count descending
    const entries = Object.entries(counts).sort((a, b) => b[1] - a[1]);

    return {
        labels: entries.map(e => e[0]),
        values: entries.map(e => e[1])
    };
}

/**
 * Calculate key metrics.
 * @param {Array} data 
 * @returns {Object}
 */
export function calculateMetrics(data) {
    const totalIncidents = data.length;
    const totalDamage = data.reduce((sum, row) => sum + row.financialDamage, 0);
    const avgDamage = totalIncidents > 0 ? totalDamage / totalIncidents : 0;

    return {
        totalIncidents: totalIncidents.toLocaleString(),
        totalDamage: Math.round(totalDamage).toLocaleString() + ' €',
        avgDamage: Math.round(avgDamage).toLocaleString() + ' €'
    };
}
