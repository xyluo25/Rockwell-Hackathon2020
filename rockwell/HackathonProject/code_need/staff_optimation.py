# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, September 19th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


# -*- coding:utf-8 -*-
##############################################################
# Created Date: Saturday, September 19th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

from deap import tools
from deap import algorithms
from deap import base
from deap import creator
import random
import datetime 
import pandas as pd 
import datetime as dt
import numpy as np
import plotly.figure_factory as ff
import plotly
import math
import json 
from datetime import date, timedelta
import calendar 
import numpy
import matplotlib.pyplot as plt
import seaborn as sns

plotly.io.orca.config.executable = '/Users/mhe2/Anaconda3/orca.cmd'
plotly.io.orca.config.save()

random.seed(30)

inputFileName = "ManufacturingOptimization_Dataset.xlsx"

def createTable(fileName):
    
    df_OperatorAttendant = pd.read_excel(open(fileName, 'rb'), sheet_name='OperatorAttendant') 

    August3 = datetime.datetime(2020,8,3)
    August10 = datetime.datetime(2020,8,10)

    df_OperatorAttendant['WK_START_DATE'] = pd.to_datetime(df_OperatorAttendant['WK_START_DATE'], infer_datetime_format=True)
    df_OperatorAttendant = df_OperatorAttendant[(df_OperatorAttendant['WK_START_DATE'] == August3)|(df_OperatorAttendant['WK_START_DATE'] == August10)]
    df_OperatorAttendant = df_OperatorAttendant[(df_OperatorAttendant['PAYCODENAME'] == 'Regular') ]

    # print(f'{"Number of Uniques Employees in table OperatorAttendant: (08/03/2020 - 08/16/2020)"}{df_OperatorAttendant.USER_ID_H.nunique()}')
    # print('\n')


    df_OperatorAttendant = df_OperatorAttendant[['USER_ID_H','DAY1','WK_START_DATE', 'WK_END_DATE', 'PAYCODENAME', 'TOT_REG_HRS']]
    df_OperatorAttendant = df_OperatorAttendant.sort_values(by=['USER_ID_H','WK_START_DATE'])

    # 
    # =================================================== Table Sheet OutputHistRes =================================================================== #
    df_OuputHistRes = pd.read_excel(open(fileName, 'rb'), sheet_name='OutputHistRes') 
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
    # =================================================== Table Sheet Certifiedification&Shift =================================================================== #
    df_Certified = pd.read_excel(open(fileName, 'rb'), sheet_name='EmployeeCertification&Shift') 
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
                    how='inner', 
                    indicator=True)


    Merge_OuputHistRes_Certified.drop(['STD_DEV_SEC', 'CX10_SEC','CX25_SEC','CX50_SEC','CX65_SEC','CX75_SEC','CERTIFICATE_ID_H'
        ,'CERTIFICATE_LEVEL  (4=certified; 1=not yet certified)','CREATION_TIME','EXPIRATION_DATE','Work Center Certification requirement','WC_NAME_H'
    ], axis='columns', inplace=True)

    # print(f'{"Total Count of Employees in Joined Certified and OuputHistRes: "}{Merge_OuputHistRes_Certified.USER_ID_H.nunique()}')
    # print('\n')


    # =================================================== Out Join table:Certifiedification,OutputHistRes,OperatorAttendant =================================================================== #
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


    rowsCount = []

    for i in range(len(df)):
        try:
            if float(df.loc[i,"WC_NAME"]):
                rowsCount.append(i)

                # if df.loc[i,"CERTIFICATE_ID"] == "Pack":
                #     df.loc[i,"WC_NAME"] = "PACK_"+ np.random.choice(["L1","L2","L3","L4"])
                # elif df.loc[i,"CERTIFICATE_ID"] == "Assembly and Test":
                #     df.loc[i,"WC_NAME"] = "ASSY_"+ np.random.choice(["L1","L2","L3","L4"])
                # else:
                #     pass

        except Exception as err:
            # not a NaN value
            pass

        try:
            if float(df.loc[i,"Shift"]):
                rowsCount.append(i)
                # df.loc[i,"Shift"] = np.random.choice(["ShiftA","ShiftB"])
        except Exception as err:
            # not a NaN value
            pass

        try:
            if float(df.loc[i,"PART_NUMBER_H"]):
                rowsCount.append(i)
                # df.loc[i,"PART_NUMBER_H"] = np.random.choice(list(df.PART_NUMBER_H.unique())[:-1])
        except Exception as err:
            # not a NaN value
            pass

        try:
            if df.loc[i,"AVG_SEC"]==0:
                rowsCount.append(i)
                # df.loc[i,"AVG_SEC"] = np.random.choice(list(df.groupby('PART_NUMBER_H')['AVG_SEC'].mean()))
        except Exception as err:
            # not a NaN value
            pass

    df.drop(df.index[rowsCount])

    df.loc[(df['DAY1'].str.contains('friday'))|(df['DAY1'].str.contains('saturday'))|(df['DAY1'].str.contains('sunday')), 'Shift'] =  "ShiftC"
    # df.loc[(df[""] == ' '), 'Shift'] =  np.random.choice(["ShiftA","ShiftB"])


    df.drop(['CERTIFICATE_ID','_merge'], axis='columns', inplace=True)
    df = df[df.WK_Date != 'o']

    # print(f'{"Number of Uniques Employees in table OperatorAttendant_OuputHistRes_Certified: "}{df.USER_ID_H.nunique()}')
    # df.to_csv('OperatorAttendant_OuputHistRes_Certified.csv',index=False)

    # print('\n')
    return df

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

