# -*- coding:utf-8 -*-
##############################################################
# Created Date: Wednesday, September 2nd 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import random, urllib3, json, requests, math, plotly 
import pandas as pd 
import datetime as dt
import numpy as np
import plotly.figure_factory as ff
from time import sleep
from plotly import io as pio
from deap import algorithms
from datetime import datetime
import random,datetime,plotly,math
from itertools import combinations
from deap import base, creator, tools
import random, numpy,sys
import time

def generate3tables():
    Table_SchedulingInfo_New = pd.DataFrame()                   
    Table_Changeovers_New = pd.DataFrame()   
    Table_ShiftCalendar_New = pd.DataFrame()
    Table_SchedulingInfo_New_Extended = pd.DataFrame()

    LenOfSimulatedData = 100
    DataRange_StartOfStart_EndOfStart = 10
    DataDiff_StartDate_EndDate = 7
    ProcessingTime_Max = 300
    ProcessingTime_Min = 1
    ChangeOverTime_Max = 30
    ChangeOverTime_Min = 5
    ProductionLine_Count = 4
    Family_Count = 6
    Priority_Count = 3

    Families_List = []
    ProductionLines_List = []
    Priorities_List = []

    start_date = []
    end_date = []
    processing_time = []
    family_type = []
    ProductionLine = []
    workorder_num = []
    changeover_time = []
    Priority = []
    
    Families_List = [np.append(Families_List,"Family_"+str(i+1)).tolist() for i in range (Family_Count )]
    ProductionLines_List = [np.append(ProductionLines_List, int(i+1)).tolist() for i in range (ProductionLine_Count)]
    Priorities_List = [np.append(Priorities_List, str(i+1)).tolist() for i in range (Priority_Count)]
    newFamily_List = []
    for fly in Families_List:
        newFamily_List =  np.append(newFamily_List, fly) 
    Families_List = newFamily_List


    # Generate the Lists of Families_List and Production Lines
    start = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
    date_list = [(start + datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, DataRange_StartOfStart_EndOfStart)]

    for i in range(LenOfSimulatedData):
        start_date = np.append(start_date, random.choice(date_list))
        end_date = np.append(end_date,(datetime.datetime.strptime(random.choice(date_list), '%Y-%m-%d')+ 
            datetime.timedelta(days=DataDiff_StartDate_EndDate)).strftime("%Y-%m-%d"))
        processing_time = np.append(processing_time,random.randint(ProcessingTime_Min,ProcessingTime_Max))
        family_type = np.append(family_type, random.choice(Families_List))
        ProductionLine = np.append(ProductionLine, random.choice(ProductionLines_List))
        Priority = np.append(Priority, random.choice(Priorities_List))
        workorder_num =  np.append(workorder_num, i)

    for j in range(Family_Count):	
        changeover_time = np.append(changeover_time, random.randint(ChangeOverTime_Min,ChangeOverTime_Max))

    Table_SchedulingInfo_New["Start_date"] = start_date
    Table_SchedulingInfo_New["Due_date"] = end_date
    Table_SchedulingInfo_New["Processing_time"] = processing_time
    Table_SchedulingInfo_New["Family"] = family_type
    Table_SchedulingInfo_New["ProductionLine"] = ProductionLine
    Table_SchedulingInfo_New["Priority"] = Priority
    Table_SchedulingInfo_New["ChangeoverSort"] = Table_SchedulingInfo_New["Family"] 
    Table_SchedulingInfo_New["WorkOrderNum"] = workorder_num
    
    Lines = [i+1 for i in range(ProductionLine_Count)] 
    Possible_Com_Of_Lines = sum([list(map(list, combinations(Lines, i))) for i in range(len(Lines) + 1)], [])
    del Possible_Com_Of_Lines[0]

    WO_Num = 0
    for index, row in Table_SchedulingInfo_New.iterrows():
        OpLines = random.choice(Possible_Com_Of_Lines)
        Option_Lines_Len = len(OpLines)
        for i in range(Option_Lines_Len):
            Table_SchedulingInfo_New_Extended = Table_SchedulingInfo_New_Extended.append({'OptionalLine': OpLines[i],
                'BasicStartDate': row.Start_date,
                'DeliveryDate':row.Due_date,
                'ProcessingTimeMins':row.Processing_time+i,
                'FamilyName':row.Family,
                'ProductionLine': row.ProductionLine,
                'WorkOrderNum': row.WorkOrderNum,
                'MaterialPriority': row.ProductionLine,
                'ChangeoverSort':row.ChangeoverSort,
                'Priority':Priority}, ignore_index=True)

            WO_Num += 1
    Table_SchedulingInfo_New["Resource"] = Table_SchedulingInfo_New["Family"] 
    Table_SchedulingInfo_New["Task"] = Table_SchedulingInfo_New["ProductionLine"] 
    Table_SchedulingInfo_New["Start"] = Table_SchedulingInfo_New["Start_date"] 
    Table_SchedulingInfo_New["Finish"] = Table_SchedulingInfo_New["Due_date"] 
    color_dict = dict(zip(Table_SchedulingInfo_New.Resource.unique(),['rgb({},{},{})'.format(i[0],i[1],i[2]) 
        for i in list(np.random.randint(255, size = (len(Table_SchedulingInfo_New.Resource.unique()),3)))]))
    fig = ff.create_gantt(Table_SchedulingInfo_New.to_dict('records'), colors = color_dict, index_col='Resource', show_colorbar=True, group_tasks=True)
    
    Table_Changeovers_New['ToChangeOver'] = Families_List
    Table_Changeovers_New['MaxChangeOverTimeMin'] = changeover_time 
    # print(Table_Changeovers_New.ToChangeOver)
   
    for date in date_list:
        Table_ShiftCalendar_New = Table_ShiftCalendar_New.append({"ProductionDate":date,"ShiftAStart": "05:15:00", "ShiftAEnd":"15:20:00", "ShiftBStart":"15:30:00","ShiftBEnd":"01:35:00"}, ignore_index=True)
    # Table_SchedulingInfo_New_Extended.to_csv('Table_SchedulingInfo_New.csv',index=False)
    # Table_Changeovers_New.to_csv('Table_Changeovers_New.csv',index=False)
    # Table_ShiftCalendar_New.to_csv('Table_ShiftCalendar_New.csv',index=False)
    return Table_SchedulingInfo_New_Extended,Table_Changeovers_New,Table_ShiftCalendar_New

