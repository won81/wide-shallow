import os

class PublicApi:
    def __init__(self):
        self.url = 'http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTrade?'
        self.service_key = os.getenv('SERVICE_KEY')
        self.payload = ''

    def get_service_key(self):
        return self.service_key

    def set_service_key(self, key):
        self.service_key = key

    def is_existed_service_key(self):
        if self.service_key:
            return True
        return False

    def make_request(self, location_code, contract_date):
        self.payload = 'LAWD_CD=' + location_code + '&' + \
                'DEAL_YMD=' + contract_date + '&' + \
                'serviceKey=' + self.service_key
        return self.url + self.payload

    def make_request(self, location_code, contract_date, service_key):
        self.payload = 'LAWD_CD=' + location_code + '&' + \
                'DEAL_YMD=' + contract_date + '&' + \
                'serviceKey=' + service_key
        return self.url + self.payload
