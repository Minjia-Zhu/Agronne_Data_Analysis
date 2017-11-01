import requests
import re
import pandas as pd
import numpy as np
import requests
import re
import nltk
from pattern.en import pluralize, singularize


KEY = '13A3E641-0C10-317C-9C08-7EF10ACA1519'
DOMAIN = 'http://quickstats.nass.usda.gov/api'
cats = ['sector_desc','group_desc','statisticcat_desc','state_alpha']
#Methods
GET = '/api_GET/?key='+ KEY
VALUES = '/get_param_values/?key='+ KEY
COUNTS = '/get_counts/?key='+ KEY

#Get all values of parameters
#Parameter table is avaliable at: https://quickstats.nass.usda.gov/api#param_define
#['source_desc','group_desc','commodity_desc',]
# for cat in cats:
	# pprint(requests.get(DOMAIN+VALUES, params={'param':cat}).content)

# sector = ["ANIMALS & PRODUCTS","CROPS","DEMOGRAPHICS","ECONOMICS","ENV''IRONMENTAL"]
# group = ["FIELD CROPS","FRUIT & TREE NUTS","HORTIC","VEGETABLES"]
# statisticcat = ["AREA HARVESTED","AREA IN PRODUCTION","SALES"]


#Get census production value data
# census_year = [2011,2012,2014,2015]
# for i in census_year:
#     f = open('census_sales_data_'+str(i)+'.csv','wb')
#     p_get = {'source_desc':'CENSUS',
#          'sector_desc': 'CROPS',
#          'group_desc': ["FIELD CROPS","FRUIT & TREE NUTS","HORTIC","VEGETABLES"],
#          'statisticcat_desc' :"SALES",
#          'unit_desc': '$',
#          'util_practice_desc':'ALL UTILIZATION PRACTICES',
#          'year':i,
#          'state_alpha':["AK","AL","AR","AZ","CA","CO","CT","DE","FL","GA","HI","IA",
# 						"ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC",
# 						"ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","OT","PA","RI","SC","SD",
# 						"TN","TX","UT","VA","VT","WA","WI","WV","WY"],
#          'format':'CSV'}
#     data = requests.get(DOMAIN+GET, params=p_get).content
#     f.write(data) 
#     f.close()
#     print('Successfully export year '+str(i)+'census_sales_data....')

#Get survey production value data
filename = 'survey_sales_data_2006-2016_all.csv'
f = open(filename,'wb')
p_get = {'source_desc':'SURVEY',
     'sector_desc': 'CROPS',
     'group_desc': ["FIELD CROPS","FRUIT & TREE NUTS","VEGETABLES"],
     'commodity_desc':['ALMONDS', 'APPLES', 'APRICOTS', 'AVOCADOS',
       'BLUEBERRIES', 'BRAMBLEBERRIES', 'BOYSENBERRIES', 'CHERRIES',
       'GRAPEFRUIT', 'LEMONS', 'LIMES', 'ORANGES', 'TANGELOS',
       'TANGERINES', 'TEMPLES', 'CRANBERRIES', 'GRAPES', 'KIWIFRUIT',
       'MACADEMIAS', 'LOGANBERRIES', 'NECTARINES', 'OLIVES', 'PEACHES',
       'PEARS', 'PLUMS & PRUNES', 'STRAWBERRIES', 'RASPBERRIES','ASPARAGUSES', 
       'BROCCOLI', 'CARROTS','CAULIFLOWER', 'CELERY', 'CUCUMBERS', 
       'CANTALOUPES','ONIONS', 'PUMPKINS', 'SQUASH','HAYS','PEANUTS', 'RAPESEED', 
       'SOYBEANS', 'SUGARBEETS', 'SUNFLOWER','COTTON','LEGUMES'],
     'unit_desc':'$',
     'util_practice_desc': ["UTILIZED","ALL UTILIZATION PRACTICES","UTILIZED, SHELLED"],
     'class_desc':["ALL CLASSES","TAME","WILD","ALFALFA","SWEET","TART",
                   "DRY EDIBLE","DRY","DRY, SPRING","DRY, SUMMER, NON-STORAGE",
                   "DRY, SUMMER, NON-STORAGE","DRY, SUMMER, STORAGE",
                  "COTTONSEED","PIMA","UPLAND"],
     'year':[2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016],
     'format':'CSV'}
data = requests.get(DOMAIN+GET, params=p_get).content
f.write(data) 
f.close()
print('Successfully export '+filename+'....')

#Remove non-numerical values in column "Value" in file "survey_sales_data_2006-2016_all.csv" before proceeding to next execution
df = pd.read_csv('survey_sales_data_2006-2016_all.csv')
value = df[['commodity_desc','state_alpha', 'state_name','year','Value']]
value["Value"] = value["Value"].apply(lambda x: float(str(x).replace(',','')))
value = value.rename(columns = {'commodity_desc':'crop'})
value = value.groupby(["year","state_alpha","crop"],as_index=False).sum().sort_values(['Value'])
#divide the value of onion by two due to overlapping calcuation
value.loc[value.crop=='ONIONS', 'Value'] = value.loc[value.crop=='ONIONS', 'Value']/2
#remove total US 
value = value.drop(value[value.state_alpha == "US"].index)
value['crop'] = value['crop'].apply(lambda x: singularize(x).lower())

#Read dependence ratop data
ratio = pd.read_excel('Dep Ratio.xlsx',sheetname = 1)
ratio = ratio[['crop', 'D=\nDependence On Insect Pollination',
       'P= Proportion Of Pollinators That Are\nHoney Beesf', 'Unnamed: 5',
       'Proportion of pollinators that are native bees (1 – P)',
       'Unnamed: 10']]
ratio = ratio.rename(columns={'D=\nDependence On Insect Pollination':'D',
              'P= Proportion Of Pollinators That Are\nHoney Beesf':'PH',
              'Proportion of pollinators that are native bees (1 – P)':'PN',
              'Unnamed: 5':'DH',
              'Unnamed: 10':'DN'})



