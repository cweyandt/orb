import datetime as dt
import numpy as np
import pandas as pd
from prophet import Prophet


def normalize(data):
    """
  Purpose:
    Normalize time series data in a Pandas Series by subtracting the minimum value for each day from all values for the day

  Args:
    data (required): a Pandas Series with timestamp index and one data column

  Returns:
    Pandas Series with normalized time series data
  """

    print("in normalize...")

    for idx, date in data.groupby(data.index.date):
        dateString = date.index[0].strftime('%Y-%m-%d')
        data[dateString] = data[dateString] - date.min()

    return data


def timeFinder(points, threshold=0.9):
    """
  Purpose:
    Suggests start and end time for resource allocation based on time series data for a given date

  Args:
    points (required): a Pandas Series with timestamp index and one data column
    threshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day

  Returns:
    Dictionary with suggested start and end time for the given date
  """

    print("in timeFinder...")

    sums, lens, ratios = pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    for i in range(points.size):
        try:
            sums[points.index[i]] = points[i:].cumsum()
        except ValueError:
            print(str(ValueError) + "in timeFinder")
            return {"start": pd.NaT, "end": pd.NaT}

        lens[points.index[i]] = ([0] * i) + list(range(0, points.size - i))

    lens.index = lens.columns
    lens.replace(0, np.nan, inplace=True)

    ratios = sums / sums.iloc[-1][0]
    ratios[ratios < threshold] = np.nan
    ratios = (lens / sums.shape[0]) / ratios

    startTime = ratios.min().idxmin()
    endTime = ratios.min(axis=1).idxmin()

    # start = pd.NaT if pd.isnull(startTime) else startTime.time()
    # end = pd.NaT if pd.isnull(endTime) else endTime.time()

    return {"start": startTime, "end": endTime}


def dateAnalyzer(data, threshold=0.9):
    """
  Purpose:
    Suggests start and end times for resource allocation based on time series data, indexed by date

  Args:
    data (required): a Pandas Series with timestamp index and one data column
    threshold (0.9): minimum percentage of timeseries area under curve (AUC) to be covered by the suggested start and end times for each day

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by date
  """
    print( "in dateAnalyzer...")
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


def dayAnalyzer(data, threshold=0.9):
    """
  Purpose:
    Suggests start and end times for resource allocation based on pre-processed time series data, indexed by day of week

  Args:
    data (required): a Pandas Dataframe with datestring index and two data columns containing suggested start and end times ("start" and "end")
    threshold (0.9): percentile of suggested start and end times for each day to return as suggestion for that day of week

  Returns:
    Pandas Dataframe of suggested start and end times, indexed by day of week
  """

    print("in dayAnalyzer...")

    startTimes = {"Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": []}
    endTimes = {"Sun": [], "Mon": [], "Tue": [], "Wed": [], "Thu": [], "Fri": [], "Sat": []}

    for date in data.index:
        day = dt.datetime.strptime(date, '%Y-%m-%d').strftime('%a')
        startTimes[day].append(data.at[date, "start"])
        endTimes[day].append(data.at[date, "end"])

    startTimes = pd.DataFrame.from_dict(startTimes, orient='index')
    endTimes = pd.DataFrame.from_dict(endTimes, orient='index')

    startPercentiles = startTimes.applymap(
        lambda x: pd.NaT if pd.isnull(x) else dt.datetime.combine(dt.datetime.min, x) - dt.datetime.min).quantile(
        1 - threshold, axis=1, numeric_only=False).apply(lambda x: (dt.datetime.min + x).time())
    endPercentiles = endTimes.applymap(
        lambda x: pd.NaT if pd.isnull(x) else dt.datetime.combine(dt.datetime.min, x) - dt.datetime.min).quantile(
        threshold, axis=1, numeric_only=False).apply(lambda x: (dt.datetime.min + x).time())

    results = pd.concat([startPercentiles, endPercentiles], axis=1)
    results.columns = ["start", "end"]

    return results


def analyze(data, level, groupby="day", dailyThreshold=0.9, overallThreshold=0.9):
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
    print ("in analyze...")
    if level == "stream" and groupby == "day":
        return dayAnalyzer(dateAnalyzer(data, threshold=dailyThreshold), threshold=overallThreshold)

    elif level == "stream" and groupby == "date":
        return dateAnalyzer(data, threshold=dailyThreshold)

    elif level == "stamp" and groupby == "day":
        return dayAnalyzer(data, threshold=overallThreshold)

    elif level == "stamp" and groupby == "date":
        print('Date-level analysis cannot be performed with stamp data; please rerun with groupby = "day" argument.')
        return data

    else:
        print('Invalid arguments; please specify level = "stream" or "stamp" and groupby = "day" or "date" to proceed.')


def predict(data, days=30, groupby="date", dailyThreshold=0.9, overallThreshold=0.9):
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

    periods = days * 288
    data = normalize(data)

    m = Prophet(weekly_seasonality=True)
    m.add_country_holidays(country_name='US')
    m.fit(pd.DataFrame({'ds': data.index, 'y': data.values}))
    future = m.make_future_dataframe(periods=periods, freq="5min")
    forecast = m.predict(future)

    predictedData = forecast[(periods * -1):]['yhat']
    predictedData.index = forecast[(periods * -1):]['ds']

    return analyze(predictedData, level="stream", groupby=groupby, dailyThreshold=dailyThreshold,
                   overallThreshold=overallThreshold)


def addtoDict(dictName, date, val):
  try: 
    dictName[date] += val
  except:
    dictName[date] = val


def errorCalc(groundTruth, model):
  '''
  onVacant[date] = minutes when actually occupied but predicted vacant
    This happens when the GT_True time happens before the model_True time OR when the GT_False time happens after the model_False time
  offOccupied[date] = minutes when actually vacant but predicted occupied
    This happens when the GT_True time happens after the model_True time OR when the GT_False time happens before the model_False time
  For zero difference, don't add to either dictionary
  '''
  global onVacant
  onVacant = dict()
  global offOccupied 
  offOccupied = dict()

  #Find first entry of each that is True / Create first naive version where we assume indices are matched up
  length = min(len(model_for_api), len(groundTruth))
  for i in range(0,length):
    date = groundTruth.index[i].date()
    diff_days = (groundTruth.index.tz_localize(None)[i] - model_for_api.index[i]).days
    diff_secs = (groundTruth.index.tz_localize(None)[i] - model_for_api.index[i]).seconds

    if i % 2 == 0: #Even indices should be True
      if diff_days < 0:
        addtoDict(onVacant, date, (model_for_api.index[i] - groundTruth.index.tz_localize(None)[i]).seconds/60)
        addtoDict(offOccupied, date, 0)
      elif diff_secs > 0:
        addtoDict(offOccupied, date, diff_secs/60)
        addtoDict(onVacant, date, 0)
      else: 
        addtoDict(onVacant, date, 0)
        addtoDict(offOccupied, date, 0)

    elif i % 2 == 1:
      if diff_days < 0:
        addtoDict(offOccupied, date, (model_for_api.index[i] - groundTruth.index.tz_localize(None)[i]).seconds/60)
        addtoDict(onVacant, date, 0)
      elif diff_secs > 0:
        addtoDict(onVacant, date, diff_secs/60)
        addtoDict(offOccupied, date, 0)
      else: 
        addtoDict(onVacant, date, 0)
        addtoDict(offOccupied, date, 0)

    #return onVacant, offOccupied
