# Extracting data from SEC’s EDGAR database

## Getting started

Use the following commands to run `edgar_history.py`:

* `git clone https://github.com/marklin36/problem_1.git`
* `source venv/bin/activate`
* and then for example: `python edgar_history.py 2016 2019 AAPL GrossProfit`

So there are four command lines arguments for the `edgar_history.py` scirpt:

* start_year
* end_year
* stock symbol (for example, AAPL, GOOG)
* field_name (for example, GrossIncome); if requested field name is not found in
the report, the user will be prompted to choose one from the list.

The generated plot will be saved in `figures` directory.

## Credits

The heavy lifting of parsing 10-Q reports is done by this [library](https://github.com/farhadab/sec-edgar-financials) 
and the code in directory `edgar` is taken from the source code of this library.

## Assessment

The parsing mechanism is very fragile, and it works only for some companies.
Here are a few tested examples:
* `python edgar_history.py 2015 2019 AAPL GrossProfit`
* `python edgar_history.py 2017 2019 IBM GrossProfit`
* `python edgar_history.py 2016 2019 GOOG GrossProfit`

## Things to improve

The script is not very robust because exception handling is poor. 