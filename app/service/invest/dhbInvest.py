# coding:utf-8
# Author：lxm

from app.service.product.product import *

modelName = "invest"
config = tools.get_config(os.path.join(configPath, "config.ini"))


# 创建投资账单
def createInvestOrder(token, agreeNextBid, pId, iUnlockConfig, fromType, money, couponId=""):
    payload = tools.get_json(os.path.join(dataPath, modelName, "createInvestOrder.json"))
    payload["fun"]["createInvestOrder"]["agreeNextBId"] = agreeNextBid
    payload["fun"]["createInvestOrder"]["bId"] = oneProductDetail(token, pId)["bId"]
    payload["fun"]["createInvestOrder"]["pId"] = pId
    payload["fun"]["createInvestOrder"]["iUnlockConfig"] = iUnlockConfig
    payload["fun"]["createInvestOrder"]["type"] = oneProductDetail(token, pId)["bType"]
    payload["fun"]["createInvestOrder"]["fromType"] = fromType
    payload["fun"]["createInvestOrder"]["money"] = money
    payload["fun"]["createInvestOrder"]["couponId"] = couponId
    payload["statics"]["token"] = token
    url = config["api"]["xwapi"]
    res = requester.post_template(url=url, payload=json.dumps(payload))
    if json.loads(res)["createInvestOrder"]["error_code"] != 0:
        tools.log().error("创建投资订单失败！")
        return None
    return json.loads(res)["createInvestOrder"]["data"]


# 确认投资账单
def sureInvestOrder(token, orderId, pId, fromType):
    payload = tools.get_json(os.path.join(dataPath, modelName, "sureInvestOrder.json"))
    payload["fun"]["sureInvestOrder"]["orderId"] = orderId
    payload["fun"]["sureInvestOrder"]["pId"] = pId
    payload["fun"]["sureInvestOrder"]["fromType"] = fromType
    payload["statics"]["token"] = token
    url = config["api"]["xwapi"]
    res = requester.post_template(url=url, payload=json.dumps(payload))
    print res


if __name__ == '__main__':
    orderInfo = createInvestOrder("a70c18342f8be2d3280c797639b1c7b8", 1, 24, 1, 0, 500)
    sureInvestOrder("a70c18342f8be2d3280c797639b1c7b8", orderInfo["orderId"], orderInfo["pId"], orderInfo["fromType"])
