/*
This file contains the test cases for get_vm.js functions.
It does not include the intereation with the DOM.
*/
const access = require('../src/acess_data');

test('should execute query and return results', async () => {
    const query = 'SELECT * FROM vending_machines WHERE status = "active"';
    const expectedResults = [{ id: 1, name: 'John Doe' }, { id: 2, name: 'Jane Doe' }];
    
    const results = await access.executeQuery(query);
    
    expect(results).toEqual(expectedResults);
    expect(access.executeQuery).toHaveBeenCalledWith(query);
});