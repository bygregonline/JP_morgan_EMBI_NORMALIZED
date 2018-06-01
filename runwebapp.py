



import os
import traceback
import sys
import pkg_resources

import pandas as pd
import openpyxl
import matplotlib
import socket
import setuptools
import base64


import numpy as np
import pickle as pkl
import xml.etree.ElementTree as et
import matplotlib.pyplot as plt
import seaborn as sns



from aniachi.systemUtils import Welcome as W
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound
from io import StringIO
from io import BytesIO
from multiprocessing import Manager
from sklearn.preprocessing import scale


mgr = Manager()
ns = mgr.Namespace()
port =8080


"""



"""
def __doc__():
    return 'Web application server'

"""



"""
def __str__():
    return 'Web application server. \n To to EMBI analysis and mead and variance reduction'
#

#



@view_config(route_name='hello', renderer='home.jinja2')
def hello_world(request):

    return {'name': 'Running Server','port':port,'pyramid':pkg_resources.get_distribution('pyramid').version
             ,'numpy':np.__version__,'pandas':pd.__version__ ,'favicon':'aniachi_logo.png','matplotlib':matplotlib.__version__,
             'fbprophet':pkg_resources.get_distribution('fbprophet').version,'openpyxl ':openpyxl.__version__,'setuptools':setuptools.__version__,
             'py_common_fetch':pkg_resources.get_distribution('py-common-fetch').version,'host':socket.gethostbyname(socket.gethostname()),
              'pyqrcode':pkg_resources.get_distribution('pyqrcode').version,'argparse':'','pypng':pkg_resources.get_distribution('pypng').version
            }



"""

"""



@view_config(route_name='entry')
def entry_point(request):
    return HTTPFound(location='app/welcome')

"""


A friendly error request 



"""

@view_config(context=Exception,  renderer='error.jinja2')
def error(context, request):
    fp = StringIO()
    traceback.print_exc(file=fp)

    return {'error':fp.getvalue(),'favicon':'logo.png'}

"""



"""

def getParamterOrdefault(d,k,v,valid):
    aux = v
    try:
        if (d[k]  in valid): aux = d[k]
    except Exception as e:
        pass
    return aux


#


#


"""
Auxiliar method if you want to test something
"""
def testSomething():
    pass



"""
A friendly 404 request 


"""

@view_config(context=HTTPNotFound, renderer='404.jinja2')
def not_found(context, request):
    request.response.status = 404
    return {}

"""



"""


def readAndFilterDataframe(file):
    try:
        print('Rerading...',os.path.join(os.getcwd(),file))

        df = pd.read_csv(os.path.join(os.getcwd(),file))
        #remove unamed columns.
        columnsToDelete = []
        for i in range(15, 29):
            columnsToDelete.append('Unnamed: ' + str(i))
        df = df.drop(columns=columnsToDelete)
        print('Fixing columns')
        #convert to data time objects
        df.Fecha = pd.to_datetime(df['Fecha'])
        print('Fixing dateTime Objects')
        print('Dataframe rows:',df.shape[0])

        ns.df = df #multitreading shared object
    except:
        print(os.path.join(os.getcwd(),file),'Not found')
        sys.exit(-1)



