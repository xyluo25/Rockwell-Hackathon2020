from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from blog.code_need.blogAPP_pyecharts import bar_line,temp_bar
from blog.models import IOpf_formaterMonth,Post
from blog.code_need.machineLearningModel import temp_machinelearning
from blog.code_need.machineSchedulingGanttChart import Hackathon_GanttChart

import pandas as pd
import os
import numpy as np



import plotly.graph_objs as go
import plotly.io as pio


from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType



# Create your views here.

def viewhtmlfile(request):
    path = "bus/202_time_space.html"
    return render(request,path)

def viewlink_kepler(request):
    #return HttpResponse()
    return render(request,"kepler.html")

def viewhtml_str(request):
    
    sTTT = """<!DOCTYPE html>
            <html>
            <head>
            <title>Page Title</title>
            </head>
            <body>

            <h1>This is a Heading</h1>
            <p>This is a paragraph.</p>

            </body>
            </html>
            """
            
    return HttpResponse(sTTT)

def viewCSV_local(request):
    file_ = os.path.join(settings.BASE_DIR, r"blog\templates\upload\Julydata.xlsx")
    
    # Do Data Processing with the file name
    df = pd.read_excel(file_)

    
    data =  str(df.to_dict())
    return HttpResponse(data)
    #return HttpResponse(file_)
    
def viewCSV_webupload(request):
    # Get the certain post
    s_t = Post.objects.get(title="asfd")
    
    # Get upload file name
    cer_p = s_t.filesUp
    
    # Get Full Path of File Name
    file_ = os.path.join(settings.BASE_DIR,str(cer_p))
    
    # Do Data Processing with the file name
    df = pd.read_excel(file_)

    
    
    data =  str(df.to_dict())
    return HttpResponse(data)

def viewcharts(request):
    x_l = [str(i) for i in range(10)]
    y_l = [i^2 for i in range(10)]

    c = Line()
    c.add_xaxis(x_l)
    c.add_yaxis("Test",y_l)
    return HttpResponse(c.render_embed())

def viewplotlyfigure(request):
    y0 = np.random.randn(50) - 1
    y1 = np.random.randn(50) + 1
    
    fig = go.Figure()
    fig.add_trace(go.Box(y=y0))
    fig.add_trace(go.Box(y=y1))
    
    return HttpResponse(fig.to_html())

def viewupload(request):
    context = {}
    
    if request.method=="POST":
        try:
            if request.FILES["document"]:
                
                uploaded_file = request.FILES["document"]
                
                print(uploaded_file.name)
                print(uploaded_file.size)
                print(request.POST.get("texA"))
                
                
                fs = FileSystemStorage()
                url = fs.save(uploaded_file.name,uploaded_file)
                    
                file_ = os.path.join(settings.BASE_DIR,r"blog\media\%s"%url)
                print("Files_Full",file_)
                df = pd.read_excel(file_)
                
                print("Columns:",df.columns)
                
                context["url"] = fs.url(url)  #bar.render_embed()
                
                context["htmlstr"] = df.to_dict()

                
                context["pyecharts"] = temp_bar()
                #context["pyecharts"] = c.render_embed()
                
                #print("This is temp_bar",temp_bar())
            
            
                tem_lst = []
                tem_lst.append(file_)
                
                Data_in,Data_out = IOpf_formaterMonth(tem_lst).concatDataFrame()

                context["barEcharts"] = bar_line(Data_in,Data_out)
            
                context["selectValues"] = ["item1","item2","item3","item4"]
        except:  
            if request.POST.get("selection"):
                print(request.POST.get("selection"))
                context["selectionResult"] = request.POST.get("selection")
                
                context["machineLearning"] = temp_machinelearning()
                
                context["ganttChart"]  = Hackathon_GanttChart(save2db_path=None).generate_gantt()
            
        
    return render(request,"upload.html",context)

