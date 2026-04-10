<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<h2>Outage Trends</h2>
<canvas id="myChart"></canvas>

<script>
const ctx = document.getElementById('myChart');

new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Day1','Day2','Day3'],
        datasets: [{
            label: 'Future Outages',
            data: {{ future | tojson }},
            borderWidth: 2
        }]
    }
});
</script>