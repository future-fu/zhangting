#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/5/12 16:52
# @Author  : Future Fu
# @FileName: t3.py

import pandas as pd
import tushare as ts

import datetime



def print_full(x):
    pd.set_option('display.max_rows', len(x))
    pd.set_option('display.max_columns', None)
    print(x)
    pd.reset_option('display.max_rows')

if __name__ == '__main__':

 df = ts.get_today_all()
 file_name = str(datetime.date.today()) + '_Astock.csv'
 file_name2 = str(datetime.date.today()) + '_zhangting.csv'
 df.to_csv('./data/'+file_name)

 # ZhangTing_df = df[(df["changepercent"]>9.5) & (df["changepercent"]<10.5) ]
 ZhangTing_df = df[(df["changepercent"]>9.8)]
 print_full(ZhangTing_df)
 ZhangTing_df.to_csv('./data/'+file_name2)


