import requests


class SMS:
    def __init__(self, number):
        self.query = {"authorization": "Sj8KZSZJBefOcjVjnSrv5KAEORR4bkaEhahUCfCehAs2WN7gXhfSwCsJDelB",
                      "variables_values": "", "route": "dlt", "sender_id": "DETTPL", "message": "138002"}
        self.number = number
        self.url = "https://www.fast2sms.com/dev/bulkV2"
        self.headers = {'cache-control': "no-cache"}

    def send_otp(self, otp):
        message = "138002"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['variables_values'] = otp
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)

    def gift_packed(self,id):
        message = "138003"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['sender_id'] = "DETTGT"
        self.query['flash'] = "0"
        self.query['variables_values'] = "INVV"
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)

    def gift_shipped(self,id):
        message = "138004"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['sender_id'] = "DETTGT"
        self.query['flash'] = "0"
        self.query['variables_values'] = id
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)

    def gift_out_for_delivery(self,id):
        message = "138005"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['sender_id'] = "DETTGT"
        self.query['flash'] = "0"
        self.query['variables_values'] = id
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)

    def gift_delivered(self,id):
        message = "138006"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['sender_id'] = "DETTGT"
        self.query['flash'] = "0"
        self.query['variables_values'] = id
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)

    def gift_order_cancelled(self):
        message = "138007"
        self.query['message'] = message
        self.query['numbers'] = self.number
        self.query['sender_id'] = "DETTGT"
        self.query['flash'] = "0"
        print(self.query)

        response = requests.request("GET", self.url, headers=self.headers, params=self.query)
        print(response.text)
