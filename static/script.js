document.addEventListener('DOMContentLoaded', function () {
    var viewMoreButtons = document.querySelectorAll('.view-more-button');

    viewMoreButtons.forEach(function (button) {
        button.addEventListener('click', function () {
            var targetId = button.getAttribute('data-target');
            var detailsRow = document.getElementById(targetId);

            if (detailsRow) {
                detailsRow.classList.toggle('details-shown');

                var buttonText = detailsRow.classList.contains('details-shown') ? 'Hide' : 'View More';
                button.textContent = buttonText;
            }
        });
    });
});



document.addEventListener('DOMContentLoaded', function () {
    var filterButton = document.getElementById('filter-btn');
    var filterContainer = document.getElementById('filter-container');

    filterButton.addEventListener('click', function () {
        filterContainer.classList.toggle('filter-visible');
    });
});



