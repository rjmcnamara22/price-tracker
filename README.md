# Price Tracker

A simple Python tool that scrapes eBay search results to track the average price of specific trading cards or collectibles over time.

It extracts prices from search result pages, filters out statistical outliers, and logs the daily average price of each product to a CSV file.

---

## Features

- Scrapes eBay search results for item prices
- Removes price outliers using IQR + trimmed range
- Tracks multiple products via `urls.txt`
- Logs daily average prices to a `CSV` file
  
---

## Requirements

- Python 3.x  
- `requests`  
- `beautifulsoup4`  
- `numpy`  

Install with:
```bash
pip install requests beautifulsoup4 numpy
