from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
import pandas as pd


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                              on_delete=models.CASCADE,
                              related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    filesUp = models.FileField(upload_to="blog/templates/upload/")
    

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title


class IOpf_formaterMonth:
    def __init__(self,filesPathList,yearMonth="201901",save2txtcsv=["201901InData.csv","201901OutData.csv"]):
        """A class to union shanghai metro in and out passenger flow data.
        
        parameters:
        folder_path : a folder path that contain only fifteen-minute passengers data. like: ./path/2号线/  and data inside "2号线" only contain "1.xls","2.xls"...
        yearMonth  : predefine the folder data's date. like: "201909" means all data inside the folder are: Sep from day 1-30 every five minutes in and out passengers flow data
        save2txtcsv : save data into a csv file or txt file, you need to change this name each time you run the this class or you will overwrite data into the save file.
        """
        self.filesPathList = filesPathList
        self.yearMonth = yearMonth
        self.save2txtcsv = save2txtcsv
        
        self.concatDataFrame()
        
    def readExcel(self,excelFullPath) -> pd.DataFrame:
        # read the input excel file
        df = pd.read_excel(excelFullPath)

        # get column names 
        columnName = df.iloc[2,:]
        columnName = [i for i in columnName if str(i) != "nan"]


        # create in and out data accordingly
        inCols =[0] + [2*i+1 for i in range(31)]
        outCols = [2*i for i in range(32)]

        datain = df.iloc[:,inCols]
        dataout = df.iloc[:,outCols]

        # generate data without invalid rows and columns
        datain_valid = datain.iloc[4:-1,:]   # exclude the summary row
        dataout_valid = dataout.iloc[4:-1,:]

        datain_valid.reset_index(inplace=True)
        dataout_valid.reset_index(inplace=True)

        # rename column names
        temp = ["old_index"]
        columnName[0] = "Time"
        columnName[-1] = "SUM"
        temp.extend(columnName)

        datain_valid.columns = temp
        dataout_valid.columns = temp
        
        if excelFullPath.split(".")[0][-2:].isdigit():
            day = excelFullPath.split(".")[0][-2:]
            
        else:
            day = "0" + excelFullPath.split(".")[0][-1]
            
        datain_valid["Date"] = self.yearMonth + day
        dataout_valid["Date"] = self.yearMonth+ day
        
        return datain_valid,dataout_valid

    def concatDataFrame(self):
        
        for i in range(len(self.filesPathList)):
            if i ==0:
                datain_FinalDF,dataout_FinalDF  = self.readExcel(self.filesPathList[i])
            else:
                in_temp,out_temp = self.readExcel(self.filesPathList[i])
                datain_FinalDF = pd.concat([datain_FinalDF,in_temp])
                dataout_FinalDF = pd.concat([dataout_FinalDF,out_temp])
                
                
        datain_FinalDF.reset_index(inplace=True)
        dataout_FinalDF.reset_index(inplace=True)
        
        # if self.save2txtcsv:
        #     datain_FinalDF.to_csv(self.save2txtcsv[0])
        #     dataout_FinalDF.to_csv(self.save2txtcsv[1])
            
        return datain_FinalDF, dataout_FinalDF





