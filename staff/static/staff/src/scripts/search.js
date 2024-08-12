document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById('inputField');
    const datalist = document.getElementById('suggestions');
    const allOptions = ['Option 1', 'Option 2', 'Option 3', 'Option 4', 'Option A', 'Option B', 'Option C'];

    inputField.addEventListener('input', () => {
        const inputValue = inputField.value.toLowerCase();
        datalist.innerHTML = '';

        const filteredOptions = allOptions.filter(option =>
            option.toLowerCase().includes(inputValue)
        );

        filteredOptions.forEach(option => {
            const optionElement = document.createElement('option');
            optionElement.value = option;
            datalist.appendChild(optionElement);
        });
    });
});