#!/usr/bin/env python3
# coding: utf-8

from multiprocessing import Pool

from napoleontoolbox.file_saver import dropbox_file_saver
from napoleontoolbox.signal import signal_generator
from napoleontoolbox.connector import napoleon_connector
from napoleontoolbox.signal import signal_utility
import json

from binance.websockets import BinanceSocketManager
from functools import partial
from binance.client import Client
import numpy as np
from napoleontoolbox.connector import napoleon_s3_connector
import pandas as pd
from datetime import datetime, timedelta

import hashlib

def pair_handling_message(fetcher, msg, compute_signal=True, compute_parallel = False):
    high_dict = fetcher.pair_dict['high']
    low_dict = fetcher.pair_dict['low']
    volu_dict = fetcher.pair_dict['volu']
    close_dict = fetcher.pair_dict['close']
    open_dict = fetcher.pair_dict['open']

    hour_high_dict = fetcher.pair_dict['hour_high']
    hour_low_dict = fetcher.pair_dict['hour_low']
    hour_volu_dict = fetcher.pair_dict['hour_volu']
    hour_close_dict = fetcher.pair_dict['hour_close']
    hour_open_dict = fetcher.pair_dict['hour_open']

    day_high_dict = fetcher.pair_dict['day_high']
    day_low_dict = fetcher.pair_dict['day_low']
    day_volu_dict = fetcher.pair_dict['day_volu']
    day_close_dict = fetcher.pair_dict['day_close']
    day_open_dict = fetcher.pair_dict['day_open']

    trade_time_unix_timestamp = msg['T']/1000
    trade_time_unix_timestamp_minute = trade_time_unix_timestamp - (trade_time_unix_timestamp % 60)
    trade_time_unix_timestamp_hour = trade_time_unix_timestamp - (trade_time_unix_timestamp % 3600)
    trade_time_unix_timestamp_day = trade_time_unix_timestamp - (trade_time_unix_timestamp % (3600*24))

    price = float(msg['p'])

    actual_day_open = day_open_dict.get(trade_time_unix_timestamp_day, np.nan)
    if np.isnan(actual_day_open):
        # we open a new hour
        if len(day_high_dict) > 1 or len(day_low_dict) > 1 or len(day_volu_dict) > 1 or len(
                day_close_dict) > 1 or len(day_open_dict) > 1:
            raise Exception('Trouble in paradise we enter a new day with no empty dictionaries')
        if len(day_high_dict) > 0 and len(day_low_dict) > 0 and len(day_volu_dict) > 0 and len(day_close_dict) > 0 and len(day_open_dict) > 0:
            key_day_ts = next(iter(day_high_dict))
            day_dt_object = datetime.utcfromtimestamp(key_day_ts)
            day_name = fetcher.pair + '_' + day_dt_object.strftime('%d_%b_%Y_%H_%M')
            print('appending one day row ' + day_name)

            day_new_data_lst = [key_day_ts, day_open_dict[key_day_ts], day_high_dict[key_day_ts],
                                 day_low_dict[key_day_ts],
                                 day_close_dict[key_day_ts], day_volu_dict[key_day_ts]]
            day_new_data = np.array(day_new_data_lst)
            print('new daily data')
            print(day_new_data)
            if fetcher.day_np is None:
                fetcher.day_np = day_new_data
            else:
                fetcher.day_np = np.vstack((fetcher.day_np, day_new_data))

            if (len(fetcher.day_np.shape) > 1 and len(fetcher.day_np) > 3):
                print('last three days')
                print(fetcher.day_np[-3:, :])

            if fetcher.minute_np is not None and len(fetcher.minute_np)>0:
                print('persisting dataframe for the previous hour')
                #fetcher.upload_last_hour_60_minutes_dataframe()
                fetcher.upload_last_day_24_hours_signals_dataframe()
                fetcher.reset_hour_np_to_lookback_window()

        # we clear every former minutes
        day_high_dict.clear()
        day_low_dict.clear()
        day_volu_dict.clear()
        day_close_dict.clear()
        day_open_dict.clear()
        day_open_dict[trade_time_unix_timestamp_day] = price

    day_close_dict[trade_time_unix_timestamp_day] = price
    day_actual_high = day_high_dict.get(trade_time_unix_timestamp_day, 0)
    if price > day_actual_high:
        day_high_dict[trade_time_unix_timestamp_day]=price
    day_actual_low = day_low_dict.get(trade_time_unix_timestamp_day, np.inf)
    if price < day_actual_low:
        day_low_dict[trade_time_unix_timestamp_day]=price
    day_actual_volu = day_volu_dict.get(trade_time_unix_timestamp_day, 0)
    day_volu_dict[trade_time_unix_timestamp_day] = day_actual_volu + float(msg['q'])

    actual_hour_open = hour_open_dict.get(trade_time_unix_timestamp_hour, np.nan)
    if np.isnan(actual_hour_open):
        # we open a new hour
        if len(hour_high_dict)>1 or len(hour_low_dict)>1 or len(hour_volu_dict)>1 or len(hour_close_dict)>1 or len(hour_open_dict)>1:
            raise Exception('Trouble in paradise we enter a new hour with no empty dictionaries')
        if len(hour_high_dict) > 0 and len(hour_low_dict) > 0 and len(hour_volu_dict) > 0 and len(hour_close_dict) > 0 and len(hour_open_dict) > 0:
            key_hour_ts = next(iter(hour_high_dict))
            hour_dt_object = datetime.utcfromtimestamp(key_hour_ts)
            hour_name = fetcher.pair + '_' + hour_dt_object.strftime('%d_%b_%Y_%H_%M')
            print('appending one hour row '+hour_name)

            hour_new_data_lst = [key_hour_ts, hour_open_dict[key_hour_ts], hour_high_dict[key_hour_ts], hour_low_dict[key_hour_ts],
                            hour_close_dict[key_hour_ts], hour_volu_dict[key_hour_ts]]
            hour_new_data = np.array(hour_new_data_lst)

            print(hour_new_data)
            if fetcher.hour_np is None:
                fetcher.hour_np = hour_new_data
            else:
                fetcher.hour_np = np.vstack((fetcher.hour_np, hour_new_data))

            if (len(fetcher.hour_np.shape)>1 and len(fetcher.hour_np)>3):
                print('last three hours')
                print(fetcher.hour_np[-3:,:])
            #fetcher.minute_df.loc[len(fetcher.minute_df)] = new_data
            if fetcher.minute_np is not None and len(fetcher.minute_np)>0:
                print('persisting dataframe for the previous hour')
                #fetcher.upload_last_hour_60_minutes_dataframe()
                fetcher.upload_last_hour_60_minutes_signals_dataframe()
                fetcher.reset_minute_np_to_lookback_window()

        # we clear every former minutes
        hour_high_dict.clear()
        hour_low_dict.clear()
        hour_volu_dict.clear()
        hour_close_dict.clear()
        hour_open_dict.clear()
        hour_open_dict[trade_time_unix_timestamp_hour] = price


    hour_close_dict[trade_time_unix_timestamp_hour] = price
    hour_actual_high = hour_high_dict.get(trade_time_unix_timestamp_hour, 0)
    if price > hour_actual_high:
        hour_high_dict[trade_time_unix_timestamp_hour]=price
    hour_actual_low = hour_low_dict.get(trade_time_unix_timestamp_hour, np.inf)
    if price < hour_actual_low:
        hour_low_dict[trade_time_unix_timestamp_hour]=price
    hour_actual_volu = hour_volu_dict.get(trade_time_unix_timestamp_hour, 0)
    hour_volu_dict[trade_time_unix_timestamp_hour] = hour_actual_volu + float(msg['q'])


    actual_open = open_dict.get(trade_time_unix_timestamp_minute, np.nan)
    if np.isnan(actual_open):
        # we open a new minute
        if len(high_dict)>1 or len(low_dict)>1 or len(volu_dict)>1 or len(close_dict)>1 or len(open_dict)>1:
            raise Exception('Trouble in paradise we enter a new minute with no empty dictionaries')
        if len(high_dict) > 0 and len(low_dict) > 0 and len(volu_dict) > 0 and len(close_dict) > 0 and len(open_dict) > 0:
            key_ts = next(iter(high_dict))
            minute_dt_object = datetime.utcfromtimestamp(key_ts)
            minute_name = fetcher.pair + '_' + minute_dt_object.strftime('%d_%b_%Y_%H_%M')
            print('appending one minute row '+minute_name)

            new_data_lst = [key_ts, open_dict[key_ts], high_dict[key_ts], low_dict[key_ts],
                            close_dict[key_ts], volu_dict[key_ts]]
            new_data = np.array(new_data_lst)

            print(new_data)
            if fetcher.minute_np is None:
                fetcher.minute_np = new_data
            else:
                fetcher.minute_np = np.vstack((fetcher.minute_np, new_data))
            if compute_signal:
                if compute_parallel:
                    fetcher.launchMinuteParallelPool()
                else:
                    fetcher.launchMinuteSequential()
            if (len(fetcher.minute_np.shape)>1 and len(fetcher.minute_np)>3):
                print('last three minutes')
                print(fetcher.minute_np[-3:,:])
            #fetcher.minute_df.loc[len(fetcher.minute_df)] = new_data
        # we clear every former minutes
        high_dict.clear()
        low_dict.clear()
        volu_dict.clear()
        close_dict.clear()
        open_dict.clear()
        open_dict[trade_time_unix_timestamp_minute] = price
    close_dict[trade_time_unix_timestamp_minute] = price
    actual_high = high_dict.get(trade_time_unix_timestamp_minute, 0)
    if price > actual_high:
        high_dict[trade_time_unix_timestamp_minute]=price
    actual_low = low_dict.get(trade_time_unix_timestamp_minute, np.inf)
    if price < actual_low:
        low_dict[trade_time_unix_timestamp_minute]=price
    actual_volu = volu_dict.get(trade_time_unix_timestamp_minute, 0)
    volu_dict[trade_time_unix_timestamp_minute] = actual_volu + float(msg['q'])

