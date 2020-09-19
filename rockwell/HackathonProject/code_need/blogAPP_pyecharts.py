# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, August 17th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################


from pyecharts import options as opts
from pyecharts.charts import Bar,Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
import pandas as pd
import sys
import os
import numpy as np


def bar_line(Data_in,Data_out):
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
    
    return bar.render_embed()
    
    
def temp_bar():
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
    
    return c.render_embed()
