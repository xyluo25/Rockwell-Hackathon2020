# -*- coding:utf-8 -*-
##############################################################
# Created Date: Friday, September 18th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


import random
import datetime 
import pandas as pd 
import datetime as dt
import numpy as np
import plotly.figure_factory as ff
import plotly.io as pio

# plotly.io.orca.config.executable = '/Users/mhe2/Anaconda3/orca.cmd'
# plotly.io.orca.config.save()


# =================================================== Table Sheet SchAug3-11 =================================================================== #


def ganttChart(dataFileName):
    
    df = pd.read_excel(open(dataFileName, 'rb'), sheet_name='SchAug3-11') 
    # MaterialNo_H

    df = df.rename(columns={"Family": "Resource", "BasicStartDate": "Start", "BasicEndDate": "Finish", "LineName":"Task"})
    df = df.sort_values(by=['Task','Start'])
    color_dict = dict(zip(df.Resource.unique(),['rgb({},{},{})'.format(i[0],i[1],i[2]) for i in list(np.random.randint(255, size = (len(df.Resource.unique()),3)))]))

    fig = ff.create_gantt(df.to_dict(orient = 'records'),
        colors = color_dict,
        index_col = "Resource",
        title = "Gantt Chart for Table SchAug3-11",
        show_colorbar = True,
        bar_width = 0.3,
        showgrid_x = False,
        showgrid_y = True,
        show_hover_fill=True)
    # fig.show()   
    # fig.write_image(r"CLS_GanttChart.png")
     
    fig_html = pio.to_html(fig)
        
    return fig_html
    

