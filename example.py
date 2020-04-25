from edgar.stock import Stock
import json

stock = Stock('AAPL')

period = 'quarterly' # or 'annual', which is the default
year = 2018 # can use default of 0 to get the latest
quarter = 1 # 1, 2, 3, 4, or default value of 0 to get the latest
# using defaults to get the latest annual, can simplify to stock.get_filing()
filing = stock.get_filing(period, year, quarter)

# financial reports (contain data for multiple years)
income_statements = filing.get_income_statements()
balance_sheets = filing.get_balance_sheets()
cash_flows = filing.get_cash_flows()

print(income_statements.reports[0])
print("\n \n")
print(income_statements.reports[1])
print(len(income_statements.reports))

# income_statements_reports = income_statements.reports
# json_object = json.loads(str(income_statements_reports).replace("'", "\""))
# json_formatted_str = json.dumps(json_object, indent=2)
#print(json_formatted_str)

# print("\n \n ")
#
# print(balance_sheets.reports)
#
# print("\n \n")
#
# print(cash_flows.reports)