# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, September 18th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################



import random
import datetime 
import pandas as pd 
import numpy as np
random.seed(30)

# filename = "./ManufacturingOptimization_Dataset.xlsx"


def create_ML_Table(inputFileName,save2local = False) -> "DataFrame":
    
    df_OperatorAttendant = pd.read_excel(open(inputFileName, 'rb'), sheet_name='OperatorAttendant') 

    August3 = datetime.datetime(2020,8,3)
    August10 = datetime.datetime(2020,8,10)

    df_OperatorAttendant['WK_START_DATE'] = pd.to_datetime(df_OperatorAttendant['WK_START_DATE'], infer_datetime_format=True)
    df_OperatorAttendant = df_OperatorAttendant[(df_OperatorAttendant['WK_START_DATE'] == August3)|(df_OperatorAttendant['WK_START_DATE'] == August10)]
    df_OperatorAttendant = df_OperatorAttendant[(df_OperatorAttendant['PAYCODENAME'] == 'Regular') ]

    # print(f'{"Number of Uniques Employees in table OperatorAttendant: (08/03/2020 - 08/16/2020)"}{df_OperatorAttendant.USER_ID_H.nunique()}')
    # print('\n')


    df_OperatorAttendant = df_OperatorAttendant[['USER_ID_H','DAY1','WK_START_DATE', 'WK_END_DATE', 'PAYCODENAME', 'TOT_REG_HRS']]
    df_OperatorAttendant = df_OperatorAttendant.sort_values(by=['USER_ID_H','WK_START_DATE'])


    # ===== Table Sheet OutputHistRes ================ #
    df_OuputHistRes = pd.read_excel(open(inputFileName, 'rb'), sheet_name='OutputHistRes') 
    df_OuputHistRes = df_OuputHistRes[(df_OuputHistRes['WC_NAME'] == 'ASSY_L1')|
    (df_OuputHistRes['WC_NAME'] == 'ASSY_L2')|
    (df_OuputHistRes['WC_NAME'] == 'ASSY_L3')|
    (df_OuputHistRes['WC_NAME'] == 'ASSY_L4')|
    (df_OuputHistRes['WC_NAME'] == 'PACK_L1')|
    (df_OuputHistRes['WC_NAME'] == 'PACK_L2')|
    (df_OuputHistRes['WC_NAME'] == 'PACK_L3')|
    (df_OuputHistRes['WC_NAME'] == 'PACK_L4')|
    (df_OuputHistRes['WC_NAME'] == 'FUNC_TEST_L1')|
    (df_OuputHistRes['WC_NAME'] == 'FUNC_TEST_L2')|
    (df_OuputHistRes['WC_NAME'] == 'FUNC_TEST_L3')|
    (df_OuputHistRes['WC_NAME'] == 'FUNC_TEST_L4')]
    
    
    df_OuputHistRes.dropna(subset=['USER_ID_H'], inplace=True)

    # print(f'{"Number of Uniques Employees in table OuputHistRes: "}{df_OuputHistRes.USER_ID_H.nunique()}')
    # print('\n')
    
    # === Table Sheet Certifiedification&Shift ============ #
    df_Certified = pd.read_excel(open(inputFileName, 'rb'), sheet_name='EmployeeCertification&Shift') 
    df_Certified = df_Certified[df_Certified['CERTIFICATE_LEVEL  (4=certified; 1=not yet certified)'] == '4-Certified']
    
    August3 = datetime.datetime(2020,8,3)
    August11 = datetime.datetime(2020,8,11)
    df_Certified = df_Certified[(df_Certified['CREATION_TIME'] <= August3)&(df_Certified['EXPIRATION_DATE'] >= August11)]

    # print(f'{"Number of Employees for Certifications: "}{df_Certified.USER_ID_H.nunique()}')
    # print(f'{"Unique Employees with Certifications: "}{df_Certified.USER_ID_H.unique()}')
    # print(df_Certified.groupby(['Work Center Certification requirement', 'Shift']).size().reset_index(name='counts'))
    # print('\n')

    def intersection(lst1, lst2): 
        lst3 = [value for value in lst1 if value in lst2] 
        return lst3 

    intersection_Certified_EmployeePer = intersection(df_OuputHistRes.USER_ID_H.unique(), df_Certified.USER_ID_H.unique())
    # print(f'{"Total Count of Employees intersection between Certified and OuputHistRes: "} {len(set(intersection_Certified_EmployeePer))}')
    # print('\n')
    
    ## Outer join tables Certifiedification&Shift and table OutputHistRes and save the new table
    Merge_OuputHistRes_Certified = pd.merge(df_OuputHistRes,
                    df_Certified,
                    on='USER_ID_H', 
                    how='outer', 
                    indicator=True)


    Merge_OuputHistRes_Certified.drop(['STD_DEV_SEC', 'CX10_SEC','CX25_SEC','CX50_SEC','CX65_SEC','CX75_SEC','CERTIFICATE_ID_H'
        ,'CERTIFICATE_LEVEL  (4=certified; 1=not yet certified)','CREATION_TIME','EXPIRATION_DATE','Work Center Certification requirement','WC_NAME_H'
    ], axis='columns', inplace=True)

    # print(f'{"Total Count of Employees in Joined Certified and OuputHistRes: "}{Merge_OuputHistRes_Certified.USER_ID_H.nunique()}')
    # print('\n')


    # Out Join table:Certifiedification,OutputHistRes,OperatorAttendant
    Merge_OuputHistRes_Certified.drop(['_merge'], axis='columns', inplace=True)
    OperatorAttendant_OuputHistRes_Certified = pd.merge(Merge_OuputHistRes_Certified,
                    df_OperatorAttendant,
                    on='USER_ID_H', 
                    how='inner', 
                    indicator=True)


    df = OperatorAttendant_OuputHistRes_Certified
    df['WK_Date'] = "o"

    August3 = datetime.datetime(2020,8,3)
    August10 = datetime.datetime(2020,8,10)

    
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('monday')), 'WK_Date'] =  datetime.datetime(2020,8,3)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('tuesday')), 'WK_Date'] =  datetime.datetime(2020,8,4)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('wednesday')), 'WK_Date'] =  datetime.datetime(2020,8,5)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('thursday')), 'WK_Date'] =  datetime.datetime(2020,8,6)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('friday')), 'WK_Date'] =  datetime.datetime(2020,8,7)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('saturday')), 'WK_Date'] =  datetime.datetime(2020,8,8)
    df.loc[(df['WK_START_DATE'] == August3) & (df['DAY1'].str.contains('sunday')), 'WK_Date'] =  datetime.datetime(2020,8,9)
    df.loc[(df['WK_START_DATE'] == August10) & (df['DAY1'].str.contains('monday')), 'WK_Date'] =  datetime.datetime(2020,8,10)
    df.loc[(df['WK_START_DATE'] == August10) & (df['DAY1'].str.contains('tuesday')), 'WK_Date'] =  datetime.datetime(2020,8,11)

    df['AVG_SEC'].values[df['AVG_SEC'] < 0] = 0
    df["AVG_SEC"].fillna(0, inplace = True) 


    for i in range(len(df)):
        try:
            if float(df.loc[i,"WC_NAME"]):
                if df.loc[i,"CERTIFICATE_ID"] == "Pack":
                    df.loc[i,"WC_NAME"] = "PACK_"+ np.random.choice(["L1","L2","L3","L4"])
                elif df.loc[i,"CERTIFICATE_ID"] == "Assembly and Test":
                    df.loc[i,"WC_NAME"] = "ASSY_"+ np.random.choice(["L1","L2","L3","L4"])
                else:
                    pass

        except Exception as err:
            # not a NaN value
            pass

        try:
            if float(df.loc[i,"Shift"]):
                df.loc[i,"Shift"] = np.random.choice(["ShiftA","ShiftB"])
        except Exception as err:
            # not a NaN value
            pass

        try:
            if float(df.loc[i,"PART_NUMBER_H"]):
                df.loc[i,"PART_NUMBER_H"] = np.random.choice(list(df.PART_NUMBER_H.unique())[:-1])
        except Exception as err:
            # not a NaN value
            pass

        try:
            if df.loc[i,"AVG_SEC"]==0:
                df.loc[i,"AVG_SEC"] = np.random.choice(list(df.groupby('PART_NUMBER_H')['AVG_SEC'].mean()))
        except Exception as err:
            # not a NaN value
            pass


    df.loc[(df['DAY1'].str.contains('friday'))|(df['DAY1'].str.contains('saturday'))|(df['DAY1'].str.contains('sunday')), 'Shift'] =  "ShiftC"

    df.drop(['CERTIFICATE_ID','_merge'], axis='columns', inplace=True)
    df = df[df.WK_Date != 'o']

    print(f'{"Number of Uniques Employees in table OperatorAttendant_OuputHistRes_Certified: "}{df.USER_ID_H.nunique()}')
    
    if save2local:
        df.to_csv('OperatorAttendant_OuputHistRes_Certified.csv',index=False)
    
    return df

