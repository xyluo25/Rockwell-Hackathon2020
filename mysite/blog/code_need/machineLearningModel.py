# -*- coding:utf-8 -*-
##############################################################
# Created Date: Monday, August 17th 2020
# Contact Info: luoxiangyong01@gmail.com
# Author/Copyright: Mr. Xiangyong Luo
##############################################################

import base64
import sys
import graphviz 
from sklearn.datasets import load_iris
from sklearn import tree


def temp_machinelearning(save2html=False):
    X, y = load_iris(return_X_y=True)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(X, y)

    #ttt = tree.plot_tree(clf,filled=True)
    #ttt
    #temp = clf.predict([])



    dot_data = tree.export_graphviz(clf, out_file=None,filled=True,rounded=True,special_characters=True) 
    graph = graphviz.Source(dot_data) 
    graph.format="png"

    data_uri = base64.b64encode(graph.pipe(format="png")).decode("utf-8")
    img_tag = "data:image/png;base64,"+data_uri
    #print(img_tag)

    data_im = """<header><h1>The Test Data：</h1></header>""" + """<div class="divCSS"><img src="%s" align="middle"></div>""" % img_tag   

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

        table{font-family: arial, sans-serif;border-collapse: collapse;}

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
        html_all = h1+h2+ html_style() + h3 + h4+ data_im +h5+h6
        return html_all

    if save2html:
        with open("tes13.html","w",encoding="utf-8") as f:
            f.write(html_all())
        
        f.close()   

    return html_all()


