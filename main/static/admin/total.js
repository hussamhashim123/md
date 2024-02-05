(function ($) {
    $(document).ready(function () {
        $(document).on('input', '.field-money input[name$="-money"]', function () {
            const moneyField = $(this);
            const inlineGroup = moneyField.closest('tr');
            const tax = inlineGroup.find('.field-tax p');
            const total = inlineGroup.find('.field-total p');
            const moneyValue = parseFloat(moneyField.val());
            if (moneyValue) {
                const calculatedTax = moneyValue * 0.03;
                const calculatedTotal = moneyValue - calculatedTax;
                tax.text(calculatedTax);
                total.text(calculatedTotal);
            } else {
                tax.text('');
                total.text('');
            }
        });


        function updateTotals() {
            let totalMoney = 0;
            let totalTax = 0;
            let totalTotal = 0;

            document.querySelectorAll('.inline-related tbody tr[id^="item_set-"]').forEach((row) => {
                const moneyField = row.querySelector('.field-money input[name$="-money"]');
                const taxField = row.querySelector('.field-tax p');
                const totalField = row.querySelector('.field-total p');
                const moneyValue = parseFloat(moneyField.value) || 0;
                const taxValue = parseFloat(taxField.innerText) || 0;
                const totalValue = parseFloat(totalField.innerText) || 0;
                totalMoney += moneyValue;
                totalTax += taxValue;
                totalTotal += totalValue;
            });

            $('.total-money').text(totalMoney);
            $('.total-tax').text(totalTax);
            $('.total-total').text(totalTotal);
        }

        $('.field-money input[name$="-money"]').on('input', updateTotals);


        setTimeout(() => {
            const addRow = document.querySelector('.add-row');
            const totalMoneyCell = document.createElement('td')
            totalMoneyCell.classList.add('totals-container')
            const totalMoney = document.createElement('span')
            totalMoney.classList.add('total-money')
            totalMoneyCell.append(totalMoney)
            const totalTaxCell = document.createElement('td')
            totalTaxCell.classList.add('totals-container')
            const totalTax = document.createElement('span')
            totalTax.classList.add('total-tax')
            totalTaxCell.append(totalTax)
            const totalTotalCell = document.createElement('td')
            totalTotalCell.classList.add('totals-container')
            const totalTotal = document.createElement('span')
            totalTotal.classList.add('total-total')
            totalTotalCell.append(totalTotal)
            addRow.prepend(totalTotalCell);
            addRow.prepend(totalTaxCell);
            addRow.prepend(totalMoneyCell);

            const emptyCell = document.createElement('td');
            emptyCell.innerText = 'Total: ';
            emptyCell.colSpan = '2'
            emptyCell.style.textAlign = 'center';
            addRow.prepend(emptyCell);
            addRow.lastElementChild.colSpan = 1;
            updateTotals();
        }, 0)
    })

})(django.jQuery);
