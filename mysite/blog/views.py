from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from django.conf import settings
from .models import Post

from pyecharts.charts import Line




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
    #return HttpResponse(c)
    return render(request,c.render_embed())

