
const AccessData = {
    // Access data for the vending machine
    executeQuery: async function(query) {
        // Simulate a database query
        return Promise.resolve([{ id: 1, name: 'John Doe' }, { id: 2, name: 'Jane Doe' }]);
    }

};

// Initialize the vending machine application

module.exports = AccessData;