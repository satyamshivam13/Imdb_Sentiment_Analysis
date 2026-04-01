(() => {
  const config = window.dashboardConfig || {};
  const distributionCanvas = document.getElementById("distribution-chart");
  const trendCanvas = document.getElementById("trend-chart");
  const filterForm = document.getElementById("dashboard-filters");

  if (!distributionCanvas || !trendCanvas || !window.Chart) {
    return;
  }

  const charts = {
    distribution: null,
    trend: null,
  };

  const palette = {
    positive: "rgba(52, 211, 153, 0.92)",
    positiveSoft: "rgba(52, 211, 153, 0.2)",
    negative: "rgba(251, 113, 133, 0.92)",
    negativeSoft: "rgba(251, 113, 133, 0.2)",
    text: "rgba(226, 232, 240, 0.9)",
    grid: "rgba(148, 163, 184, 0.16)",
  };

  const toJson = async (url) => {
    const response = await fetch(url, { headers: { Accept: "application/json" } });
    if (!response.ok) {
      throw new Error(`Request failed: ${response.status}`);
    }
    return response.json();
  };

  const updateDistributionChart = (payload) => {
    const labels = ["Positive", "Negative"];
    const values = [payload.positive.count, payload.negative.count];
    const colors = [palette.positive, palette.negative];

    if (!charts.distribution) {
      charts.distribution = new Chart(distributionCanvas, {
        type: "doughnut",
        data: {
          labels,
          datasets: [
            {
              data: values,
              backgroundColor: colors,
              borderColor: [palette.positiveSoft, palette.negativeSoft],
              borderWidth: 2,
              hoverOffset: 8,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: "68%",
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: palette.text,
                usePointStyle: true,
                pointStyle: "circle",
              },
            },
            tooltip: {
              callbacks: {
                label(context) {
                  const total = payload.total || 1;
                  const value = context.parsed;
                  const percentage = ((value / total) * 100).toFixed(1);
                  return `${context.label}: ${value} (${percentage}%)`;
                },
              },
            },
          },
        },
      });
      return;
    }

    charts.distribution.data.labels = labels;
    charts.distribution.data.datasets[0].data = values;
    charts.distribution.update();
  };

  const updateTrendChart = (payload) => {
    const labels = payload.labels || [];
    const positiveSeries = payload.series?.positive || [];
    const negativeSeries = payload.series?.negative || [];

    if (!charts.trend) {
      charts.trend = new Chart(trendCanvas, {
        type: "line",
        data: {
          labels,
          datasets: [
            {
              label: "Positive",
              data: positiveSeries,
              borderColor: palette.positive,
              backgroundColor: palette.positiveSoft,
              tension: 0.35,
              pointRadius: 3,
              pointHoverRadius: 5,
              fill: false,
            },
            {
              label: "Negative",
              data: negativeSeries,
              borderColor: palette.negative,
              backgroundColor: palette.negativeSoft,
              tension: 0.35,
              pointRadius: 3,
              pointHoverRadius: 5,
              fill: false,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: {
            mode: "index",
            intersect: false,
          },
          scales: {
            x: {
              ticks: { color: palette.text },
              grid: { color: palette.grid },
            },
            y: {
              beginAtZero: true,
              ticks: { color: palette.text, precision: 0 },
              grid: { color: palette.grid },
            },
          },
          plugins: {
            legend: {
              position: "bottom",
              labels: {
                color: palette.text,
                usePointStyle: true,
                pointStyle: "line",
              },
            },
            tooltip: {
              callbacks: {
                title(items) {
                  return items[0]?.label || "";
                },
                label(context) {
                  return `${context.dataset.label}: ${context.parsed.y}`;
                },
              },
            },
          },
        },
      });
      return;
    }

    charts.trend.data.labels = labels;
    charts.trend.data.datasets[0].data = positiveSeries;
    charts.trend.data.datasets[1].data = negativeSeries;
    charts.trend.update();
  };

  const loadCharts = async () => {
    const [distributionPayload, trendPayload] = await Promise.all([
      toJson(config.distributionUrl),
      toJson(config.trendUrl),
    ]);

    updateDistributionChart(distributionPayload);
    updateTrendChart(trendPayload);
  };

  if (filterForm) {
    filterForm.addEventListener("submit", () => {
      const submitButton = filterForm.querySelector("button[type='submit']");
      if (submitButton) {
        submitButton.disabled = true;
      }
    });
  }

  loadCharts().catch((error) => {
    console.error("Dashboard chart loading failed", error);
  });
})();
