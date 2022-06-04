from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from dash import Dash, html, dcc, dash_table,Input, Output, State,callback_context, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import yfinance as yf
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio
import pandas as pd
#from pandas import DataFrame
import json
from datetime import datetime, date, timedelta
from time import strftime
import talib
from numpy import isnan
import pandas as pd
import sqlite3
from layouts import index_string_login, index_string_logout
con = sqlite3.connect("./chart.db", check_same_thread=False)

#from app import con
#from layouts import graph_layout,sidebar,content,sidebar_right,modal

#THIS CALLBACK IS THE START OF THE SEARCH AND CHOOSING INDICATOR
@callback(
    Output('stock-graph', 'figure'),
    Output("modal_error", "is_open"),
    Output("remove_indicator","options"),
    Output("modal_title", "children"),
    Output("modal_body","children"),
    Output("welcome","children"),
    Output("input-search-dcc","value"),
    Output("strategyTable","children"),
    Output("strategyMessage","children"),
    Output("strategySummary","children"),

    State("input-search", "value"),

    Input('submit-search', 'n_clicks'),
    [State("date-range", "start_date"),
    State("date-range", "end_date")],
    #FOR ONLY ONE INPUT PERIOD INDICATOR
    State('overlap_input1', 'value'),
    Input('overlap_add1', 'n_clicks'),
    [State("overlap_modal1", "is_open"),
    State("overlap_modelinput1","data")],
    #FOR TWO INPUT PERIOD INDICATOR, IT IS BB BANDS
    State('overlap_input2', 'value'),
    State('overlap_input2_std', 'value'),
    Input('overlap_add2', 'n_clicks'),
    [State("overlap_modal2", "is_open"),
    State("overlap_modelinput2","data")],
    #FOR THREE INPUT PERIOD INDICATOR LIKE MACD
    State('inputnumber31', 'value'),
    State('inputnumber32', 'value'),
    State('inputnumber33', 'value'),
    Input('input_add3', 'n_clicks'),
    [State("input_modal3", "is_open"),
    State("input_modelinput3","data")],
    #FOR FOUR INPUT PERIOD INDICATOR STOACH
    State('inputnumber41', 'value'),
    State('inputnumber42', 'value'),
    State('inputnumber43', 'value'),
    Input('input_add4', 'n_clicks'),
    [State("input_modal4", "is_open"),
    State("input_modelinput4","data")],
    #FOR THE STRATEGY INDICATOR 51 61,62 71,72,73
    State('inputnumber51', 'value'),
    State('inputnumber61', 'value'),
    State('inputnumber62', 'value'),
    State('inputnumber71', 'value'),
    State('inputnumber72', 'value'),
    State('inputnumber73', 'value'),
    Input('input_add5', 'n_clicks'),
    State("input_modelinput5","data"),
    #FOR REMOVE INDICATOR
    Input('submit-removal', 'n_clicks'),
    State("remove_indicator",'value'),

    #Input('submit-save', 'n_clicks'),
    #FOR THE URL PATHNAME REFRESH
    Input('url', 'pathname'),

    # State("savefigure_name", "value"),
    # State("inputnotes","value"),
    # Input("savefigure_name_save","n_clicks"),

    State('table', 'selected_cells'),
    Input("loadfigure_name_load","n_clicks"),
    #FOR OBV INDICATOR AS IT IS WITHOUT ANY PERIOD NUMBER
    Input("volume", "value"),

    prevent_initial_call=True
)
def startloadchart(input1_search, submit_search,start_date,end_date,
                   inputnumber1,overlap_add1,is_open1,overlap_value1,
                   inputnumber2,overlap_add2,is_open2,overlap_value2,overlap_value2_std,
                   inputnumber31,inputnumber32,inputnumber33,input_add3,input_modal3,input_modelinput3,
                   inputnumber41,inputnumber42,inputnumber43,input_add4,input_modal4,input_modelinput4,
                   inputnumber51,inputnumber61,inputnumber62,inputnumber71,inputnumber72,inputnumber73,
                   input_add5,input_modelinput5,
                   submit_removal,remove_indicator,
                   urlpath,
                   #savefigure_name, inputnotes,savefigure_name_save,
                   selected_cells,loadfigure_name_load,volume):
    triggered_id = callback_context.triggered[0]['prop_id']
    print(triggered_id)
    print(callback_context.triggered)
    print(callback_context.inputs)

    if 'submit-search.n_clicks' == triggered_id:
        submit_search_fig=figurechart(input1_search,start_date,end_date)
        #IF SEARCH SYMBOL IS WRONG
        if submit_search_fig == "empty":
            return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        #IF SEARCH SYMBOL IS EMPTY, RETURN NO UPDATE
        if submit_search_fig is None:
            new_data = list(session["fig"].data).copy()
            del new_data[0:2]
            #print(fig1.data)
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data if x['name'] != None])).copy()
            error_msg_title, error_msg="Cannot find the stock ticker symbol","We cannot find this stock ticker symbol in this period! Please try again!"
            return [session["fig"],True,current_indicator_list,error_msg_title,error_msg,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        # IF SEARCH SUCCESS, RETURN, THE FIGURE CHART AND EMPTY THE TAB STRATEGY
        return [submit_search_fig,False,[],dash.no_update,dash.no_update,dash.no_update,session['symbol'],"","",""]

    elif 'overlap_add1.n_clicks' == triggered_id:
    # or callback_context.inputs['volume.value'] == "OBV":
    #     if callback_context.inputs['volume.value'] == "OBV":
    #         print("OBV")
    #         add_fig_list1=add_figure1(None,"OBV")
    #     else:
        add_fig_list1=add_figure1(inputnumber1,overlap_value1)
        if add_fig_list1 is None:
            return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]

        #return [add_fig_list1[0], False, add_fig_list1[1],dash.no_update]
        print("ok")
        return [add_fig_list1[0], False, add_fig_list1[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]

    elif 'volume.value' == triggered_id:
        print("obv")

        if callback_context.triggered[0]['value'] == 'OBV':
            add_fig_list1=add_figure1(None,"OBV")
        # if add_fig_list1 is None:
        #     return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update]
            #return [add_fig_list1[0], False, add_fig_list1[1],dash.no_update]
            return [add_fig_list1[0], False, add_fig_list1[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]

    elif 'overlap_add2.n_clicks' == triggered_id:
        add_fig_list2=add_figure2(inputnumber2,overlap_add2)
        if add_fig_list2 is None:
            return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        #return [add_fig_list2[0], False, add_fig_list2[1],dash.no_update]
        return [add_fig_list2[0], False, add_fig_list2[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
    elif 'input_add3.n_clicks' == triggered_id:
        print("add3")
        add_fig_list3=add_figure3(inputnumber31,inputnumber32,inputnumber33)
        if add_fig_list3 is None:
            return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        return [add_fig_list3[0], False, add_fig_list3[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
    elif 'input_add4.n_clicks' == triggered_id:
        print("add4")
        add_fig_list4=add_figure4(inputnumber41,inputnumber42,inputnumber43)
        if add_fig_list4 is None:
            return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        return [add_fig_list4[0], False, add_fig_list4[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
    elif 'input_add5.n_clicks' == triggered_id:
        print("add5")
        if input_modelinput5=="SMACROSS":
            strategy_list5=strategy_smacross("SMACROSS",inputnumber51,input1_search,start_date,end_date)
        if input_modelinput5=="GOLDENDEATHCROSS":
            strategy_list5=strategy_goldendeathcross("GOLDENDEATHCROSS",inputnumber61,inputnumber62,input1_search,start_date,end_date)
        if input_modelinput5=="MACDS":
            strategy_list5=strategy_macds("MACDS",inputnumber71,inputnumber72,inputnumber73,input1_search,start_date,end_date)
        if strategy_list5 is None :
            return [dash.no_update,True,dash.no_update,"Please enter correct number!","Please enter correct number! Please try again!",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        print("sessionsymbol",session['symbol'])
        return [strategy_list5[0], False, strategy_list5[1],dash.no_update,dash.no_update,dash.no_update,session['symbol'],strategy_list5[2],strategy_list5[3],strategy_list5[4]]
#SMACROSS"},{"label": "Golden Cross and Death Cross","value":"GOLDENDEATHCROSS"},{"label": "MACD Strategy","value":"MACDS"}]
    elif 'submit-removal.n_clicks' == triggered_id:
        print(remove_indicator)
        remove_fig_list=remove_figure(remove_indicator)
        #print("remove:",remove_fig_list)
        #return [remove_fig_list[0], False,remove_fig_list[1],dash.no_update]
        if len(remove_fig_list) == 2:
            return [remove_fig_list[0], False,remove_fig_list[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        else:
            return [remove_fig_list[0], False,remove_fig_list[1],dash.no_update,dash.no_update,dash.no_update,dash.no_update,"","",""]
    # elif 'savefigure_name_save.n_clicks' == triggered_id:
    #     save_fig_list=savechart(savefigure_name,inputnotes)
    #     #return [save_fig_list[0],False,save_fig_list[1],dash.no_update]
    #     return [save_fig_list[0],False,save_fig_list[1]]
    elif 'loadfigure_name_load.n_clicks' == triggered_id:
        load_fig_list=loadchart(selected_cells)
        #return [load_fig_list[0],False,load_fig_list[1],dash.no_update]
        print("load fig:",load_fig_list[2])
        return [load_fig_list[0],False,load_fig_list[1],dash.no_update,dash.no_update,dash.no_update,load_fig_list[2],load_fig_list[3],load_fig_list[4],load_fig_list[5]]
    #IF URL FRESH TO GRAPH, EITHER IT IS NOT LOGIN OR ALREADY LOGIN
    elif callback_context.triggered[0]['value'] == '/graph':
        print("sessionid:",session.get("user_id"))
        if session.get("user_id") is None:
            app.index_string = index_string_logout
            print("none userid")
            return [dash.no_update, False,dash.no_update,"/login",dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
            #return redirect ("/login")
        #IF IT IS LOGIN, MAIN POINT IS THE FIRST LOGIN TIME TO LOAD LAST SESSION OR LOAD FROM THE DATABASE RECORD
        else:
            #app.index_string = index_string_login
            print("has userid")
            path_graph_list=path_graph()
            #BELOW CHECK WHETHER THE CHART INCLUDING THE STRATEGY TABLE ON TAB STRATEGY OR NOT
            if len(path_graph_list) == 3:
                print("3")
                return [path_graph_list[0],False,path_graph_list[1],dash.no_update,dash.no_update,path_graph_list[2],session['symbol'],dash.no_update,dash.no_update,dash.no_update]
            else:
                print("5")
                return [path_graph_list[0],False,path_graph_list[1],dash.no_update,dash.no_update,path_graph_list[2],session['symbol'],path_graph_list[3],path_graph_list[4],path_graph_list[5]]

#THIS FUNCTION FOR LOADING THE FIRST CHART
def figurechart(symbol,start_date,end_date):
    if symbol is None or symbol == "":
        return "empty"
    #TWO METHOD TO LOAD THE OHLC DATA, HISORY HAS MORE DATA THAN DOWNLOAD
    stock=yf.Ticker(symbol)
    dfe=stock.history(start=start_date, end=end_date)
    #dfe = yf.download(symbol,start=start_date, end=end_date)
    temp=dfe.to_string()
    if dfe.empty:
        return None
    #IF SEARCH SYMBOL SUCCESSFULLY FIND, REMOVE ALL THE EXISITING STATUS DATA
    if session.get('fightml') is not None:
        del session['fightml']
    if session.get('dft') is not None:
        del session['dft']
    if session.get('dfs') is not None:
        del session['dfs']
    if session.get('transactionheader') is not None:
        del session['transactionheader']


    #MAKING SUBPLOT AT THE BEGINNING WITH CANDLESTICK CHART AND VOLUME
    fig1 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1,subplot_titles=(symbol+"--"+stock.info['shortName']+'--OHLC', 'Volume'), row_width=[2,10])
    #specs=[[{'secondary_y':True}],[{}]],
    fig1.add_trace(go.Candlestick(x=dfe.index.values,open=dfe['Open'], high=dfe['High'],low=dfe['Low'], close=dfe['Close'],name=stock.info['shortName']),row=1, col=1)
    fig1.add_trace(go.Bar(x=dfe.index.values, y=dfe['Volume'],name="Volume",opacity=0.5,marker= dict(color=list(map(SetColorV,dfe['Open'], dfe['Close'])))),row=2, col=1)
    fig1=update_fig_layout(fig1)

    session["fig"]=fig1
    session["df"]=dfe
    session["symbol"]=symbol
    return fig1

#FUNCTION TO UPDATE LAYOUT AND AXES AFTER ADDING OR REMOVE TRACE
def update_fig_layout(fig1):
    fig1.update_layout(height=750,margin={'t':70,'r':20,'l':20,'b':20},autosize=True,legend=dict(orientation="h",yanchor="bottom",y=1.0,xanchor="right",x=1),
                       modebar_add=['drawline',
                                    'drawopenpath',
                                    'drawclosedpath',
                                    'drawcircle',
                                    'drawrect',
                                    'eraseshape'
                                    ],
                       modebar_remove=[],)
    fig1.update_xaxes(
        showticklabels=True,
        tickmode='auto',
        autorange=True,
        ticks='inside',
        rangeslider_visible=False,
        rangeselector=dict(
           buttons=list([
               dict(count=1, label="1m", step="month", stepmode="backward"),
               dict(count=6, label="6m", step="month", stepmode="backward"),
               dict(count=1, label="YTD", step="year", stepmode="todate"),
               dict(count=1, label="1y", step="year", stepmode="backward"),
               dict(step="all")
           ])
        ),
        #CAN BE ADDED THE HOLIDAY TOO BUT TROUBLE TO CHECK WHICH COUNTRY
        rangebreaks=[
            dict(bounds=["sat", "mon"]), #hide weekends
        ],
        showspikes=True, showgrid=False, tickangle=0,spikecolor="green", spikesnap="cursor", spikemode="across"
    )
    #fig1.update_xaxes(showspikes=True, showgrid=False, tickangle=-90,spikecolor="green", spikesnap="cursor", spikemode="across")
    fig1.update_yaxes(showspikes=True,
                      #dtick=10,
                      #ticklabelstep=100,
                      spikecolor="orange",
                      spikethickness=1,
                      spikesnap="cursor",
                      #spikedash="dot",
                      spikemode="across+marker",
                      #secondary_y=False
                     )
    return(fig1)

#THIS CALLBACK IS FOR UPDATE THE PRICE AND COMPANY DATA EACH TIME WHEN USER ADDING, REMOVEING INDICATOR OR LOAD SAVE FILE.
@callback(
    Output('website', 'href'),
    Output('logo_url', 'src'),
    Output('shortName', 'children'),
    Output('symbol', 'children'),
    Output('currentPrice','children'),
    Output('diffPrice','children'),

    # Output('previousClose','children'),
    # Output('open','children'),
    # Output('dayHigh','children'),
    # Output('dayLow','children'),
    # Output('volume1','children'),
    # Output('averageVolume10days','children'),
    # Output('fiftyTwoWeekHigh','children'),
    # Output('fiftyTwoWeekLow','children'),
    # Output('trailingPE',"children"),
    Output('ticker_data','children'),

    State('input-search', 'value'),
    Input('submit-search', 'n_clicks'),
    Input('input-search-dcc', 'value'),
    #Input('url','pathname'),
    # State('table', 'selected_cells'),
    # Input("loadfigure_name_load","n_clicks"),
    prevent_initial_call=True)
def company_info(input_search,submit_search,input_search_dcc):
    triggered_id = callback_context.triggered[0]['prop_id']
    print("company ",callback_context.triggered)

# METHOD TO SHOW EACH DATA PCS BY PCS INSTEAD OF TABLE
#     if 'submit-search.n_clicks' == triggered_id :
#         if input_search is None :
#             return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
#         ticker = yf.Ticker(input_search)
#         print(type(ticker))
#         if 'symbol' in ticker.info.keys():
#             #ticker_json=json.dumps(ticker.info,indent=4)
#             diffprice=ticker.info["currentPrice"]-ticker.info["previousClose"]
#             diff="{}{:.2f}".format("+" if diffprice>=0 else "",diffprice)
#             pe="{:.2f}".format(ticker.info["trailingPE"])
#             print(ticker.info["volume"])
#             return [ticker.info["website"],ticker.info["logo_url"],ticker.info["shortName"],ticker.info["symbol"],ticker.info["currentPrice"],diff,ticker.info["previousClose"],ticker.info["open"],ticker.info["dayHigh"],ticker.info["dayLow"],ticker.info["volume"],ticker.info["averageVolume10days"],ticker.info["fiftyTwoWeekHigh"],ticker.info["fiftyTwoWeekLow"],pe]

#         else:
#             return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
#     if triggered_id == 'input-search-dcc.value':
#         ticker = yf.Ticker(callback_context.triggered[0]['value'])
#         diffprice=ticker.info["currentPrice"]-ticker.info["previousClose"]
#         diff="{}{:.2f}".format("+" if diffprice>=0 else "",diffprice)
#         pe="{:.2f}".format(ticker.info["trailingPE"])
#         print(ticker.info["volume"])
#         return [ticker.info["website"],ticker.info["logo_url"],ticker.info["shortName"],ticker.info["symbol"],ticker.info["currentPrice"],diff,ticker.info["previousClose"],ticker.info["open"],ticker.info["dayHigh"],ticker.info["dayLow"],ticker.info["volume"],ticker.info["averageVolume10days"],ticker.info["fiftyTwoWeekHigh"],ticker.info["fiftyTwoWeekLow"],pe]

    #COMPANY INFO LEFT SIDE HAVE TWO TRIGGER , EITHER BY SEARCH OR DCC UPDATE BY LOAD TABLE OR GRAPH URL REFRESH
    if 'submit-search.n_clicks' == triggered_id :
        if input_search is None :
            return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        ticker = yf.Ticker(input_search)
        print(type(ticker))
        if 'symbol' not in ticker.info.keys():
            return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]
        else:
            #ticker_json=json.dumps(ticker.info,indent=4)
            diff, tickerTable=diff_tickerTable(ticker)
            return [ticker.info["website"],ticker.info["logo_url"],ticker.info["shortName"],ticker.info["symbol"],ticker.info["currentPrice"],diff,tickerTable]
    if triggered_id == 'input-search-dcc.value':
        ticker = yf.Ticker(callback_context.triggered[0]['value'])
        diff, tickerTable=diff_tickerTable(ticker)
        return [ticker.info["website"],ticker.info["logo_url"],ticker.info["shortName"],ticker.info["symbol"],ticker.info["currentPrice"],diff,tickerTable]

#TO MAKE DIFF AND TICKER TABLE FOR COMPANY INFO
def diff_tickerTable(ticker):
    diffprice=ticker.info["currentPrice"]-ticker.info["previousClose"]
    diff="{}{:.2f}".format("+" if diffprice>=0 else "",diffprice)
    pe="{:.2f}".format(ticker.info["trailingPE"])
    print(ticker.info["volume"])
    ticker_info={'attribute':[ 'LastClose', 'open', 'dayHigh', 'dayLow', 'volume', 'AvgVol10d',  '52WeekHigh', '52WeekLow','PE'],
                 'data':[ticker.info["previousClose"], ticker.info["open"], ticker.info["dayHigh"], ticker.info["dayLow"], ticker.info["volume"], ticker.info["averageVolume10days"], ticker.info["fiftyTwoWeekHigh"], ticker.info["fiftyTwoWeekLow"],pe]}

    dfi = pd.DataFrame(ticker_info)
    tickerTable=dash_table.DataTable(dfi.to_dict('records'),
                                     fixed_columns={'headers':True},
                                     cell_selectable=False,
                                     style_header = {'display': 'none'},
                                     style_data_conditional=[{'if': {'column_id': 'attribute'},'textAlign': 'left'}],
                                     style_cell = {'border': 'none',"background-color": "#f8f9fa"},
                                    )
    return diff, tickerTable
# @callback(
#     Output("overlap", "value"),
#     Output("momentum", "value"),
#     Output("volume", "value"),
#     Output("volatility", "value"),
#     #Output("input-search", "debounce"),
#     Input('overlap_add1', 'n_clicks'),
#     Input('overlap_add2', 'n_clicks'),
#     Input('input_add3', 'n_clicks'),
#     Input('input_add4', 'n_clicks'),
#     prevent_initial_call=True
# )
# def default_value(overlap_add1,overlap_add2,input_add3,input_add4):
#     triggered_id = callback_context.triggered[0]['prop_id']
#     if triggered_id == "overlap_add1.n_clicks" or triggered_id == "overlap_add2.n_clicks" or triggered_id == "input_add3.n_clicks" or triggered_id == "input_add4.n_clicks":
#         print("default")
#         return ["","","",""]

#CALLBACK TO POP THE STATIC MODAL FOR DIFFERENT INDICATOR AND MODAL 1 -4 IS FOR DIFFERENT MODAL AND DIFFERENT INDICATOR, SOME INDICATOR REQUIRED ONE INPUT, SOME REQUIRED MORE INPUT
@callback(
    Output("overlap_modal1", "is_open"),
    Output("overlap_modelinput1","data"),
    Output("overlap_modal2", "is_open"),
    Output("overlap_modelinput2","data"),
    Output("input_modal3", "is_open"),
    Output("input_modelinput3","data"),
    Output("input_modal4", "is_open"),
    Output("input_modelinput4","data"),
    #SELECTION OF DROPDOWN MANUEL
    [Input("overlap", "value")],
    [Input("momentum", "value")],
    [Input("volume", "value")],
    [Input("volatility", "value")],
    #STATUS OF MODAL BOX AND ADD CLICK BUTTON
    [State("overlap_modal1", "is_open")],
    Input('overlap_add1', 'n_clicks'),
    [State("overlap_modal2", "is_open")],
    Input('overlap_add2', 'n_clicks'),
    [State("input_modal3", "is_open")],
    Input('input_add3', 'n_clicks'),
    [State("input_modal4", "is_open")],
    Input('input_add4', 'n_clicks'),

    prevent_initial_call=True
)
def toggle_modal(overlapvalue,momentum,volume,volatility, is_open1,n1,is_open2,n2,is_open3,n3,is_open4,n4):
    triggered_id = callback_context.triggered[0]['prop_id']
    #BELOW IF ELSE SELECT THE FOUR DROPDOWN BOX INDICATOR AND THEN POP UP THE CORRECT MODAL:
    if triggered_id == "overlap.value":
        if callback_context.inputs['overlap.value']=="BBANDS":
            return [False, "", True, overlapvalue,False,None,False,None]
        return [True, overlapvalue, False,None,False,None,False,None]

    elif triggered_id == "momentum.value":
        if callback_context.inputs['momentum.value']=="MACD":
            return [False, None, False, None,True,momentum,False,None]
        elif callback_context.inputs['momentum.value']=="STOCH":
            return [False, None, False, None,False,None,True,momentum]
        return [True,momentum,False,None,False,None,False,None]
    elif triggered_id == "volume.value":
        #IT SEEMS BELOW COMMENTS IS NOT WORK
        #if callback_context.inputs['volume.value']=="OBV":
        if callback_context.triggered[0]['value']=="OBV":
            return[False,volume,False,n2,False,n3,False,None]
        return [True, volume, False, n2,False,n3,False,None]
    elif triggered_id == "volatility.value":
        return [True, volatility, False, n2,False,n3,False,None]
    #USED TO CLOSE THE INPUT PERIOD MODAL BOX
    elif triggered_id == "overlap_add1.n_clicks":
        return [False,dash.no_update,False,"",False,n3,False,None]
    elif triggered_id == "overlap_add2.n_clicks":
        return [False,dash.no_update,False,"",False,n3,False,None]
    elif triggered_id == "input_add3.n_clicks":
        return [False,dash.no_update,False,"",False,n3,False,None]
    elif triggered_id == "input_add4.n_clicks":
        return [False,dash.no_update,False,"",False,n3,False,None]

#THIS CALLBACK IS NOT USED ANYMORE TO ADD REMOVE INDICATOR
# @app.callback(
#     Output("remove_indicator","options"),
#     State("modelinput","data"),
#     Input('submit-button-state', 'n_clicks'),
#     State('input1', 'value'),
#     prevent_initial_call=True
# )
# def indicator_history(overlap_value,n,inputnumber1):
#     triggered_id = callback_context.triggered[0]['prop_id']
#     if 'submit-button-state.n_clicks' == triggered_id:

#         new_data = list(session["fig"].data).copy()

#         # for i in range(len(new_data)):
#         #     if new_data[i]['name'] == "ema"+str(inputnumber):
#         #         #new_data.pop[i]
#         #         del new_data[i]
#         #         fig1.data=new_data
#         #         return fig1
#         del new_data[0]
#         temp=[x['name'] for x in new_data]
#         print(temp)
#         return (temp)
#         #return ([overlap_value+str(inputnumber1)])


def path_graph():
    #print(session["fig"])
    #IF THE SESSION FIG IS NONE WHEN LOGIN FIRST TIME, IT LOADED THE DATA FROM DATABASE
    if session.get("fig") is None:
        db = con.cursor()
        rows=[]
        for row in db.execute("SELECT notesname,userid, stockname,stocksymbol,graphnotes,statusjson,df,transactionjson,summaryjson,htmljson,transactionheader FROM chartstatus WHERE userid=(?) ORDER by time DESC ",(session["user_id"],)):
            rows.append(row)
        con.commit()
        #NEED TO CHECK AND ADD FUNCTION IF THERE IS NO DATABASE RECORD, MAY BE NEED TO RETURN AAPL AT LEAST
        if len(rows) ==0:
            fig1=figurechart(symbol="AAPL",start_date=date.today()-timedelta(days=365),end_date=date.today()-timedelta(days=1))
            session['fig']=fig1
            session["symbol"]="AAPL"
            new_data = list(session["fig"].data).copy()
            del new_data[0:2]
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
            #msg="Hi {},today is {}".format(session['username'],date.today().strftime("%b %d, %Y"))
            welcomemsg="Hi {}".format(session['username'])
            return [session["fig"],current_indicator_list,welcomemsg,"", "", ""]
        #FROM THE LOADING DATA FROM DATABASE, IT REQUIRED TO CONVERT THE JSON STRING TO FIGURE AND DATAFRAME
        #figjson=json.loads(rows[0]["statusjson"])
        figjson=json.loads(rows[0][5])
        fig10=pio.from_json(figjson)
        session["fig"]=fig10
        dfstring=rows[0][6]
        dfjson=json.loads(dfstring)
        session["df"]=pd.read_json(dfjson)
        session['symbol']=row[0][3]
        #CHECK THE STRATEGY DATA AVAILABLE AND CONVERT TO DATAFRAME
        if len(rows[0][7]) != 0:
            djson = json.loads(rows[0][7])
            dft=pd.DataFrame.from_dict(djson, orient='index')
            dft.index=dft.index.str.slice(0, 10, 1)
            dft.index=pd.to_datetime(dft.index, unit='s')
            session['dft']=dft
        if len(rows[0][8]) != 0:
            djson = json.loads(rows[0][8])
            dfs=pd.DataFrame.from_dict(djson, orient='index')
            dfs.index=dfs.index.str.slice(0, 10, 1)
            dfs.index=pd.to_datetime(dfs.index, unit='s')
            session['dfs']=dfs
        htmljson=json.loads(rows[0][9])
        fightml=pio.from_json(htmljson)
        #session["fightml"]=fightml
        if len(rows[0][7]) != 0:
            headerMessage=rows[0][10]
            session['transactionheader']=headerMessage
            session['dft']=dft
            session['dfs']=dfs
            strategyTable,strategySummary=strategy_table(dft,dfs)
            session["fig"]=fig10
            session["df"]=pd.read_json(dfjson)
            session["symbol"]=rows[0][3]
            #session["fightml"]=go.Figure(fig10)

            new_data = list(fig10.data).copy()
            del new_data[0:2]
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
            #welcomemsg="Hi {},today is {}".format(session['username'],date.today().strftime("%b %d, %Y"))
            welcomemsg="Hi {}".format(session['username'])
            return [fig10,current_indicator_list,welcomemsg,strategyTable, headerMessage, strategySummary]
        #REMOVE PREVIOUS SESSION DFT,DFS, TRANSACTIONHEADER IF CURRENTLY LOADING DATA DONT HAVE STRATEGY DATA
        else:
            if session.get('transactionheader') is not None:
                del session['transactionheader']
            if session.get('dft') is not None:
                del session['dft']
            if session.get('dfs') is not None:
                del session['dfs']
            session["symbol"]=rows[0][3]
            new_data = list(session["fig"].data).copy()
            del new_data[0:2]
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
            #welcomemsg="Hi {},today is {}".format(session['username'],date.today().strftime("%b %d, %Y"))
            welcomemsg="Hi {}".format(session['username'])
            return [session["fig"],current_indicator_list,welcomemsg,"", "", ""]

    #IF IT IS NOT LOGIN FOR FIRST TIME, THERE MUST HAVE SESSION FIG AND USE THOSE SESSION TO REFRESH THE CHART AND STRATEGY
    else:
        fig10=session["fig"]
        #session["fightml"]=go.Figure(fig10)
        print("have session")
        #print(fig10.data)
        new_data = list(fig10.data).copy()
        del new_data[0:2]
        current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
        #welcomemsg="Hi {},today is {}".format(session['username'],date.today().strftime("%b %d, %Y"))
        welcomemsg="Hi {}".format(session['username'])
        if session.get('dft') is not None:
            dft=session['dft']
        if session.get('dfs') is not None:
            dfs=session['dfs']
            strategyTable,strategySummary=strategy_table(dft,dfs)
            return [fig10,current_indicator_list,welcomemsg,strategyTable,session['transactionheader'],strategySummary]
        else:
            return [fig10,current_indicator_list,welcomemsg]

#ADD TRACE FOR INDICATOR WHICH IS ONLY ONE INPUT NUMBER
def add_figure1(inputnumber,overlap_value):
    df=session["df"]
    if overlap_value == "SMA":
        try:
            ma=talib.SMA(df['Close'], timeperiod=inputnumber)
        except:
            return None
    elif overlap_value == "EMA":
        try:
            ma=talib.EMA(df['Close'], timeperiod=inputnumber)
        except:
            return None
    elif overlap_value == "ADX":
        try:
            ma=talib.ADX(df['High'],df['Low'],df['Close'], timeperiod=inputnumber)
        except:
            return None
    elif overlap_value == "DX":
        try:
            ma=talib.DX(df['High'],df['Low'],df['Close'], timeperiod=inputnumber)
            minus_dm=talib.MINUS_DM(df['High'],df['Low'], timeperiod=inputnumber)
            plus_dm=talib.PLUS_DM(df['High'],df['Low'], timeperiod=inputnumber)
            minus_dmframe=minus_dm.to_frame()
            plus_dmframe=plus_dm.to_frame()
        except:
            return None
    elif overlap_value == "MOM":
        try:
            ma=talib.MOM(df['Close'], timeperiod=inputnumber)
        except:
            return None

    elif overlap_value == "OBV":
        try:
            ma=talib.OBV(df['Close'],df['Volume'])
        except:
            return None

    elif overlap_value == "ATR":
        try:
            ma=talib.ATR(df['High'],df['Low'],df['Close'], timeperiod=inputnumber)
        except:
            return None
    elif overlap_value == "RSI":
        try:
            ma=talib.RSI(df['Close'], timeperiod=inputnumber)
        except:
            return None
    maframe=ma.to_frame()
    fig1=session["fig"]
    #fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, subplot_titles=(symbol+"--"+stock.info['shortName']+'--OHLC', 'Volume'), row_width=[1,5],figure=fig1)
    #fig1 =  make_subplots(shared_xaxes=True, vertical_spacing=0.1,figure=fig1)
    name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()
    print("indicator: ",name_list)
    #IF THE TRACE IS NEED TO ADD IN THIRD SUBPLOT, NEED TO REMOVE OLD THIRD SUBPLOT FIRST
    if overlap_value == "ADX" or overlap_value == "DX" or overlap_value == "MOM" or overlap_value == "OBV" or overlap_value == "ATR" or overlap_value == "RSI":
        third_row_indicator=find_third_row()
        if third_row_indicator is not None:
            remove_figure(third_row_indicator)

        fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],overlap_value+"" if inputnumber is None else overlap_value+str(inputnumber)),
                                             row_width=[2,2,10],figure=fig1)
        #subplot_titles=(session["symbol"]+"--"+stock.info['shortName']+'--OHLC','Volume',overlap_value)
        print(fig1)
        print(fig1.layout.xaxis3)
        if overlap_value == "DX":
            fig1.add_trace(go.Scatter(mode="lines", x=maframe.index.values, y=maframe[0],legendgroup="DX",name=overlap_value+"" if inputnumber is None else
                                      overlap_value+str(inputnumber),), row=3, col=1)
            fig1.add_trace(go.Scatter(mode="lines", x=minus_dmframe.index.values, y=minus_dmframe[0],legendgroup="DX",name=overlap_value+"" if inputnumber is None else   overlap_value+""+str(inputnumber),) ,row=3, col=1)
            fig1.add_trace(go.Scatter(mode="lines", x=plus_dmframe.index.values, y=plus_dmframe[0],legendgroup="DX",name=overlap_value+"" if inputnumber is None else overlap_value+""+str(inputnumber),) ,row=3, col=1)
        #IF TRACE IS ADX,MOM,OBV,ATR,RSI
        else:
            fig1.add_trace(go.Scatter(mode="lines", x=maframe.index.values, y=maframe[0],name=overlap_value+"" if inputnumber is None else overlap_value+str(inputnumber),),row=3, col=1)
            # fig1.add_hline(y=80, line_width=1, line_dash="dot", line_color="red",row=3)
            # fig1.add_hline(y=20, line_width=1, line_dash="dot", line_color="red",row=3)
        fig1=update_fig_layout(fig1)
        fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],overlap_value+"" if inputnumber is None else overlap_value+str(inputnumber)),
                                             row_width=[2,2,10],figure=fig1)


    else:
        print("trace",overlap_value+str(inputnumber))
        third_row_indicator=find_third_row()
        if third_row_indicator is not None:
            fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             #subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],overlap_value+"" if inputnumber is None else overlap_value+str(inputnumber)),
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],third_row_indicator),
                                             row_width=[2,2,10],figure=fig1)
        else:
            fig1 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1]),
                                             row_width=[2,10],figure=fig1)

        fig1.add_trace(go.Scatter(mode="lines", x=maframe.index.values, y=maframe[0],name=overlap_value+str(inputnumber)),row=1, col=1)
    session["fig"]=fig1
    session["fightml"]=go.Figure(fig1)
    #print(session["fig"])
    new_data = list(session["fig"].data).copy()
    print("new_data:",new_data)
    del new_data[0:2]

    print("new_data_new:",new_data)
    current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
    print(callback_context.triggered[0]['value'])
    print(callback_context.inputs)
    print(callback_context.inputs_list)
    print(fig1.data)
    print(current_indicator_list)
    return [fig1,current_indicator_list]

