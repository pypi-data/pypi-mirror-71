import requests
import json
import pytest
import assertions

HOST_URL = "54.236.47.36:31236"


def _trigger_requests(req_method, url, header, data, proxies=None):
    print("\n\nRegenerating traffic from CloudVector events....")
    return requests.request(method=req_method, url=url, proxies=proxies, headers=header, data=data, verify=False)


def test_app_demo_oauth_token(password, client_id, grant_type, email, client_secret, dummy):
    data = {}
    data["password"] = password
    data["client_id"] = client_id
    data["grant_type"] = grant_type
    data["email"] = email
    data["client_secret"] = client_secret
    data["dummy"] = dummy
    
    req = {
             "data": data,
             "headers": {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Authorization': 'Bearer', 'Cache-Control': 'private, no-store', 'Connection': 'keep-alive', 'Content-Length': '267', 'Content-Type': 'application/json; charset=utf-8', 'Date': 'Tue, 16 Jun 2020 21:16:14 GMT', 'Etag': 'W/"0322e4092449f3cca28943c93fdbb1b8"', 'Pragma': 'no-cache', 'Server': 'nginx/1.17.10', 'User-Agent': 'python/gevent-http-client-1.4.2', 'Vary': 'Origin', 'X-Request-Id': '9d27cb38-ae4e-4248-8fdc-066061cc4bd8', 'X-Runtime': '0.173629', 'Set-Cookie-params': None}
          }
    resp = _trigger_requests("POST", "http://54.236.47.36:31236/app-demo/oauth/token",
                      header=req["headers"],
                      data=json.dumps(data))
    print(resp.status_code)
    print(resp.text)
    assertions.assert_for_app_demo_oauth_token(req,resp)





