About
=====

Python bindings for btc-trade.com.ua. I am Not associated -- use at your own risk, etc.

Installation
============

::

  pip install btctrade

Using
=====

::

  import btctrade

  btc = btctrade.Btctrade('<public key>', '<private key>')

  btc.get_my_orders('btc_uah')


Supported calls
===============

Public methods (you can call these method without public and private keys)

- get_deals(pair)
- get_sell_trades(pair)
- get_buy_trades(pair)
- get_japan_stats(pair)


Private methods(public and private keys are required)

- get_balance()
- sell(pair, price, amount)
- buy(pair, price, amount)
- get_my_orders(pair)
- get_order_status(order_id)
- remove_order(order_id)
- bid(pair, amount)
- ask(pair, amount)


Donations
=========

- BTC: 1J2ZSc97yzrGihULVMPCtEZs7zUDD6j7v
- ETH: 0x86735BCB1990CE2E2C264F850732255a7D9dEC21