#ADD TRACE FOR THE BB BANDS
def add_figure2(inputnumber, std):
    df=session["df"]
    try:
        upperband, middleband, lowerband=talib.BBANDS(df['Close'], timeperiod=inputnumber,nbdevup=std, nbdevdn=std, matype=0)
    except:
        return None

    upperbandframe=upperband.to_frame()
    middlebandframe=middleband.to_frame()
    lowerbandframe=lowerband.to_frame()
    fig1=session["fig"]
    #fig1 = make_subplots(shared_xaxes=True, vertical_spacing=0.1,figure=fig1)

    fig1.add_trace(go.Scatter(mode="lines",fill=None, x=upperbandframe.index.values, y=upperbandframe[0],legendgroup="BBANDS",name="BBANDS "+str(inputnumber)+" "+str(std),marker= {"color": "#ccc"},),row=1, col=1)
    fig1.add_trace(go.Scatter(mode="lines",fill='tonexty', x=lowerbandframe.index.values, y=lowerbandframe[0],legendgroup="BBANDS",name="BBANDS "+str(inputnumber)+" "+str(std),showlegend=False,marker= {"color": "#ccc"}),row=1, col=1)
    fig1.add_trace(go.Scatter(mode="lines", x=middlebandframe.index.values, y=middlebandframe[0],legendgroup="BBANDS",name="BBANDS "+str(inputnumber)+" "+str(std),showlegend=False,marker= {"color": "#ccc"}),row=1, col=1)

    session["fig"]=fig1
    session["fightml"]=go.Figure(fig1)
    #print(session["fig"])
    new_data = list(session["fig"].data).copy()
    del new_data[0:2]
    print(fig1.data)

    current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data if x['name'] != None])).copy()
    print(callback_context.triggered[0]['value'])
    print(callback_context.inputs)
    print(callback_context.inputs_list)
    return [fig1,current_indicator_list]

