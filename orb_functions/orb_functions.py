def normalize(data):
  """
  Purpose:
    Normalize time series data in a Pandas Series by subtracting the minimum value for each day from all values for the day

  Args:
    data (required): a Pandas Series with timestamp index and one data column

  Returns:
    Pandas Series with normalized time series data
  """

  for idx, date in data.groupby(data.index.date):
    dateString = date.index[0].strftime('%Y-%m-%d')
    data[dateString] = data[dateString] - date.min()

  return data

def timeFinder(points, threshold = 0.9):
  """
  Purpose:
    Suggests start and end time for resource allocation based on time series data for a given date

  Args:
    points (required): a Pandas Series with timestamp index and one data column
    threshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day

  Returns:
    Dictionary with suggested start and end time for the given date
  """

  sums, lens, ratios = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

  for i in range(points.size):
    try:
      sums[points.index[i]] = points[i:].cumsum()
    except ValueError:
      return {"start": pd.NaT, "end": pd.NaT}

    lens[points.index[i]] = ([0] * i) + list(range(0, points.size - i))

  lens.index = lens.columns
  lens.replace(0, np.nan, inplace=True)

  ratios = sums / sums.iloc[-1][0]
  ratios[ratios < threshold] = np.nan
  ratios = (lens / sums.shape[0]) / ratios

  startTime = ratios.min().idxmin()
  endTime = ratios.min(axis=1).idxmin()

  start = pd.NaT if pd.isnull(startTime) else startTime.time()
  end = pd.NaT if pd.isnull(endTime) else endTime.time()

  return {"start": start, "end": end}

def dateAnalyzer(data, threshold = 0.9):
  """
  Purpose:
    Suggests start and end times for resource allocation based on time series data, indexed by date

  Args:
    data (required): a Pandas Series with timestamp index and one data column
    threshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by date
  """

  data = normalize(data)

  startDatetimes = {}
  endDatetimes = {}

  for idx, date in data.groupby(data.index.date):
    dateString = date.index[0].strftime('%Y-%m-%d')
    
    if dateString not in startDatetimes: 
      startDatetimes[dateString] = []
      endDatetimes[dateString] = []

    times = timeFinder(date, threshold)
    startDatetimes[dateString].append(times["start"])
    endDatetimes[dateString].append(times["end"])

  results = pd.concat([pd.DataFrame(startDatetimes), pd.DataFrame(endDatetimes)]).transpose()
  results.columns = ["start", "end"]

  return results

def dayAnalyzer(data, threshold = 0.9):
  """
  Purpose:
    Suggests start and end times for resource allocation based on pre-processed time series data, indexed by day of week

  Args:
    data (required): a Pandas Dataframe with datestring index and two data columns containing suggested start and end times ("start" and "end")
    threshold (0.9): percentile of suggested start and end times for each day to return as suggestion for that day of week

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by day of week
  """

  startTimes = {"Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": []}
  endTimes = {"Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": []}
  
  for date in data.index:
    day = dt.datetime.strptime(date, '%Y-%m-%d').strftime('%a')
    startTimes[day].append(data.at[date, "start"])
    endTimes[day].append(data.at[date, "end"])

  startTimes = pd.DataFrame.from_dict(startTimes, orient='index')
  endTimes = pd.DataFrame.from_dict(endTimes, orient='index')

  startPercentiles = startTimes.applymap(lambda x: pd.NaT if pd.isnull(x) else dt.datetime.combine(dt.datetime.min, x) - dt.datetime.min).quantile(1 - threshold, axis=1, numeric_only=False).apply(lambda x: (dt.datetime.min + x).time())
  endPercentiles = endTimes.applymap(lambda x: pd.NaT if pd.isnull(x) else dt.datetime.combine(dt.datetime.min, x) - dt.datetime.min).quantile(threshold, axis=1, numeric_only=False).apply(lambda x: (dt.datetime.min + x).time())

  results = pd.concat([startPercentiles, endPercentiles], axis=1)
  results.columns = ["start", "end"]

  return results

def analyze(data, level, groupby = "day", dailyThreshold = 0.9, overallThreshold = 0.9):
  """
  Purpose:
    Suggests start and end times for resource allocation based on time series data

  Args:
    data (required): a Pandas Series with timestamp index and one data column if level = "stream" or a Pandas Dataframe with datestring index and two data columns containing suggested start and end times ("start" and "end") if level = "stamp"
    level (required): "stream" if passing in a Pandas Series with timestamp index and one data column or "stamp" if passing in a Pandas Dataframe with datestring index and two data columns containing suggested start and end times ("start" and "end")
    groupby ("day"): "date" to return results aggregated by date or "day" to return results aggregated by day of week
    dailyThreshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day
    overallThreshold (0.9): percentile of suggested start and end times for each day to return as suggestion for that day of week if groupby = "day"

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by date or day of week depending on arguments
  """

  if level == "stream" and groupby == "day":
    return dayAnalyzer(dateAnalyzer(data, threshold = dailyThreshold), threshold = overallThreshold)

  elif level == "stream" and groupby == "date":
    return dateAnalyzer(data, threshold = dailyThreshold)

  elif level == "stamp" and groupby == "day":
    return dayAnalyzer(data, threshold = overallThreshold)

  elif level == "stamp" and groupby == "date":
    print('Date-level analysis cannot be performed with stamp data; please rerun with groupby = "day" argument.')
    return data

  else:
    print('Invalid arguments; please specify level = "stream" or "stamp" and groupby = "day" or "date" to proceed.')

def predict(data, days = 30, groupby = "date", dailyThreshold = 0.9, overallThreshold = 0.9):
  """
  Purpose:
    Suggests start and end times for resource allocation based on predictions extrapolated from provided time series data

  Args:
    data (required): a Pandas Series with timestamp index and one data column
    days (39): number of days of data to extrapolate
    groupby ("date"): "date" to return results aggregated by date or "day" to return results aggregated by day of week
    dailyThreshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day
    overallThreshold (0.9): percentile of suggested start and end times for each day to return as suggestion for that day of week if groupby = "day"

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by date or day of week depending on arguments
  """

  periods = days * 144
  data = normalize(data)

  m = Prophet(weekly_seasonality=True)
  m.add_country_holidays(country_name='US')
  m.fit(pd.DataFrame({'ds':data.index, 'y':data.values}))
  future = m.make_future_dataframe(periods = periods, freq = "5min")
  forecast = m.predict(future)

  predictedData = forecast[(periods * -1):]['yhat']
  predictedData.index = forecast[(periods * -1):]['ds']
  
  return analyze(predictedData, level = "stream", groupby = groupby, dailyThreshold = dailyThreshold, overallThreshold = overallThreshold)