import sys
import time
from string import ascii_uppercase

import requests
import xlwings as xw
from bs4 import BeautifulSoup

CBU_URL = "https://cbu.uz/en/"
SHEET_USD = "USD_2026"
SHEET_EUR = "EUR_2026"


def get_html(url, timeout=5):
    print(">>> Fetching exchange rates from CBU...")
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
        return resp.text
    except requests.ConnectionError as e:
        print(f">>> Loss of connectivity:\n{e}")
        time.sleep(10)
        sys.exit(1)
    except requests.Timeout as e:
        print(f">>> Request timed out:\n{e}")
        time.sleep(10)
        sys.exit(1)
    except requests.RequestException as e:
        print(f">>> Request failed:\n{e}")
        time.sleep(10)
        sys.exit(1)


def parse_rates_from_html(html):
    soup = BeautifulSoup(html, "lxml")

    calendar_div = soup.find("div", class_="input_calendar")
    if not calendar_div:
        raise RuntimeError("Calendar div not found: div.input_calendar")

    inp = calendar_div.find("input")
    if not inp or not inp.has_attr("value"):
        raise RuntimeError("Calendar input/value not found inside div.input_calendar")

    currency_date = inp["value"]
    print(f">>> FX Rates date: {currency_date}")

    rates = {"USD": 0.0, "EUR": 0.0}

    for item in soup.find_all("div", class_="exchange__item_value")[:5]:
        code = item.strong.text.strip() if item.strong else ""

        if code in rates:
            rate_str = item.text.split("=")[1].strip()
            rates[code] = float(rate_str)

    return rates, currency_date


def fetch_exchange_rates():
    html = get_html(CBU_URL, timeout=5)
    return parse_rates_from_html(html)


def get_excel_cell_from_date(date_str):
    day = int(date_str[:2]) + 2
    month_index = int(date_str[3:5])
    column = ascii_uppercase[month_index]
    return f"{column}{day}"


def write_to_excel(file_path, cell, rates):
    print(f">>> Writing to Excel at {file_path}...")
    wb = xw.Book(file_path)

    wb.sheets[SHEET_USD][cell].value = rates["USD"]
    wb.sheets[SHEET_EUR][cell].value = rates["EUR"]
    wb.save()

    print(">>> Excel file saved.")


def main():
    print(">>> Starting exchange rate fetcher...")

    file_path = r"\\peter\ZDrive\00016243\Desktop\FX_Rate\excel_files\FX_2026.xlsx"
    rates, date_str = fetch_exchange_rates()
    cell = get_excel_cell_from_date(date_str)

    print(f">>> Rates fetched: USD = {rates['USD']}, EUR = {rates['EUR']}")
    print(f">>> Writing rates to cell {cell}...")

    write_to_excel(file_path, cell, rates)
    print(">>> Program finished.")


if __name__ == "__main__":
    main()