#ADD TRACE FOR THE MACD
def add_figure3(fastperiod1, slowperiod1, signalperiod1):
    df=session["df"]
    #macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    try:
        macd, macdsignal, macdhist = talib.MACD(df['Close'], fastperiod=fastperiod1, slowperiod=slowperiod1, signalperiod=signalperiod1)
    except:
        return None

    macdframe=macd.to_frame()
    macdsignalframe=macdsignal.to_frame()
    macdhistframe=macdhist.to_frame()
    fig1=session["fig"]
    name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()
    third_row_indicator=find_third_row()
    if third_row_indicator is not None:
        remove_figure(third_row_indicator)

    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                         subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],"MACD "+str(fastperiod1)+" "+str(slowperiod1)+" "+str(signalperiod1)),
                                         row_width=[2,2,10],figure=fig1)

    fig1.add_trace(go.Scatter(mode="lines",fill=None, x=macdframe.index.values, y=macdframe[0],legendgroup="MACD",name="MACD "+str(fastperiod1)+" "+str(slowperiod1)+" "+str(signalperiod1),marker= {"color": "blue"},),row=3, col=1)
    fig1.add_trace(go.Scatter(mode="lines",fill='tonexty', x=macdsignalframe.index.values, y=macdsignalframe[0],legendgroup="MACD",name="MACD "+str(fastperiod1)+" "+str(slowperiod1)+" "+str(signalperiod1),showlegend=False,marker= {"color": "orange"}),row=3, col=1)
    fig1.add_trace(go.Bar( x=macdhistframe.index.values, y=macdhistframe[0],legendgroup="MACD",name="MACD "+str(fastperiod1)+" "+str(slowperiod1)+" "+str(signalperiod1),showlegend=False,marker= {"color": "red"}),row=3, col=1)
    fig1=update_fig_layout(fig1)
    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                         subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],"MACD "+str(fastperiod1)+" "+str(slowperiod1)+" "+str(signalperiod1)),
                                         row_width=[2,2,10],figure=fig1)

    session["fig"]=fig1
    session["fightml"]=go.Figure(fig1)
    #print(session["fig"])
    new_data = list(session["fig"].data).copy()
    del new_data[0:2]
    print(fig1.data)

    current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data if x['name'] != None])).copy()
    print(callback_context.triggered[0]['value'])
    print(callback_context.inputs)
    print(callback_context.inputs_list)
    return [fig1,current_indicator_list]

