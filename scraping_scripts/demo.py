import requests

parameters = {"apiKey": 'dBTnllEokTHF4+NOiEopD0e3MDFLP7vH', "format": 'csv',
              "adminNo": '54421.52265', "endDate": '09/30/2019_23:45',
              "startDate": '10/01/1909_00:00', "wdid":'7201654'}

response = requests.get("https://dwr.state.co.us/Rest/GET/api/v2/analysisservices/callanalysisbywdid/",
                        params=parameters)

url_content = response.content
csv_file = open('downloaded.csv', 'wb')
csv_file.write(url_content)
csv_file.close()