(async () => {
    let entries = performance.getEntries().map((e) => e.toJSON()).sort((a, b) => a.name.localeCompare(b.name));
    window.perf = {};

    for (let entry of entries) {
        for (let key in entry) {
            // Filter out certain time values and specific properties
            if ((typeof entry[key] === 'number' && entry[key] > 0) || key === 'fetchStart' || key === 'domainLookupStart') {
                delete entry[key];
            }
        }

        if (!window.perf[entry.entryType]) {
            window.perf[entry.entryType] = [];
        }
        window.perf[entry.entryType].push(entry);
    }
    return window.perf
})();
