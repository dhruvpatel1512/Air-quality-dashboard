import analysis
print('analysis imported OK')
# Quick sanity-check: load a small portion if file exists
try:
    df = analysis.load_data('data/AirQualityUCI.csv')
    print('loaded rows:', None if df is None else len(df))
    dfc = analysis.clean_data(df)
    print('cleaned rows:', None if dfc is None else len(dfc))
except Exception as e:
    print('error during load/clean:', e)
