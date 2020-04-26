from downloader import Company

company = Company("Oracle Corp", "0001341439")
out = company.get_filings_url(filing_type='10-Q')
print(out)