class staffSchedulingProblem:
    """This class encapsulates the staff Scheduling problem
    """
    def __init__(self, hardConstraintPenalty,fileNAME):
        ## We start to putin Staff information here for optimization
        ## Load scheduling data and split the data to shiftssssss --- 
        df = pd.read_excel(open(fileNAME, 'rb'), sheet_name='SchAug3-11') 
         
        df_Line1 = df.loc[df['LineName'].str.contains("Line 1")] 
        df_Line2 = df.loc[df['LineName'].str.contains("Line 2")] 
        df_Line3 = df.loc[df['LineName'].str.contains("Line 3")] 
        df_Line4 = df.loc[df['LineName'].str.contains("Line 4")] 

        ShitfA_Start = datetime.time(5, 15, 00, 00)
        ShitfA_End = datetime.time(15, 20, 00, 00)

        ShitfB_Start = datetime.time(15, 30, 00, 00)
        ShitfB_End = datetime.time(1, 35, 00, 00)

        ShitfC_Start = datetime.time(4, 45, 00, 00)
        ShitfC_End = datetime.time(16, 35, 00, 00)
         
        Line1_MaxTime = max (df_Line1.BasicEndDate)
        Line1_MinTime = min (df_Line1.BasicEndDate)

        Line2_MaxTime = max (df_Line2.BasicEndDate)
        Line2_MinTime = min (df_Line2.BasicEndDate)

        Line3_MaxTime = max (df_Line3.BasicEndDate)
        Line3_MinTime = min (df_Line3.BasicEndDate)

        Line4_MaxTime = max (df_Line4.BasicEndDate)
        Line4_MinTime = min (df_Line4.BasicEndDate)
         
        def findDay(date): 
            born = date.weekday() 
            return (calendar.day_name[born]) 
         
        TwoShiftWeekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        OneShiftWeekdays = ["Friday", "Saturday", "Sunday"]

        Shift_List = []

        # Get the shift A time: 05:15:00 - 15:20:00
        # Get the shift B time: 15:30:00 - 01:35:00
        # Get the shift C time: 04:45:00 - 16:35:00
        ## Calculate the total shift in between largest day and smalleest day
        smallest_day = min(df.BasicStartDate)
        largest_day = max(df.BasicEndDate)
         
        delta_days = (datetime.datetime.date(largest_day) - datetime.datetime.date(smallest_day) + timedelta(days=1)).days       # as timedelta
        shift_counts = 0
        day = smallest_day

        headList = []
        while (day <= largest_day + timedelta(days=1)):
            if findDay(day) in TwoShiftWeekdays:
                shift_counts += 2
                headList.append("ShiftA")
                headList.append("ShiftB")
                
            else:
                shift_counts += 1
                headList.append("ShiftC")
            day = day + timedelta(days=1)


        def DetermineTheShiftOfTheDay(MinTime, MaxTime):
            Shift_List = []
            if findDay(datetime.datetime.date(MinTime)) in TwoShiftWeekdays:
                if (datetime.datetime.time(MinTime) >= ShitfA_Start) and (datetime.datetime.time(MinTime) <= ShitfA_Start):
                    Shift_List.append("Shift A")
                    Shift_List.append("Shift B")
                else:
                    Shift_List.append("Shift B")
            if findDay(datetime.datetime.date(MinTime)) in OneShiftWeekdays:
                Shift_List.append("Shift C")

            if findDay(datetime.datetime.date(MaxTime)) in TwoShiftWeekdays:
                if (datetime.datetime.time(MaxTime) >= ShitfA_Start) and (datetime.datetime.time(MaxTime) <= ShitfA_Start):
                    Shift_List.append("Shift A")
                else:
                    Shift_List.append("Shift A")
                    Shift_List.append("Shift B")

            if findDay(datetime.datetime.date(MaxTime)) in OneShiftWeekdays:
                Shift_List.append("Shift C")

            MiddleDay_ShiftList = []
            delta = MaxTime - MinTime       # as timedelta
         
            if (delta.days - 1)>0:
                # print((delta.days - 1))

                for days_to_add in range(1,delta.days):
                    added_day = MinTime + timedelta(days=days_to_add)
                    if findDay(datetime.datetime.date(added_day)) in TwoShiftWeekdays:
                        MiddleDay_ShiftList.append("Shift A")
                        MiddleDay_ShiftList.append("Shift B")
                    else:
                        MiddleDay_ShiftList.append("Shift C")


            Shift_List[1:1] = MiddleDay_ShiftList
            
            static = 8
            try:
                # if ShiftC in list
                ind_c = Shift_List.index("Shift C")
                
                Shift_List = [0]*(static-ind_c) + Shift_List
                
                Shift_List = Shift_List + [0]*(15-len(Shift_List))
            except Exception as err:
                startDay = findDay(datetime.datetime.date(MinTime))
                
                # "Monday", "Tuesday", "Wednesday", "Thursday"
                if startDay == "Monday":
                    if Shift_List[0] == "Shift B":
                        # if delta.days >= 2:
                        Shift_List = [0]*1 + Shift_List
                        
                    Shift_List = Shift_List + [0]*(15-len(Shift_List))
                    
                if startDay == "Tuesday":
                    if Shift_List[0] == "Shift B":
                         Shift_List = [0]*3 + Shift_List
                    Shift_List = Shift_List + [0]*(15-len(Shift_List))
            
                    
                if startDay == "Wednesday":
                    if Shift_List[0] == "Shift B":
                         Shift_List = [0]*5 + Shift_List
                    Shift_List = Shift_List + [0]*(15-len(Shift_List))
                    
                if startDay == "Thursday":
                    if Shift_List[0] == "Shift B":
                         Shift_List = [0]*7 + Shift_List
                    Shift_List = Shift_List + [0]*(15-len(Shift_List))

            return Shift_List


        Line1_Shift_List = DetermineTheShiftOfTheDay(Line1_MinTime,Line1_MaxTime) 
        Line2_Shift_List = DetermineTheShiftOfTheDay(Line2_MinTime,Line2_MaxTime) 
        Line3_Shift_List = DetermineTheShiftOfTheDay(Line3_MinTime,Line3_MaxTime) 
        Line4_Shift_List = DetermineTheShiftOfTheDay(Line4_MinTime,Line4_MaxTime) 

 

        def replace(a,lineN= 1):
            b = []
            for i in a:
                if i != 0:
                    b.append(lineN)
                else:
                    b.append(i)
            return b

        Line1_Shift_List = replace(Line1_Shift_List,lineN= 1)
        Line2_Shift_List = replace(Line2_Shift_List,lineN= 2)
        Line3_Shift_List = replace(Line4_Shift_List,lineN= 3)    
        Line4_Shift_List = replace(Line4_Shift_List,lineN= 4)


        df = pd.DataFrame([Line1_Shift_List,Line2_Shift_List,Line3_Shift_List,Line4_Shift_List])
        df.columns = headList
        # print(df)
        self.Lines_With_Work = df




        # df_staff = pd.read_csv("OperatorAttendant_OuputHistRes_Certified.csv")
        df_staff = createTable(fileNAME)
        
        staff_ids_counts = df_staff.USER_ID_H.nunique()
        staff_ids = df_staff.USER_ID_H.unique()
        print(staff_ids_counts)
        # a = k
        df = pd.read_excel(open(fileNAME, 'rb'), sheet_name='SchAug3-11') 
        def findDay(date): 
            born = date.weekday() 
            return (calendar.day_name[born]) 
         
        TwoShiftWeekdays = ["Monday", "Tuesday", "Wednesday", "Thursday"]
        OneShiftWeekdays = ["Friday", "Saturday", "Sunday"]
 
        ## Calculate the total shift in between largest day and smalleest day
        smallest_day = min(df.BasicStartDate)
        largest_day = max(df.BasicEndDate)
         
        delta_days = (datetime.datetime.date(largest_day) - datetime.datetime.date(smallest_day) + timedelta(days=1)).days       # as timedelta
        shift_counts = 0
        day = smallest_day
        while (day <= largest_day + timedelta(days=1)):
            if findDay(day) in TwoShiftWeekdays:
                shift_counts += 2
            else:
                shift_counts += 1
            day = day + timedelta(days=1)


        self.staff_ids_counts =  staff_ids_counts
        self.shift_counts =  shift_counts

        self.shiftPreference  = np.random.randint(1, size=(self.staff_ids_counts*self.shift_counts)) #[x for x in range(self.staff_ids_counts*self.shift_counts)] 
        self.hardConstraintPenalty = hardConstraintPenalty
        self.staffs = ["Employee_%s"%(i+1) for i in range(staff_ids_counts)]

        self.shiftMin = [2, 2]
        self.shiftMax = [3, 3]

        # max shifts per week allowed for each staff
        self.maxShiftsPerWeek = 5

        # number of weeks we create a schedule for:
        self.weeks = 1

        # useful values:
        self.shiftPerDay = len(self.shiftMin)
        self.shiftsPerWeek = shift_counts
        self.shifts = shift_counts

    def __len__(self):

        return self.staff_ids_counts*self.shift_counts

    def TwoStaffLineOneThreeStaffsLinesTwoThreeFour(self, staffShiftsDict):
        violations = 0

        staffShiftsDict_Table = pd.DataFrame.from_dict(staffShiftsDict,orient="index")

        for i in range(staffShiftsDict_Table.shape[1]):
            tem = list(staffShiftsDict_Table.iloc[:,i])

            if tem.count(1) >2:
                violations += tem.count(1)

            if tem.count(2) > 3 :
                violations += tem.count(2)

            if tem.count(3) > 3 :
                violations += tem.count(3)

            if tem.count(4) > 3 :
                violations += tem.count(4)
        return violations

    def OnlyAssignStaffWhenThereIsWork(self, staffShiftsDict):
        # print(staffShiftsDict)
        violations = 0

        staffShiftsDict_Table = pd.DataFrame.from_dict(staffShiftsDict,orient="index")

        self.Lines_With_Work

        for i in range(staffShiftsDict_Table.shape[1]):

            # print(staffShiftsDict_Table.shape[1])
            # print(self.Lines_With_Work.shape)
            # print(self.Lines_With_Work.iloc[:,i])

            set_a = set(self.Lines_With_Work.iloc[:,i])
            set_b = set(staffShiftsDict_Table.iloc[:,i])

            # viola = 
            if (set_b - set_a):
                violations += 50
        return violations

    def getCost(self, schedule):
        """
        Calculates the total cost of the various violations in the given schedule
        ...
        :param schedule: a list of binary values describing the given schedule
        :return: the calculated cost
        """

        if len(schedule) != self.__len__():
            raise ValueError("size of schedule list should be equal to ", self.__len__())

        # convert entire schedule into a dictionary with a separate schedule for each staff:
        staffShiftsDict = self.getstaffShifts(schedule)
        # print(staffShiftsDict)

        # a = k 
        OnlyAssignStaffWhenThereIsWork = self.OnlyAssignStaffWhenThereIsWork(staffShiftsDict)
        # a = k
        TwoStaffLineOneThreeStaffsLinesTwoThreeFour = self.TwoStaffLineOneThreeStaffsLinesTwoThreeFour(staffShiftsDict)

        consecutiveShiftViolations = self.countConsecutiveShiftViolations(staffShiftsDict)           # count the various violations:
        shiftsPerWeekViolations = self.countShiftsPerWeekViolations(staffShiftsDict)[1]
        staffsPerShiftViolations = self.countstaffsPerShiftViolations(staffShiftsDict)[1]
        # shiftPreferenceViolations = self.countShiftPreferenceViolations(staffShiftsDict)
        hardContstraintViolations = OnlyAssignStaffWhenThereIsWork + TwoStaffLineOneThreeStaffsLinesTwoThreeFour#+ consecutiveShiftViolations + staffsPerShiftViolations + shiftsPerWeekViolations           # calculate the cost of the violations:
        # softContstraintViolations = shiftPreferenceViolations

        return self.hardConstraintPenalty * hardContstraintViolations #+ softContstraintViolations
 

    def getstaffShifts(self, schedule):
        """
        Converts the entire schedule into a dictionary with a separate schedule for each staff
        :param schedule: a list of binary values describing the given schedule
        :return: a dictionary with each staff as a key and the corresponding shifts as the value
        """
        shiftsPerstaff = self.__len__() // len(self.staffs)
 
        staffShiftsDict = {}
        shiftIndex = 0

        for staff in self.staffs:
            staffShiftsDict[staff] = schedule[shiftIndex:shiftIndex + shiftsPerstaff]
            shiftIndex += shiftsPerstaff
 
        return staffShiftsDict

    # def getstaffShifts(self, schedule):
    #     """
    #     Converts the entire schedule into a dictionary with a separate schedule for each staff
    #     :param schedule: a list of binary values describing the given schedule
    #     :return: a dictionary with each staff as a key and the corresponding shifts as the value
    #     """
    #     shiftsPerstaff = self.__len__() // len(self.staffs)
 
    #     staffShiftsDict = {}
    #     shiftIndex = 0

    #     for staff in self.staffs:
    #         staffShiftsDict[staff] = schedule[shiftIndex:shiftIndex + shiftsPerstaff]
    #         shiftIndex += shiftsPerstaff
 
    #     return staffShiftsDict

    def countConsecutiveShiftViolations(self, staffShiftsDict):
        """
        Counts the consecutive shift violations in the schedule
        :param staffShiftsDict: a dictionary with a separate schedule for each staff
        :return: count of violations found
        """
        violations = 0
        # iterate over the shifts of each staff:
        for staffShifts in staffShiftsDict.values():                                    # look for two cosecutive '1's:
            # print(staffShifts)
            # a = k
            for shift1, shift2 in zip(staffShifts, staffShifts[1:]):
                if shift1 >0 and shift2 >0:
                    violations += 1
        return violations

    def countShiftsPerWeekViolations(self, staffShiftsDict):
        """
        Counts the max-shifts-per-week violations in the schedule
        :param staffShiftsDict: a dictionary with a separate schedule for each staff
        :return: count of violations found
        """
        violations = 0
        weeklyShiftsList = []
        # iterate over the shifts of each staff:
        for staffShifts in staffShiftsDict.values():  # all shifts of a single staff
            # iterate over the shifts of each weeks:
            for i in range(0, self.weeks * self.shiftsPerWeek, self.shiftsPerWeek):
                # print(i)
                # count all the '1's over the week:
                weeklyShifts = sum(staffShifts[i:i + self.shiftsPerWeek])
                weeklyShiftsList.append(weeklyShifts)
                if weeklyShifts > self.maxShiftsPerWeek:
                    violations += weeklyShifts - self.maxShiftsPerWeek
        # print(weeklyShiftsList)
        # a = k
        return weeklyShiftsList, violations

    def countstaffsPerShiftViolations(self, staffShiftsDict):      
        """
        Counts the number-of-staffs-per-shift violations in the schedule
        :param staffShiftsDict: a dictionary with a separate schedule for each staff
        :return: count of violations found
        """
        totalPerShiftList = [sum(shift) for shift in zip(*staffShiftsDict.values())]   # sum the shifts over all staffs:

        # print(totalPerShiftList)
        # a = k
        violations = 0                                                                 # iterate over all shifts and count violations:
        for shiftIndex, numOfstaffs in enumerate(totalPerShiftList):
            dailyShiftIndex = shiftIndex % self.shiftPerDay                            # -> 0, 1, or 2 for the 3 shifts per day
            if (numOfstaffs > self.shiftMax[dailyShiftIndex]):
                violations += numOfstaffs - self.shiftMax[dailyShiftIndex]
            elif (numOfstaffs < self.shiftMin[dailyShiftIndex]):
                violations += self.shiftMin[dailyShiftIndex] - numOfstaffs
        return totalPerShiftList, violations

    def countShiftPreferenceViolations(self, staffShiftsDict):
        """
        Counts the staff-preferences violations in the schedule
        :param staffShiftsDict: a dictionary with a separate schedule for each staff
        :return: count of violations found
        """
        violations = 0
        for staffIndex, shiftPreference in enumerate(self.shiftPreference):            # duplicate the shift-preference over the days of the period
            preference = shiftPreference * (self.shiftsPerWeek // self.shiftPerDay)    # iterate over the shifts and compare to preferences:
            shifts = staffShiftsDict[self.staffs[staffIndex]]

            for pref, shift in zip(preference, shifts):
                if pref == 0 and shift == 1:
                    violations += 1

        return violations

    def printScheduleInfo(self, schedule):
        """
        Prints the schedule and violations details
        :param schedule: a list of binary values describing the given schedule
        """
        staffShiftsDict = self.getstaffShifts(schedule)

        print("Schedule for each staff:")
        for staff in staffShiftsDict:  # all shifts of a single staff
            print(staff, ":", staffShiftsDict[staff])

        # print("consecutive shift violations = ", self.countConsecutiveShiftViolations(staffShiftsDict))
        # print()p

        weeklyShiftsList, violations = self.countShiftsPerWeekViolations(staffShiftsDict)
        # print("weekly Shifts = ", weeklyShiftsList)
        # print("Shifts Per Week Violations = ", violations)
        # print()

        totalPerShiftList, violations = self.countstaffsPerShiftViolations(staffShiftsDict)
        # print("staffs Per Shift = ", totalPerShiftList)
        # print("staffs Per Shift Violations = ", violations)
        # print()
        
        dataframeS = pd.DataFrame.from_dict(staffShiftsDict, orient='index')
        DFcolumns = ["Monday_ShiftA","Monday_ShiftB","Tuesday_ShiftA","Tuesday_ShiftB","Wednesday_ShiftA","Wednesday_ShiftB","Thursday_ShiftA","Thursday_ShiftB","Friday_ShiftC","Saturday_ShiftC","Sunday_ShiftC","Monday_ShiftA","Monday_ShiftB","Tuesday_ShiftA","Tuesday_ShiftB"]
        
        dataframeS.columns = DFcolumns
        
        table_html = dataframeS.to_html(justify="center")
        
        def html_style():
            html_style = """
            <style>
            h1,title{
                border: 1px solid #dddddd;
                text-align:center;
                width:auto;
                font-family: arial, sans-serif;
                border-collapse: collapse;
                padding:15px;
                }

            td, th {border: 1px solid #dddddd;text-align: center;padding: 15px;}

            th{color: darkblue; background-color:#dddddd;}

            table{font-family: arial, sans-serif;border-collapse: collapse;float:center;}

            header{
                text-align:center;
            }

            .divCSS{
                text-align:center;
            }
            </style>
            <style>
                img{width:auto;}
            </style>
            """
            return html_style


        def html_all():
            h1 = "<html>"
            h2 = """<head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"/><meta name="viewport" content="initial-scale=1,maximum-scale=1,user=scalable=no" />"""
            h3 = "</head>"
            h4 = "<body>"
            h5 = "</body>"
            h6 = "</html>"
            html_all = h1+h2+ html_style() + h3 + h4+ table_html +h5+h6
            return html_all

        # print(table_html)
        return html_all()
        
class staff_assig_main:
    
    def __init__(self, original_file):
        self.original_file = original_file
    
    
    def final_result_table(self):
        # problem constants:
        HARD_CONSTRAINT_PENALTY = 10  # the penalty factor for a hard-constraint violation

        # Genetic Algorithm constants:
        POPULATION_SIZE = 300
        P_CROSSOVER = 0.9  # probability for crossover
        P_MUTATION = 0.1   # probability for mutating an individual
        MAX_GENERATIONS = 300
        HALL_OF_FAME_SIZE = 30

        # set the random seed:
        RANDOM_SEED = 42
        random.seed(RANDOM_SEED)

        toolbox = base.Toolbox()

        # create the nurse scheduling problem instance to be used:
        nsp = staffSchedulingProblem(HARD_CONSTRAINT_PENALTY,fileNAME=self.original_file)

        # define a single objective, maximizing fitness strategy:
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))

        # create the Individual class based on list:
        creator.create("Individual", list, fitness=creator.FitnessMin)

        # create an operator that randomly returns 0 or 1:
        toolbox.register("Integers", random.randint, 0, 4)

        # create the individual operator to fill up an Individual instance:
        toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.Integers, len(nsp))

        # create the population operator to generate a list of individuals:
        toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


        # fitness calculation
        def getCost(individual):
            return nsp.getCost(individual),  # return a tuple


        toolbox.register("evaluate", getCost)

        # genetic operators:
        toolbox.register("select", tools.selTournament, tournsize=2)
        toolbox.register("mate", tools.cxTwoPoint)
        # toolbox.register("mutate", tools.mutFlipBit, indpb=1.0/len(nsp))
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0/len(nsp))
        toolbox.register("mutate", tools.mutUniformInt, low=0, up=4, indpb=1.0/len(nsp))


        # create initial population (generation 0):
        population = toolbox.populationCreator(n=POPULATION_SIZE)

        # prepare the statistics object:
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", numpy.min)
        stats.register("avg", numpy.mean)

        # define the hall-of-fame object:
        hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

        # perform the Genetic Algorithm flow with hof feature added:
        population, logbook = eaSimpleWithElitism(population, toolbox, cxpb=P_CROSSOVER, mutpb=P_MUTATION,
                                                ngen=MAX_GENERATIONS, stats=stats, halloffame=hof, verbose=True)

        # print best solution found:
        best = hof.items[0]
        print("-- Best Individual = ", best)
        print("-- Best Fitness = ", best.fitness.values[0])
        print()
        print("-- Schedule = ")
        table_html_str = nsp.printScheduleInfo(best)

        # # extract statistics:
        # minFitnessValues, meanFitnessValues = logbook.select("min", "avg")

        # # plot statistics:
        # sns.set_style("whitegrid")
        # plt.plot(minFitnessValues, color='red')
        # plt.plot(meanFitnessValues, color='green')
        # plt.xlabel('Generation')
        # plt.ylabel('Min / Average Fitness')
        # plt.title('Min and Average fitness over Generations')
        # plt.show()
        
        return table_html_str









