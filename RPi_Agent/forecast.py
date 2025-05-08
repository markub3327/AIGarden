from influxdb_client_3 import InfluxDBClient3, Point
from prophet import Prophet
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime, timedelta, timezone


# Step 1: Read data
# InfluxDB credentials
INFLUXDB_URL = "http://localhost:8181"
INFLUXDB_TOKEN = "apiv3_Xt_e04hbvSMpZYofueUcbM_Z7GnfI4K5E32PtGw9k9gOIuonpOhDMBHHOzi9SrvyH1Kbfp-dAjiUWhoFi2QHow"
INFLUXDB_ORG = "home"
INFLUXDB_DB = "ai_garden"

client = InfluxDBClient3(host=INFLUXDB_URL,
                         database=INFLUXDB_DB,
                         token=INFLUXDB_TOKEN,)


def query_in_chunks(feature, chunk_days=1, total_days=30):
    # Initialize empty DataFrame to store all results
    all_data = pd.DataFrame()

    # Calculate end time (now) and start time
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(days=total_days)

    # Query data in chunks
    current_end = end_time
    while current_end > start_time:
        current_start = max(current_end - timedelta(days=chunk_days), start_time)

        chunk_df = client.query(
            f"""
                SELECT time, {feature}
                FROM "home"
                WHERE time >= '{current_start.isoformat()}' 
                AND time < '{current_end.isoformat()}'
                AND {feature} is NOT NULL
                ORDER BY time ASC;
            """
        ).to_pandas()

        if len(chunk_df) == 0:
            print("No more data to fetch.")
            break

        # Append chunk to main DataFrame
        all_data = pd.concat([chunk_df, all_data], ignore_index=True)

        # Move window
        current_end = current_start

        print(f"Fetched chunk from {current_start} to {current_end}, got {len(chunk_df)} records")

    return all_data


for feature in ['temperature', 'pressure', 'humidity', 'battery_voltage', 'solar_voltage', 'soil_kiwi', 'soil_pelargonium', 'water_level']:
    df = query_in_chunks(feature)
    print(df)

    # Ensure column names match Prophet expectations
    df.rename(columns={'time': 'ds', f'{feature}': 'y'}, inplace=True)

    # Step 2: Fit the model
    model = Prophet(daily_seasonality=True)  # yearly_seasonality=True
    model.fit(df)

    # Step 3: Create future dataframe (forecast 1 month ahead hourly)
    future = model.make_future_dataframe(periods=(5 * 24), freq='h')  # 5 days * 24 hours
    forecast = model.predict(future)
    forecast = forecast[forecast['ds'] > df['ds'].max()]

    # Store in InfluxDB
    for index, row in forecast.iterrows():
        print(f"Writing forecast for {feature} at {row['ds']} with value {row['yhat']}")
        point = (
            Point("home")
            .tag("room", "Balcony")
            .field(f"forecast_{feature}", row['yhat'])
            .time(row['ds'])
        )
        client.write(point)

    # # Step 4: Visualization
    # # Assuming `forecast` is your forecast dataframe and `model` is your trained Prophet model
    # fig, ax = plt.subplots(figsize=(12, 6))
    # # Plot only the forecast without confidence intervals
    # ax.plot(forecast['ds'], forecast['yhat'], label='Forecast')
    # # Optionally, you can plot the actual data too
    # feature_styled = feature.capitalize().replace("_", " ")
    # ax.plot(df['ds'], df['y'], label='Actual')  # If you have the original data in `df`
    # ax.set_title(f'Forecast for feature {feature_styled}')
    # ax.set_xlabel('Date')
    # ax.set_ylabel(f'{feature_styled}')
    # ax.legend()
    # fig.savefig(f"forecast_{feature}.png", dpi=300, bbox_inches='tight')
    #
    # fig2 = model.plot_components(forecast)
    # ax = fig2.gca()
    # ax.set_title(f"Forecast components for feature {feature_styled}")
    # fig2.savefig(f"forecast_components_{feature}.png", dpi=300, bbox_inches='tight')
