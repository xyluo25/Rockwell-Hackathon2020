from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseNotFound,Http404
from django.conf import settings
from django.core.files.storage import FileSystemStorage


from HackathonProject.code_need.GanttChart_original import ganttChart
from HackathonProject.code_need.sweetvis_downtime import createSweetviz
from HackathonProject.code_need.TablePreparation import create_ML_Table
# from HackathonProject.code_need.staff_optimation import staff_assig_main
from HackathonProject.code_need.staffAssignmentApplication import staff_assig_main


from HackathonProject.code_need.nurseSchedulingProblem import nspDjango

import pandas as pd
import os
import numpy as np

import plotly.graph_objs as go
import plotly.io as pio


# from HackathonProject.code_need.blogAPP_pyecharts import bar_line,temp_bar
# from HackathonProject.models import IOpf_formaterMonth,Post
# from HackathonProject.code_need.machineLearningModel import temp_machinelearning
# from HackathonProject.code_need.machineSchedulingGanttChart import Hackathon_GanttChart
# from HackathonProject.code_need.CLS_Solver_GA import GA_CLS_slover
# from pyecharts import options as opts
# from pyecharts.charts import Bar, Line
# from pyecharts.commons.utils import JsCode
# from pyecharts.globals import ThemeType


def viewHomepage(request):
    context_homepage = {"ani":True}
    
    return render(request,"WelcomePage_django.html",context_homepage)

def viewAbout(request):
    
    context_aboutpage= {"ab":True}
    
    return render(request,"AboutPage_django.html",context_aboutpage)

def viewComputation(request):
    context = {}
    
    if request.method=="POST":
        try:
            if request.FILES["document"]:
                uploaded_file = request.FILES["document"]
                
                print(uploaded_file.name)
                print(uploaded_file.size)
                print(request.POST.get("texA"))
                print(request.POST.get("texB"))
                # print(request.POST.get("texC"))
                
                fs = FileSystemStorage()
                url = fs.save(uploaded_file.name,uploaded_file)
                    
                file_ = os.path.join(settings.BASE_DIR,r"HackathonProject\media\%s"%url)
                print("Files_Full",file_)
                # df = pd.read_excel(file_)
                
                
                context["url"] = fs.url(url)  #bar.render_embed()
                
                # tem_lst = []
                # tem_lst.append(file_)
                
                # Data_in,Data_out = IOpf_formaterMonth(tem_lst).concatDataFrame()

                # context["barEcharts"] = bar_line(Data_in,Data_out)
            
                # context["selectValues"] = ["item1","item2","item3","item4"]

                # context["selectionResult"] = request.POST.get("selection")
                
                # context["machineLearning"] = temp_machinelearning()
                
                # context["ganttChart"]  = Hackathon_GanttChart(save2db_path=None).generate_gantt()
                # context["ganttChart"]  = GA_CLS_slover().Not_Main()
                context["ganttChart"] = ganttChart(file_)
                
                context["sweetViz"] = createSweetviz(file_,outputName = "Rockwell_sweetViz_1.html")
                
                # context["nurseSchedulingProblem"] = nspDjango().main()[1]
                context["staff_SchedulingOpt"] = staff_assig_main(file_).final_result_table()
                
                url = None
                
        except Exception as err:
            raise Http404("Page does not exist, please make sure to input data inside file section.")
            # return HttpResponseNotFound("<h1 style='float:center;'>Page Not Found!</h1>")

    # return render(request,"upload01.html",context)
    return render(request,"upload01.html",context)

def viewAnimation(request):
    
    context_ani = {}
    
    if request.method == 'POST':
        pass
    
    return render(request,"animationPage_django.html",context_ani)








