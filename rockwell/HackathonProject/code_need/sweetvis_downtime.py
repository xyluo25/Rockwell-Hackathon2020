# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, September 18th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import sweetviz as sv
import pandas as pd

def createSweetviz(dataFileName,sheetName = "DowntimeInfo",outputName = "Rockwell_sweetViz.html",showOnWeb = False,save2local=False):
    
    df = pd.read_excel(open(dataFileName, 'rb'), sheet_name=sheetName) 
    df = df.drop(['DOWNTIME_ID','MRP_CONTROLLER_S','SALES_ORDER_NUM', 'RESPONDED_BY_USER_NAME_H','DT_COMMENTS','WORK_CENTER','ENTERED_BY_USER_NAME_H','LOGGED_UP_BY_USER_NAME_H'], axis=1)
    
    df['SOLUTION'].fillna("Don't Care", inplace = True) 
    df['GROUP_NAME'].fillna("Don't Care", inplace = True) 
    df['WORK_ORDER'].fillna("Don't Care", inplace = True)

    my_report = sv.analyze(df)
    
    # output= os.path.join(settings.BASE_DIR,r"HackathonProject\media\%s"%outputName)
    output = "A string"
    sweetviz_html = my_report.show_html(filepath=output,onWeb=showOnWeb,saveFile=save2local) # Default arguments will generate to "SWEETVIZ_REPORT.html"
    
    return sweetviz_html