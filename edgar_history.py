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

    one_year_income_statements = []
    one_year_balance_sheets = []
    one_year_cash_flows = []

    for i in range(1, 5):
        filing = stock.get_filing(period='quarterly', year=year, quarter=i)

        income_statements = filing.get_income_statements().reports
        balance_sheets = filing.get_balance_sheets().reports
        cash_flows = filing.get_cash_flows().reports

        income_statement = None
        for report in income_statements:
            # choose the report from the correct year, covering only 3 months (not cumulative)
            report_year = int(report.date.year)
            report_period = int(report.months)

            # this condition can be relaxed later
            if report_year == year and report_period == 3:
                income_statement = report.map
                income_statement['exact_date'] = report.date
                income_statement['period'] = 3
                break
        one_year_income_statements.append(income_statement)

        balance_sheet = None
        for report in balance_sheets:
            report_year = int(report.date.year)
            if report_year == year:
                balance_sheet = report.map
                balance_sheet['exact_date'] = report.date
                balance_sheet['period'] = None
                break
        one_year_balance_sheets.append(balance_sheet)

        cash_flow = None
        for report in cash_flows:
            report_year = int(report.date.year)
            report_period = int(report.months)
            if report_year == year:
                cash_flow = report.map
                cash_flow['exact_date'] = report.date
                cash_flow['period'] = report_period
                break
        one_year_cash_flows.append(cash_flow)

    return {
        "income_statements": one_year_income_statements,
        "balance_sheets": one_year_balance_sheets,
        "cash_flows": one_year_cash_flows
    }

def get_data(company_name, start_year, end_year):
    data = []
    for year in range(start_year, end_year + 1):
        one_year_data = get_data_from_one_year(company_name, year)
        # sleep for 0.5 second
        time.sleep(0.5)
        data.append(one_year_data)

    income_statements = []
    for one_year_data in data:
        income_statements = income_statements + one_year_data['income_statements']

    balance_sheets = []
    for one_year_data in data:
        balance_sheets = balance_sheets + one_year_data['balance_sheets']

    cash_flows = []
    for one_year_data in data:
        cash_flows = cash_flows + one_year_data['cash_flows']

    return {
        "income_statements": income_statements,
        "one_year_balance_sheets": balance_sheets,
        "one_year_cash_flows": cash_flows
    }

def data_to_df(data):
    """
    A list of
    :param data: A list of dictionaries
    :return: pandas data frame
    """
    # find all the keys
    all_keys = set()
    for report in data:
        if report:
            all_keys.update(report.keys())

    all_keys = list(all_keys)
    all_keys.remove('exact_date')
    all_keys.remove('period')
    all_keys.sort()
    columns = ['exact_date', 'period'] + all_keys

    rows = []
    for q_data in data:
        if q_data:
            row = [q_data['exact_date'], q_data['period']]
            for key in all_keys:
                if key in q_data.keys():
                    row.append(q_data[key].value)
                else:
                    row.append(None)

            rows.append(row)

    df = pd.DataFrame(np.array(rows), columns=columns)
    df[all_keys] = df[all_keys].apply(pd.to_numeric)
    df.drop_duplicates(inplace=True)
    df['exact_date'] = pd.to_datetime(df['exact_date'], format='%Y%m%d', errors='raise')

    return df


def plot(df, field_name, company_name=""):
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_fmt = mdates.DateFormatter('%Y')

    fig, ax = plt.subplots(figsize=(15, 8))
    ax.plot('exact_date', field_name, data=df, label=field_name)

    # format the ticks
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_fmt)
    ax.xaxis.set_minor_locator(months)

    ax.set_title(f"Plot of {field_name[8:]} for {company_name}")
    fig.autofmt_xdate()
    plt.legend()

    plt.savefig(f"figures/{company_name}_{field_name}.png", dpi=300)
    plt.show()

###########################################################################
###########################################################################


def main():
    start_year = int(sys.argv[1])
    end_year = int(sys.argv[2])
    company_name = sys.argv[3]
    field_name = "us-gaap_" + sys.argv[4]

    print("Downloading data")
    data = get_data(company_name, start_year=start_year, end_year=end_year)

    df = data_to_df(data['income_statements'])

    plot(df, "us-gaap_GrossProfit")

    print(df.head(100))
    # data_keys = get_available_fields_from_data(data)
    # df = data_to_pd(data)
    # print("Download completed")
    #
    # while True:
    #     if field_name not in data_keys:
    #         for field_name in sorted(list(data_keys)):
    #             print(field_name[8:])
    #
    #         print(f"\n '{sys.argv[4]}' has not been found in the report.")
    #         field_name = "us-gaap_" + input("\n Enter the field from the list above: \n")
    #
    #         continue
    #
    #     plot(df, field_name, company_name)
    #
    #     print("\n The generated plot has been saved in figures directory.")
    #
    #     field_name = input("\n Please enter new field or type 'exit' to close the program (and load new data) \n")
    #
    #     if field_name == 'exit':
    #         sys.exit()
    #     else:
    #         field_name = "us-gaap_" + field_name



if __name__ == "__main__":
    main()
