# -- coding:utf-8 --
import json
import time
import requests
from requests.exceptions import Timeout
from typing import List
from eth_account import Account
from eth_utils import is_checksum_address, to_checksum_address, to_hex
from .LMRequest import *
from lm_sdk.common.LMServiceError import ServiceErrorCode, ServiceErrorMsg
from lm_sdk.common.LMTypeDTO import TypeDTO
from lm_sdk.common.LMRsa import RSAUtil


class LMChainService(object):
    def __init__(self):
        """ Constructs and sends a :class:`LMChainService <LMChainService>`.

        antRestUrl: `蚂蚁`Baas平台链接.
        """
        self.antRestUrl = "https://rest.baas.alipay.com"

    def chainDeploy(self, chainDeployRequest: LMChainDeployRequest):
        """ 合约部署

        :param chainDeployRequest: LMChainDeployRequest实例.
        :return: 状态码.
        """
        if not isinstance(chainDeployRequest, LMChainDeployRequest):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数类型错误!"})
        result = self.checkParams(chainDeployRequest)
        if result is not None:
            return result
        if not chainDeployRequest.contractData:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "合约内容为空!"})

        inputParamResult = self.checkInputParams(chainDeployRequest.inputParams)
        if not isinstance(inputParamResult, list):
            return inputParamResult
        chainDeployRequest.inputParams = inputParamResult

        contractDataResult = self.getFullContractData(chainDeployRequest)
        if not isinstance(contractDataResult, dict):
            return contractDataResult
        chainDeployRequest.contractData = contractDataResult["contractData"]

        paramObj = dict()
        chainType = chainDeployRequest.chainType
        paramObj["link"] = chainType
        paramObj["contractData"] = chainDeployRequest.contractData

        if chainType == chainDeployRequest.curSupPlatform["ETH"]:  # 以太坊
            hexValueResult = self.transferERC20Token(chainDeployRequest)
            if not isinstance(hexValueResult, dict):
                return hexValueResult

            paramObj["address"] = chainDeployRequest.ethAddress
            paramObj["hexValue"] = hexValueResult["hexValue"]
            paramObj["inputParam"] = chainDeployRequest.inputParams
        elif chainType == chainDeployRequest.curSupPlatform["ANT"]:  # 蚂蚁
            if chainDeployRequest.antAddress:
                tokenResult = self.getTokenForAnt(chainDeployRequest.accessId, chainDeployRequest.privateKey)
                if not isinstance(tokenResult, dict):
                    return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"],
                                       "message": "加载token失败, 请校验accessId与privateKey的正确性!"})

                paramObj["token"] = tokenResult["token"]
                paramObj["account"] = chainDeployRequest.antAddress
                paramObj["accessId"] = chainDeployRequest.accessId
                paramObj["mykmsKeyId"] = chainDeployRequest.mykmsKeyId
                paramObj["tenantid"] = chainDeployRequest.tenAntId

        return self.sendPost(paramObj, chainDeployRequest.appId, chainDeployRequest.publicKey,
                             chainDeployRequest.passBack,
                             chainDeployRequest.hostUrl + chainDeployRequest.methodPath)

    def chainCall(self, chainCallRequest: LMChainCallRequest):
        """ 调用合约

        :param chainCallRequest: LMChainCallRequest实例.
        :return: 状态码.
        """
        if not isinstance(chainCallRequest, LMChainCallRequest):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数类型错误!"})
        result = self.checkParams(chainCallRequest)
        if result is not None:
            return result
        if not chainCallRequest.contractAddress:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "contractAddress为空!"})
        if not isinstance(chainCallRequest.needSign, bool) or chainCallRequest.needSign is None:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "needSign为空!"})
        if not isinstance(chainCallRequest.functionName, str):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数{functionName}类型必须为<str>"})

        inputParamResult = self.checkInputParams(chainCallRequest.inputParams)
        if not isinstance(inputParamResult, list):
            return inputParamResult
        chainCallRequest.inputParams = inputParamResult

        outputParamResult = self.checkOutputParams(chainCallRequest.outputParam)
        if not isinstance(outputParamResult, list):
            return outputParamResult
        chainCallRequest.outputParam = outputParamResult

        paramObj = dict()
        chainType = chainCallRequest.chainType
        paramObj["link"] = chainType
        paramObj["contractAddress"] = chainCallRequest.contractAddress
        paramObj["needSign"] = chainCallRequest.needSign

        if chainType == chainCallRequest.curSupPlatform["ETH"]:  # 以太坊
            hexValueResult = self.transferERC20TokenByCall(chainCallRequest)
            if not isinstance(hexValueResult, dict):
                return hexValueResult

            paramObj["hexValue"] = hexValueResult["hexValue"]
            paramObj["functionName"] = chainCallRequest.functionName
            paramObj["inputParam"] = chainCallRequest.inputParams
            paramObj["outputParam"] = chainCallRequest.outputParam
            paramObj["address"] = chainCallRequest.ethAddress
        elif chainType == chainCallRequest.curSupPlatform["ANT"]:  # 蚂蚁
            if chainCallRequest.antAddress:
                tokenResult = self.getTokenForAnt(chainCallRequest.accessId, chainCallRequest.privateKey)
                if not isinstance(tokenResult, dict):
                    return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"],
                                       "message": "加载token失败, 请校验accessId与privateKey的正确性!"})

                paramObj["token"] = tokenResult["token"]
                paramObj["account"] = chainCallRequest.antAddress
                paramObj["accessId"] = chainCallRequest.accessId
                paramObj["mykmsKeyId"] = chainCallRequest.mykmsKeyId
                paramObj["tenantid"] = chainCallRequest.tenAntId

            functionName = chainCallRequest.functionName + "(" + ','.join([param["typeName"] for param in chainCallRequest.inputParams]) + ")"
            paramObj["functionName"] = functionName
            antInputParams = [param["typeValue"] for param in chainCallRequest.inputParams]
            paramObj["paramStr"] = json.dumps(antInputParams)
            paramObj["outTypes"] = json.dumps(outputParamResult)

        return self.sendPost(paramObj, chainCallRequest.appId, chainCallRequest.publicKey, chainCallRequest.passBack,
                             chainCallRequest.hostUrl + chainCallRequest.methodPath)

    def chainSelect(self, chainSelectRequest: LMChainSelectRequest):
        """ 交易记录查询

        :param chainSelectRequest: LMChainSelectRequest实例
        :return: 状态码.
        """
        if not isinstance(chainSelectRequest, LMChainSelectRequest):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数类型错误!"})
        result = self.checkParams(chainSelectRequest)
        if result is not None:
            return result
        if not chainSelectRequest.transHash:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "transHash为空!"})

        paramObj = dict()
        chainType = chainSelectRequest.chainType
        paramObj["link"] = chainType
        paramObj["hash"] = chainSelectRequest.transHash

        if chainType == chainSelectRequest.curSupPlatform["ETH"]:  # 以太坊
            paramObj["address"] = chainSelectRequest.ethAddress
        elif chainType == chainSelectRequest.curSupPlatform["ANT"]:  # 蚂蚁
            if chainSelectRequest.antAddress:
                paramObj["account"] = chainSelectRequest.antAddress

        return self.sendPost(paramObj, chainSelectRequest.appId, chainSelectRequest.publicKey,
                             chainSelectRequest.passBack, chainSelectRequest.hostUrl + chainSelectRequest.methodPath)

    def getTokenForAnt(self, accessId, privateKey):
        """ 从`蚂蚁`平台获取Token

        :param accessId: `蚂蚁`平台租户的 access-id.
        :param privateKey: 私钥.
        :return: `蚂蚁`平台Token.
        """
        if not privateKey:
            return None
        now = str(int(time.time() * 1000))
        message = accessId + now
        secret = RSAUtil.rsa2Sign(message, privateKey)
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "accessId": accessId,
            "time": now,
            "secret": secret,
        }
        try:
            response = requests.post(url=self.antRestUrl + "/api/contract/shakeHand", headers=headers,
                                     data=json.dumps(data))
            resultJson = response.json()
            if resultJson["success"] is True:
                return {"token": resultJson["data"]}
            else:
                return json.dumps({"code": resultJson["code"], "message": resultJson["data"]})
        except Timeout:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": "网络异常,请稍后重试!"})
        except:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": ServiceErrorMsg["SERVER_ERROR"]})

    def transferERC20Token(self, chainDeployRequest):
        """ ERC-20Token交易

        :param chainDeployRequest: LMChainDeployRequest实例.
        :return: 交易签名的Hex.
        """
        transObj = self.getNocePrice(chainDeployRequest.hostUrl, chainDeployRequest.contractData, chainDeployRequest.ethAddress)
        if not isinstance(transObj, dict):
            return transObj
        gasPrice = transObj["gasPrice"]
        nonce = transObj["nonce"]
        gasLimit = transObj["gasLimit"]
        try:
            transData = dict(nonce=nonce, gasPrice=gasPrice, gas=gasLimit, value=0, data=chainDeployRequest.contractData)
            trans = Account.sign_transaction(transData, chainDeployRequest.privateKey)
            hexValue = to_hex(trans.rawTransaction)
        except:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "交易签名失败!"})
        return {"hexValue": hexValue}

    def transferERC20TokenByCall(self, chainCallRequest):
        """ 对调用的函数进行签名

        :param chainCallRequest: LMChainCallRequest实例.
        :return: 交易签名的Hex.
        """
        postData = {
            "functionName": chainCallRequest.functionName,
            "inputParam": chainCallRequest.inputParams,
            "outputParam": chainCallRequest.outputParam,
        }
        hexDataResult = self.getHexDate(url=chainCallRequest.hostUrl + "/chain/encode", postData=postData)
        if not isinstance(hexDataResult, dict):
            return hexDataResult
        hexData = hexDataResult["hexData"]

        transObj = self.getNocePrice(chainCallRequest.hostUrl, hexData, chainCallRequest.ethAddress, chainCallRequest.contractAddress)
        if not isinstance(transObj, dict):
            return transObj
        gasPrice = transObj["gasPrice"]
        nonce = transObj["nonce"]
        gasLimit = transObj["gasLimit"]
        try:
            if is_checksum_address(chainCallRequest.contractAddress):
                contractAddress = chainCallRequest.contractAddress
            else:
                contractAddress = to_checksum_address(chainCallRequest.contractAddress)

            transData = dict(nonce=nonce, gasPrice=gasPrice, gas=gasLimit, to=contractAddress, value=0, data=hexData)
            trans = Account.sign_transaction(transData, chainCallRequest.privateKey)
            hexValue = to_hex(trans.rawTransaction)
        except:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "交易签名失败!"})
        return {"hexValue": hexValue}

    def getNocePrice(self, hostUrl, hexData, ethAddress, contractAddress=None):
        """ 获取该地址所需交易信息

        :param hostUrl: 请求链接的域名.
        :param hexData: 待部署的合约data.
        :param ethAddress: ETH账户地址.
        :return:<dict> 交易信息.
        """
        url = hostUrl + "/chain/getNoncePrice"
        if contractAddress is None:
            data = {
                "address": ethAddress,
                "contractData": hexData,
            }
        else:
            data = {
                "address": ethAddress,
                "contractData": hexData,
                "contractAddress": contractAddress,
            }
        try:
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url=url, headers=headers, data=json.dumps(data))
            resultJson = response.json()
            if resultJson["code"] == "111111":
                gasPrice = resultJson["data"]["gasPrice"]
                nonce = resultJson["data"]["nonce"]
                gasLimit = resultJson["data"]["gasLimit"]
                return {"gasPrice": gasPrice, "nonce": nonce, "gasLimit": gasLimit}
            else:
                return json.dumps({"code": resultJson["code"], "message": resultJson["msg"]})
        except Timeout:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": "网络异常,请稍后重试!"})
        except:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": ServiceErrorMsg["SERVER_ERROR"]})

    def getFullContractData(self, chainDeployRequest):
        """ 构造完整合约Data

        :param chainDeployRequest: LMChainDeployRequest实例.
        :return: 完整合约的Data
        """
        if chainDeployRequest.inputParams:
            postData = {
                "inputParam": chainDeployRequest.inputParams
            }
            hexDataResult = self.getHexDate(url=chainDeployRequest.hostUrl + "/chain/encode", postData=postData)
            if not isinstance(hexDataResult, dict):
                return hexDataResult
            contractData = chainDeployRequest.contractData + hexDataResult["hexData"]
        else:
            contractData = chainDeployRequest.contractData

        return {"contractData": contractData}

    def getHexDate(self, url, postData):
        """ 生成16进制的data

        :param url: 请求链接.
        :param postData: 传入的参数
        :return: 十六进制的Data
        """
        try:
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url=url, headers=headers, data=json.dumps(postData))
            resultJson = response.json()
            if resultJson["code"] == "111111":
                return {"hexData": resultJson["data"]}
            else:
                return json.dumps({"code": resultJson["code"], "message": resultJson["msg"]})
        except Timeout:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": "网络异常,请稍后重试!"})
        except:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": ServiceErrorMsg["SERVER_ERROR"]})

    def sendPost(self, data, appId, publicKey, passBack, url):
        """ 调用接口

        :param data: 需要加密的数据.
        :param appId: UN链盟控制台中`项目`的 APPID.
        :param publicKey: UN链盟控制台中`项目`的 Public Key.
        :param passBack: 自定义参数.
        :param url: 接口地址.
        :return: 状态码.
        """
        if passBack:
            data['passBack'] = passBack
        try:
            strEncrypt = RSAUtil.rsaEncrypt(json.dumps(data), publicKey)
        except:
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "公钥填写错误!"})

        postData = {
            "appId": appId,
            "sign": strEncrypt,
            "timestamp": time.time(),
        }
        try:
            headers = {
                "Content-Type": "application/json"
            }
            response = requests.post(url=url, headers=headers, data=json.dumps(postData))
            resultJson = json.loads(response.text)
        except Timeout:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": "网络异常,请稍后重试!"})
        except:
            return json.dumps({"code": ServiceErrorCode["SERVER_ERROR"], "message": ServiceErrorMsg["SERVER_ERROR"]})

        return json.dumps(resultJson)

    def checkInputParams(self, inputParams: List[TypeDTO]):
        """ 检查合约的入参

        :param inputParams: 传入的入参.
        :return: 格式化的入参.
        """
        params = list()
        if inputParams is None:
            return params
        if not isinstance(inputParams, list):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数{inputParams}类型必须为<list>!"})

        for typeDTO in inputParams:
            if not isinstance(typeDTO, TypeDTO):
                return json.dumps(
                    {"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数{inputParams}数据类型必须为<list<TypeDTO>>!"})
            if typeDTO.isInvalid is False:
                param = {"typeName": typeDTO.typeName, "typeValue": typeDTO.typeValue}
                params.append(param)
            else:
                return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "数据类型TypeDTO的name为空!"})
        return params

    def checkOutputParams(self, outputParams: List[str]):
        """ 检查合约的出参

        :param outputParams: 传入的出参.
        :return: 格式化的出参.
        """
        params = list()
        if outputParams is None:
            return params
        if not isinstance(outputParams, list):
            return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数{outputParam}类型必须为<list>!"})
        for param in outputParams:
            if not isinstance(param, str):
                return json.dumps({"code": ServiceErrorCode["INVALID_FIELD"], "message": "请求参数{outputParam}类型必须为<list<str>>!"})
            params.append(param.lower())
        return params

    def checkParams(self, chainRequest):
        """ 检查参数

        :param chainRequest: 请求参数类的实例.
        :return: None或状态码.
        """
        if not isinstance(chainRequest, LMChainRequest):
            return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "请求参数类型错误!"})

        if not chainRequest.appId:
            return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "appId为空!"})

        if not chainRequest.chainType:
            return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "链类型{chainType}为空!"})
        elif chainRequest.chainType not in chainRequest.curSupPlatform.values():
            return json.dumps(
                {"code": ServiceErrorCode['INVALID_FIELD'], "message": f"暂不支持链类型{chainRequest.chainType}!"})

        if not chainRequest.publicKey:
            return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "公钥为空!"})

        if chainRequest.chainType == chainRequest.curSupPlatform['ETH']:  # 以太坊
            if not chainRequest.ethAddress:
                return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "账户地址为空!"})
        elif chainRequest.chainType == chainRequest.curSupPlatform['ANT']:  # 蚂蚁
            if chainRequest.antAddress:
                if not chainRequest.accessId:
                    return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "accessid为空!"})
                if not chainRequest.mykmsKeyId:
                    return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "mykmsKeyId为空!"})
                if not chainRequest.tenAntId:
                    return json.dumps({"code": ServiceErrorCode['INVALID_FIELD'], "message": "tenAntId为空!"})

        return None