@view_config(route_name='dataset')
def datasetServer(request):



    format = getParamterOrdefault(request.params,'format','default',['html','json','xml','serialized','csv','excel'])
    if (format=='csv'):

        s = StringIO()
        ns.df.to_csv(s)
        r = Response(s.getvalue(), content_type='application/CSV', charset='UTF-8')
    elif (format=='json'):
        df = ns.df
        s = StringIO()
        df.to_json(s)
        r = Response(s.getvalue(), content_type='application/json', charset='UTF-8')
    elif (format=='xml'):
        df =ns.df
        root = et.Element('root')

        for i, row in df.iterrows():

            data = et.SubElement(root, 'row')
            data.set('iter', str(i))
            for head in df.columns:
                aux = et.SubElement(data, head)
                if head =='Fecha':
                    aux.text = str(row[head].strftime('%Y-%d-%m'))
                else:
                    aux.text = str(row[head])


        r = Response(et.tostring(root), content_type='application/xml', charset='UTF-8')
    elif (format=='html'):
        df = ns.df
        s = StringIO()
        df.to_html(s,index=True)
        r = Response(s.getvalue(), content_type='text/html', charset='UTF-8')
    elif (format=='serialized'):

        r = Response(base64.encodebytes(pkl.dumps(ns.df)).decode('utf-8'), content_type='text/html', charset='UTF-8')
    elif (format == 'excel'):
        b= BytesIO()
        pd.ExcelWriter(b)

        ns.df.to_excel(b)
        r = Response(b.getvalue(), content_type='application/force-download', content_disposition='attachment; filename=data.xls')

    else:
        r = Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')

    return r


"""

return an empty dataframe to avoid errors


"""

def getNormalizedDataAsDF(country):

    try:
        mx_scale = scale(ns.df[country])

        d = {'Fecha': ns.df.Fecha, country: ns.df[country], 'NORMALIZED': mx_scale}
        return pd.DataFrame(d)
    except:

        return pd.DataFrame(dict())


"""


"""

def getIntParameter(d,k,v,r):


    aux=int(v)
    try:
        if isinstance(int(d[k]), int):
            if int(d[k]) in r:
                aux= int(d[k])

    except Exception as e:
        pass

    return aux

"""



"""

@view_config(route_name='normalized')
def normalizedServer(request):
    format = getParamterOrdefault(request.params, 'format', 'default',
                                  ['html', 'json', 'xml', 'serialized', 'csv', 'excel'])
    country = getParamterOrdefault(request.params, 'country', 'default',
                                  ['LATINO','REP_DOM','BRAZIL','COLOMBIA','ECUADOR','ARGENTINA','MEXICO','PERU','PANAMA','VENEZUELA','URUGUAY','CHILE','EL_SALVADOR'])

    if country == 'default' or format == 'default':
        r = Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')
        return r
    else:
        df= getNormalizedDataAsDF(country)
        if (format == 'csv'):

            s = StringIO()
            df.to_csv(s)
            r = Response(s.getvalue(), content_type='application/CSV', charset='UTF-8')
        elif (format == 'json'):

            s = StringIO()
            df.to_json(s)
            r = Response(s.getvalue(), content_type='application/json', charset='UTF-8')
        elif (format == 'xml'):

            root = et.Element('root')

            for i, row in df.iterrows():

                data = et.SubElement(root, 'row')
                data.set('iter', str(i))
                for head in df.columns:
                    aux = et.SubElement(data, head)
                    if head == 'Fecha':
                        aux.text = str(row[head].strftime('%Y-%d-%m'))
                    else:
                        aux.text = str(row[head])

            r = Response(et.tostring(root), content_type='application/xml', charset='UTF-8')
        elif (format == 'html'):

            s = StringIO()
            df.to_html(s, index=True)
            r = Response(s.getvalue(), content_type='text/html', charset='UTF-8')
        elif (format == 'serialized'):

            r = Response(base64.encodebytes(pkl.dumps(df)).decode('utf-8'), content_type='text/html',charset='UTF-8')
        elif (format == 'excel'):
            b = BytesIO()
            pd.ExcelWriter(b)

            df.to_excel(b)
            r = Response(b.getvalue(), content_type='application/force-download',
                         content_disposition='attachment; filename=data.xls')


        return r

