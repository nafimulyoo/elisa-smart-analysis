# app/routers/analysis.py
from fastapi import APIRouter, Depends, HTTPException, status
import asyncio
from typing import Annotated
from datetime import datetime, timedelta
import json
from utils.elisa_api_cache import async_fetch_compare, async_fetch_heatmap, async_fetch_monthly, async_fetch_daily, async_fetch_now, async_fetch_fakultas, async_fetch_gedung, async_fetch_lantai
from mas_llm.actions.analyze_page import now_analysis, heatmap_analysis, compare_faculty_analysis, daily_analysis, monthly_analysis
# from pyinstrument import Profiler
from functools import wraps
import time
import pandas as pd
from prophet import Prophet

# def profile_endpoint(async_mode=True):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(*args, **kwargs):
#             # Initialize profiler (enable async mode)
#             profiler = Profiler(async_mode=async_mode)
#             profiler.start()

#             # Execute the endpoint
#             start_time = time.time()
#             result = await func(*args, **kwargs)
#             end_time = time.time()

#             # Stop profiling and print results
#             profiler.stop()
#             print(f"\n=== Profiling results for {func.__name__} ===")
#             print(f"Total time: {end_time - start_time:.2f}s")
#             print(profiler.output_text(unicode=True, color=True))
#             profiler.write_html("profile_report.html")

#             return result
#         return wrapper
#     return decorator

data_router = APIRouter(prefix="/api", tags=["data"])

