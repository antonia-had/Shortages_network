#retrieving hydrological data for one streamflow gauge

import requests

parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv',
              "abbrev": 'COLUTACO', "max-measDate": '10/11/2020',
              "min-measDate": '01/01/1951', 'fields': ['stationNum', 'abbrev', 'measType', 'measDate', 'value', 'measUnit']}

response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/surfacewater/surfacewatertsday/",
                        params=parameters)

url_content = response.content
csv_file = open('test2.csv', 'wb')
csv_file.write(url_content)
csv_file.close()
