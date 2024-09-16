document.addEventListener('DOMContentLoaded', function () {
    var courseTypeField = document.querySelector('#id_course_type');
    var oldPriceField = document.querySelector('.field-old_price');
    var priceField = document.querySelector('.field-price');

    function togglePriceFields() {
        if (courseTypeField.value === 'Paid') {
            oldPriceField.style.display = 'block';
            priceField.style.display = 'block';
        } else {
            oldPriceField.style.display = 'none';
            priceField.style.display = 'none';
        }
    }

    // Initial call to set the correct visibility
    togglePriceFields();

    // Add event listener to the course_type select field
    courseTypeField.addEventListener('change', togglePriceFields);
});
