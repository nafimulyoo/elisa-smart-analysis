import pandas as pd
from prophet import Prophet
from metagpt.tools.tool_registry import register_tool

@register_tool()
def prophet_forecast(dataframe: pd.DataFrame, timestamp_col: str, y_cols: list, periods: int = 30) -> pd.DataFrame:
    """
    Perform time series forecasting using Prophet for multiple y columns independently.

    Args:
        dataframe (pd.DataFrame): The input DataFrame containing the timestamp and y columns.
        timestamp_col (str): The name of the timestamp column.
        y_cols (list): A list of column names to predict.
        periods (int): The number of future periods to forecast. Default is 30.

    Returns:
        pd.DataFrame: A DataFrame containing the forecasted values for all y columns.
    """
    results = []

    for y_col in y_cols:
        # Prepare data for Prophet
        df = dataframe[[timestamp_col, y_col]].rename(columns={timestamp_col: 'ds', y_col: 'y'})

        # Initialize and fit Prophet model
        model = Prophet()
        model.fit(df)

        # Make future dataframe and predict
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)

        # Add y_col name to the forecast columns
        forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast.columns = ['ds', f'{y_col}_yhat', f'{y_col}_yhat_lower', f'{y_col}_yhat_upper']

        # Append to results
        results.append(forecast)

    # Merge all forecasts on the 'ds' column
    final_forecast = results[0]
    for result in results[1:]:
        final_forecast = final_forecast.merge(result, on='ds', how='outer')

    return final_forecast