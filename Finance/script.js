// Fetch Stock Data using Alpha Vantage API
function fetchStockData() {
  const symbol = document.getElementById('stock-symbol').value.toUpperCase();
  if (!symbol) {
    alert('Please enter a stock symbol.');
    return;
  }

  const apiKey = ' WWJF4M4ZUZWBNRTC'; // Replace with your Alpha Vantage API key
  const url = `https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=${symbol}&interval=5min&apikey=${apiKey}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data['Error Message']) {
        document.getElementById('stock-data').innerText = 'Invalid stock symbol. Please try again.';
        return;
      }

      const timeSeries = data['Time Series (5min)'];
      const latestTime = Object.keys(timeSeries)[0];
      const latestData = timeSeries[latestTime];

      const open = parseFloat(latestData['1. open']).toFixed(2);
      const high = parseFloat(latestData['2. high']).toFixed(2);
      const low = parseFloat(latestData['3. low']).toFixed(2);
      const close = parseFloat(latestData['4. close']).toFixed(2);
      const volume = parseInt(latestData['5. volume']).toLocaleString();

      document.getElementById('stock-data').innerHTML = `
        <p><strong>Symbol:</strong> ${symbol}</p>
        <p><strong>Open:</strong> $${open}</p>
        <p><strong>High:</strong> $${high}</p>
        <p><strong>Low:</strong> $${low}</p>
        <p><strong>Close:</strong> $${close}</p>
        <p><strong>Volume:</strong> ${volume}</p>
      `;
    })
    .catch(error => {
      console.error('Error fetching stock data:', error);
      document.getElementById('stock-data').innerText = 'Error fetching stock data. Please try again later.';
    });
}

// Initialize the dashboard
document.addEventListener('DOMContentLoaded', () => {
  fetchPrices();
  fetchNews();
});