def viewupload_00(request):
    context = {}
    
    if request.method=="POST":

        uploaded_file = request.FILES["document"]
        
        print(uploaded_file.name)
        print(uploaded_file.size)
        print(request.POST.get("texA"))

        
        fs = FileSystemStorage()
        url = fs.save(uploaded_file.name,uploaded_file)
              
        file_ = os.path.join(settings.BASE_DIR,r"blog\media\%s"%url)
        print("Files_Full",file_)
        df = pd.read_excel(file_)
        
        print("Columns:",df.columns)
        
        context["url"] = fs.url(url)  #bar.render_embed()
        
        context["htmlstr"] = df.to_dict()


        from pyecharts import options as opts
        from pyecharts.charts import Bar
        from pyecharts.commons.utils import JsCode
        from pyecharts.globals import ThemeType

        list2 = [
            {"value": 12, "percent": 12 / (12 + 3)},
            {"value": 23, "percent": 23 / (23 + 21)},
            {"value": 33, "percent": 33 / (33 + 5)},
            {"value": 3, "percent": 3 / (3 + 52)},
            {"value": 33, "percent": 33 / (33 + 43)},
        ]

        list3 = [
            {"value": 3, "percent": 3 / (12 + 3)},
            {"value": 21, "percent": 21 / (23 + 21)},
            {"value": 5, "percent": 5 / (33 + 5)},
            {"value": 52, "percent": 52 / (3 + 52)},
            {"value": 43, "percent": 43 / (33 + 43)},
        ]

        c = (
            Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
            .add_xaxis([1, 2, 3, 4, 5])
            .add_yaxis("product1", list2, stack="stack1", category_gap="50%")
            .add_yaxis("product2", list3, stack="stack1", category_gap="50%")
            .set_series_opts(
                label_opts=opts.LabelOpts(
                    position="right",
                    formatter=JsCode(
                        "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                    ),
                )
            )
        )
        context["pyecharts"] = c.render_embed()
        
        
        tem_lst = []
        tem_lst.append(file_)
        
        Data_in,Data_out = IOpf_formaterMonth(tem_lst).concatDataFrame()

        timeSeries = list(Data_in["Time"])
        y_in = list(Data_in["徐泾东"])
        y_out= list(np.array(Data_out["徐泾东"])*-1)


        bar= (
            Bar(init_opts = opts.InitOpts(width="1200px",height="800px",theme=ThemeType.DARK))
            .add_xaxis(timeSeries)
            .add_yaxis(
                "bar_In",
                y_in,
                )
            .add_yaxis(
                "bar_Out",
                y_out,
                label_opts=opts.LabelOpts(position="bottom"),
                gap="-100%"
                )
            .set_global_opts(
                title_opts= opts.TitleOpts(title="Rail Transit Passenger In and Out Flow XuJingDong Station by Time"),
                datazoom_opts = opts.DataZoomOpts(type_="inside"),
                toolbox_opts = opts.ToolboxOpts(),
                legend_opts= opts.LegendOpts(pos_top="30px"),
                xaxis_opts = opts.AxisOpts(
                    axislabel_opts= opts.LabelOpts(
                        rotate=-30
                    )
                )
            )
        )

        line=(
            Line(init_opts = opts.InitOpts(width="1200px",height="800px"))
            .add_xaxis(timeSeries)
            .add_yaxis(
                "line_In",
                y_in,
                is_smooth=True,
                label_opts=opts.LabelOpts(is_show=False),
                linestyle_opts=opts.LineStyleOpts(
                    width=3,
                    color="green"
                )
                )
            .add_yaxis(
                "line_Out",
                y_out,
                label_opts=opts.LabelOpts(is_show=False),
                is_smooth=True,
                linestyle_opts=opts.LineStyleOpts(
                    width=3,
                    color = "blue"
                )
                )
            .set_global_opts(
                datazoom_opts = opts.DataZoomOpts(type_="inside"),
                toolbox_opts = opts.ToolboxOpts(),
                legend_opts= opts.LegendOpts(pos_top="30px"),
                xaxis_opts = opts.AxisOpts(
                    axislabel_opts= opts.LabelOpts(
                        rotate=-30
                    )
                )
            )
        )
        
        bar.overlap(line)
        
        
        context["barEcharts"] = bar.render_embed()
        
        
    return render(request,"upload.html",context)
