# RealQuoteList_PU
## unit_info
+ discription = 最新所有品种代码表，保证金率，手续费率。
+ lang = C++
+ type = pu
## Interface
### getAllSymbolInfoLists
#### input
#### output
{
    "symbolinfolists":      #所有合约信息列表
    [
        {
            "symbol" : "str",      #标的名
            "symbolinfo" :        # 标的信息
            {
                "marginrate" : "float",       #合约保证金率
                "feerate" : "float"             #合约手续费率
            }
        }
    ]
}
#### meta_data
+ ownerID = 500
+ ownerGroupID = 200
+ acCode = 777
+ did = 9527
+ zipDataSize = 692k
+ rawDataSize = 1428k
+ md5 = lkjliudfadf12jolx
+ dataTime = 20200109
+ version = 1.0
+ description = 这里写了一堆的数据描述
### getAllSymbolLists
#### input
#### output
{
    "symbollists" :         #所有合约列表
    [
        {"symbol" : "str"}    #标的名
    ]
}
#### meta_data
+ ownerID = 500
+ ownerGroupID = 200
+ acCode = 777
+ did = 9527
+ zipDataSize = 692k
+ rawDataSize = 1428k
+ md5 = lkjliudfadf12jolx
+ dataTime = 20200109
+ version = 1.0
+ description = 这里写了一堆的数据描述
### getSymbolInfoListsBySymbolLists
#### input
+ symbollists={"symbol":["cu2007"]}   #合约列表
#### output
{
    "symbolinfolists":      #所有合约信息列表
    [
        {
            "symbol" : "str",      #标的名
            "symbolinfo" :        # 标的信息
            {
                "marginrate" : "float",       #合约保证金率
                "feerate" : "float"             #合约手续费率
            }
        }
    ]
}


#### meta_data
+ ownerID = 500
+ ownerGroupID = 200
+ acCode = 777
+ did = 9527
+ zipDataSize = 692k
+ rawDataSize = 1428k
+ md5 = lkjliudfadf12jolx
+ dataTime = 20200109
+ version = 1.0
+ description = 这里写了一堆的数据描述

----
# 拓扑图如下
```mermaid
    graph TB

```
        