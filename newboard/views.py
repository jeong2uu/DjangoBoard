# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render

from django.views.decorators.csrf import csrf_exempt
from elasticsearch import Elasticsearch
import boardelastic as es
import json
import time

# db객체 생성
myboard = es.BoardTable()

#테스트 창
def test(request):
    return render(request, 'newboard/testBoard.html')

#게시판 메인화면
@csrf_exempt  
def boardMain(request):
    #모든데이터 조회
    content = {
        "query" : { 
            "match_all":{}
        },
        "size" : 100
    }
    tabledata = myboard.search_data(content)
    # print(len(tabledata))

    rowdatas = []

    if len(tabledata) == 0 :
        context = {'bool' : True }
        rowdatas = None
    else:
        for i in range(len(tabledata)):     
            rowdata = {}    #초기화
            rowdata['bid'] = tabledata[i]['_id']
            rowdata['title'] = tabledata[i]['_source']['title']
            rowdata['writer'] = tabledata[i]['_source']['writer']
            rowdata['datetime'] = tabledata[i]['_source']['datetime']
            rowdata['note'] = tabledata[i]['_source']['note']
            # print(rowdata)
            rowdatas.append(rowdata)
            
        #context = { 'content' : rowdatas }
        context = { 'content' : rowdatas, 'test' : json.dumps(rowdatas) }
    
    # print(context)
    # return HttpResponse(context)
    return render(request, 'newboard/newboardMain.html', context)

# 글 등록 모달창
def boardWrite(request):
    return render(request, 'newboard/newboardWrite.html')

# 글 등록 기능 동작    
@csrf_exempt    #보안을 포기
def insertData(request):
    data = json.loads(request.body)

    myboard.insert_data(data)
    time.sleep(1.2)        
    
    return HttpResponse("insert success!")

@csrf_exempt
def boardDetail(request):
    resultdata = []
    if request.method == 'POST':
        data = json.loads(request.body)
        print("============boardDetail============")
        print(data)
        title = data['title']
        content = {
            "query" : {
                "bool": {
                    "must" : [
                        {"match" : {"title" : title }}
                        ]
                    }
                }
            }
        srdata = myboard.search_data(content)
        print(srdata)
        rqdata = srdata[0]['_source']
        rqdataId = srdata[0]['_id']
        print(rqdata)
        print(rqdataId)

        if rqdataId == data['bid']:
            resultdata.append(rqdata)
    
    result = { 'content' : resultdata, 'bid' : rqdataId }
    print(result)
    
    return render(request, 'newboard/newboardDetail.html',result)

@csrf_exempt
def boardUpdate(request):
    resultdata = []
    if request.method == "POST":
        data = json.loads(request.body)
        print("============boardUpdate============")
        print(data)
        bid = data['bid']
        print(bid)
        srdata = myboard.search(bid)
        print(srdata)
        rqdata = srdata['_source']
        print(rqdata)
        resultdata.append(rqdata)
    
    result = { 'content' : resultdata ,'bid' : bid }

    return render(request, 'newboard/newboardUpdate.html', result)

@csrf_exempt
def updateData(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("============updateData============")
        print(data)
        rdata = data['paramList']
        bid = rdata[0]['bid']
        updata = rdata[1]
        print("num : {}, updata : {}".format(bid, updata))

        myboard.update(bid, updata)

    return render(request, 'newboard/newboardUpdate.html')

@csrf_exempt
def deleteData(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("============deleteData============")
        print(data)
        delnum = data['checkNum']
        print(delnum)
        if delnum < 2 : 
            deldata = data['checkList'][0]
            myboard.delete_data(deldata)
        else :
            deldata = data['checkList']
            print(deldata)

            for i in deldata:
                myboard.delete_data(i)
            
    return HttpResponse("delete success!")