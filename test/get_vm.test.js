require('jest-fetch-mock').enableMocks();
const VM = require('../src/get_vm');

describe('getMachineDetails', () => {
    it('should fetch the machine details', async () => {
        const vm = new VM();
        await vm.getMachineDetails();
        expect(vm.data).toEqual({
        vm1: {
            name: 'Snack Machine',
            location: '1st floor',
            review: '4.5/5',
            status: 'active',
            description: 'This is a snack machine.',
        },
        vm2: {
            name: 'Drink Machine',
            location: '2nd floor',
            review: '4/5',
            status: 'inactive',
            description: 'This is a drink machine.',
        },
        });
    });
    });