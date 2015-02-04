import requests
import pandas as pd
import numpy as np

mytoken = "d2a5fa6361536255294468c21a3fbb3d5bad59cc" # this is my API key
def state_data(token, variables, year = 2010, state = "*", survey = "sf1"):
  state = [str(i) for i in state]# make sure the input for state (integers) are strings
  variables = ",".join(variables) # squish all the variables into one string
  year = str(year)
  combine = ["http://api.census.gov/data/", year, "/", survey, "?key=", mytoken,
             "&get=", variables, "&for=state:"] # make a list of all the components to construct a URL
  incomplete_url = "".join(combine) # the URL without the state tackd on to the end
  complete_url = map(lambda i: incomplete_url + i, state) # now the state is tacked on to the end; one URL per state or for "*"
  r = []
  r = map(lambda i: requests.get(i), complete_url) # make an API call to each complete_url
  data = map(lambda i: i.json(), r)
  df = pd.DataFrame(dict(zip(*v)) for v in data)
#  print df
  print complete_url

state_data(token = mytoken, state = "*", variables = ["P0010001", "P0010001"])
#state_data(token = mytoken, state = [47, 48, 49, 50], variables = ["P0010001", "P0010001"])
