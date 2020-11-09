# submits API request to collect data on all streamflow gauges in Division 5
import requests

parameters = {"apiKey": 'szZKDBs3HWjF4+NOiEopD0e3MDFLP7vH', "format": 'csv', "dateFormat": "dateOnly", "division": '5'}

response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/surfacewater/surfacewaterstations/",
                        params=parameters)

url_content = response.content
csv_file = open('div5_gauges.csv', 'wb')
csv_file.write(url_content)
csv_file.close()