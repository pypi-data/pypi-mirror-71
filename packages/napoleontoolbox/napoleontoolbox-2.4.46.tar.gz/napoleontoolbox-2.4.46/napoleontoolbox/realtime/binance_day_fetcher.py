#!/usr/bin/env python3
# coding: utf-8

from binance.websockets import BinanceSocketManager
from functools import partial
from binance.client import Client
import numpy as np
from napoleontoolbox.connector import napoleon_s3_connector
import pandas as pd
import datetime
from napoleontoolbox.realtime import binance_minute_fetcher

class NaPoleonBinanceMinutesFetcher(object):
    def __init__(self,pair, local_root_directory, binance_public, binance_secret, aws_public, aws_secret, aws_region ,bucket='napoleon-minutes'):
        self.bucket = bucket
        self.local_root_directory = local_root_directory
        self.client = Client(binance_public, binance_secret)
        self.aws_client = napoleon_s3_connector.NapoleonS3Connector(aws_public,aws_secret,region=aws_region)
        self.pair = pair
        self.nbsc = binance_minute_fetcher.NaPoleonBinanceMinutesFetcher(pair,local_root_directory, binance_public, binance_secret, aws_public, aws_secret, aws_region)

    def hour_day_fetcher(self):
        dfs_list = self.nbsc.get_aws_last24_passed_full_hours()
        dfs_list['day_ts'] = dfs_list.ts.apply(lambda x: datetime.datetime.fromtimestamp(x).date())
        dfs_list.ts = dfs_list.ts.apply(lambda x: datetime.datetime.fromtimestamp(x))
        dfs_list = dfs_list.sort_values('ts')
        current_day_df = dfs_list[dfs_list.day_ts>=datetime.datetime.today().date()]

        available_hours = current_day_df.hour_ts.unique()
        hourly_df = pd.DataFrame()

        ##Reconstitute hourly ohlc

        for hour in available_hours:
            current_df_hour = current_day_df[current_day_df.hour_ts == hour]
            approx_open_hour = current_df_hour['open'].values[0]
            approx_close_hour = current_df_hour['close'].values[-1]
            approx_high_hour = max(current_df_hour['high'].values)
            approx_low_hour = min(current_df_hour['low'].values)
            approx_ohlc_hour =  pd.DataFrame(np.array([[approx_open_hour,approx_high_hour,approx_low_hour, approx_close_hour, hour]]), columns = ['open', 'high', 'low', 'close', 'hour_ts'])
            if hourly_df.empty:
                hourly_df = approx_ohlc_hour
            else:
                hourly_df = pd.concat([hourly_df, approx_ohlc_hour], ignore_index=True)

        hourly_df.hour_ts = hourly_df.hour_ts.apply(lambda x: datetime.datetime.fromtimestamp(x))
        hourly_df.index = hourly_df.hour_ts
        hourly_df = hourly_df.loc[:,hourly_df.columns != 'hour_ts']

        ##Reconstitute last day ohlc

        approx_open_day = hourly_df['open'].values[0]
        approx_close_day = hourly_df['close'].values[-1]
        approx_high_day = max(hourly_df['high'].values)
        approx_low_day = min(hourly_df['low'].values)
        last_day_df = pd.DataFrame(np.array([[approx_open_day,approx_high_day,approx_low_day, approx_close_day]]), columns = ['open', 'high', 'low','close'])
        return hourly_df, last_day_df