"""




"""
@view_config(route_name='rawCharts')
def chartRawDataServer(request):
    format = getParamterOrdefault(request.params, 'format', 'not',
                                  ['png', 'jpg'])

    country = getParamterOrdefault(request.params, 'country', 'not',
                                     ['LATINO','REP_DOM','BRAZIL','COLOMBIA','ECUADOR','ARGENTINA','MEXICO','PERU','PANAMA','VENEZUELA','URUGUAY','CHILE','EL_SALVADOR'])

    dpi = getIntParameter(request.params, 'dpi', -1, range(20, 301))



    if dpi==-1 or country=='not' or format=='not':
        return Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')
    else:

        plt.clf()
        plt.title('J.P. Morgan Emerging Markets Bond Index: '+country)
        plt.grid(True)

        plt.plot(ns.df.Fecha,ns.df[country], label=country)

        plt.legend()
        plt.ylabel('Percentage')
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        ax = plt.axes([.60, -0.13, 0.25, 0.8], frameon=True)

        ax.imshow(ns.img, alpha=0.112)
        ax.axis('off')
        figure = BytesIO()

        plt.savefig(figure, format=format, dpi=dpi)




    if format == 'png':
        content_type = "image/png"
    else:
        content_type = "image/jpg"

    return Response(body=figure.getvalue(), content_type=content_type)



"""




"""
@view_config(route_name='correlationCharts')
def chartCorrDataServer(request):
    format = getParamterOrdefault(request.params, 'format', 'not',
                                  ['png', 'jpg'])

    annot = getParamterOrdefault(request.params, 'annot', 'True',
                                  ['true', 'false'])

    if annot in ['false', 'False', 'no', 'not']:
        annot=False
    else:
        annot=True


    dpi = getIntParameter(request.params, 'dpi', -1, range(20, 301))

    if dpi == -1  or format == 'not':
        return Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')
    else:

        df = ns.df.corr()

        plt.clf()

        mask = np.zeros_like(df, dtype=np.bool)
        mask[np.triu_indices_from(mask)] = True
        cmap = sns.diverging_palette(250, -15, n=190)

        # Draw the heatmap with the mask and correct aspect ratio
        plt.title('J.P. Morgan Emerging Markets Bond  Correlation Index')

        sns.heatmap(df.corr(), cmap=cmap, center=0, mask=mask,
                    square=True, linewidths=.2, cbar_kws={"shrink": .6}, annot=annot)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        ax = plt.axes([.60, 0.43, 0.10, 0.6], frameon=True)

        ax.imshow(ns.img, alpha=0.142)
        ax.axis('off')
        figure = BytesIO()
        plt.savefig(figure, format=format, dpi=dpi)


    if format == 'png':
        content_type = "image/png"
    else:
        content_type = "image/jpg"

    return Response(body=figure.getvalue(), content_type=content_type)




"""




"""
@view_config(route_name='correlationData')
def corrChartServer(request):
    format = getParamterOrdefault(request.params, 'format', 'default',
                                  ['html', 'json', 'xml', 'serialized', 'csv', 'excel'])
    if format == 'default':
        r = Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')
    else:
        df= ns.df.corr()
        if (format == 'csv'):

            s = StringIO()
            df.to_csv(s)
            r = Response(s.getvalue(), content_type='application/CSV', charset='UTF-8')
        elif (format == 'json'):

            s = StringIO()
            df.to_json(s)
            r = Response(s.getvalue(), content_type='application/json', charset='UTF-8')
        elif (format == 'xml'):

            root = et.Element('root')

            for i, row in df.iterrows():

                data = et.SubElement(root, 'row')
                data.set('iter', str(i))
                for head in df.columns:
                    aux = et.SubElement(data, head)
                    if head == 'Fecha':
                        aux.text = str(row[head].strftime('%Y-%d-%m'))
                    else:
                        aux.text = str(row[head])

            r = Response(et.tostring(root), content_type='application/xml', charset='UTF-8')
        elif (format == 'html'):

            s = StringIO()
            df.to_html(s, index=True)
            r = Response(s.getvalue(), content_type='text/html', charset='UTF-8')
        elif (format == 'serialized'):

            r = Response(base64.encodebytes(pkl.dumps(df)).decode('utf-8'), content_type='text/html',charset='UTF-8')
        elif (format == 'excel'):
            b = BytesIO()
            pd.ExcelWriter(b)

            df.to_excel(b)
            r = Response(b.getvalue(), content_type='application/force-download',
                         content_disposition='attachment; filename=data.xls')


    return r