class RealTimeSignalEnsemblingParalleLauncher():
    def __init__(self, starting_date=None, running_date=None, drop_token='', dropbox_backup=True, BINANCE_PUBLIC='', BINANCE_SECRET='', AWS_PUBLIC='', AWS_SECRET='', AWS_REGION='',bucket='', local_root_directory='../data',underlying = None, pair = None, frequence='daily', selected_algo='',user='napoleon',  db_path_suffix = '_run.sqlite', list_pkl_file_suffix = 'my_list.pkl',freqly_return_pkl_filename_suffix='freqly_candels.pkl'):
        self.starting_date = starting_date
        self.running_date = running_date
        self.pair = pair
        self.BINANCE_PUBLIC = BINANCE_PUBLIC
        self.BINANCE_SECRET = BINANCE_SECRET

        self.dropbox_backup =dropbox_backup
        self.drop_token =drop_token
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)

        self.AWS_PUBLIC = AWS_PUBLIC
        self.AWS_SECRET = AWS_SECRET
        self.AWS_REGION = AWS_REGION
        self.bucket = bucket

        self.client = Client(BINANCE_PUBLIC, BINANCE_SECRET)
        self.aws_client = napoleon_s3_connector.NapoleonS3Connector(AWS_PUBLIC,AWS_SECRET,region=AWS_REGION)
        self.pair = pair
        self.generic_columns = ['ts', 'open', 'high', 'low', 'close', 'volumefrom']
        self.minute_df = pd.DataFrame(columns=self.generic_columns)

        self.hour_df = pd.DataFrame(columns=self.generic_columns)

        self.minute_np = None
        self.minute_signal_np = None
        self.hour_np = None
        self.pair_dict = {}
        self.pair_dict['high'] = {}
        self.pair_dict['low'] = {}
        self.pair_dict['volu'] = {}
        self.pair_dict['close'] = {}
        self.pair_dict['open'] = {}
        self.pair_dict['hour_high'] = {}
        self.pair_dict['hour_low'] = {}
        self.pair_dict['hour_volu'] = {}
        self.pair_dict['hour_close'] = {}
        self.pair_dict['hour_open'] = {}

        self.pair_dict['day_high'] = {}
        self.pair_dict['day_low'] = {}
        self.pair_dict['day_volu'] = {}
        self.pair_dict['day_close'] = {}
        self.pair_dict['day_open'] = {}

        self.args = []
        self.counter = 1
        self.seed = 0
        self.local_root_directory = local_root_directory

        self.underlying = underlying
        self.list_pkl_file_suffix = list_pkl_file_suffix
        self.frequence=frequence
        self.selected_algo=selected_algo

        self.dates_stub = self.starting_date.strftime('%d_%b_%Y') + '_' + self.running_date.strftime('%d_%b_%Y')

        self.list_pkl_file_name = self.dates_stub + '_' + self.underlying + '_' + self.frequence + '_' + self.selected_algo + self.list_pkl_file_suffix
        print('selected algos')
        print(self.list_pkl_file_name)
        if self.dropbox_backup:
            self.signals_list =  self.dbx.download_pkl(self.list_pkl_file_name)
        else:
            self.signals_list = napoleon_connector.load_pickled_list(local_root_directory=self.local_root_directory,
                                                                 list_pkl_file_name=self.list_pkl_file_name)
        self.signal_mapping={}
        max_lookback_window = 0
        for me_signal in self.signals_list:
            self.args.append((me_signal))
            self.counter = self.counter + 1
            run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
            params = json.loads(run_json_string)
            salty = str(int(hashlib.sha1(run_json_string.encode('utf-8')).hexdigest(), 16) % (10 ** 8))
            params = json.loads(run_json_string)
            readable_label = params['signal_type'] + str(params['trigger']) + salty
            self.signal_mapping[me_signal]=readable_label
            if params['lookback_window']>max_lookback_window:
                max_lookback_window=params['lookback_window']
        self.max_lookback_window = max_lookback_window

        self.args.sort()
        self.user = user
        self.db_path_suffix = db_path_suffix
        self.filename =  user + db_path_suffix
        self.db_path = self.local_root_directory + self.filename
        self.runs = []
        self.totalRow = 0
        self.empty_runs_to_investigate = []
        self.dbx = dropbox_file_saver.NaPoleonDropboxConnector(drop_token=drop_token,dropbox_backup=dropbox_backup)
        self.freqly_return_pkl_filename_suffix=freqly_return_pkl_filename_suffix
        self.saving_return_path = self.local_root_directory+self.underlying+self.freqly_return_pkl_filename_suffix

        self.last_minute = None


    def get_aws_last_passed_full_hours(self, nb_last_hours = 24):
        date_now = datetime.utcnow()
        files_to_fetch = []
        #minute_name = self.pair + '_' + date_now.strftime('%d_%b_%Y_%H_%M')
        #files_to_fetch.append(minute_name)
        d = date_now
        for i in range(nb_last_hours):
            d = d - timedelta(hours=1)
            minute_name = self.pair + '_' + d.strftime('%d_%b_%Y_%H')
            files_to_fetch.append(minute_name)
        aggregated_df = None
        for me_file in files_to_fetch:
            df = None
            try:
                df = self.aws_client.download_dataframe_from_csv(self.bucket, me_file)
            except Exception as e:
                print(e)
                df = None
            if aggregated_df is not None:
                if df is not None:
                    print(me_file)
                    print(df.shape)
                    aggregated_df = pd.concat([aggregated_df, df])
            if aggregated_df is None:
                if df is not None:
                    print(df.shape)
                    aggregated_df = df

        print('size fetched')
        print(aggregated_df.shape)

        aggregated_df = aggregated_df.sort_values(by=['date'])
        aggregated_df['date'] = pd.to_datetime(aggregated_df['date'])
        aggregated_df = aggregated_df.set_index(aggregated_df['date'])
        aggregated_df = aggregated_df.drop(columns=['date'])
        test = aggregated_df.pivot_table(index=['date'], aggfunc='size')
        print('max duplication')
        print(test.max())

        aggregated_df = aggregated_df.drop_duplicates()
        test = aggregated_df.pivot_table(index=['date'], aggfunc='size')
        print('max duplication  after dropping duplicates')
        print(test.max())

        print('size fetched after dropping duplicates')
        print(aggregated_df.shape)
        return aggregated_df

    def start_fetching_pair(self):
        bm = BinanceSocketManager(self.client)
        pair_callback = partial(pair_handling_message, self)
        bm.start_aggtrade_socket(self.pair, pair_callback)
        bm.start()

    def reset_minute_np_to_lookback_window(self, loolback_window = 70):
        print('minutes shape before hour reset')
        print(self.minute_np.shape)
        print(self.minute_signal_np.shape)
        self.minute_np = self.minute_np[-loolback_window:]
        self.minute_signal_np = self.minute_signal_np[-loolback_window:]
        print('minutes shape afteer hour reset')
        print(self.minute_np.shape)
        print(self.minute_signal_np.shape)

    def update_minute_dataframe(self):
        print('updating minute df')
        if len(self.minute_np.shape)>1:
            updated_df=pd.DataFrame(data=self.minute_np, columns = self.generic_columns, index=range(len(self.minute_np)))
        else:
            updated_df=pd.DataFrame(data=self.minute_np.reshape(1,len(self.minute_np)), columns = self.generic_columns, index=[0])
        updated_df['ts'] = updated_df['ts'].astype(int)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.minute_df = updated_df
        self.last_minute = max(self.minute_df.index)

    def reset_hour_np_to_lookback_window(self, loolback_window = 70):
        print('hours shape before day reset')
        print(self.hour_np.shape)
        self.hour_np = self.hour_np[-loolback_window:]
        print('hours shape after day reset')
        print(self.hour_np.shape)

    def upload_last_day_24_hours_signals_dataframe(self):
        print('updating 24 hours day df')

        updated_df=pd.DataFrame(data=self.hour_np, columns = self.generic_columns, index=range(len(self.minute_signal_np)))
        # updated_df = updated_df.astype(
        #     {'ts': 'float64', 'open': 'float64', 'high': 'float64', 'low': 'float64', 'close': 'float64','volumefrom': 'float64'}
        #                                )
        updated_df['ts']=updated_df['ts'].astype(int)
        updated_df['hour_ts'] = updated_df['ts']-updated_df['ts']%3600
        updated_df['day_ts'] = updated_df['ts']-updated_df['ts']%(3600*24)
        updated_df = updated_df.astype({'hour_ts': 'int64'})
        updated_df = updated_df.astype({'day_ts': 'int64'})
        if updated_df['day_ts'].nunique()>1:
            print('too many days saved together : investigate')
        day_timestamp = updated_df['day_ts'].max()
        day_dt_object = datetime.utcfromtimestamp(day_timestamp)
        filename = self.pair+'_'+day_dt_object.strftime('%d_%b_%Y') #str(hourr_timestamp)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.hour_df = updated_df
        local_path = self.local_root_directory + filename
        self.minute_df.to_csv(local_path)
        self.aws_client.upload_file(self.bucket,local_path)

    def upload_last_hour_60_minutes_signals_dataframe(self):
        print('updating 60 minutes hour df')
        updated_df=pd.DataFrame(data=self.minute_np, columns = self.generic_columns, index=range(len(self.minute_np)))
        #updated_df = updated_df.astype({'ts': 'float32','open': 'float32', 'high': 'float32', 'low': 'float32', 'close': 'float32', 'volumefrom': 'float32'})
        updated_df['ts']=updated_df['ts'].astype(int)
        updated_df['hour_ts'] = updated_df['ts']-updated_df['ts']%3600
        updated_df = updated_df.astype({'hour_ts': 'int64'})
        if updated_df['hour_ts'].nunique()>1:
            print('too many hours saved together : investigate')
        hour_timestamp = updated_df['hour_ts'].max()
        hour_dt_object = datetime.utcfromtimestamp(hour_timestamp)
        filename = self.pair+'_'+hour_dt_object.strftime('%d_%b_%Y_%H') #str(hourr_timestamp)
        updated_df['ts'] = pd.to_datetime(updated_df['ts'], unit='s')
        updated_df = updated_df.sort_values(by=['ts'])
        updated_df = updated_df.rename(columns={"ts": "date"}, errors="raise")
        updated_df = updated_df.set_index(updated_df['date'])
        updated_df = updated_df.drop(columns=['date'])
        self.minute_df = updated_df
        local_path = self.local_root_directory + filename
        self.minute_df.to_csv(local_path)
        self.aws_client.upload_file(self.bucket,local_path)

    def download_minute_dataframe(self, filename):
        dataframe = self.aws_client.download_dataframe_from_csv(self.bucket, filename)
        return dataframe

    def launchMinuteParallelPool(self, use_num_cpu):
        print('launching parallel computation for alphas at '+str(self.last_minute))
        with Pool(processes=use_num_cpu) as pool:
            run_results = pool.starmap(self.runMinuteSignal, self.args)
        print('parallel computation done')
        print('results length')
        print(len(run_results))


    def launchMinuteSequential(self):
        self.update_minute_dataframe()
        print('launching sequential computation for alphas at '+str(self.last_minute))
        run_results = []
        for meArg in self.args:
            run_results.append(self.runMinuteSignal(meArg))
        print('results length')
        print(len(run_results))
        new_data_sig = np.array(run_results)
        if len(self.minute_np.shape)>1:
            new_data_sig = np.hstack((self.minute_np[-1,:].reshape(1, len(self.generic_columns)), new_data_sig.reshape(1, len(new_data_sig))))
        else:
            new_data_sig = np.hstack((self.minute_np.reshape(1, len(self.generic_columns)), new_data_sig.reshape(1, len(new_data_sig))))

        print(new_data_sig)
        if self.minute_signal_np is None:
            self.minute_signal_np = new_data_sig
        else:
            self.minute_signal_np = np.vstack((self.minute_signal_np, new_data_sig))
        if len(self.minute_signal_np.shape)>1 and len(self.minute_signal_np)>3:
            print('last three signals')
            print(self.minute_signal_np[-3:])

    def runMinuteSignal(self, me_signal):
        ## idiosyncratic run itself
        run_json_string = signal_utility.recover_to_sql_column_format(me_signal)
        params = json.loads(run_json_string)
        signal_type = params['signal_type']
        normalization = params['normalization']
        trigger = params['trigger']
        transaction_costs = params['transaction_costs']
        if normalization and not signal_generator.is_signal_continuum(signal_type):
            return
        lookback_window = params['lookback_window']
        if lookback_window>self.minute_df.shape[0]:
            return np.nan
        freqly = self.minute_df.iloc[-lookback_window:,:].copy()
        signal_generation_method_to_call = getattr(signal_generator, signal_type)
        last_generated_signal = signal_utility.compute_last_signal(freqly, lookback_window,
                                                                   lambda x: signal_generation_method_to_call(
                                                                       data=x, **params))
        return last_generated_signal



    def hour_day_fetcher(self):
        dfs_list = self.get_aws_last24_passed_full_hours()
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



