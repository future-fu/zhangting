#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2021/9/17 17:58
# @Author  : Future Fu
# @FileName: yeji_20210917.py

import os, sys
import baostock as bs
import pandas as pd


def predict_yeji(code):
    #### 登陆系统 ####
    lg = bs.login()
    # 显示登陆返回信息
    print('login respond error_code:' + lg.error_code)
    print('login respond  error_msg:' + lg.error_msg)
    #### 获取公司业绩预告 ####
    str1=''
    if code[0:2] =='00' :
        str1='sz.'+code
    else:
        str1='sh.'+code
    print('code:'+str1)
    rs_forecast = bs.query_forecast_report(str1, start_date="2020-01-01", end_date="2021-12-31")
    print('query_forecast_reprot respond error_code:' + rs_forecast.error_code)
    print('query_forecast_reprot respond  error_msg:' + rs_forecast.error_msg)
    rs_forecast_list = []
    while (rs_forecast.error_code == '0') & rs_forecast.next():
        # 分页查询，将每页信息合并在一起
        rs_forecast_list.append(rs_forecast.get_row_data())
    result_forecast = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)
    #### 结果集输出到csv文件 ####
    result_forecast.to_csv("data\\res2.csv", encoding="utf-8", index=False,mode='a')
    print(result_forecast)
    #### 登出系统 ####
    bs.logout()

if __name__ == '__main__':
  file = open("data\\res2.csv", 'w').close()
  predict_yeji('002411')
  predict_yeji('002574')
  predict_yeji('000893')
  predict_yeji('603167')