#ADD TRACE FOR THE STOCH
def add_figure4(fastk_period1, slowk_period1, slowd_period1):
    df=session["df"]
    try:
        slowk, slowd = talib.STOCH(df['High'],df['Low'],df['Close'], fastk_period=fastk_period1, slowk_period=slowk_period1, slowk_matype=0, slowd_period=slowd_period1, slowd_matype=0)
    except:
        return None

    slowkframe=slowk.to_frame()
    slowdframe=slowd.to_frame()
    fig1=session["fig"]
    name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()
    third_row_indicator=find_third_row()
    if third_row_indicator is not None:
        remove_figure(third_row_indicator)

    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                         subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],"STOCH "+str(fastk_period1)+" "+str(slowk_period1)+" "+str(slowd_period1)),
                                         row_width=[2,2,10],figure=fig1)

    fig1.add_trace(go.Scatter(mode="lines",fill=None, x=slowkframe.index.values, y=slowkframe[0],legendgroup="STOCH",name="STOCH "+str(fastk_period1)+" "+str(slowk_period1)+" "+str(slowd_period1),marker= {"color": "blue"},),row=3, col=1)
    fig1.add_trace(go.Scatter(mode="lines", x=slowdframe.index.values, y=slowdframe[0],legendgroup="STOCH",name="STOCH "+str(fastk_period1)+" "+str(slowk_period1)+" "+str(slowd_period1),showlegend=False,marker= {"color": "orange"}),row=3, col=1)
    #fig1.add_trace(go.Bar(x=dfe.index.values, y=dfe['Volume'],name="Volume"),row=2, col=1)
    fig1=update_fig_layout(fig1)
    fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                         subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],"STOCH "+str(fastk_period1)+" "+str(slowk_period1)+" "+str(slowd_period1)),
                                         row_width=[2,2,10],figure=fig1)

    session["fig"]=fig1
    session["fightml"]=go.Figure(fig1)
    #print(session["fig"])
    new_data = list(session["fig"].data).copy()
    del new_data[0:2]
    print(fig1.data)

    current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data if x['name'] != None])).copy()
    print(callback_context.triggered[0]['value'])
    print(callback_context.inputs)
    print(callback_context.inputs_list)
    return [fig1,current_indicator_list]

#TO CHECK WHETHER THERE ARE THREE CHART IN THE MAIN PLOT
def find_third_row():
    fig1=session["fig"]
    new_data =list(fig1.data).copy()
    for i in range(len(new_data)):
        if new_data[i]['yaxis'] == 'y3':
            return new_data[i]['name']
    return None

#IT IS FOR DELETE ONE INDICATOR , INDICATOR EITHER IN MAIN CANDLE STICK CHART AND EASY TO REMOVE. IF IT IS IN THIRD SUBPLOT, WE NEED TO UPDATE SUBPLOT TO ROW 2, ALSO, IT REQUIRED TO REMOVE STRATEGY IN SECOND TAP IF THE INDICATOR IS STRATEGY
def remove_figure(remove_indicator):
    fig1=session["fig"]
    third_row_indicator=find_third_row()
    new_data =list(fig1.data).copy()
    new_data1=[]
    print("new_data: ",new_data)
    print("remove i:",remove_indicator)
    for i in range(len(new_data)):
        if new_data[i]['name'] != remove_indicator:
            new_data1.append(new_data[i])
    fig1.data=new_data1
    print("fig1:",fig1)
    name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()
    #GET THE INDICATOR LIST FOR REMOVE
    temp=list(dict.fromkeys([x['name'] for x in new_data1])).copy()
    del temp[0:2]

    #print(temp)
    print(remove_indicator,third_row_indicator,name_list,remove_indicator[0:3])
    if remove_indicator[0:3] == "ADX" or remove_indicator[0:2] == "DX" or remove_indicator[0:3] == "MOM" or remove_indicator[0:3] == "OBV" or remove_indicator[0:3] == "ATR" or remove_indicator[0:4] == "MACD" or remove_indicator[0:3] == "RSI" or remove_indicator[0:5] == "STOCH" or remove_indicator[0:5] == "MACDS":

        fig1 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1,subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1]),row_width=[2,10],figure=fig1)
        print("fig1lay:",fig1.layout)
        print(fig1.layout.annotations[0])
        #REMOVE THE LAYOUT ANNOTATION AND AXIS TO MAKE IT IS 2 ROW SUBPLOTS
        temp1=list(fig1.layout.annotations)
        if len(temp1)==3:
            del temp1[2]
            print (temp1)
            fig1.layout.pop('yaxis3')
            fig1.layout.pop('xaxis3')
        # del fig1.layout.yaxis3
        # del fig1.layout.xaxis3
        fig1.layout.annotations=temp1
        #del fig1.layout.annotations[3]
        print("fig1lay:",fig1.layout)
    session['fig']=fig1
    session["fightml"]=go.Figure(fig1)
    #CHECK THE REMOVE INDICATOR IS STRATEGY AND REMOVE THE STARTEGY TABLE
    if remove_indicator[0:5] == "MACDS" or remove_indicator[0:16] == "GOLDENDEATHCROSS" or remove_indicator[0:8] == "SMACROSS":
        del session['dft']
        del session['dfs']
        del session['transactionheader']
        return [fig1, temp, "","",""]
    return [fig1, temp]

#CALLBACK FOR TO OPEN SAVE MODAL AND AFTER INPUT THE NOTES AND SAVE NAME, IT CLOSE
@callback(
    Output("Notes_modal", "is_open"),
    Output("savefigure_name", "value"),
    Output("inputnotes","value"),
    #SUBMIT SAVE BUTTON AND POP UP SAVE MODAL
    State("Notes_modal", "is_open"),
    Input("submit-save", "n_clicks"),
    #WRITE SAVE NAME AND NOTES AND SAVE AND MODAL CLOSE
    State("savefigure_name", "value"),
    State("inputnotes","value"),
    Input("savefigure_name_save","n_clicks"),

    prevent_initial_call=True
)
def toggle_modal_save(noted_modal,submit_save,savefigure_name,inputnotes,savefigure_name_save):
    triggered_id = callback_context.triggered[0]['prop_id']
    print("save trigger:",callback_context.triggered)
    if 'submit-save.n_clicks' == triggered_id:
        return [True,"",""]
    if 'savefigure_name_save.n_clicks' == triggered_id:
        save_fig_list=savechart(savefigure_name,inputnotes)
        #return [save_fig_list[0],False,save_fig_list[1],dash.no_update]
        return [False,"",""]

