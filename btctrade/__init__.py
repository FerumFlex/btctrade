__version__ = (0, 1, '0')


import copy
import random
import hashlib
import time
import logging
import requests

# support Python2 and Python 3
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


logger = logging.getLogger('btctrade')


class BtctradeException(Exception):
    pass


class Btctrade(object):
    def __init__(self, public_key=None, private_key=None):
        self.base_url = 'https://btc-trade.com.ua/api/'
        self.public_key = public_key
        self.private_key = private_key

    def __get_nonce(self):
        return '{:.7f}'.format(time.time()).replace('.', '')

    def __get_out_order_id(self):
        key = "my_randm" + str(random.randrange(1, 1000000000000000000))
        m = hashlib.sha256()
        m.update(key.encode('utf8'))
        return m.hexdigest()

    def __sign_payload(self, payload):
        assert self.private_key

        data = payload + self.private_key
        m = hashlib.sha256()
        m.update(data.encode('utf8'))
        return m.hexdigest()

    def __get_headers(self, payload):
        headers = {
            'Accept': "application/json",
            'Content-Type': "application/x-www-form-urlencoded",
            'public_key': self.public_key,
            'api_sign': self.__sign_payload(payload),
        }
        return headers

    def __request(self, path, method='get', params=None, out_order_id=None):
        assert method in ('get', 'post')

        url = '{}{}'.format(self.base_url, path)

        if method == 'get':
            logger.info('Request method {}, url {}, params {}'.format(method, url, params))
            result = requests.get(url, params=params)
        else:
            data = copy.copy(params or {})
            data.update({
                'out_order_id': out_order_id or self.__get_out_order_id(),
                'nonce': self.__get_nonce(),
            })

            payload = urlencode(data)
            headers = self.__get_headers(payload)

            logger.info('Request method {}, url {}, params {}, headers {}'.format(method, url, data, headers))
            result = requests.post(url, payload, headers=headers)

        logger.info('Response status code {}, content {}'.format(result.content, result.status_code))
        if result.status_code != 200:
            raise BtctradeException(result.content)

        try:
            data = result.json()
        except Exception:
            raise BtctradeException(result.content)

        if isinstance(data, dict):
            status = data.get('status')
            if isinstance(status, bool) and not status:
                description = data.get('description', 'No error description')
                raise BtctradeException(description)

        return data

    def get_deals(self, pair):
        return self.__request('deals/{}'.format(pair))

    def get_sell_trades(self, pair):
        return self.__request('trades/sell/{}'.format(pair))

    def get_buy_trades(self, pair):
        return self.__request('trades/buy/{}'.format(pair))

    def get_japan_stats(self, pair):
        return self.__request('japan_stat/high/{}'.format(pair))

    def get_balance(self, out_order_id=None):
        return self.__request('balance', method='post', out_order_id=out_order_id)

    def sell(self, pair, price, amount, out_order_id=None):
        params = {
            'price': price,
            'count': amount,
        }
        return self.__request('sell/{}'.format(pair), method='post', params=params, out_order_id=out_order_id)

    def buy(self, pair, price, amount, out_order_id=None):
        params = {
            'price': price,
            'count': amount,
        }
        return self.__request('buy/{}'.format(pair), method='post', params=params, out_order_id=out_order_id)

    def get_my_orders(self, pair, out_order_id=None):
        return self.__request('my_orders/{}'.format(pair), method='post', out_order_id=out_order_id)

    def get_order_status(self, order_id, out_order_id=None):
        return self.__request('order/status/{}'.format(order_id), method='post', out_order_id=out_order_id)

    def remove_order(self, order_id, out_order_id=None):
        return self.__request('remove/order/{}'.format(order_id), method='post', out_order_id=out_order_id)

    def bid(self, pair, amount, out_order_id=None):
        params = {
            'amount': amount,
        }
        return self.__request('bid/{}'.format(pair), params=params, method='post', out_order_id=out_order_id)

    def ask(self, pair, amount, out_order_id=None):
        params = {
            'amount': amount,
        }
        return self.__request('ask/{}'.format(pair), params=params, method='post', out_order_id=out_order_id)
