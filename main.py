from bs4 import BeautifulSoup
import requests
import numpy as np
import csv
from datetime import datetime

def get_prices_by_link(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    search_results = soup.find("ul", {"class": "srp-results"}).find_all("li", {"class": "s-item"})

    item_prices = []
    for result in search_results:
        price_tag = result.find("span", {"class": "s-item__price"})
        if not price_tag:
            continue
        price_text = price_tag.text.strip()
        if "to" in price_text:
            continue
        try:
            price = float(price_text.replace("US $", "").replace("$", "").replace(",", ""))
            item_prices.append(price)
        except ValueError:
            continue
    return item_prices

def filter_prices(prices):
    data = np.array(prices)

    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    filtered = data[(data >= lower) & (data <= upper)]

    sorted_data = np.sort(filtered)
    n = len(sorted_data)
    trim_low = int(n * 0.10)
    trim_high = int(n * 0.90)
    final = sorted_data[trim_low:trim_high]

    return final

def save_to_file(product_name, prices):
    avg_price = np.around(np.mean(prices), 2)
    row = [datetime.today().strftime("%B-%d-%Y"), product_name, avg_price]
    with open("prices.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def main():
    try:
        with open("urls.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("'urls.txt' not found.")
        return

    for line in lines:
        try:
            product_name, url = line.split(",", 1)
            prices = get_prices_by_link(url)
            if not prices:
                print(f"No prices found for {product_name}")
                continue
            filtered = filter_prices(prices)
            save_to_file(product_name, filtered)
            print(f"{product_name}: {len(filtered)} prices | Avg: ${np.mean(filtered):.2f}")
        except Exception as e:
            print(f"Error processing line: {line}\n   → {e}")

if __name__ == "__main__":
    main()