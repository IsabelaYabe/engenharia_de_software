// Dados fictícios para simular vending machines e estoque de produtos
const vendingMachines = [
    { id: 1, name: "Vending Machine 1", products: [
        { name: "Coca-Cola", stock: 10 },
        { name: "Pepsi", stock: 5 },
        { name: "Água Mineral", stock: 20 }
    ]},
    { id: 2, name: "Vending Machine 2", products: [
        { name: "Chips", stock: 15 },
        { name: "Chocolate", stock: 8 },
        { name: "Suco de Laranja", stock: 12 }
    ]},
    { id: 3, name: "Vending Machine 3", products: [
        { name: "Biscoito", stock: 25 },
        { name: "Sanduíche", stock: 5 },
        { name: "Café", stock: 30 }
    ]}
];

// Função para carregar os dados de estoque na tabela
function loadStockTable() {
    const tableBody = document.querySelector('#stock-table tbody');
    tableBody.innerHTML = ''; // Limpa a tabela antes de adicionar os dados

    vendingMachines.forEach(machine => {
        machine.products.forEach(product => {
            const row = document.createElement('tr');
            row.classList.add('product-row'); // Adiciona uma classe para usar no filtro

            const vmCell = document.createElement('td');
            const productNameCell = document.createElement('td');
            const productStockCell = document.createElement('td');

            vmCell.textContent = machine.name;
            productNameCell.textContent = product.name;
            productStockCell.textContent = product.stock;

            row.appendChild(vmCell);
            row.appendChild(productNameCell);
            row.appendChild(productStockCell);
            tableBody.appendChild(row);
        });
    });
}

// Função para filtrar os produtos com base no texto digitado nos dois filtros
function filterProducts() {
    const vmFilterValue = document.getElementById('vm-filter').value.toLowerCase();
    const productFilterValue = document.getElementById('product-filter').value.toLowerCase();
    const rows = document.querySelectorAll('.product-row');

    rows.forEach(row => {
        const vmName = row.querySelector('td:first-child').textContent.toLowerCase(); // Nome da VM na primeira célula
        const productName = row.querySelector('td:nth-child(2)').textContent.toLowerCase(); // Nome do produto na segunda célula

        // Verifica se o nome da VM e o nome do produto contêm os valores dos filtros
        if (vmName.includes(vmFilterValue) && productName.includes(productFilterValue)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Carrega a tabela de estoque ao carregar a página
window.onload = loadStockTable;
