# -- coding:utf-8 --


class LMChainRequest(object):
    def __init__(self):
        """ Constructs and sends a :class:`LMChainRequest <LMChainRequest>`.

        appId:<str> UN链盟控制台中`项目`的 APPID.
        chainType:<str> 区块链类型: ANT(蚂蚁), ETH(以太坊).
        hostUrl:<str> 请求地址的域名.
        methodPath:<str> 请求路径.
        publicKey:<str> UN链盟控制台中`项目`的 Public Key.
        privateKey:<str> 区块链所需私钥. (ETH: 创建钱包账户时的私钥; ANT: `蚂蚁开放联盟链`平台申请AccessKey私钥文件时的access.key)
        ethAddress:<str> UN链盟控制台中`项目`的Ethereum账户地址.
        accessId:<str> `蚂蚁开放联盟链`平台`证书及开发组件`中`AccessKey`的 access-id.
        tenAntId:<str> `蚂蚁`平台`账户信息`中的 租户ID.
        antAddress:<str> UN链盟控制台中`项目`的蚂蚁TBaas账户名称. (`蚂蚁开放联盟链`平台`链账户管理`中所用账户的 账户名称)
        mykmsKeyId:<str> `蚂蚁开放联盟链`平台`链账户管理`中所用账户的 mykmsKeyId. (目前只支持`密钥托管`账户)
        inputParams:<list<TypeDTO>> 合约函数的入参.
        passBack:<dict> 额外自定义参数.
        curSupPlatform:<dict> 当前支持的链类型.
        """

        self.appId = None
        self.chainType = None
        self.hostUrl = None
        self.methodPath = None
        self.publicKey = None
        self.privateKey = None
        self.ethAddress = None
        self.accessId = None
        self.tenAntId = None
        self.antAddress = None
        self.mykmsKeyId = None
        self.inputParams = None
        self.passBack = None
        self.curSupPlatform = {
            "ETH": "ETH",
            "ANT": "ANT",
        }

    def __str__(self):
        return f"<LMChainRequest: {self.appId}, {self.chainType}>"

    def __repr__(self):
        return f"<LMChainRequest: {self.appId}, {self.chainType}>"


class LMChainDeployRequest(LMChainRequest):
    def __init__(self):
        """ Constructs and sends a :class:`LMChainDeployRequest <LMChainDeployRequest>`.

        contractData:<str> 合约内容 (ANT：solidity版本不能超过4.0.23).
        methodPath:<str> 请求路径.
        """
        super(LMChainDeployRequest, self).__init__()

        self.contractData = None
        self.methodPath = "/chain/deploy.do"

    def __str__(self):
        return f"<LMChainDeployRequest: {self.appId}, {self.chainType}>"

    def __repr__(self):
        return f"<LMChainDeployRequest: {self.appId}, {self.chainType}>"


class LMChainCallRequest(LMChainRequest):
    def __init__(self):
        """ Constructs and sends a :class:`LMChainCallRequest <LMChainCallRequest>`.

        contractAddress:<str> 合约地址，部署合约sdk返回.
        functionName:<str> 调用的合约的方法名.
        outputParam:<list<str>> 调用的合约的出参数据类型.
        needSign:<bool> 是否需要签名.
        methodPath:<str> 请求路径.
        """
        super(LMChainCallRequest, self).__init__()

        self.contractAddress = None
        self.functionName = None
        self.outputParam = None
        self.needSign = None
        self.methodPath = "/chain/callContract.do"

    def __str__(self):
        return f"<LMChainCallRequest: {self.appId}, {self.chainType}, {self.contractAddress}, {self.functionName}>"

    def __repr__(self):
        return f"<LMChainCallRequest: {self.appId}, {self.chainType}, {self.contractAddress}, {self.functionName}>"


class LMChainSelectRequest(LMChainRequest):
    def __init__(self):
        """ Constructs and sends a :class:`LMChainSelectRequest <LMChainSelectRequest>`.

        transHash: 交易hash.
        methodPath: 请求路径.
        """
        super(LMChainSelectRequest, self).__init__()

        self.transHash = None
        self.methodPath = "/chain/searchContract.do"

    def __str__(self):
        return f"<LMChainSelectRequest: {self.appId}, {self.chainType}, {self.transHash}>"

    def __repr__(self):
        return f"<LMChainSelectRequest: {self.appId}, {self.chainType}, {self.transHash}>"
