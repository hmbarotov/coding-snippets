import time
from string import ascii_uppercase

import requests
import xlwings as xw
from bs4 import BeautifulSoup


def fetch_exchange_rates():
    print(">>> Fetching exchange rates from CBU...")
    try:
        response = requests.get("https://cbu.uz/en/", timeout=5)
    except requests.ConnectionError as e:
        print(f">>> Loss of connectivity: \n{e}")
        time.sleep(10)
        exit()

    except requests.Timeout as e:
        print(f">>> Request timed out: \n{e}")
        time.sleep(10)
        exit()

    soup = BeautifulSoup(response.text, "lxml")

    currency_data = soup.find("div", class_="input_calendar").input["value"]
    print(f">>> FX Rates date: {currency_data}")

    rates = {"USD": 0, "EUR": 0, "RUB": 0}
    for item in soup.find_all("div", class_="exchange__item_value")[:5]:
        code = item.strong.text
        print(item.text)
        if code in rates:
            rates[code] = float(item.text.split("=")[1].strip())

    return rates, currency_data


def get_excel_cell_from_date(date_str):
    day = int(date_str[:2]) + 2
    month_index = int(date_str[3:5])
    column = ascii_uppercase(month_index)
    return f"{column}{day}"


def write_to_excel(file_path, cell, rates):
    print(f">>> Writing to Excel at {file_path}...")
    wb = xw.Book(file_path)
    wb.sheets["USD_2026"][cell].value = rates["USD"]
    wb.sheets["EUR_2026"][cell].value = rates["EUR"]
    wb.save()

    print(">>> Excel file saved.")


def main():
    print(">>> Starting exchange rate fetcher...")
    file_path = "C:\\Users\\User\\Desktop\\FX_Rates.xlsx"
    rates, date_str = fetch_exchange_rates()
    cell = get_excel_cell_from_date(date_str)

    print(f">>> Rates fetched: USD = {rates['USD']}, EUR = {rates['EUR']}")
    print(f">>> Writing rates to cell {cell}...")

    write_to_excel(file_path, cell, rates)
    print(">>> Program finished.")


if __name__ == "__main__":
    print(fetch_exchange_rates())
