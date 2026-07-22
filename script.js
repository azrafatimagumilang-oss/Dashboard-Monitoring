<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>


<script>

const overcut = {{ summary.overcut }};
const undercut = {{ summary.undercut }};
const ongrade = {{ summary.ongrade }};
const exposes = {{ summary.exposes }};

const total = overcut + undercut + ongrade + exposes;

new Chart(document.getElementById('statusChart'), {

    type: 'pie',

    data: {

        labels: [
    'Overcut',
    'Undercut',
    'On Grade',
    'Exposes'
],

        datasets: [{
           data: [
    overcut,
    undercut,
    ongrade,
    exposes
],

            backgroundColor: [
    '#dc3545',
    '#198754',
    '#5e5b58',
    '#ffc107'
]
        }]
    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                position: 'bottom'
            },

            tooltip: {

                callbacks: {

                    label: function(context) {

                        let value = context.raw;

                        let persen =
                            ((value / total) * 100).toFixed(1);

                        return context.label +
                               ': ' +
                               value +
                               ' (' +
                               persen +
                               '%)';
                    }

                }

            }

        }

    }

});
const trendCtx =
document.getElementById('trendChart');

new Chart(trendCtx, {

    type: 'line',

    data: {

        labels: {{ trend_chart.labels|tojson }},

        datasets: [

            {
                label: 'Overcut',

                data: {{ trend_chart.overcut|tojson }},

                borderColor: '#dc3545',

                backgroundColor: '#dc3545',

                tension: 0.3
            },

            {
                label: 'Undercut',

                data: {{ trend_chart.undercut|tojson }},

                borderColor: '#198754',

                backgroundColor: '#198754',

                tension: 0.3
            }

        ]

    },

    options: {

        responsive: true,

        plugins: {

            legend: {
                position: 'bottom'
            }

        },

        scales: {

            y: {
                beginAtZero: true
            }

        }

    }

});

</script>
</body>
</html>