@data_router.get("/now")
# @profile_endpoint()
async def get_now_analysis(faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_now(faculty, building, floor)

@data_router.get("/daily")
# @profile_endpoint()
async def get_daily_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_daily(date, faculty, building, floor)


async def fetch_concurrent_daily_dates(dates: list, faculty: str = "", building: str = "", floor: str = "") -> list:
    """
    Concurrently fetch daily data for multiple dates
    """
    tasks = [async_fetch_daily(date.strftime('%Y-%m-%d'), faculty, building, floor) for date in dates]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def fetch_concurrent_monthly_months(year_months: list, faculty: str = "", building: str = "", floor: str = "") -> list:
    """
    Concurrently fetch monthly data for multiple year-month combinations
    """
    tasks = [async_fetch_monthly(ym, faculty, building, floor) for ym in year_months]
    return await asyncio.gather(*tasks, return_exceptions=True)


@data_router.get("/daily/from-to")
async def get_daily_analysis_from_to(start_date: str, end_date: str, faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch daily data for a range of dates.

    Args:
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        faculty: Faculty code filter
        building: Building code filter
        floor: Floor code filter

    Returns:
        A list of daily data for the specified date range.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Generate all dates we need to fetch
    dates_to_fetch = []
    current_date = start_date

    while current_date <= end_date:
        dates_to_fetch.append(current_date)
        current_date += timedelta(days=1)

    # Fetch data concurrently
    all_daily_data = await fetch_concurrent_daily_dates(dates_to_fetch, faculty, building, floor)
    
    # Process responses
    processed_data = {}
    for date, daily_data in zip(dates_to_fetch, all_daily_data):
        if isinstance(daily_data, Exception):
            print(f"Failed to fetch data for {date}: {str(daily_data)}")
            continue
            
        try:
            processed_data[date.strftime('%Y-%m-%d')] = daily_data
        except KeyError as e:
            print(f"Malformed data for {date}: {str(e)}")
    
    # return api response as json
    return processed_data

@data_router.get("/monthly/from-to")
async def get_monthly_analysis_from_to(start_date: str, end_date: str, faculty: str = "", building: str = "", floor: str = ""):
    """
    Fetch monthly data for a range of dates.

    Args:
        start_date: Start date in YYYY-MM format
        end_date: End date in YYYY-MM format
        faculty: Faculty code filter
        building: Building code filter
        floor: Floor code filter

    Returns:
        A list of monthly data for the specified date range.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date, '%Y-%m').date()
    end_date = datetime.strptime(end_date, '%Y-%m').date()

    # Generate all year-month combinations we need to fetch
    year_months_to_fetch = []
    current_date = start_date

    while current_date <= end_date:
        year_months_to_fetch.append(current_date.strftime('%Y-%m'))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year+1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month+1)

    # Fetch data concurrently
    all_monthly_data = await fetch_concurrent_monthly_months(year_months_to_fetch, faculty, building, floor)
    
    # Process responses
    processed_data = {}
    for ym, monthly_data in zip(year_months_to_fetch, all_monthly_data):
        if isinstance(monthly_data, Exception):
            print(f"Failed to fetch data for {ym}: {str(monthly_data)}")
            continue
            
        try:
            processed_data[ym] = monthly_data

        except KeyError as e:
            print(f"Malformed data for {ym}: {str(e)}")
    
    return processed_data



@data_router.get("/daily/forecast")
async def forecast_daily_energy(faculty: str = "", building: str = "", floor: str = "", days_to_forecast: int = 7 ):
    """
    Forecast energy usage using daily data with hourly samples (async version).

    Args:
        faculty: Faculty code filter
        building: Building code filter
        floor: Floor code filter
        days_to_forecast: Number of days to forecast ahead

    Returns:
        A table containing:
        - ds: Datestamp (datetime)
        - yhat: Forecast value (energy usage)
        - yhat_lower: Lower bound of the prediction interval
        - yhat_upper: Upper bound of the prediction interval
    """
    # 1. Fetch historical data (last 60 days) concurrently

    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7*5)
    current_date = start_date
    
    # Generate all dates we need to fetch

    dates_to_fetch = []

    # start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)
    while current_date <= end_date:
        dates_to_fetch.append(current_date)
        current_date = current_date + timedelta(days=1)

       
    # Fetch data concurrently
    all_daily_data = await fetch_concurrent_daily_dates(dates_to_fetch, faculty, building, floor)
    # Process responses
    all_hourly_data = []
    for date, daily_data in zip(dates_to_fetch, all_daily_data):
        if isinstance(daily_data, Exception):
            print(f"Failed to fetch data for {date}: {str(daily_data)}")
            continue
            
        try:
            for hour_data in daily_data['hourly_data']:
                hour = int(hour_data['hour'].split(':')[0])
                timestamp = datetime.combine(date, datetime.min.time()) + timedelta(hours=hour)
                all_hourly_data.append({
                    'ds': timestamp,
                    'y': hour_data['energy']
                })
        except KeyError as e:
            print(f"Malformed data for {date}: {str(e)}")
    
    if not all_hourly_data:
        raise ValueError("No historical data available for forecasting")
    
    # 2. Prepare DataFrame for Prophet
    df = pd.DataFrame(all_hourly_data)
    
    # 3. Create and fit model
    model = Prophet(
        daily_seasonality=True,
        weekly_seasonality=True,
        yearly_seasonality=False,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10
    )
    
    # Add holidays (same as before)
    holidays = pd.DataFrame({
        'holiday': 'academic_break',
        'ds': pd.to_datetime([
            '2023-12-23', '2023-12-24', '2023-12-25', '2023-12-31',
            '2024-01-01',
            '2024-03-11', '2024-03-12', '2024-03-13',
            '2024-05-01',
            '2024-05-16', '2024-05-17', '2024-05-18',
        ]),
        'lower_window': -1,
        'upper_window': 1
    })
    
    model.add_country_holidays(country_name='ID')
    model.add_regressor('is_weekend')
    
    # Add weekend flag
    df['is_weekend'] = df['ds'].dt.dayofweek >= 5
    
    model.fit(df)
    
    # 4. Make future dataframe
    future = model.make_future_dataframe(periods=24*days_to_forecast, freq='H', include_history=False)
    future['is_weekend'] = future['ds'].dt.dayofweek >= 5
    
    # 5. Make forecast
    forecast = model.predict(future)
    
    # 6. Plot results
    # fig = model.plot(forecast)
    # plt.title(f'Hourly Energy Forecast for {faculty} {building} {floor}')
    # plt.xlabel('Date')
    # plt.ylabel('Energy Usage (kWh)')
    # return forecast, fig

    history = df[['ds', 'y']]
    forecast_important = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    # rename column for clarity

    forecast_important.rename(
        columns={
            'ds': 'datetime',
            'yhat': 'predicted_energy_usage',
            'yhat_lower': 'predicted_energy_lower',
            'yhat_upper': 'predicted_energy_upper',
        },
        inplace=True,
    )

    history.rename(
        columns={
            'ds': 'datetime',
            'y': 'energy_usage'
        },
        inplace=True,
    )

    history_json = history.to_json(orient="records")
    forecast_json = forecast_important.to_json(orient="records")

    return {"history": history_json, "forecast": forecast_json}


@data_router.get("/monthly/forecast")
async def forecast_monthly_energy(faculty: str = "", building: str = "", floor: str = "", days_to_forecast: int = 30):
    """
    Forecast energy usage using monthly data with daily samples (async version).
    
    Args:
        faculty: Faculty code filter
        building: Building code filter
        floor: Floor code filter
        months_to_forecast: Number of months to forecast ahead
        
    Returns:
        A tuple containing:
        - forecast dataframe
        - main plot figure
        - components plot figure
    """
    # 1. Generate all year-month combinations we need to fetch
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=36*30)  # Approx 24 months
    
    year_months_to_fetch = []
    current_date = start_date

    while current_date <= end_date:
        year_months_to_fetch.append(current_date.strftime('%Y-%m'))
        if current_date.month == 12:
            current_date = current_date.replace(year=current_date.year+1, month=1)
        else:
            current_date = current_date.replace(month=current_date.month+1)
    
    # Fetch data concurrently
    all_monthly_data = await fetch_concurrent_monthly_months(year_months_to_fetch, faculty, building, floor)
    # Process responses
    all_daily_data = []
    for ym, monthly_data in zip(year_months_to_fetch, all_monthly_data):
        if isinstance(monthly_data, Exception):
            print(f"Failed to fetch data for {ym}: {str(monthly_data)}")
            continue
            
        try:
            for daily_data in monthly_data['daily_data']:
                timestamp_str = daily_data['timestamp'].split()[0]
                timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d')
                all_daily_data.append({
                    'ds': timestamp,
                    'y': daily_data['energy']
                })
        except KeyError as e:
            print(f"Malformed data for {ym}: {str(e)}")
    
    if not all_daily_data:
        raise ValueError("No historical data available for forecasting")
    
    # 2. Prepare DataFrame for Prophet
    df = pd.DataFrame(all_daily_data)
    
    # 3. Create and fit model
    model = Prophet(
        daily_seasonality=False,
        weekly_seasonality=True,
        yearly_seasonality=True,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10
    )
    
    # Add holidays (same as before)
    holidays = pd.DataFrame({
        'holiday': 'academic_break',
        'ds': pd.to_datetime([
            '2022-07-01', '2022-07-02', '2022-07-03', '2022-07-04',
            '2023-07-01', '2023-07-02', '2023-07-03', '2023-07-04',
            '2022-12-23', '2022-12-24', '2022-12-25', '2022-12-31',
            '2023-12-23', '2023-12-24', '2023-12-25', '2023-12-31',
            '2022-05-15', '2022-05-16', '2022-05-17',
            '2023-05-15', '2023-05-16', '2023-05-17',
        ]),
        'lower_window': -2,
        'upper_window': 2
    })
    
    model.add_country_holidays(country_name='ID')
    model.add_regressor('is_weekend')
    
    # Add weekend flag
    df['is_weekend'] = df['ds'].dt.dayofweek >= 5
    
    model.fit(df)
    
    # 4. Make future dataframe
    future = model.make_future_dataframe(periods=days_to_forecast, freq='D', include_history=False)
    future['is_weekend'] = future['ds'].dt.dayofweek >= 5
    
    # 5. Make forecast
    forecast = model.predict(future)
    
    # 6. Plot results
    # fig1 = model.plot(forecast)
    # plt.title(f'Daily Energy Forecast for {faculty} {building} {floor}')
    # plt.xlabel('Date')
    # plt.ylabel('Energy Usage (kWh)')
    
    # fig2 = model.plot_components(forecast)
    # return forecast, fig1, fig2

    history = df[['ds', 'y']]
    forecast_important = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
    # rename column for clarity

    forecast_important.rename(
        columns={
            'ds': 'datetime',
            'yhat': 'predicted_energy_usage',
            'yhat_lower': 'predicted_energy_lower',
            'yhat_upper': 'predicted_energy_upper',
        },
        inplace=True,
    )

    history.rename(
        columns={
            'ds': 'datetime',
            'y': 'energy_usage'
        },
        inplace=True,
    )

    history_json = history.to_json(orient="records")
    forecast_json = forecast_important.to_json(orient="records")

    return {"history": history_json, "forecast": forecast_json}


@data_router.get("/monthly")
# @profile_endpoint()
async def get_monthly_analysis(date: str, faculty: str = "", building: str = "", floor: str = ""):
    return await async_fetch_monthly(date, faculty, building, floor)


@data_router.get("/heatmap")
# @profile_endpoint()
async def get_heatmap_analysis(start: str, end: str, faculty: str = None, building: str = None, floor: str = None):
    return await async_fetch_heatmap(start, end, faculty, building, floor)


@data_router.get("/compare")
# @profile_endpoint()
async def get_compare(date: str):
    return await async_fetch_compare(date)

@data_router.get("/get-fakultas")
# @profile_endpoint()
async def get_faculty():
    return await async_fetch_fakultas()

@data_router.get("/get-gedung")
# @profile_endpoint()
async def get_building(fakultas: str):
    return await async_fetch_gedung(fakultas)

@data_router.get("/get-lantai")
# @profile_endpoint()
async def get_floor(fakultas: str, gedung: str):
    return await async_fetch_lantai(fakultas, gedung)