"""

"""


@view_config(route_name='normalizedCharts', renderer='normalized.jinja2')
def varianceAnalysisServer(request):


    country = getParamterOrdefault(request.params, 'country', 'not',
                                     ['LATINO','REP_DOM','BRAZIL','COLOMBIA','ECUADOR','ARGENTINA','MEXICO','PERU','PANAMA','VENEZUELA','URUGUAY','CHILE','EL_SALVADOR'])

    dpi = getIntParameter(request.params, 'dpi', -1, range(20, 301))



    if dpi==-1 or country=='not' or format=='not':
        return Response('Bad paramters ' + str(request.params), content_type='text/html', charset='UTF-8')

    else:
        auxdata = scale(ns.df[country])
        d = {'variance': str(round(ns.df[country].var(), 4)),'mean':str(round(ns.df[country].mean(), 4)), 'normal_variance':str(round(auxdata.var(),4)),
             'normal_mean': str(round(auxdata.mean(), 4)),'country':country}

        plt.clf()
        plt.title(country)
        plt.grid(True)
        plt.text(1500, -0.3, 'Normalized mean=0, var =1', style='italic', fontsize=7,
                 bbox={'facecolor': 'blue', 'alpha': 0.1, 'pad': 10})
        plt.plot(ns.df.Fecha,auxdata, label='Normalized data')
        plt.plot(ns.df.Fecha,ns.df[country], label='Raw Data')
        plt.legend()
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        ax = plt.axes([.30, 0.43, 0.30, 0.6], frameon=True)

        ax.imshow(ns.img, alpha=0.182)
        ax.axis('off')

        figure = BytesIO()
        plt.savefig(figure, format='png', dpi=dpi)

        d['both_images'] = base64.b64encode(figure.getvalue()).decode()


        #FROM HERE
        plt.clf()


        plt.hist(ns.df[country],label='Raw Data')
        plt.hist(auxdata,label='Normalized')
        plt.legend()
        plt.grid(True)
        fig = plt.gcf()
        fig.set_size_inches(18.5, 10.5)
        ax = plt.axes([.30, 0.43, 0.30, 0.6], frameon=True)

        ax.imshow(ns.img, alpha=0.182)
        ax.axis('off')

        figure = BytesIO()
        plt.savefig(figure, format='png', dpi=dpi)

        d['histograms_images'] = base64.b64encode(figure.getvalue()).decode()

        return d











#


#

if __name__ == '__main__ww':
    readAndFilterDataframe('data/Serie_Historica_Spread_del_EMBI.csv')
    ns.img = plt.imread('matplotlib.png')
    print(varianceAnalysisServer(None))












if __name__ == '__main__':

    os.system('clear')

    #W.printWelcome()

    print(W.printLibsVersion(
        ['pyramid', 'numpy', 'openpyxl', 'pandas', 'matplotlib', 'datetime', 'setuptools',
         'py-common-fetch', 'argparse', 'pyqrcode']))

    readAndFilterDataframe('data/Serie_Historica_Spread_del_EMBI.csv')
    ns.img=plt.imread('matplotlib.png')

    with Configurator() as config:
        config.include('pyramid_jinja2')

        config.add_route('entry', '/')
        config.add_route('hello', '/app/welcome')
        config.add_route('dataset', '/app/dataset')
        config.add_route('normalized', '/app/normalized')
        config.add_route('rawCharts', '/app/rawchart')
        config.add_route('correlationCharts', '/app/correlationchart')
        config.add_route('correlationData', '/app/correlationdata')
        config.add_route('normalizedCharts', '/app/normalizedchart')




        config.add_static_view(name='app/static/', path='static/')

        print(__file__)
        config.scan('__main__')
        app = config.make_wsgi_app()
        print('running sevrer:', port)
        server = make_server('0.0.0.0', port, app)
        server.serve_forever()


