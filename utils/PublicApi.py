import os

class PublicApi:
    def __init__(self):
        self.url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'
        self.service_key = os.getenv('SERVICE_KEY')
        self.payload = ''

    def make_request(self, location_code, contract_date):
        self.payload = 'LAWD_CD=' + location_code + '&' + \
                'DEAL_YMD=' + contract_date + '&' + \
                'serviceKey=' + self.service_key
        return self.url + self.payload
