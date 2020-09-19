## Generate simulation data for scheduling
## Prepared by: Meiling He
## Date: 08/12/2020
from datetime import datetime
import pandas as pd
import random,datetime,plotly,math
import numpy as np
import plotly.figure_factory as ff 
from time import sleep
from itertools import combinations
import plotly.io as pio
import os

class Hackathon_GanttChart:
    
    def __init__(self,save2db_path=None):
        """save2db_path : if provided, tables will saved to the path dir    """
        
        self.save2db_path = save2db_path
        
        self.__dataPrepared()
        self.generate_shiftcalendar()
        self.generate_changeovers()
        self.Table_A,self.Table_B = self.generate_SchedulingInfo_newExtend()

    def __dataPrepared(self) -> None:
        self.LenOfSimulatedData = 100
        self.DataRange_StartOfStart_EndOfStart = 10
        self.DataDiff_StartDate_EndDate = 7
        self.ProcessingTime_Max = 300
        self.ProcessingTime_Min = 1
        self.ChangeOverTime_Max = 30
        self.ChangeOverTime_Min = 5
        self.ProductionLine_Count = 6
        self.Family_Count = 6
        self.Priority_Count = 3
        ## ------------------------------------ Initializating Lists of Variables ------------------------------------------ ##

        self.Families = []
        self.ProductionLines = []
        self.Priorities = []
        self.start_date = []
        self.end_date = []
        self.processing_time = []
        self.family_type = []
        self.ProductionLine = []
        self.workorder_num = []
        self.changeover_time = []
        # Generate the Lists of Families and Production Lines
        self.Families = [np.append(self.Families,"Family_"+str(i+1)).tolist() for i in range (self.Family_Count )]
        self.ProductionLines = [np.append(self.ProductionLines, int(i+1)).tolist() for i in range (self.ProductionLine_Count)]
        # ProductionLineCode = [np.append(ProductionLineCode, str(i)).tolist() for i in range (ProductionLine_Count+1)]

        self.Priorities = [np.append(self.Priorities,"P"+str(i+1)).tolist() for i in range (self.Priority_Count)]
        # print(Families)
        # print(ProductionLines)
        # print(Priorities)

        # Generate the Lists of Families and Production Lines
        self.start = datetime.datetime.strptime(datetime.datetime.today().strftime("%Y-%m-%d"), "%Y-%m-%d")
        self.date_list = [(self.start + datetime.timedelta(days=x)).strftime("%Y-%m-%d") for x in range(0, self.DataRange_StartOfStart_EndOfStart)]

        for i in range(self.LenOfSimulatedData):
            self.start_date = np.append(self.start_date, random.choice(self.date_list))
            self.end_date = np.append(self.end_date,(datetime.datetime.strptime(random.choice(self.date_list), '%Y-%m-%d')+ 
                datetime.timedelta(days=self.DataDiff_StartDate_EndDate)).strftime("%Y-%m-%d"))
            self.processing_time = np.append(self.processing_time,random.randint(self.ProcessingTime_Min,self.ProcessingTime_Max))
            self.family_type = np.append(self.family_type, random.choice(self.Families))
            self.ProductionLine = np.append(self.ProductionLine, random.choice(self.ProductionLines))
            self.workorder_num = np.append(self.workorder_num,i)

        for j in range(self.Family_Count):  
            self.changeover_time = np.append(self.changeover_time, random.randint(self.ChangeOverTime_Min,self.ChangeOverTime_Max))
            pass

    def generate_SchedulingInfo_newExtend(self) ->"list of Tables":
        # plotly.io.orca.config.executable = '/Users/mhe2/Anaconda3/orca.cmd'
        # plotly.io.orca.config.save()
        # Table_SchedulingInfo = pd.read_csv("getScheduleInfoData.csv")
        # Table_Changeovers = pd.read_csv("getChangeovers.csv")
        # Table_ShiftCalendar = pd.read_csv("getShiftCalendar.csv")
        Table_SchedulingInfo_New = pd.DataFrame()     
                     

        Table_SchedulingInfo_New["Start_date"] = self.start_date
        Table_SchedulingInfo_New["Due_date"] = self.end_date
        Table_SchedulingInfo_New["Processing_time"] = self.processing_time
        Table_SchedulingInfo_New["Family"] = self.family_type
        Table_SchedulingInfo_New["ProductionLine"] = self.ProductionLine
        Table_SchedulingInfo_New["Workorder_num"] = self.workorder_num



    
        ## Extend the Scheduling Info table to have two columns: Optional lines, Processing time of the line
     

        Lines = [i+1 for i in range(self.ProductionLine_Count)] 
        Possible_Com_Of_Lines = sum([list(map(list, combinations(Lines, i))) for i in range(len(Lines) + 1)], [])
        del Possible_Com_Of_Lines[0]
        #print(Possible_Com_Of_Lines)


        Table_SchedulingInfo_New_Extended = pd.DataFrame()

        for index, row in Table_SchedulingInfo_New.iterrows():
            OpLines = random.choice(Possible_Com_Of_Lines)
            Option_Lines_Len = len(OpLines)
            for i in range(Option_Lines_Len):
                Table_SchedulingInfo_New_Extended = Table_SchedulingInfo_New_Extended.append(
                    {'OptionalLine': OpLines[i],
                    'Start_date': row.Start_date,
                    'Due_date':row.Due_date,
                    'Processing_time':row.Processing_time+i,
                    'Family':row.Family,
                    'ProductionLine': row.ProductionLine,
                    'Workorder_num': row.Workorder_num}, ignore_index=True)

        if self.save2db_path:
            path_out_1 = os.path.join(self.save2db_path,'Table_SchedulingInfo_New.csv')
            path_out_2 = os.path.join(self.save2db_path,'Table_SchedulingInfo_New_Extended.csv')
            Table_SchedulingInfo_New.to_csv(path_out_1,index=False)
            Table_SchedulingInfo_New_Extended.to_csv(path_out_2,index=False)

        Table_SchedulingInfo_New["Resource"] = Table_SchedulingInfo_New["Family"] 
        Table_SchedulingInfo_New["Task"] = Table_SchedulingInfo_New["ProductionLine"] 
        Table_SchedulingInfo_New["Start"] = Table_SchedulingInfo_New["Start_date"] 
        Table_SchedulingInfo_New["Finish"] = Table_SchedulingInfo_New["Due_date"] 

        return [Table_SchedulingInfo_New,Table_SchedulingInfo_New_Extended]

    def generate_gantt(self) ->"gantt_html":
        Table_SchedulingInfo_New = self.Table_A
        color_dict = dict(zip(Table_SchedulingInfo_New.Resource.unique(),['rgb({},{},{})'.format(i[0],i[1],i[2]) 
            for i in list(np.random.randint(255, size = (len(Table_SchedulingInfo_New.Resource.unique()),3)))]))
        fig = ff.create_gantt(Table_SchedulingInfo_New.to_dict('records'), colors = color_dict, index_col='Resource', show_colorbar=True, group_tasks=True)
        
        fig.update_layout(template="presentation")

        fig_html = pio.to_html(fig)
        #print(fig_html)
        #fig.show()
        return fig_html

    def generate_changeovers(self) -> pd.DataFrame:
        Table_Changeovers_New = pd.DataFrame()   
        Table_Changeovers_New['ToChangeOver'] = self.Families
        Table_Changeovers_New['MaxChangeOverTimeMin'] = self.changeover_time 
        #print(Table_Changeovers_New)
        if self.save2db_path:
            path_out = os.path.join(self.save2db_path,'Table_Changeovers_New.csv')
            Table_Changeovers_New.to_csv(path_out,index=False)
        return Table_Changeovers_New

    def generate_shiftcalendar(self) -> pd.DataFrame:

        Table_ShiftCalendar_New = pd.DataFrame()
        
        Table_ShiftCalendar_New["ShiftAStartTime"] = "05:15:00"
        Table_ShiftCalendar_New["StiftAEndTime"] = "15:20:00"
        Table_ShiftCalendar_New["ShiftBStartTime"] = "15:30:00"
        Table_ShiftCalendar_New["ShiftBEndTime"] = "01:35:00"

        if self.save2db_path:
            path_out = os.path.join(self.save2db_path,'Table_ShiftCalendar_New.csv')
            Table_ShiftCalendar_New.to_csv(path_out,index=False)
        return Table_ShiftCalendar_New


Hackathon_GanttChart().generate_gantt()