#SAVE THE CURRENT CHART AND STRATEGY TO DATABASE WITH FILE NAME AND MESSAGE
def savechart(savefigure_name,inputnotes):
    session_df=session["df"]
    session_fig=session["fig"]
    session_fightml=session["fightml"]
    new_data =list(session["fig"].data).copy()
    #MAKE DF DATAFRAME TO STRING FOR SAVING IN DATABASE
    #dfstr=session_df.to_string()
    dfstr=json.dumps(session_df.to_json())

    #MAKE THE FIGURE TO JSON STRING TO SAVE IN DATABASE
    figjson = json.dumps(session_fig.to_json())
    fightmljson=json.dumps(session_fightml.to_json())
    print(session_fig.layout)
    textlayout=session_fig.layout
    print(textlayout['annotations'][0]['text'])
    #stock_symbol = new_data[0]['name'].rsplit("--")
    #GET THE STOCK NAME AND SYMBOL AND SPLIT TO NAME AND SYMBOL
    stock= textlayout['annotations'][0]['text'].rsplit("--")
    stock_symbol=stock[0]
    stockname=stock[1]
    print(stock_symbol," ",stockname)
    db = con.cursor()
    #CHECK THE DFT DFS TRANSACTIONHEADER DATAFRAME AVAILABLE AND CONVERT  TO JSON STRONG AND SAVE TO DATABASE
    if session.get('dft') is not None:
        session_dft_json=session['dft'].to_json(orient="index")
    else:
        session_dft_json=""
    if session.get('dfs') is not None:
        session_dfs_json=session['dfs'].to_json(orient="index")
    else:
        session_dfs_json=""
    if session.get('transactionheader') is not None:
        session_transactionheader=session['transactionheader']
    else:
        session_transactionheader=""
    db.execute("INSERT INTO chartstatus (notesname,userid, stockname,stocksymbol,graphnotes,statusjson,df,transactionjson,summaryjson,htmljson,transactionheader) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                           (savefigure_name,session["user_id"],stockname,stock_symbol,inputnotes,figjson,dfstr,session_dft_json,session_dfs_json,fightmljson,session_transactionheader))
    con.commit()
    #GET THE REMOVE INDICATOR LIST
    temp=list(dict.fromkeys([x['name'] for x in new_data])).copy()
    del temp[0:2]
    return [session_fig,temp]

#CALLBACK TO POP LOAD MODAL TABLE AND THEN LOADED THE SAVE DATA FROM DATABASE
@callback(
    Output("Load_modal", "is_open"),
    Output("submit-load", "n_clicks"),
    Output("loadfigure_name_load","n_clicks"),
    Output("tablerow","children"),

    State("Load_modal", "is_open"),
    #POP UP THE LOADING MODAL
    [Input("submit-load", "n_clicks")],
    #BUTTON TO LOADED TABLE AFTER ROW SELECTED
    Input("loadfigure_name_load","n_clicks"),
    prevent_initial_call=True,
)
def toggle_modal_load(is_open,n1,n2):
    #IF LOAD BUTTON CLICKS
    if n1:
        # NO NEED TO FETCH ROW BY ROW, WE CAN FETCHALL ROW AT ONE TIME IN DATAFRAME
        # for row in db.execute("SELECT userid, stockname,stocksymbol,graphnotes,statusjson FROM chartstatus WHERE userid=5 AND stockname=(?)",(inputnumber,)):
        # rows.append(row)
        # con.commit()
        db = con.cursor()
        rows=db.execute("SELECT id,notesname,time, stockname,stocksymbol,graphnotes FROM chartstatus WHERE userid=(?) ORDER by time DESC ",(session["user_id"],))
        df = pd.DataFrame(rows.fetchall())
        #df.columns = rows.keys()
        print(df)
        print(rows)
        #df.columns = rows.column_names
        df.columns = ['id','notesname','time', 'stockname','stocksymbol','graphnotes']
        return [True, 0, 0,generate_table(df, len(df.index))]
    #ADDED BUTTON PRESS AFTER ROW SELECTED, IT WILL CLOSED AND IT ALSO HAVE ANOTHER OUTPUT IN ANOTHER CALLBACK
    if n2:
        return [False, 0,0,dash.no_update]

#CALLBACK TO SELECT WHOLE ROLL OF LOADING TABLE BY CHANGING THE COLOR OF THE ROW CELL
@callback(
    Output('table', 'style_data_conditional'),
    #Input('table','data'),
    Input('table', 'selected_cells'),
    prevent_initial_call=True)
def rowselected(selected_cells):
    row_color=[{'if': {'row_index': 'odd'},'backgroundColor': 'rgb(220, 220, 220)'},
               {"if": {"state": "selected"},"backgroundColor": "rgb(120, 120, 120)","border": "0px"},
               {'if': {'row_index': selected_cells[0]['row']},'backgroundColor': 'rgb(120, 120, 120)'},
             ]
    return row_color

#LOAD THE SAVED CHART FROM DATABASE
def loadchart(selected_cells):
    session_df=session["df"]
    session_fig=session["fig"]
    if selected_cells != None:
        print("cell:",selected_cells)
        rowindex=selected_cells[0]['row_id']
        print("rowindex:",rowindex)
        db = con.cursor()
        rows=[]
        for row in db.execute("SELECT notesname,userid, stockname,stocksymbol,graphnotes,statusjson,df,transactionjson,summaryjson,htmljson,transactionheader FROM chartstatus WHERE userid=(?) AND id=(?) ORDER by time DESC ",(session["user_id"],rowindex)):
            rows.append(row)
        con.commit()
        #CONVERT BACK THE SAVED FIGURE TO FIG OBJECT
        figjson=json.loads(rows[0][5])
        fig11=pio.from_json(figjson)
        fig10=go.Figure(fig11)
        session["fig"]=fig10
        #CONVERT  THE DF TO DATAFRAME FROM DATABASE
        dfstring=rows[0][6]
        print(type(dfstring))
        #print(dfstring)
        dfjson=json.loads(dfstring)
        session["df"]=pd.read_json(dfjson)
        print("dfjson")
        print(dfjson)
        print(rows[0][7])
        #CONVER THE STRATEGY TRANSACTION AND SUMMARY FROM STR TO DATAFRAME
        if len(rows[0][7]) != 0:
            djson = json.loads(rows[0][7])
            dft=pd.DataFrame.from_dict(djson, orient='index')
            dft.index=dft.index.str.slice(0, 10, 1)
            dft.index=pd.to_datetime(dft.index, unit='s')
            session['dft']=dft
        if len(rows[0][8]) != 0:
            djson = json.loads(rows[0][8])
            dfs=pd.DataFrame.from_dict(djson, orient='index')
            dfs.index=dfs.index.str.slice(0, 10, 1)
            dfs.index=pd.to_datetime(dfs.index, unit='s')
            session['dfs']=dfs
        session["symbol"]=rows[0][3]
        htmljson=json.loads(rows[0][9])
        fightml=pio.from_json(htmljson)
        #session["fightml"]=fightml
        if len(rows[0][7]) != 0:
            headerMessage=rows[0][10]
            session['transactionheader']=headerMessage
            session['dft']=dft
            session['dfs']=dfs
            strategyTable,strategySummary=strategy_table(dft,dfs)
            #print(fightml)

            new_data = list(session["fig"].data).copy()
            del new_data[0:2]
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
            return [session["fig"],current_indicator_list,rows[0][3],strategyTable, headerMessage, strategySummary]
        else:
            if session.get('transactionheader') is not None:
                del session['transactionheader']
            if session.get('dft') is not None:
                del session['dft']
            if session.get('dfs') is not None:
                del session['dfs']

            new_data = list(session["fig"].data).copy()
            del new_data[0:2]
            current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
            return [session["fig"],current_indicator_list,rows[0][3],"", "", ""]

    return [dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update,dash.no_update]


#FUNCTION TO GENERATE THE LOADING TABLE BY INPUT THE DATAFRAME
def generate_table(dataframe, max_rows=10):
    #dataframe=dataframe.drop(columns=["id"])
    dashtable=dash_table.DataTable(dataframe.to_dict('records'),[{"name": i, "id": i} for i in dataframe.columns], css=[{"selector": ".show-hide", "rule": "display: none"}],id='table',
    #dashtable=dash_table.DataTable(dataframe.to_dict('records'),columns=[{'id':['Save Name','Date','Name','Symbol','Notes Reminder'],'name':['Save Name','Date','Name','Symbol','Notes Reminder']}], css=[{"selector": ".show-hide", "rule": "display: none"}],id='table',
    # dashtable=dash_table.DataTable(dataframe.to_dict('records'),[{"name": 'Save Name', "id": 'Save Name'},{"name":'Date', "id":'Date'},{"name":'Name', "id":'Name'},{"name":'Symbol', "id":'Symbol'},{"name": 'Notes Reminder', "id": 'Notes Reminder'}], css=[{"selector": ".show-hide", "rule": "display: none"}],id='table',

        style_data_conditional=[
            {
                 'if': {'row_index': 'odd'},
                 'backgroundColor': 'rgb(220, 220, 220)'
                # "if": {"state": "selected"},              # 'active' | 'selected'
                # "backgroundColor": "rgb(220, 220, 220)",
                #"border": "1px solid blue",
            }
        ],
        style_header={
            'backgroundColor': 'rgb(210, 210, 210)',
            'color': 'black',
            'fontWeight': 'bold'
        },
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto',
        },
        style_cell_conditional=[
        {'if': {'column_id': 'id'},
         'width': '0%'}],
        #row_selectable='single',
        # selected_rows=[1,3],
        hidden_columns=["id"],
    ),
    return dashtable

#THERE ARE OTHER METHOD TO GENERATE TABLE USING HTML AND ROM DATAFRAME
# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])

# def generate_table(dataframe, max_rows=10):
#     return dbc.Table.from_dataframe(dataframe, striped=True, bordered=True, hover=True, responsive=True,index=False)

