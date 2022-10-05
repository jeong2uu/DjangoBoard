# -*- coding: utf-8 -*-
from elasticsearch import Elasticsearch
import json
import time
import math

class UserInfoTable:
    # 접속 정보
    __hosts = 'localhost'
    __port = 9200
    __index_name = 'usertable'
    __index_type = 'user'
    # es = Elasticsearch(hosts='localhost', port=9200)

    def __init__(self):
        self.es = Elasticsearch(hosts = self.__hosts, port = self.__port)

    #create indices
    def create_index(self,body):
        if not self.es.indices.exists(index=self.__index_name):
            res = self.es.indices.create(index=self.__index_name, body=body)
        return res

    # Method to store data in elasticsearch
    def insert_data(self, data):
        res = self.es.index(index=self.__index_name, doc_type=self.__index_type, body=data )
        return res

    # get_source same func search_data
    def search_data(self, data=None):
        if data is None:
            data = {
            "query" : {"match_all":{}}
            }
        else:
            data = data 

        body= data 
        res = self.es.search(index=self.__index_name, body=body)
        a = res['hits']
        b = a['hits']

        return b

    def search(self, id):
        res = self.es.get(index=self.__index_name, doc_type=self.__index_type, id=id)

        return res

    # delete index
    def delete_index(self):
        if self.es.indices.exists(index=self.__index_name):
            return self.es.indices.delete(index=self.__index_name)

    #delete just one row of index what user want
    def delete_data(self, id):
        res = self.es.delete(index=self.__index_name, doc_type=self.__index_type, id=id)
        
        return res

    # update_data
    def update(self,id, doc):
        body={
            'doc' : doc
        }

        res = self.es.update(index=self.__index_name, doc_type=self.__index_type ,id=id, body=body)

        return res