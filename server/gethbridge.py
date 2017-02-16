import urllib2
import json as jjss

geth_addr = 'http://localhost:8545'
from_addr = '0x2fcdbd9ee6c3a72fbeccf11170970209a89045ba'
to_addr = '0xf2cf7e48f33981f38c0f4af971b8bdd6f7a9582a'
gas = '0xffffff'

def get32hex(i):
    return '%064x' % i

def requestWithJSON(json):
    print json
    encoded_json = jjss.dumps(json)
    print encoded_json
    req = urllib2.Request(url=geth_addr, data=encoded_json)
    response_data = urllib2.urlopen(req)
    response = response_data.read()
    return jjss.loads(response)

def addScore(account, score):
    data = '0xddcbf794' + get32hex(int(account)) + get32hex(int(score))
    json = {
        "jsonrpc" : "2.0",
        "method" : "eth_sendTransaction",
        "params" : [
            {
                "from" : from_addr,
                "to" : to_addr,
                "gas" : gas,
                "data" : data,
            }
        ],
        "id" : 1
    }
    return requestWithJSON(json)

def getBalance(account):
    data = '0x1e010439' + get32hex(int(account))
    json = {
        "jsonrpc" : "2.0",
        "method" : "eth_call",
        "params" : [
            {
                "from" : from_addr,
                "to" : to_addr,
                "data" : data,
            },
            "latest"
        ],
        "id" : 1
    }
    return requestWithJSON(json)

def useScore(account, cost):
    data = '0x56e2fa01' + get32hex(int(account)) + get32hex(int(cost))
    json = {
        "jsonrpc" : "2.0",
        "method" : "eth_sendTransaction",
        "params" : [
            {
                "from" : from_addr,
                "to" : to_addr,
                "gas" : gas,
                "data" : data,
            }
        ],
        "id" : 1
    }
    return requestWithJSON(json)