#THIS CALLBACK IS FOR DOWNLOAD CHART AS HTML FILE
#THE HTML FILE IS JUST A LARGE FIG SUBPLOT OBJECT INCLUDING TABLE FIGURE IF NECESSSARY.
@callback(
    Output("downloadChart", "data"),
    Input("downloadChartbtn", "n_clicks"),
    prevent_initial_call=True,
)
def download_chart(n_clicks):
    triggered_id = callback_context.triggered[0]['prop_id']
    print(callback_context.triggered)
    fig1=session['fig']
    if session.get('dft') is not None:
        dft=session['dft']
    if session.get('dfs') is not None:
        dfs=session['dfs']
    if session.get('transactionheader') is not None:
        headerMessage=session['transactionheader']
    if 'downloadChartbtn.n_clicks' == triggered_id:
        print("download chart")
        session["fightml"] = go.Figure(fig1)

        fig2=session["fightml"]
        print(fig2)
        print(session['symbol'])
        if session.get('dft') is not None:

            thirdrowname=find_third_row()
            if thirdrowname is None:
                rows=2
                specs=specs=[[{}],[{}],[{'type':'table'}],[{'type':'table'}]]
                row_width=[3,3,3,10]
                subplot_titles=(session['symbol'], 'Volume',"TradingRecord","TradingSummary")
            else:
                rows=3
                specs=specs=[[{}],[{}],[{}],[{'type':'table'}],[{'type':'table'}]]
                row_width=[3,3,3,3,10]
                subplot_titles=(session['symbol'], 'Volume',thirdrowname,"TradingRecord","TradingSummary")
            fig2 = make_subplots(rows=rows+2, cols=1, shared_xaxes=False, vertical_spacing=0.1,specs=specs,subplot_titles=subplot_titles, row_width=row_width,figure=fig2)

            fig2.add_trace(go.Table(name="TradingRecord",
                header=dict(values=['IndexBar', 'Action', 'Date','Last Price','Last Qty','Invest Amount','Last Balance','Profit','Profit %','Close','New Balance'],
                            fill_color='rgb(210, 210, 210)',align='left',line_color='darkslategray'),
                cells=dict(values=[dft.indexbar, dft.state, dft.time, dft.oldprice,dft.oldqty, dft.investamt, dft.oldbalance, dft.profit,dft.profitpercent, dft.close, dft.newbalance],
                           height=30,line_color='darkslategray',
                fill_color='white',align='left')),row=rows+1, col=1)

            fig2.add_trace(go.Table(name="TradingSummary",header=dict(values=['Trading Count','Success Count','Success Rate','Total Invest','Total Profit','Profit %'],
                                                                      fill_color='rgb(210, 210, 210)',align='left',line_color='darkslategray'),
                cells=dict(values=[dfs.tradingcount, dfs.successcount, dfs.successrate, dfs.totalinvest,dfs.totalprofit, dfs['profit%']],height=30,line_color='darkslategray',
                fill_color='white',align='left')),row=rows+2, col=1)
            fig2.update_layout(
                height=850,margin={'t':120,'r':20,'l':20,'b':20},
                title={'text': headerMessage,
                       #'y':1.0,
                       'x':0.5,
                       'xanchor': 'center','yanchor': 'top'},
                # xaxis_title="X Axis Title",
                # yaxis_title="Y Axis Title",
                # legend_title="Legend Title",
                font=dict(
                    #family="Courier New, monospace",
                    size=15,
                    #color="RebeccaPurple"
                )
            )
            fig2 = make_subplots(rows=rows+2, cols=1, shared_xaxes=False, vertical_spacing=0.1,specs=specs,subplot_titles=subplot_titles, row_width=row_width,figure=fig2)
        else:
            fig2.update_layout(
                height=850,margin={'t':120,'r':20,'l':20,'b':20},
                title={'text': session['symbol']+" Chart",
                       #'y':1.0,
                       'x':0.5,
                       'xanchor': 'center','yanchor': 'top'},
                # xaxis_title="X Axis Title",
                # yaxis_title="Y Axis Title",
                # legend_title="Legend Title",
                font=dict(
                    #family="Courier New, monospace",
                    size=15,
                    #color="RebeccaPurple"
                )
            )
        session["fightml"]=go.Figure(fig2)

        fig1=session["fightml"]
        filename="./download/"+session['symbol']+date.today().strftime("%Y-%m-%d")+'.html'
        temp=fig1.write_html(filename,
                    full_html=True,
                    include_plotlyjs='cdn',
                    config={'scrollZoom': True,'responsive': True,'displaylogo':False})
        return dcc.send_file(
            #"./fig.html"
            #"./abc.html"
            #"./"+filename
            filename
        )

