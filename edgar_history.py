import sys
from bs4 import BeautifulSoup as bsoup
import requests
from edgar.stock import Stock


def get_data_from_one_year(company_name, year):
    stock = Stock(company_name)

    data = []

    for i in range(1, 5):
        filing = stock.get_filing(period='quarterly', year=year, quarter=i)
        income_statement = filing.get_income_statements().reports[0].map
        balance_sheet = filing.get_balance_sheets().reports[0].map
        cash_flow = filing.get_cash_flows().reports[0].map

        one_quarter_data = {k: v for k, v in enumerate(income_statement)}
        one_quarter_data.update(balance_sheet)
        one_quarter_data.update(cash_flow)

        data.append(one_quarter_data)

    return data


def get_available_fields_from_data(data):
    



def get_data(company_name, start_year, end_year):
    pass

def extract_data(raw_html, field_name):
    pass


def main():
    start_year = sys.argv[1]
    end_year = sys.argv[2]
    company_name = sys.argv[3]
    field_name = sys.argv[4]

    print(start_year)
    print(end_year)
    print(company_name)
    print(field_name)

    apple_data = get_data_from_one_year("AAPL", year=2018)

    print(apple_data)


if __name__ == "__main__":
    main()