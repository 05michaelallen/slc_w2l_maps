#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 09:04:21 2020

@author: mallen
"""

# import packages 
import requests as r
import getpass, pprint, time, os, cgi, json
import geopandas as gpd

# aet input directory, change working directory
wd = "/home/vegveg/slc_w2l_maps/"
os.chdir(wd)
api = 'https://lpdaacsvc.cr.usgs.gov/appeears/api/'

### parameters
# start and end date
startDate = '01-01-2005'
endDate = '01-01-2020'

# name the task
task_name = 'slc_lst_day'

# input username and password
user = getpass.getpass(prompt = 'Enter NASA Earthdata Login Username: ')
password = getpass.getpass(prompt = 'Enter NASA Earthdata Login Password: ')

# insert api url, call login service, provide credentials & return json
token_response = r.post('{}login'.format(api), auth = (user, password)).json()
del user, password
token_response

# list all products
product_response = r.get('{}product'.format(api)).json()
# Create a dictionary indexed by product name & version
products = {p['ProductAndVersion']: p for p in product_response}
# print metadata for product
products['MYD21A2.006']

# create a list of the requested products
prods = ['MYD21A1D.006', 'MYD21A1N.006', 'MYD21A2.006'] # note: can request layers from more than one product

# list layers from products
r.get('{}product/{}'.format(api, prods[2])).json()

# create list of layers
layers = [(prods[0],'LST_1KM'),
          (prods[0],'QC'),
          #(prods[0],'View_Angle'),
          #(prods[1],'LST_1KM'),
          #(prods[1],'QC'),
          #(prods[1],'View_Angle'),
          #(prods[2],'LST_Day_1KM'),
          #(prods[2],'LST_Night_1KM'),
          #(prods[0],'View_Time')
          ]

# convert tupled list of layers to list of dict
prodLayer = []
for l in layers:
    prodLayer.append({
            "layer": l[1],
            "product": l[0]
          })
    
# save token
token = token_response['token']
head = {'Authorization': 'Bearer {}'.format(token)}

# import the request shapefile
nps = gpd.read_file('./data/shp/slc_request_bbox.shp').to_json()
# convert to json
nps = json.loads(nps)

# select task type, projection, and output
task_type = 'area'
proj = 'geographic'
outFormat = 'netcdf4'
recurring = False

# compile into an area request
task = {
    'task_type': task_type,
    'task_name': task_name,
    'params': {
         'dates': [
         {
             'startDate': startDate,
             'endDate': endDate
         }],
         'layers': prodLayer,
         'output': {
                 'format': {
                         'type': outFormat}, 
                         'projection': proj},
         'geo': nps,
    }
}

# submit
task_response = r.post('{}task'.format(api), json=task, headers=head).json()
task_response