#THIS CALLBACK AND ABOVE GENERATE STARTEGY CONTENT TO MAKE THE STRATEGY MODAL BOX DYNAMICALLY AND PUT USER SELECTION IN THE INPUT_MODEALINPUT5
@callback(
    Output("input_modal5", "is_open"),
    Output("input_modelinput5","data"),
    Output("strategy_content","children"),

    Input("strategy", "value"),
    State("input_modal5", "is_open"),
    Input('input_add5', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_strategy_modal(strategy,is_open,n1):
    #WE CAN USE INPUT STRATEGY TO KNOW USER SELECTION OR USE CALLBACK_CONTEXT_TRIGGERED
    triggered_id = callback_context.triggered[0]['prop_id']
    if triggered_id == "strategy.value":
        if callback_context.inputs['strategy.value']=="SMACROSS":
            return [True,strategy,generate_content_strategy("SMACROSS")]
        elif callback_context.inputs['strategy.value']=="GOLDENDEATHCROSS":
            return [True,strategy,generate_content_strategy("GOLDENDEATHCROSS")]
        elif callback_context.inputs['strategy.value']=="MACDS":
            return [True,strategy,generate_content_strategy("MACDS")]
    elif triggered_id == "input_add5.n_clicks":
        return [False,strategy,dash.no_update]

#THIS FUNCTION USED TO DYNAMICALLY GENERATE THE MODAL BOX OF THE THREE STRATEGY FOR USER INPUT
#EVEN DYNAMICALLY GENERATE, THE ID OF OTHER MODAL BOX NEEDED TO BE ADDED AS IT WILL BE ERROR AS OTHER CALLBACK CANNOT FIND THIS ID
def generate_content_strategy(selection):

    if selection == "SMACROSS":
        strategy_content=html.Div([
                            html.Div(["SMA Crossing ",
                                        dbc.Input(id="inputnumber51", type="number", placeholder="Please enter time period"),
                                        #, style={'marginRight':'10px'}
                            ]),
                            html.Div(id="inputnumber61"),
                            html.Div(id="inputnumber62"),
                            html.Div(id="inputnumber71"),
                            html.Div(id="inputnumber72"),
                            html.Div(id="inputnumber73"),
                        ])
    elif selection == "GOLDENDEATHCROSS":
        strategy_content = html.Div([
                            html.Div(id="inputnumber51"),
                            html.Div([
                                "Golden Cross and Death Cross",
                                dbc.Input(id="inputnumber61", type="number", placeholder="Please enter SMA fast time period...50"),
                                dbc.Input(id="inputnumber62", type="number", placeholder="Please enter SMA slow time period...200"),
                            ]),
                            html.Div(id="inputnumber71"),
                            html.Div(id="inputnumber72"),
                            html.Div(id="inputnumber73"),
                            ]),

    elif selection == "MACDS":
        strategy_content = html.Div([
                            html.Div(id="inputnumber51"),
                            html.Div([
                                html.Div(id="inputnumber61"),
                                html.Div(id="inputnumber62"),
                            ]),
                            html.Div([
                                "MACD Stratgy",
                                dbc.Input(id="inputnumber71", type="number", placeholder="Please enter Fast K...12"),
                                dbc.Input(id="inputnumber72", type="number", placeholder="Please enter Slow K...26"),
                                dbc.Input(id="inputnumber73", type="number", placeholder="Please enter Slow D...9"),
                              ]),
                            ])
    return strategy_content
#OUR STRATEGY BASED ON CAPTIAL OF 10000 AND ONCE WE MEET CONDITION BUY OR SELL WE CHECK THE AMOUNT OF STOCK UNIT IN INTEGER THAT WE CAN BUY OR SELL EACH TIME AND THERE IS SOME LITTLE BALANCE CASH.
#ONCE CONDITION IS MEET IN BUYING (LAST MUST BE SELLING), WE BUY THOSE QTY OF STOCK TO SETTLE THE TRANSACTION FIRST AND THEN FOLLOW THE CORRECT DIRECTION TO SELL AGAIN USING ALL THE BALANCE
#WE PASS THE CONDITION FUNCTION AND THE DATAFRAME OF THE OHLC TOGETHER WITH THE INDICATOR INSIDE THIS DFE
def strategy(condition,dfe):
    #THIS IS LIST OF TOTAL BAR WHETHER BUY, SELL, NONE NO ACTION. THE NUBMER IS THE BAR INDEX
    listbuysell=[]
    #THIS IS LIST OF THE BUY SELL BAR INDEX AND USE FOR ADDING MARKING IN THE CHART TO SHOWN WHEN IS THE ACTION TAKEN
    listbs=[]
    #POS IS ZERO MEAN USER DID NOT BUY SELL YET AS CONDITION IS NOT MEET AT THE BEGINNGING AND NEEDED TO WAIT A NUMBER OF BAR FOR CONDITION MEET, POS IS 1 MEAN USER ALREADY IN TRANSACTION
    pos=0
    #NO OF BUY TRANSACTION
    buy_no=0
    #NO OF SELL TRANSACTION
    sell_no=0
    #STATE MEAN NOW IT IS BUY ACTION OR SELL ACTION
    state=""
    capital=10000
    #ORIGINAL BALANCE IS 10000
    balance=capital
    #STOCKQTY MEAN THE INTEGER NUMBER OF STOCK THAT USER CAN BUY ACCORDING TO THE BALANCE
    stockqty=0

    previous_price=0
    previous_qty=0
    # dfe=session["df"]
    # dfe['sme14']=talib.SMA(dfe['Close'], timeperiod=14)
    print("dfe7:",dfe.columns[7])
    dft = pd.DataFrame(columns = ['indexbar','state','time','oldprice','oldqty','investamt','oldbalance','profit','profitpercent','close','newbalance'])
    #BELOW IS THE LOOP FOR ALL THE INDEX BAR AND THERE ARE THREE PARTS , FIRST IS JUMP OUT ALL NAN VALUE,
    #SECOND PART IS WAITING THE CONDITION MEET TO START THE FIRST TRADE BY USING POS=0
    #THIRD PART IS AFTER THE THE FIRST TRADE ALREADY, AND IT IS ACTUAL TRADE PROCESS BASED ON THE CONDITION MET
    #WE PASS THE CORRESPOND STRATEGY FUNCTION AS THE CONDITION BELOW
    for i in range(len(dfe.index)):
        #print(i,listbuysell)
        #FIRST PART TO JUMP OUT OF THE NAN VALUE
        if condition(i,dfe) == "not start":
            listbuysell.append("none")
        #IT IS SECOND PART
        elif pos == 0:
            if condition(i,dfe)=="buy":
                listbs.append(i)
                state="buy"
                listbuysell.append(state)
                pos=1
                buy_no+=1
                stockqty=int(balance/float(dfe['Close'][i]))
                print("buy:i:{},previousprice:{:.2f},previousqty:{},investamt:{:.2f},previousbalance:{:.2f},previous_profit:{:.2f},previous_profitpercent:{:.2%},current_close:{:.2f},newbalance:{:.2f}".format(i,float(dfe['Close'][i]),stockqty,stockqty*float(dfe['Close'][i]),balance,0,0,float(dfe['Close'][i]),balance))

                #MAKE A ROW OF TRANSACTION AND CONCAT TO THE DFT TRANSACTION DATAFRAME
                dl = [{'indexbar':i,'state':state,'time':pd.to_datetime(str(dfe.index.values[i])).strftime("%d %b %Y"),'oldprice':round(float(dfe['Close'][i]),2), 'oldqty':stockqty,'investamt':round(stockqty*float(dfe['Close'][i]),2),'oldbalance':round(balance,2),'profit':0,'profitpercent':0.00,'close':round(float(dfe['Close'][i]),2), 'newbalance':round(balance,2)}]
                dfl = pd.DataFrame(dl)
                dft=pd.concat((dft, dfl),ignore_index=True)

                balance=balance-stockqty*float(dfe['Close'][i])
                previous_price=float(dfe['Close'][i])
                previous_qty=stockqty
                previous_balance=balance
            elif condition(i,dfe)=="sell":
                listbs.append(i)
                state="sell"
                listbuysell.append(state)
                pos=1
                sell_no+=1
                stockqty=int(balance/float(dfe['Close'][i]))
                print("sell:i:{},previousprice:{:.2f},previousqty:{},investamt:{:.2f},previousbalance:{:.2f},previous_profit:{:.2f},previous_profitpercent:{:.2%},current_close:{:.2f},newbalance:{:.2f}".format(i,float(dfe['Close'][i]),stockqty,stockqty*float(dfe['Close'][i]),balance,0,0,float(dfe['Close'][i]),balance))

                #MAKE A ROW OF TRANSACTION AND CONCAT TO THE DFT TRANSACTION DATAFRAME
                dl = [{'indexbar':i,'state':state,'time':pd.to_datetime(str(dfe.index.values[i])).strftime("%d %b %Y"),'oldprice':round(float(dfe['Close'][i]),2), 'oldqty':stockqty,'investamt':round(stockqty*float(dfe['Close'][i]),2),'oldbalance':round(balance,2),'profit':0,'profitpercent':0.00,'close':round(float(dfe['Close'][i]),2), 'newbalance':round(balance,2)}]
                dfl = pd.DataFrame(dl)
                dft=pd.concat((dft, dfl),ignore_index=True)

                balance=balance-stockqty*float(dfe['Close'][i])
                print("sell:i:{},balance:{}".format(i,balance))
                previous_price=float(dfe['Close'][i])
                previous_qty=stockqty
                previous_balance=balance
            else:
                listbuysell.append("none")
        #IT IS THE THIRD PART IN ACTUAL TRADING
        elif pos == 1:
            if condition(i,dfe)=="buy" and state == "sell":
                listbs.append(i)
                state="buy"
                listbuysell.append(state)
                buy_no+=1
                balance=previous_balance+previous_qty*previous_price+previous_qty*(previous_price-float(dfe['Close'][i]))
                previous_profit=previous_qty*(previous_price-float(dfe['Close'][i]))
                previous_profitpercent=(previous_price-float(dfe['Close'][i]))/previous_price

                # print("date:{},{}:i:{},previousprice:{:.2f},previousqty:{},investamt:{:.2f},previousbalance:{:.2f},previous_profit:{:.2f},previous_profitpercent:{:.2%},current_close:{:.2f},newbalance:{:.2f}".format(
                #     dfe.index.values[i].astype(datetime.datetime),state,i,previous_price,previous_qty,previous_price*previous_qty,previous_balance,previous_profit,previous_profitpercent,float(dfe['Close'][i]),balance))
                #MAKE A ROW OF TRANSACTION AND CONCAT TO THE DFT TRANSACTION DATAFRAME
                dl = [{'indexbar':i,'state':state,'time':pd.to_datetime(str(dfe.index.values[i])).strftime("%d %b %Y"), 'oldprice':round(previous_price,2),'oldqty':previous_qty,'investamt':round(previous_price*previous_qty,2),'oldbalance':round(previous_balance,2),'profit':round(previous_profit,2), 'profitpercent':round(previous_profitpercent,2), 'close':round(float(dfe['Close'][i]),2),'newbalance':round(balance,2)}]
                dfl = pd.DataFrame(dl)
                dft=pd.concat((dft, dfl),ignore_index=True)
                stockqty=int(balance/float(dfe['Close'][i]))
                #THIS PART WILL CHECK WEHTER THE BALANCE IS ENOUGH FOR NEXT TRADE, IF IT IS NOT ENOUGH TO BUY EVEN ONE STOCK, THE TRANSACTION STOP AND WILL NOT CONTINUE FOR THE REST OF BAR
                if stockqty > 1:
                    balance=balance-stockqty*float(dfe['Close'][i])
                else:
                    for j in range(i,len(dfe.index)-1):
                        listbuysell.append("none")
                    break
                previous_price=dfe['Close'][i]
                previous_qty=stockqty
                previous_balance=balance
            elif condition(i,dfe)=="sell" and state == "buy":
                listbs.append(i)
                state="sell"
                listbuysell.append(state)
                sell_no+=1
                balance=previous_balance+previous_qty*previous_price+previous_qty*(float(dfe['Close'][i])-previous_price)
                previous_profit=previous_qty*(float(dfe['Close'][i])-previous_price)
                previous_profitpercent=(float(dfe['Close'][i])-previous_price)/previous_price
                print(previous_profitpercent)
                # print("date:{},{}:i:{},previousprice:{:.2f},previousqty:{},investamt:{:.2f},previousbalance:{:.2f},previous_profit:{:.2f},previous_profitpercent:{:.2%},current_close:{:.2f},newbalance{:.2f}".format(dfe.index.values[i].astype(datetime.datetime),state,i,previous_price,previous_qty,previous_price*previous_qty,previous_balance,previous_profit,previous_profitpercent,float(dfe['Close'][i]),balance))
                print("test")
                #MAKE A ROW OF TRANSACTION AND CONCAT TO THE DFT TRANSACTION DATAFRAME
                dl = [{'indexbar':i,'state':state,'time':pd.to_datetime(str(dfe.index.values[i])).strftime("%d %b %Y") , 'oldprice':round(previous_price,2),'oldqty':previous_qty,'investamt':round(previous_price*previous_qty,2),'oldbalance':round(previous_balance,2),'profit':round(previous_profit,2), 'profitpercent':round(previous_profitpercent,2), 'close':round(float(dfe['Close'][i]),2),'newbalance':round(balance,2)}]
                dfl = pd.DataFrame(dl)
                dft=pd.concat((dft, dfl),ignore_index=True)
                #THIS PART WILL CHECK WEHTER THE BALANCE IS ENOUGH FOR NEXT TRADE, IF IT IS NOT ENOUGH TO BUY EVEN ONE STOCK, THE TRANSACTION STOP AND WILL NOT CONTINUE FOR THE REST OF BAR
                stockqty=int(balance/float(dfe['Close'][i]))
                if stockqty > 1:
                    balance=balance-stockqty*float(dfe['Close'][i])
                else:
                    for j in range(i,len(dfe.index)-1):
                        listbuysell.append("none")
                    break
                previous_price=dfe['Close'][i]
                previous_qty=stockqty
                previous_balance=balance
            else:
                listbuysell.append("none")

                # print("{}:,transactions:{},qty:{},close:{:.2f},sme:{:.2f},balance:{:.2f},onhold_pervious_price:{:.2f},hold_qty:{}".format(listbuysell[-1],i,stockqty,float(dfe['Close'][i]),float(dfe['sme14'][i]),balance,previous_price, previous_qty))

    if state == "buy":
        balance=balance+previous_qty*previous_price+previous_qty*(float(dfe['Close'][len(dfe.index)-1])-previous_price)
    elif state == "sell":
        balance=balance+previous_qty*previous_price+previous_qty*(previous_price-float(dfe['Close'][len(dfe.index)-1]))
#     print("{}:,transactions:{},qty:{},close:{:.2f},sme:{:.2f},balance:{:.2f},pervious_price:{:.2f},previous_qty:{}".format(state,len(dfe.index)-1,stockqty,float(dfe['Close'][len(dfe.index)-1]),float(dfe['sme14'][len(dfe.index)-1]),balance,previous_price,previous_qty))

    # print(dft)
    # print(dft['investamt'].sum())
    # print("profitpercent:{:.2%}".format(dft.query("profitpercent>0")['profitpercent'].count()))
    # print("tradingcount:{},totalinvest:{:.2f},totalprofit:{:.2f},profitpercent:{:.2%},tradeprofitcount:{},tradesucessrate:{:.2%}".format(len(dft),dft['investamt'].sum(),dft['profit'].sum(),dft['profit'].sum()/dft['investamt'].sum(),dft.query("profitpercent>0")['profitpercent'].count(),dft.query("profitpercent>0")['profitpercent'].count()/len(dft)))
    #strategytab=dbc.Table.from_dataframe(dft,responsive=True,size="sm",striped=True, bordered=True, hover=True,id="strategy_table")
    #strategytab=dash_table.DataTable(dft.to_dict('records'),id="strategy_table",page_size=10)
    print("tradingcount:{},totalinvest:{:.2f},totalprofit:{:.2f},profitpercent:{:.2%},tradeprofitcount:{},tradesucessrate:{:.2%}".format(len(dft),dft['investamt'].sum(),dft['profit'].sum(),dft['profit'].sum()/dft['investamt'].sum(),dft.query("profitpercent>0")['profitpercent'].count(),dft.query("profitpercent>0")['profitpercent'].count()/len(dft)))
    #AFTER ALL LOOP, THE TRANSACTION STORE IN DFT, AND THE SUMMARY OF STATISTIC IS STORED IN DFS
    dfs = pd.DataFrame(columns = ['tradingcount','successcount','successrate','totalinvest','totalprofit','profit%'])
    print(dfs)
    print(dft)
    dt= [{'tradingcount':len(dft),'successcount':dft.query("profitpercent>0")['profitpercent'].count(),'successrate':"{:.2%}".format(dft.query("profitpercent>0")['profitpercent'].count()/float(len(dft))),'totalinvest':capital,'totalprofit':round(dft['profit'].sum(),2),'profit%':"{:.2%}".format(dft['profit'].sum()/capital)}]
    df2 = pd.DataFrame(dt)
    dfs=pd.concat((dfs, df2),ignore_index=True)
    print(dfs)
    print("testend")
    return [listbuysell,listbs,buy_no,sell_no,balance,dft,dfs]

#BELOW THREE FUNCTION IS THE CORE FUNCTION FOR THE STARTEGY TO DETERMINE BUY SELL ACTION. WE CAN ADD OTHER FUNCTION BASED ON BELOW , IMPORTANT IS DETERMINE BUY SELL CONDITION
#JUST INPUT THE INDICATOR DATAFRAME AND i IS THE INDEX OF ROW BAR EACH DAY
def sma(i,dfe):
    # DONT TAKE ANY ACTION UNTIL THE INDICATOR IS NOT NAN
    if isnan(dfe[dfe.columns[7]][i]):
        return "not start"
    if dfe['Close'][i] >= dfe["SMACROSS"][i]:
        return "buy"
    else:
        return "sell"
def strategy_smacross(input_modelinput5,inputnumber51,input1_search,start_date,end_date):
        fig1=session["fig"]
        print("have session")
        #print(fig10.data)
        dfe=session["df"]
        dfe[input_modelinput5]=talib.SMA(dfe['Close'], timeperiod=inputnumber51)

        smalist=strategy(sma,dfe)
        dfe['buysell']=smalist[0]
        dft=smalist[5]
        dfs=smalist[6]
        #session["fig"]=fig1
        print("test sma")
        #print(smalist[5])
        #print(dfe.index.values)
        dfe['seq']=[i for i in range(0,len(dfe))]
        print (dfe['seq'])
#         fig1 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1,subplot_titles=("ab"+"--"+"name"+'--OHLC', 'Volume'),
#                          row_width=[2,10],figure=fig1
#                         )
        #fig1=go.Figure(fig1)
        print(fig1)
        name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()

        third_row_indicator=find_third_row()
        if third_row_indicator is not None:
            fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],third_row_indicator),
                                             row_width=[2,2,10],figure=fig1)
        else:
            fig1 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1]),
                                             row_width=[2,10],figure=fig1)

        fig1.add_trace(go.Scatter(mode="lines", x=dfe.index.values, y=dfe[input_modelinput5],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber51)),row=1, col=1)

        fig1.add_trace(go.Scatter(mode="markers+text", x=dfe.index.values, y=dfe['Low'],legendgroup=input_modelinput5, name=input_modelinput5+str(inputnumber51),
                                  #marker_symbol='triangle-up',
                                  marker_symbol=list(map(Setshape, dfe['buysell'])),
                                  marker_line_color="midnightblue",
                                  marker_color=list(map(SetColor,dfe["buysell"])),
                                  marker_line_width=1, marker_size=10,
                                  selectedpoints=smalist[1],
                                  text=list(map(Settext, dfe['seq'],dfe['buysell'])),
                                  textposition='bottom center',
                                  #selected=dict(marker=dict(color=list(map(SetColor,dfe["buysell"])))),
                                  #selected_marker_color=list(map(SetColor,dfe["buysell"])),
                                  #selected_marker_color="red",
                                  unselected_marker_size=0),row=1, col=1)
        print("test sma1")
        headerMessage="{} SMA Crossing: Using SMA with certain time period to determine Buy/Sell Strategy (Start:{}, End:{})".format(session["symbol"],start_date,end_date)
        #strategyMessage=html.H3(headerMessage,className="fs-2 fw-bold text-center text-primary")
        strategyTable,strategySummary=strategy_table(dft,dfs)
        session["fig"]=fig1
        #session["fightml"]=fig1

        #print(smalist[5])
        new_data = list(fig1.data).copy()
        del new_data[0:2]
        current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
        #print(type(fig1))
        #print(fig1)
        #print(smalist[5])
        #  return [fig1,current_indicator_list,smalist[5]]
        #session["fightml"]=fig2
        session["fig"]=fig1
        session['dft']=dft
        session['dfs']=dfs
        session['transactionheader']=headerMessage
        #session['symbol']=input1_search
        session['symbol']=fig1.layout.annotations[0].text.rsplit("--")[0]
        return [fig1,current_indicator_list,strategyTable, headerMessage, strategySummary]

