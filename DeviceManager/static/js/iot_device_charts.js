class TemperatureChart {
    constructor(ctx) {
        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [0, 50],
                    backgroundColor: [this.getTemperatureColor(0), 'rgba(200, 200, 200, 0.1)'],
                    borderWidth: 2,
                    borderColor: 'rgba(255, 255, 255, 0.8)'
                }]
            },
            options: {
                responsive: true,
                cutout: '60%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            },
            plugins: [{
                id: 'temperatureDisplay',
                beforeDraw: (chart) => this.drawTemperature(chart)
            }]
        });
    }

    getTemperatureColor(temp) {
        if (temp <= -30) return '#0000FF';  // Blue
        if (temp <= -27.5) return '#0022FF';
        if (temp <= -25) return '#0044FF';
        if (temp <= -22.5) return '#0066FF';
        if (temp <= -20) return '#0088FF';
        if (temp <= -17.5) return '#00AAFF';
        if (temp <= -15) return '#00CCFF';
        if (temp <= -12.5) return '#00EEFF';
        if (temp <= -10) return '#00FFFF';  // Cyan
        if (temp <= -7.5) return '#00FFDD';
        if (temp <= -5) return '#00FFBB';
        if (temp <= -2.5) return '#00FF99';
        if (temp <= 0) return '#00FF77';
        if (temp <= 2.5) return '#00FF55';
        if (temp <= 5) return '#00FF33';
        if (temp <= 7.5) return '#00FF11';
        if (temp <= 10) return '#11FF00';
        if (temp <= 12.5) return '#33FF00';
        if (temp <= 15) return '#55FF00';
        if (temp <= 17.5) return '#77FF00';
        if (temp <= 20) return '#99FF00';
        if (temp <= 22.5) return '#BBFF00';
        if (temp <= 25) return '#DDFF00';
        if (temp <= 27.5) return '#FFFF00';  // Yellow
        if (temp <= 30) return '#FFDD00';
        if (temp <= 32.5) return '#FFBB00';
        if (temp <= 35) return '#FF9900';
        if (temp <= 37.5) return '#FF7700';
        if (temp <= 40) return '#FF5500';
        if (temp <= 42.5) return '#FF3300';
        if (temp <= 45) return '#FF1100';
        return '#FF0000';  // Red
    }
    
    
    

    drawTemperature(chart) {
        const {ctx, width, height} = chart;
        ctx.save();
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';

        const centerX = width / 2;
        const centerY = height / 2;
        const temperature = chart.data.datasets[0].data[0];

    // Draw colored background circle
    const radius = Math.min(width, height) * 0.3; // Adjust size as needed
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
    ctx.fillStyle = 'black';
    ctx.fill();

    // Draw main temperature
    ctx.font = 'bold ' + (height / 8) + 'px Arial';
    ctx.fillStyle = 'white';
    ctx.fillText(temperature.toFixed(1) + '°C', centerX, centerY);

    ctx.restore();
    }

    update(temperature) {
        this.chart.data.datasets[0].data = [temperature, 50 - temperature];
        this.chart.data.datasets[0].backgroundColor[0] = this.getTemperatureColor(temperature);
        this.chart.update();
    }

    noData() {
        this.chart.data.datasets[0].data = [0, 50];
        this.chart.data.datasets[0].backgroundColor[0] = '#CCCCCC';
        this.chart.update();
    }
}

class PressureChart {
    constructor(ctx) {
        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                datasets: [{
                    data: [900, 1100],
                    backgroundColor: [this.getPressureColor(0), 'rgba(200, 200, 200, 0.1)'],
                    borderWidth: 2,
                    borderColor: 'rgba(255, 255, 255, 0.8)'
                }]
            },
            options: {
                responsive: true,
                cutout: '60%',
                plugins: {
                    legend: { display: false },
                    tooltip: { enabled: false }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true
                }
            },
            plugins: [{
                id: 'pressureDisplay',
                beforeDraw: (chart) => this.drawPressure(chart)
            }]
        });
    }
    

    getPressureColor(pressure) {
        if (pressure <= 950) return '#0000FF';
        if (pressure <= 980) return '#4169E1';
        if (pressure <= 1000) return '#00BFFF';
        if (pressure <= 1020) return '#00FFFF';
        if (pressure <= 1040) return '#00FF7F';
        if (pressure <= 1060) return '#ADFF2F';
        return '#FFFF00';
    }

    drawPressure(chart) {
        const {ctx, width, height} = chart;
        ctx.save();
        ctx.fillStyle = 'white';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
    
        const centerX = width / 2;
        const centerY = height / 2;
        const pressure = chart.data.datasets[0].data[0];
    
        // Draw colored background circle
        const radius = Math.min(width, height) * 0.3;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.fillStyle = 'black';
        ctx.fill();
    
        // Draw main pressure
        ctx.font = 'bold ' + (height / 8) + 'px Arial';
        ctx.fillStyle = 'white';
        ctx.fillText(pressure.toFixed(0) + ' hPa', centerX, centerY);
    
        ctx.restore();
    }
    

    update(pressure) {
        this.chart.data.datasets[0].data = [pressure, 1100 - pressure];
        this.chart.data.datasets[0].backgroundColor[0] = this.getPressureColor(pressure);
        this.chart.update();
    }
    

    noData() {
        this.chart.data.datasets[0].data = [900, 1100];
        this.chart.data.datasets[0].backgroundColor[0] = '#CCCCCC';
        this.chart.update();
    }
}
