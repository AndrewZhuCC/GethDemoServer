import urllib2
import json as jjss

geth_addr = 'http://localhost:8545'
from_addr = '0x6e20cdcaa581373bf592d676d9c305183bb64b8a'
to_addr = '0x97c10115dfff1866f3cfbd6b8d4b237c7a53286a'
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
    return response

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

