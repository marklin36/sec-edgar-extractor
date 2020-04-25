import sys
from edgar.stock import Stock
import time
import numpy as np
import pandas as pd
from collections import namedtuple
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys



def get_data_from_one_year(company_name, year):
    stock = Stock(company_name)

    data = []

    for i in range(1, 5):
        filing = stock.get_filing(period='quarterly', year=year, quarter=i)
        income_statement = filing.get_income_statements().reports[0].map
        balance_sheet = filing.get_balance_sheets().reports[0].map
        cash_flow = filing.get_cash_flows().reports[0].map

        one_quarter_data = income_statement
        one_quarter_data.update(balance_sheet)
        one_quarter_data.update(cash_flow)

        # trick to maintain the same structure of the data
        my_date_obj = namedtuple('MyStruct', 'value')
        date = my_date_obj(value=f"{year}_{i}")
        one_quarter_data["date"] = date

        data.append(one_quarter_data)

    return data


def get_available_fields_from_data(data):
    all_fields = set()

    # add the fields from the first quarter
    all_fields.update(data[0].keys())

    for quarter_data in data[1:]:
        all_fields.intersection_update(quarter_data.keys())

    return all_fields


def get_data(company_name, start_year, end_year):
    data = []
    for year in range(start_year, end_year + 1):
        one_year_data = get_data_from_one_year(company_name, year)
        # sleep for 0.5 second
        time.sleep(0.5)
        data = data + one_year_data

    return data


def data_to_pd(data):
    col_names = list(get_available_fields_from_data(data))
    col_names.sort()

    rows = []

    for q_data in data:
        row = [q_data[key].value for key in col_names]
        rows.append(row)

    df = pd.DataFrame(np.array(rows), columns=col_names)
    columns = list(df.columns)
    columns.remove("date")
    df[columns] = df[columns].apply(pd.to_numeric)

    df['date'] = df['date'].apply(lambda s: s[:4] + str(3 * int(s[5])) + "01")
    df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='ignore')

    return df


def plot(df, field_name, company_name=""):
    years = mdates.YearLocator()  # every year
    months = mdates.MonthLocator()  # every month
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot('date', field_name, data=df, label=field_name)

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_title(field_name[8:])

    fig.autofmt_xdate()
    plt.legend()

    plt.savefig(f"figures/{company_name}_{field_name}.png", dpi=300)
    plt.show()


def main():
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    company_name = sys.argv[3]
    field_name = "us-gaap_" + sys.argv[4]

    print("Downloading data")
    data = get_data("AAPL", start_year=start_year, end_year=end_year)
    data_keys = get_available_fields_from_data(data)
    df = data_to_pd(data)

    print("Download completed")

    while True:
        if field_name not in data_keys:
            for field_name in data_keys:
                print(field_name[8:])

            print(f"\n '{sys.argv[4]}' has not been found in the report.")
            field_name = "us-gaap_" + input("\n Enter the field from the list above: ")

        plot(df, field_name, "AAPL")
        print("\n The generated plot has been saved in figures directory.")

        field_name = input("\n Please enter new field or type 'exit' to close the program or load new data.")

        if field_name == 'exit':
            sys.exit()
        else:
            field_name = "us-gaap_" + field_name



if __name__ == "__main__":
    main()
