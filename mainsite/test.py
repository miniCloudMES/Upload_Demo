# -*- coding: utf-8 -*-
"""
-------------------------------------------------
  File Name：   test for uwsgi check
  Description : MiniMES Company
  Author :    Karo Lin
  date：     2023/1/29
  Copyright follow MIT definitions.
-------------------------------------------------
  Change Activity:
          2023/1/29:
-------------------------------------------------
"""
__author__ = 'Karo Lin'


# Use the script to test uwsgi is working or not.
# uwsgi --socket :8001 --wsgi-file test.py
# Then check url 127.0.0.0:8001 with Browser.

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b"Hello World"]
