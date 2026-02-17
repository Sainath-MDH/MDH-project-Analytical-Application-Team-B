/**
 * Data Loader Module
 * Responsible for fetching and parsing CSV data using PapaParse.
 */

// Load PapaParse from CDN in index.html, so it's available globally as 'Papa'

export async function loadData(url) {
    return new Promise((resolve, reject) => {
        Papa.parse(url, {
            download: true,
            header: true,
            dynamicTyping: true, // Automatically converts numbers
            skipEmptyLines: true,
            complete: (results) => {
                if (results.data && results.data.length > 0) {
                    console.log(`Successfully loaded ${results.data.length} rows.`);
                    resolve(results.data);
                } else {
                    reject(new Error("No data found in CSV."));
                }
            },
            error: (error) => {
                reject(error);
            }
        });
    });
}