class ClosedLoopScheduling:

    def __init__(self):
        # plotly.io.orca.config.executable = '/Users/roche/anaconda3/pkgs/plotly-orca-1.3.1-1/orca.cmd'
        # plotly.io.orca.config.save()
        self.__Import_And_CleanData()            # This line would get the intial solution, and optional lines to chose for each WO
        self. HardConstraintPenalty = 150
    def __len__(self):
        return self.WO_SIZE

    def __Import_And_CleanData(self):
        JobID = random.randint(1,1000)
        
        self.Table_SchedulingInfo,self.Table_ChangeOverInfo,self.Table_CalendarInfo = generate3tables()

        self.Table_SchedulingInfo['ProductionLineCode_Cap'] = self.Table_SchedulingInfo.OptionalLine#.apply(lambda x: x.split('')[-1])
        self.Table_CalendarInfo["ProductionDate_ShiftA"] = pd.to_datetime(self.Table_CalendarInfo["ProductionDate"] +' '+ self.Table_CalendarInfo["ShiftAStart"])
        self.Table_CalendarInfo['ShiftAStart'] =  pd.to_datetime(self.Table_CalendarInfo['ShiftAStart'] )
        self.Table_CalendarInfo['ShiftAEnd'] =  pd.to_datetime(self.Table_CalendarInfo['ShiftAEnd'] )
        self.Table_CalendarInfo["ShiftA_deltaT_minutes"] =  ((self.Table_CalendarInfo["ShiftAEnd"] - self.Table_CalendarInfo["ShiftAStart"]).dt.total_seconds())/60
        self.Table_CalendarInfo["ShiftB_deltaT_minutes"] = self.Table_CalendarInfo["ShiftA_deltaT_minutes"] 
        
        FamilyGp_DupCount = self.Table_SchedulingInfo.groupby('FamilyName').size().sort_values(ascending=False).to_frame('DuplicateCount')    # save the results in a dataframe [FamilyName, DuplicateCount] 
        self.Schedule_Info =pd.DataFrame()
        for FamulyNameGroupItem, _ in FamilyGp_DupCount.iterrows():   
            df_grouped = self.Table_SchedulingInfo.loc[self.Table_SchedulingInfo.FamilyName == FamulyNameGroupItem]  # df_grouped.loc[~df_grouped.ChangeoverSort.isin(self.Table_ChangeOverInfo.ToChangeOver.tolist()), 'ChangeoverSort'] = '1020Other'
            self.Schedule_Info = self.Schedule_Info.append(df_grouped, ignore_index = True)
       
        self.Schedule_Info.assign(MaxChangeOverTimeMin="") 
        # 5.1. ACurrent_Start Maximum ChangeOver Time of each family to the self.Schedule_Info table
        for i, val in enumerate(self.Table_ChangeOverInfo.ToChangeOver.tolist()): 
            self.Schedule_Info.loc[self.Schedule_Info.ChangeoverSort == val, 'MaxChangeOverTimeMin'] = self.Table_ChangeOverInfo.MaxChangeOverTimeMin.iloc[i]
        # ----------------------- 6. Create a completely new table to save the scheduled work  (!!! 6.1. Sort WPT based on Family Group ) - #
        self.minor_ChangeOver_Mins = 2.53
        ## print('#---------------- 6.1. Sort WPT based on Family Group ---------------#') 
        self.Schedule_Info["Optional_Lines"] = self.Schedule_Info.ProductionLineCode_Cap
        # # ==================================== Objective Function Construction ======================================= #
        self.Unique_WO_Array = self.Schedule_Info['WorkOrderNum'].unique()
        self.WO_SIZE = len(self.Unique_WO_Array)
        Unique_WO_Df = pd.DataFrame({'WorkOrderNum':self.Unique_WO_Array})
        ## print("# 2D Matrics for each work order:O_Lines,P_Times,WP_Times ")
        O_Lines = [list((self.Schedule_Info['Optional_Lines'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()]
        P_Times = [list((self.Schedule_Info['ProcessingTimeMins'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()]
        ## print("# 2D-1. Zaro paCurrent_Starting to make sure all optionals lines have same number of lines")
        self.O_Lines_Array = np.array([i + [0]*(len(max(O_Lines, key=len))-len(i)) for i in O_Lines])
        self.P_Times_Array = np.array([i + [0]*(len(max(P_Times, key=len))-len(i)) for i in P_Times])
        ## print("# 2D-2. If an element equalt to 0, relace with previous value in the row")
        for idx, item in np.ndenumerate(self.O_Lines_Array):
            if item == 0:
                self.O_Lines_Array[(idx[0],idx[1])] = self.O_Lines_Array[(idx[0],idx[1]-1)] 
                self.P_Times_Array[(idx[0],idx[1])] = self.P_Times_Array[(idx[0],idx[1]-1)] 
        ## print("# 1D Matrics for each work order:self.CV_Times, self.CV_Sorts, self.Fmily_T, self.BStart_Dates, self.Del_Dates")
        self.Schedule_Info['BasicEndDate'] =  self.Schedule_Info['DeliveryDate'] 
        self.CV_Times = np.array([list(set(self.Schedule_Info['MaxChangeOverTimeMin'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()])
        self.CV_Sorts = np.array([list(set(self.Schedule_Info['ChangeoverSort'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()])
        self.Fmily_T = np.array([list(set(self.Schedule_Info['FamilyName'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()])
        self.BStart_Dates = np.array([list(set(self.Schedule_Info['BasicStartDate'].loc[self.Schedule_Info['WorkOrderNum'] == x['WorkOrderNum']])) for _, x in Unique_WO_Df.iterrows()])
      
    def Run_ToGetAllLines_Objectives(self,Chromosome_Solution):
        Performances_df = pd.DataFrame()
        line_viol = self.CandidateViolation(Chromosome_Solution) 
        for Line_Code in range(1,5):
            self.__Objectives_Of_Each_Line(Line_Code,Chromosome_Solution)
            Performances_df = Performances_df.append(pd.DataFrame({'LineName':'Line '+str(Line_Code),
                                                                'MakeSpanTime':(self.Line_Total_PT+self.Line_Total_CV_Times)/(60)},
                                                               index=[0]), ignore_index = True)
        MkSpan_Dif = round(Performances_df['MakeSpanTime'].max() - Performances_df['MakeSpanTime'].min(),2)
        return  150*line_viol+50*(MkSpan_Dif/24) 

    def Final_Run(self,Chromosome_Solution):
        print(Chromosome_Solution)
        Performances_df = pd.DataFrame()
        PT_Mini = 0
        line_viol = self.CandidateViolation(Chromosome_Solution) 
        self.OutputData_Of_Lines =pd.DataFrame()
        OutputData =pd.DataFrame()
        Unique_Lines = self.Schedule_Info.Optional_Lines.nunique()
        for Line_Code in range(1,Unique_Lines+1):
            Schedule_Of_The_Line,Start,Finish  = self.__FinalRun_Obj_Of_Each_Line_SaveData(Line_Code,Chromosome_Solution)
            self.OutputData_Of_Lines = self.OutputData_Of_Lines.append(Schedule_Of_The_Line)
            Schedule_Of_The_Line.Start = Start
            Schedule_Of_The_Line.Finish = Finish
            OutputData = OutputData.append(Schedule_Of_The_Line)
            Performances_df = Performances_df.append(pd.DataFrame({'LineName':'Line '+str(Line_Code),
                                                                 'FamilyAtDayStartFactor':1,
                                                                'ProcessingTime':self.Line_Total_PT/(60),
                                                                'ChangeoverTime':self.Line_Total_CV_Times/(60),
                                                                'MakeSpanTime':(self.Line_Total_PT+self.Line_Total_CV_Times)/(60)},
                                                               index=[0]), ignore_index = True)
        
        MkSpan_Dif = round(Performances_df['MakeSpanTime'].max() - Performances_df['MakeSpanTime'].min(),2)
        PT_Mini =round(Performances_df['ProcessingTime'].sum(),2)
        CVTimes_Mini =round(Performances_df['ChangeoverTime'].sum(),2)
        Performances_df = Performances_df.append(pd.DataFrame({'LineName':'AllLines',
                                                                'FamilyAtDayStartFactor':1,
                                                                'ProcessingTime':PT_Mini,
                                                                'ChangeoverTime':CVTimes_Mini,
                                                                'MakeSpanTime':(PT_Mini+CVTimes_Mini)},
                                                                index=[0]), ignore_index = True)
        single_Objective = 150*line_viol+50*(MkSpan_Dif/24)
        OutputData = OutputData.rename(columns={"Task": "LineName", "Start":"BasicStartDate", "Finish":"BasicEndDate", "Resource":"Family"})
        
    def Plot_Gantt_Chart(self):
        # ------------------------------- Ploting the results by using Plotly Gantt Chart ---------------------------------------------- #
        print(f'{"The shape of the OutputData_Of_Lines:  "}{self.OutputData_Of_Lines.shape[0]}')
        color_dict = dict(zip(self.OutputData_Of_Lines.Resource.unique(),['rgb({},{},{})'.format(i[0],i[1],i[2]) for i in list(np.random.randint(255, size = (len(self.OutputData_Of_Lines.Resource.unique()),3)))]))
        fig = ff.create_gantt(self.OutputData_Of_Lines.to_dict(orient = 'records'),
                            colors = color_dict,
                            index_col = "Resource",
                            title = "Genetic Algorithm based Optimization",
                            show_colorbar = True,
                            bar_width = 0.3,
                            showgrid_x = False,
                            showgrid_y = True,
                            show_hover_fill=True)
        
        fig_html = pio.to_html(fig)
        # fig.show()
        # print(fig_html)
        # fig.write_image(r"CLS_GanttChart.png") 
        return fig_html
         
    def CandidateViolation(self,Chromosome_Solution):
        line_viol = 0
        for idx, item in np.ndenumerate(Chromosome_Solution):
            if item not in self.O_Lines_Array[idx[0]]:
                line_viol += 1
        return line_viol        

    def __Objectives_Of_Each_Line(self,Line_Code,Chromosome_Solution):
            ## print('#---------------- 6.2. Reset the initial start and end -------------#')
        Line_Curr_End = self.Table_CalendarInfo.ProductionDate_ShiftA + pd.to_timedelta(self.minor_ChangeOver_Mins*60, unit='s') 
        Line_Curr_End = Line_Curr_End[0]
        Shift_AandB_Period = self.Table_CalendarInfo.ShiftA_deltaT_minutes.values[0] + self.Table_CalendarInfo.ShiftB_deltaT_minutes.values[0]
        ShiftBAPeriod = 220  # in mins  (3 hours 40 minutes)
        self.Line_CumMakeSpan = 0
        self.Line_Total_PT = 0
        self.Line_Total_CV_Times = 0
        Line_WO_Idxes = []
        Chromosome_Solution = np.array(Chromosome_Solution)
        for ii, item in np.ndenumerate(np.array(np.where(Chromosome_Solution == Line_Code))):
            Line_WO_Idxes.append(item)
        # 2D Matrics
        Line_CV_Sorts = self.CV_Sorts[(Line_WO_Idxes),0]
        self.Line_Families = self.Fmily_T[(Line_WO_Idxes),0]
        Line_CV_Times = self.CV_Times[(Line_WO_Idxes),0]
        ## print("6.2. Use all lines WorkOrder indexes to find total CV time and Family Sort Change ")
        Previous_CV = Line_CV_Sorts[0]
        self.CV_Times_Each_Order = []
        for CV_idx, CV_ele in np.ndenumerate(Line_CV_Sorts):
            if CV_ele != Previous_CV:
                self.Line_Total_CV_Times += Line_CV_Times[CV_idx]
                self.CV_Times_Each_Order = np.append(self.CV_Times_Each_Order,Line_CV_Times[CV_idx])
            else:
                self.Line_Total_CV_Times += self.minor_ChangeOver_Mins
                self.CV_Times_Each_Order = np.append(self.CV_Times_Each_Order,self.minor_ChangeOver_Mins)
            Previous_CV = CV_ele
        ## print("6.3.=========== Use all lines WorkOrder indexes to find the total processing time ================= ")
        self.P_Times_Each_Order = []
        self.Line_Late_Falg = []
        curr_line_idx = 0
        for _, WO_idx in np.ndenumerate(Line_WO_Idxes):
            for i in np.where(self.O_Lines_Array[WO_idx]==Line_Code):
                for j in i:
                    curr_line_idx=j
            self.Line_Total_PT += self.P_Times_Array[(WO_idx,curr_line_idx)]
            self.P_Times_Each_Order = np.append(self.P_Times_Each_Order,self.P_Times_Array[(WO_idx,curr_line_idx)]) 
    
    def __FinalRun_Obj_Of_Each_Line_SaveData(self,Line_Code,Chromosome_Solution):
        ## print('#---------------- 6.2. Reset the initial start and end -------------#')
        Line_Curr_End = self.Table_CalendarInfo.ProductionDate_ShiftA + pd.to_timedelta(self.minor_ChangeOver_Mins*60, unit='s')
        Line_Curr_End = Line_Curr_End[0]
        self.PlanStartTime = Line_Curr_End
        intial_start_date = Line_Curr_End
        Shift_AandB_Period = self.Table_CalendarInfo.ShiftA_deltaT_minutes.values[0] + self.Table_CalendarInfo.ShiftB_deltaT_minutes.values[0]
        Shift_A_Period = self.Table_CalendarInfo.ShiftA_deltaT_minutes.values[0]
        ShiftBAPeriod = 220  # in mins  (3 hours 40 minutes)
        self.Line_CumMakeSpan = 0
        self.Line_Total_PT = 0
        self.Line_Total_CV_Times = 0
        ## print("4. Obtain the line work order indexes for the line by determine at what positon line 1/2/3/4 is used")
        Line_WO_Idxes = []
        Chromosome_Solution = np.array(Chromosome_Solution)
        for ii, item in np.ndenumerate(np.array(np.where(Chromosome_Solution == Line_Code))):
            Line_WO_Idxes.append(item)
        ## print("5. Find the processing time, setup time, CV sorts, families, line calendar start time and delivery time for each line")
        Line_WO_Num = self.Unique_WO_Array[(Line_WO_Idxes)]
        # 2D Matrics
        Line_CV_Sorts = self.CV_Sorts[(Line_WO_Idxes),0]
        self.Line_Families = self.Fmily_T[(Line_WO_Idxes),0]
        Line_CV_Times = self.CV_Times[(Line_WO_Idxes),0]
 
        Previous_CV = Line_CV_Sorts[0]
        self.CV_Times_Each_Order = []
        for CV_idx, CV_ele in np.ndenumerate(Line_CV_Sorts):
            if CV_ele != Previous_CV:
                self.Line_Total_CV_Times += Line_CV_Times[CV_idx]
                self.CV_Times_Each_Order = np.append(self.CV_Times_Each_Order,Line_CV_Times[CV_idx])
            else:
                self.Line_Total_CV_Times += self.minor_ChangeOver_Mins
                self.CV_Times_Each_Order = np.append(self.CV_Times_Each_Order,self.minor_ChangeOver_Mins)
            Previous_CV = CV_ele
        ## print("6.3. Use all lines WorkOrder indexes to find the total processing time ")
        self.P_Times_Each_Order = []
        curr_line_idx = 0
        for _, WO_idx in np.ndenumerate(Line_WO_Idxes):
            for i in np.where(self.O_Lines_Array[WO_idx]==Line_Code):
                for j in i:
                    curr_line_idx=j
            self.Line_Total_PT += self.P_Times_Array[(WO_idx,curr_line_idx)]
            self.P_Times_Each_Order = np.append(self.P_Times_Each_Order,self.P_Times_Array[(WO_idx,curr_line_idx)])
        ## print("# 6.3.1. Define a dataframe to save all results for plotting")
        LineSequence = 0
        Schedule_Of_The_Line =pd.DataFrame()
        for P_Time_idx, P_Time_ele in np.ndenumerate(self.P_Times_Each_Order):
            Line_Remainder = self.Line_CumMakeSpan%(Shift_AandB_Period)
            Line_Curr_CV_Time = self.CV_Times_Each_Order[P_Time_idx]
            Line_Curr_P_Time = self.P_Times_Each_Order[P_Time_idx]
            self.Line_CumMakeSpan += Line_Curr_P_Time + Line_Curr_CV_Time 
            if (Line_Remainder + Line_Curr_P_Time) > Shift_AandB_Period: 
                SecondP_of_P_Time = Line_Remainder + Line_Curr_P_Time-Shift_AandB_Period  
                FirstP_of_P_Time  = Line_Curr_P_Time - SecondP_of_P_Time  
                Line_Curr_Start =  Line_Curr_End + pd.to_timedelta((Line_Curr_CV_Time)*60, unit='s')
                Line_Curr_End   =  Line_Curr_Start + pd.to_timedelta((FirstP_of_P_Time*60), unit='s')     
                Schedule_Of_The_Line = Schedule_Of_The_Line.append(pd.DataFrame({'Task':'Line '+str(Line_Code), 
                                                                                           'Start':Line_Curr_Start,
                                                                                           'Finish':Line_Curr_End,
                                                                                           'ProcessingTimeInMins':FirstP_of_P_Time,
                                                                                           'WorkOrderNum':str(Line_WO_Num[P_Time_idx]) ,
                                                                                           'Resource': self.Line_Families[P_Time_idx], 
                                                                                           'ChangeoverTimeInMins':Line_Curr_CV_Time,
                                                                                           'WorkOrderSplitCounter':0,
                                                                                            },
                                                                                            index=[0]), ignore_index = True)
 
                Line_Curr_Start_b = Line_Curr_End + pd.to_timedelta((ShiftBAPeriod)*60, unit='s')
                Line_Curr_End   = Line_Curr_Start_b + pd.to_timedelta(SecondP_of_P_Time*60, unit='s')
                Schedule_Of_The_Line = Schedule_Of_The_Line.append(pd.DataFrame({'Task':'Line '+str(Line_Code), 
                                                                                           'Start':Line_Curr_Start_b,
                                                                                           'Finish':Line_Curr_End,
                                                                                           'ProcessingTimeInMins':Line_Curr_P_Time, 
                                                                                           'WorkOrderNum':str(Line_WO_Num[P_Time_idx]) ,
                                                                                           'Resource': self.Line_Families[P_Time_idx], 
                                                                                           'ChangeoverTimeInMins':0,
                                                                                           'WorkOrderSplitCounter':0,
                                                                                           },
                                                                                           index=[LineSequence]), ignore_index = True)
 
            else:
                Line_Curr_Start = Line_Curr_End    + pd.to_timedelta(Line_Curr_CV_Time*60, unit='s')
                Line_Curr_End   = Line_Curr_Start  + pd.to_timedelta((Line_Curr_P_Time*60), unit='s')
                Schedule_Of_The_Line = Schedule_Of_The_Line.append(pd.DataFrame({'Task':'Line '+str(Line_Code), 
                                                                                           'Start':Line_Curr_Start,
                                                                                           'Finish':Line_Curr_End,
                                                                                           'ProcessingTimeInMins':Line_Curr_P_Time,
                                                                                           'WorkOrderNum':str(Line_WO_Num[P_Time_idx]),
                                                                                           'Resource': self.Line_Families[P_Time_idx], 
                                                                                           'ChangeoverTimeInMins':Line_Curr_CV_Time,
                                                                                           'WorkOrderSplitCounter':0,
                                                                                           },
                                                                                           index=[LineSequence]), ignore_index = True)
 
            # ----------------------------------------- Check Performances - Lateness --------------------------------- #
            Line_Curr_End_Date =  np.array(Line_Curr_End, dtype='datetime64[D]')
            Line_Curr_Start_Date = np.array(Line_Curr_Start, dtype='datetime64[D]')                      ## print("6.5.1. Compute the late count for the order")
            prevWONumber = Line_WO_Num[P_Time_idx] 
            LineSequence += 10
           
        Start = pd.DataFrame()
        Finish = pd.DataFrame()
        # PlanDeliveryDate = pd.DataFrame()
        for idx,rows in Schedule_Of_The_Line.iterrows():
            Start = Start.append(pd.DataFrame({'Start':Schedule_Of_The_Line.Start[idx].strftime('%Y/%m/%d %I:%M:%S %p') },index=[idx]), ignore_index = True)
            Finish =  Finish.append(pd.DataFrame({'Finish':Schedule_Of_The_Line.Finish[idx].strftime('%Y/%m/%d %I:%M:%S %p')},index=[idx]), ignore_index = True)
        return Schedule_Of_The_Line,Start,Finish
    
    def initial_solution(self):
        unique_elements,_ = np.unique(self.O_Lines_Array, return_counts=True)
        self.NumberOfLines = len(unique_elements)
        Chromosome_Solution = []
        for row in self.O_Lines_Array: 
            Chromosome_Solution.append(row[random.randint(0, self.NumberOfLines-1)])
        Chromosome_Solution = np.array(Chromosome_Solution)
        print(f'{"Chromosome_Solution shape: "}{len(Chromosome_Solution)}')
        return Chromosome_Solution

def eaSimpleWithElitism(population, toolbox, cxpb, mutpb, ngen, stats=None,
             halloffame=None, verbose=__debug__):
    """This algorithm is similar to DEAP eaSimple() algorithm, with the modification that
    halloffame is used to implement an elitism mechanism. The individuals contained in the
    halloffame are directly injected into the next generation and are not subject to the
    genetic operators of selection, crossover and mutation.
    """
    logbook = tools.Logbook()
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")

    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # Begin the generational process
    for gen in range(1, ngen + 1):
        # print(gen)

        # Select the next generation individuals
        offspring = toolbox.select(population, len(population) - hof_size)

        # Vary the pool of individuals
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # add the best back to population:
        offspring.extend(halloffame.items)

        # Update the hall of fame with the generated individuals
        halloffame.update(offspring)

        # Replace the current population by the offspring
        population[:] = offspring

        # Append the current generation statistics to the logbook
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook

class GA_CLS_slover:
    def __init__(self,fileName = "Table_SchedulingInfo_New.csv",MAX_GENERATIONS=10):
        
        # plotly.io.orca.config.executable = '/Users/roche/anaconda3/pkgs/plotly-orca-1.3.1-1/orca.cmd'
        # plotly.io.orca.config.save()
        
        self.fileName = fileName
        self.MAX_GENERATIONS = MAX_GENERATIONS
    
    def Not_Main(self):
        MAX_GENERATIONS = self.MAX_GENERATIONS
        POPULATION_SIZE = 100
        P_CROSSOVER = 0.9
        P_MUTATION = 0.1
        HALL_OF_FAME_SIZE = 5
        RANDOM_SEED = 42   

        # Get the information of total unique lines 
        # "Table_SchedulingInfo_New.csv"
        # df = pd.read_csv(self.fileName)
        a,b,c = generate3tables()
        df = a
        
        max_line = df['OptionalLine'].nunique()
        random.seed(RANDOM_SEED)
        toolbox = base.Toolbox()
        CloseLS = ClosedLoopScheduling()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))        # define a single objective, maximizing fitness strategy:
        creator.create("Individual", list, fitness=creator.FitnessMin)     # create the Individual class based on list:
        toolbox.register("Integers", random.randint, 1, max_line)  
        toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.Integers, len(CloseLS))   # create the individual operator to fill up an Individual instance:
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator) # create the population operator to generate a list of individuals:
        def getCost(individual):                                           # fitness calculation: cost of the suggested olution
            return CloseLS.Run_ToGetAllLines_Objectives(individual),
        toolbox.register("evaluate", getCost)                                                    
        toolbox.register("select", tools.selTournament, tournsize=3)
        toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0/len(CloseLS))
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(CloseLS))
        toolbox.register("mutate", tools.mutUniformInt, low=1, up=max_line, indpb=1.0/len(CloseLS))
            
        
        t0= time.process_time()
        population = toolbox.populationCreator(n=POPULATION_SIZE)     # create initial population (generation 0):
        stats = tools.Statistics(lambda ind: ind.fitness.values)      # prepare the statistics object:
        stats.register("min", np.min)
        stats.register("avg", np.mean)
        hof = tools.HallOfFame(HALL_OF_FAME_SIZE)                     # define the hall-of-fame object:
        population, logbook = eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)
        # =========================== print best solution found: ======================================================== #
        best = hof.items[0]
        minFitnessValues, meanFitnessValues = logbook.select("min", "avg")         # extract statistics:  
        CloseLS.Final_Run(best)
        print("Time elapsed: ", (time.process_time()- t0)/60)
        fig_html = CloseLS.Plot_Gantt_Chart()
        return fig_html