def goldendeathcross(i,dfe):
    #BELOW IS TOO SIMPLE TO DETERMINE BUY SELL ACTION
    # if dfe['fast'][i] > dfe['slow'][i]:
    #     return True
    # elif dfe['fast'][i] < dfe['slow'][i]:
    #     return False
    print("i:{} ,i-1 fast:{:2f},i-1 slow:{:2f}, i fast:{:2f},i slow:{:2f}".format(i, dfe['fast'][i-1],dfe['slow'][i-1],dfe['fast'][i],dfe['slow'][i]))
    # DONT TAKE ANY ACTION UNTIL THE INDICATOR IS NOT NAN
    if isnan(dfe[dfe.columns[7]][i]):
        return "not start"
    # if isnan(dfe[dfe.columns[8]][i-1]):
    #     return "not start"
    #CROSSING METHOD IS TO DETERMINE THE LAST DAY AND TODAY INDICATOR
    if dfe['fast'][i] > dfe['slow'][i] and dfe['fast'][i-1] <= dfe['slow'][i-1]:
        return "buy"
    elif dfe['fast'][i] < dfe['slow'][i] and dfe['fast'][i-1] >= dfe['slow'][i-1]:
        return "sell"
def strategy_goldendeathcross(input_modelinput5,inputnumber61,inputnumber62,input1_search,start_date,end_date):
        fig1=session["fig"]
        print("have sessiongolden")
        #print(fig10.data)
        dfe=session["df"]
        dfe['slow']=talib.SMA(dfe['Close'], timeperiod=inputnumber62)

        dfe['fast']=talib.SMA(dfe['Close'], timeperiod=inputnumber61)
        smalist=strategy(goldendeathcross,dfe)
        dfe['buysell']=smalist[0]
        dft=smalist[5]
        dfs=smalist[6]
        dfe['seq']=[i for i in range(0,len(dfe))]
        name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()

        third_row_indicator=find_third_row()
        if third_row_indicator is not None:
            fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],third_row_indicator),
                                             row_width=[2,2,10],figure=fig1)
        else:
            fig1 = make_subplots(rows=2, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1]),
                                             row_width=[2,10],figure=fig1)

        fig1.add_trace(go.Scatter(mode="lines", x=dfe.index.values, y=dfe['fast'],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber61)+" "+str(inputnumber62)),row=1, col=1)
        fig1.add_trace(go.Scatter(mode="lines", x=dfe.index.values, y=dfe['slow'],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber61)+" "+str(inputnumber62)),row=1, col=1)

        fig1.add_trace(go.Scatter(mode="markers+text", x=dfe.index.values, y=dfe['Low'],legendgroup=input_modelinput5, name=input_modelinput5+str(inputnumber61)+" "+str(inputnumber62),
                                  #marker_symbol='triangle-up',
                                  marker_symbol=list(map(Setshape, dfe['buysell'])),
                                  marker_line_color="midnightblue",
                                  marker_color=list(map(SetColor,dfe["buysell"])),
                                  marker_line_width=1, marker_size=10,
                                  selectedpoints=smalist[1],
                                  text=list(map(Settext, dfe['seq'],dfe['buysell'])),
                                  textposition='bottom center',
                                  #selected=dict(marker=dict(color=list(map(SetColor,dfe["buysell"])))),
                                  #selected_marker_color=list(map(SetColor,dfe["buysell"])),
                                  #selected_marker_color="red",
                                  unselected_marker_size=0),row=1, col=1)
        print("test goldendeath")
        headerMessage="{} Golden Death Crossing: Using SMA with certain time period to determine Buy/Sell Strategy (Start:{}, End:{})".format(session["symbol"],start_date,end_date)
        #strategyMessage=html.H3(headerMessage,className="fs-2 fw-bold text-center text-primary")
        strategyTable,strategySummary=strategy_table(dft,dfs)
        session["fig"]=fig1
        #session["fightml"]=fig1

        #print(smalist[5])
        new_data = list(fig1.data).copy()
        del new_data[0:2]
        current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
        session["fig"]=fig1
        session['dft']=dft
        session['dfs']=dfs
        session['transactionheader']=headerMessage
        #session['symbol']=input1_search
        session['symbol']=fig1.layout.annotations[0].text.rsplit("--")[0]
        return [fig1,current_indicator_list,strategyTable, headerMessage, strategySummary]

def macds(i,dfe):
    # DONT TAKE ANY ACTION UNTIL THE INDICATOR IS NOT NAN
    #if isnan(dfe[dfe.columns[7]][i]) or isnan(dfe[dfe.columns[8]][i]) or isnan(dfe[dfe.columns[9]][i]):
    if isnan(dfe['macd'][i]) or isnan(dfe['macdsignal'][i]) or isnan(dfe['macdhist'][i]):
        return "not start"
    if dfe['macdhist'][i]>0 and dfe['macdhist'][i-1]<0:
        return "buy"
    elif dfe['macdhist'][i]<0 and dfe['macdhist'][i-1]>0:
        return "sell"

def strategy_macds(input_modelinput5,inputnumber71,inputnumber72,inputnumber73,input1_search,start_date,end_date):
        fig1=session["fig"]
        print("have sessionmacds")
        dfe=session["df"]
        macd, macdsignal, macdhist = talib.MACD(dfe['Close'], fastperiod=inputnumber71, slowperiod=inputnumber72, signalperiod=inputnumber73)
        dfe['macd']=macd
        dfe['macdsignal']=macdsignal
        dfe['macdhist']=macdhist
        #with pd.option_context('display.max_rows', None,):
        for i in range(len(dfe)):
            print (i," ",dfe['macdhist'][i])
        with pd.option_context('display.max_rows', None,):
            print(dfe)
        smalist=strategy(macds,dfe)
        dfe['buysell']=smalist[0]
        dft=smalist[5]
        dfs=smalist[6]
        dfe['seq']=[i for i in range(0,len(dfe))]
        name_list=list(dict.fromkeys([x['name'] for x in list(fig1.data)])).copy()
        third_row_indicator=find_third_row()
        if third_row_indicator is not None:
            print("remove")
            remove_figure(third_row_indicator)
        fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73)),
                                             row_width=[2,2,10],figure=fig1)
        fig1.add_trace(go.Scatter(mode="lines",fill=None, x=dfe.index.values, y=dfe['macd'],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73) ,marker= {"color": "blue"},),row=3, col=1)
        fig1.add_trace(go.Scatter(mode="lines",fill='tonexty', x=dfe.index.values, y=dfe['macdsignal'],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73),showlegend=False,marker= {"color": "orange"}),row=3, col=1)
        fig1.add_trace(go.Bar( x=dfe.index.values, y=dfe['macdhist'],legendgroup=input_modelinput5,name=input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73),showlegend=False,marker= {"color": "red"}),row=3, col=1)
        fig1.add_trace(go.Scatter(mode="markers+text", x=dfe.index.values, y=dfe['Low'],legendgroup=input_modelinput5, name=input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73),
                                  #marker_symbol='triangle-up',
                                  marker_symbol=list(map(Setshape, dfe['buysell'])),
                                  marker_line_color="midnightblue",
                                  marker_color=list(map(SetColor,dfe["buysell"])),
                                  marker_line_width=1, marker_size=10,
                                  selectedpoints=smalist[1],
                                  text=list(map(Settext, dfe['seq'],dfe['buysell'])),
                                  textposition='bottom center',
                                  #selected=dict(marker=dict(color=list(map(SetColor,dfe["buysell"])))),
                                  #selected_marker_color=list(map(SetColor,dfe["buysell"])),
                                  #selected_marker_color="red",
                                  unselected_marker_size=0),row=1, col=1)
        fig1 = make_subplots(rows=3, cols=1, shared_xaxes=False, vertical_spacing=0.1,
                             subplot_titles=(session["symbol"]+"--"+name_list[0]+'--OHLC',name_list[1],input_modelinput5+str(inputnumber71)+" "+str(inputnumber72)+" "+str(inputnumber73)),
                                             row_width=[2,2,10],figure=fig1)

        headerMessage="{} MACD Strategy: Using MACD to determine Buy/Sell Strategy (Start:{}, End:{})".format(session["symbol"],start_date,end_date)
        #strategyMessage=html.H3(headerMessage,className="fs-2 fw-bold text-center text-primary")
        strategyTable,strategySummary=strategy_table(dft,dfs)
        session["fig"]=fig1
        #session["fightml"]=fig1

        #print(smalist[5])
        new_data = list(fig1.data).copy()
        del new_data[0:2]
        current_indicator_list=list(dict.fromkeys([x['name'] for x in new_data])).copy()
        session["fig"]=fig1
        session['dft']=dft
        session['dfs']=dfs
        session['transactionheader']=headerMessage
        #session['symbol']=input1_search
        session['symbol']=fig1.layout.annotations[0].text.rsplit("--")[0]
        return [fig1,current_indicator_list,strategyTable, headerMessage, strategySummary]





#BASE ON THE DFT TRANSACTION RECORD AND DFS TRANSACTION SUMMARY TO CREATE THE TABLE
def strategy_table(dft,dfs):
    strategyTable=dash_table.DataTable(dft.to_dict('records'),#id="strategyTable",
            page_size=10,
            style_data_conditional=[{
                             'if': {'row_index': 'odd'},
                             'backgroundColor': 'rgb(220, 220, 220)'
                            # "if": {"state": "selected"},              # 'active' | 'selected'
                            # "backgroundColor": "rgb(220, 220, 220)",
                            #"border": "1px solid blue",
            }],
                style_header={
                    'backgroundColor': 'rgb(210, 210, 210)',
                    'color': 'black',
                    'fontWeight': 'bold',
                    'textAlign': 'center'
                },
                style_table={'overflowX': 'scroll'},
                style_data={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                style_cell_conditional=[
                {'if': {'column_id': 'id'},
                 'width': '0%'}],
            )
    strategySummary=dash_table.DataTable(dfs.to_dict('records'),#id="strategySummary",page_size=10,
            style_data_conditional=[{
             'if': {'row_index': 'odd'},
             'backgroundColor': 'rgb(220, 220, 220)'
            # "if": {"state": "selected"},              # 'active' | 'selected'
            # "backgroundColor": "rgb(220, 220, 220)",
            #"border": "1px solid blue",
            }],
    style_header={
        'backgroundColor': 'rgb(210, 210, 210)',
        'color': 'black',
        'fontWeight': 'bold',
        'textAlign': 'center'
    },
    style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
    },
    style_table={'overflowX': 'scroll'},
    style_cell_conditional=[
    {'if': {'column_id': 'id'},
     'width': '0%'}],
    )
    return [strategyTable,strategySummary]



#BELOW FOUR FUNCTION TO CHANGE ATTRIBUTE OR COLOR OF THE LINE OR BAR DEPEND ON VALUE OF THE DATA
def SetColorV(open,close):
    if(close>=open):
        return "green"
    else:
        return "red"
def Setshape(x):
    if x == "sell":
        return "triangle-down"
    elif x == "buy":
        return "triangle-up"
    else:
        return "triangle-up"
def SetColor(buysell):
    if (buysell=="buy"):
        return "green"
    elif (buysell=="sell"):
        return "red"
    else:
        return "red"
def Settext(x,buysell):
    if buysell == "sell" or buysell == "buy":
        return x
    else:
        return ""