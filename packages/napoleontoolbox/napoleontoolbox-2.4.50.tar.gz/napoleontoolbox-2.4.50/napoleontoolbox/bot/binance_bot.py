#!/usr/bin/env python3
# coding: utf-8

import ccxt
import urllib.parse,  urllib.request
from urllib.parse import urljoin, urlencode
import json, hashlib, hmac, time
from datetime import datetime
import requests


class NaPoleonBinanceFutureBot(object):

    def __init__(self, BINANCE_PUBLIC, BINANCE_PRIVATE):
        self.apiKey = BINANCE_PUBLIC
        self.secret = BINANCE_PRIVATE
        Binancecle2 = {
            'api_key': BINANCE_PUBLIC,
            'api_secret': BINANCE_PRIVATE,
        }
        print('Connexion to Binance Future')
        exchange_id = 'binance'
        exchange_class = getattr(ccxt, exchange_id)
        self.exchange = exchange_class({
            'apiKey': Binancecle2['api_key'],
            'secret': Binancecle2['api_secret'],
            'timeout': 10000,
            'enableRateLimit': True,
            'options': {'defaultType': 'future'},
        })

    def cancel_all_orders(self):
        Cleaner = self.exchange.fetch_open_orders('BTC/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'BTC/USDT')
        Cleaner = self.exchange.fetch_open_orders('ETH/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'ETH/USDT')
        Cleaner = self.exchange.fetch_open_orders('LTC/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'LTC/USDT')
        Cleaner = self.exchange.fetch_open_orders('EOS/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'EOS/USDT')
        Cleaner = self.exchange.fetch_open_orders('XRP/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'XRP/USDT')
        Cleaner = self.exchange.fetch_open_orders('BCH/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'BCH/USDT')
        Cleaner = self.exchange.fetch_open_orders('TRX/USDT')
        L = len(Cleaner)
        if L > 0:
            for i in range(0, L):
                self.exchange.cancel_order(Cleaner[i]['info']['orderId'], 'TRX/USDT')

    def get_balance_low_level(self):
        BASE_URL = 'https://api.binance.com'
        PATH = '/api/v3/account'
        timestamp = int(time.time() * 1000)
        headers = {
            'X-MBX-APIKEY': self.apiKey
        }
        params = {
            'recvWindow': 5000,
            'timestamp': timestamp
        }
        query_string = urllib.parse.urlencode(params)
        params['signature'] = hmac.new(self.secret.encode('utf-8'), query_string.encode('utf-8'),
                                       hashlib.sha256).hexdigest()
        url = urljoin(BASE_URL, PATH)
        print(url)
        r = requests.get(url, headers=headers, params=params)
        dataSet = r.json()
        print(dataSet)

    def get_balance(self):
        # Recupérer la balance
        balance = self.exchange.fetchTotalBalance(params={})
        Donnees = self.exchange.fetchTickers()
        jeu = balance['USDT']
        print(balance)
        # print(Donnees)
        ETH = float(Donnees['ETH/USDT']['info']['lastPrice'])
        BTC = float(Donnees['BTC/USDT']['info']['lastPrice'])
        LTC = float(Donnees['LTC/USDT']['info']['lastPrice'])
        TRX = float(Donnees['TRX/USDT']['info']['lastPrice'])
        XRP = float(Donnees['XRP/USDT']['info']['lastPrice'])
        EOS = float(Donnees['EOS/USDT']['info']['lastPrice'])
        BCH = float(Donnees['BCH/USDT']['info']['lastPrice'])
        minBTC = 20 / BTC
        minETH = 20 / ETH
        minLTC = 20 / LTC
        minXRP = 20 / XRP
        minEOS = 20 / EOS
        minTRX = 20 / TRX
        minBCH = 20 / BCH
        # jeu = input('combien on mise dans le bouzin?')
        print('Montant sur le compte future : {} USDT'.format(round(float(jeu), 2)))
        return balance, Donnees, minBTC, minETH, minLTC, minXRP, minEOS, minTRX, minBCH

    def change_position(self,pose):
        balance, Donnees, minBTC, minETH, minLTC, minXRP, minEOS, minTRX, minBCH = self.get_balance()
        ETH = float(Donnees['ETH/USDT']['info']['lastPrice'])
        BTC = float(Donnees['BTC/USDT']['info']['lastPrice'])
        LTC = float(Donnees['LTC/USDT']['info']['lastPrice'])
        TRX = float(Donnees['TRX/USDT']['info']['lastPrice'])
        XRP = float(Donnees['XRP/USDT']['info']['lastPrice'])
        EOS = float(Donnees['EOS/USDT']['info']['lastPrice'])
        BCH = float(Donnees['BCH/USDT']['info']['lastPrice'])
        # calculer avec le last de binance!
        Tbtc = round(pose[0] * balance['USDT'] / BTC, 4)
        Teth = round(pose[1] * balance['USDT'] / ETH, 3)
        Teos = round(pose[2] * balance['USDT'] / EOS, 3)
        Txrp = round(pose[3] * balance['USDT'] / XRP, 0)
        Tltc = round(pose[4] * balance['USDT'] / LTC, 2)
        Ttrx = round(pose[5] * balance['USDT'] / TRX, 0)
        Tbch = round(pose[6] * balance['USDT'] / BCH, 3)
        balance2 = self.exchange.fapiPrivate_get_positionrisk()
        PBTC, PETH, PLTC, PXRP, PTRX, PBCH, PEOS = 0, 0, 0, 0, 0, 0, 0
        for i in range(len(balance2)):
            if balance2[i]['symbol'] == 'BTCUSDT':
                PBTC = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'ETHUSDT':
                PETH = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'LTCUSDT':
                PLTC = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'XRPUSDT':
                PXRP = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'TRXUSDT':
                PTRX = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'EOSUSDT':
                PEOS = balance2[i]['positionAmt']
            elif balance2[i]['symbol'] == 'BCHUSDT':
                PBCH = balance2[i]['positionAmt']
        # trades à faire:
        Ebtc = - float(PBTC) if Tbtc == 0 else round(float(Tbtc) - float(PBTC), 4)
        Eeth = - float(PETH) if Teth == 0 else round(float(Teth) - float(PETH), 2)
        Eeos = - float(PEOS) if Teos == 0 else round(float(Teos) - float(PEOS), 2)
        Eltc = - float(PLTC) if Tltc == 0 else round(float(Tltc) - float(PLTC), 2)
        Exrp = - float(PXRP) if Txrp == 0 else round(float(Txrp) - float(PXRP), 0)
        Etrx = - float(PTRX) if Ttrx == 0 else round(float(Ttrx) - float(PTRX), 0)
        Ebch = - float(PBCH) if Tbch == 0 else round(float(Tbch) - float(PBCH), 0)

        if Ebtc > minBTC:
            coursbtc = float(Donnees['BTC/USDT']['info']['bidPrice']) - 1
            self.exchange.create_order(symbol='BTC/USDT', type='limit', side='buy', amount=Ebtc, price=coursbtc)
        elif Ebtc < -minBTC:
            coursbtc = float(Donnees['BTC/USDT']['info']['askPrice']) + 1
            self.exchange.create_order(symbol='BTC/USDT', type='limit', side='sell', amount=abs(Ebtc), price=coursbtc)
        if Eeth > minETH:
            courseth = float(Donnees['ETH/USDT']['info']['bidPrice']) - 0.05
            self.exchange.create_order(symbol='ETH/USDT', type='limit', side='buy', amount=Eeth, price=courseth)
        elif Eeth < -minETH:
            courseth = float(Donnees['ETH/USDT']['info']['askPrice']) + 0.05
            self.exchange.create_order(symbol='ETH/USDT', type='limit', side='sell', amount=abs(Eeth), price=courseth)
        if Eltc > minLTC:
            coursltc = float(Donnees['LTC/USDT']['info']['bidPrice']) - 0.02
            self.exchange.create_order(symbol='LTC/USDT', type='limit', side='buy', amount=Eltc, price=coursltc)
        elif Eltc < -minLTC:
            coursltc = float(Donnees['LTC/USDT']['info']['askPrice']) + 0.02
            self.exchange.create_order(symbol='LTC/USDT', type='limit', side='sell', amount=abs(Eltc), price=coursltc)
        if Exrp > minXRP:
            coursxrp = float(Donnees['XRP/USDT']['info']['bidPrice']) - 0.0001
            self.exchange.create_order(symbol='XRP/USDT', type='limit', side='buy', amount=Exrp, price=coursxrp)
        elif Exrp < -minXRP:
            coursxrp = float(Donnees['XRP/USDT']['info']['askPrice']) + 0.0001
            self.exchange.create_order(symbol='XRP/USDT', type='limit', side='sell', amount=abs(Exrp), price=coursxrp)
        if Eeos > minEOS:
            courseos = float(Donnees['EOS/USDT']['info']['bidPrice'])
            self.exchange.create_order(symbol='EOS/USDT', type='limit', side='buy', amount=Eeos, price=courseos)
        elif Eeos < -minEOS:
            courseos = float(Donnees['EOS/USDT']['info']['askPrice'])
            self.exchange.create_order(symbol='EOS/USDT', type='limit', side='sell', amount=abs(Eeos), price=courseos)
        if Etrx > minTRX:
            courstrx = float(Donnees['TRX/USDT']['info']['bidPrice'])
            self.exchange.create_order(symbol='TRX/USDT', type='limit', side='buy', amount=Etrx, price=courstrx)
        elif Etrx < -minTRX:
            courstrx = float(Donnees['TRX/USDT']['info']['askPrice'])
            self.exchange.create_order(symbol='TRX/USDT', type='limit', side='sell', amount=abs(Etrx), price=courstrx)
        if Ebch > minBCH:
            coursbch = float(Donnees['BCH/USDT']['info']['bidPrice'])
            self.exchange.create_order(symbol='BCH/USDT', type='limit', side='buy', amount=Ebch, price=coursbch)
        elif Ebch < -minBCH:
            coursbch = float(Donnees['BCH/USDT']['info']['askPrice'])
            self.exchange.create_order(symbol='BCH/USDT', type='limit', side='sell', amount=abs(Ebch), price=coursbch)

