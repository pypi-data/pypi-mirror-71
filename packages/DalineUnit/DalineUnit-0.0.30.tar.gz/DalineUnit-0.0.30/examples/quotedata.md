# QueryQuoteList
## unit_info
+ description = CTP接口每日获取代码表，保证金率，手续费率，期货，期权。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = tu

# HisDataProduceHF
## upper_unit
## unit_info
+ description = 根据缓存下的实时数据生产历史tick频，秒频数据，只生产基础频率。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = tu


# HisDataProduceLF
## unit_info
+ description = 根据缓存下的实时数据生产历史分钟频，小时频，日频，周频，月频，年频数据，只生产基础频率。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = tu

# RealQuoteList
## unit_info
+ description = 最新所有品种代码表，保证金率，手续费率。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
无
## Interface
...

# HisQuoteList
## unit_info
+ description = 历史代码表，保证金率，手续费率。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
无
## Interface
...

# CTPDataStore
## unit_info
+ description = CTP数据落地，数据生产用，不对外提供服务，对外接口用于查询数据接收和存储情况，数据文件存储位置。要控制磁盘IO，每10秒写一次，数据落地文件可以按交易所分，数据生产TU再处理。落地文件按交易日，每交易日，每交易所一个。保留最近10个交易日，超过删除。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
+ RealQuoteList
## Interface
...

# CTPRealData
## unit_info
+ description = 接收CTP实时数据，仅对外直接推送，不做其他逻辑。相当于仅对CTP实时数据接口进行封装
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
+ RealQuoteList
## Interface
...

# RealQuoteHF
## unit_info
+ description = 接收上级单元实时tick数据推送，生成tick队列，合成tick频K bar，多频，合成秒频Kbar，多频。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
+ CTPRealData
## Interface
...

# RealQuoteLF
## unit_info
+ description = 接收上级单元实时tick数据推送，生成分钟频Kbar，多分钟频，多小时频，日频。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
+ CTPRealData
## Interface
...

# HisQuoteHF
## unit_info
+ description = 根据历史数据文件处理tick频和秒频。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
无
## Interface
...

# HisQuoteLF
## unit_info
+ description = 根据历史数据文件处理分钟频，小时频，日频，周频，月频，年频。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
无
## Interface
...

# AllQuote
## unit_info
+ description = 对于涉及当日及历史数据的合并请求处理，不支持订阅，订阅从实时数据模块做。
+ lang = cpp
+ folder = .\UnitDesign\quote\
+ type = pu
## upper_unit
+ RealQuoteHF
+ RealQuoteLF
+ HisQuoteHF
+ HisQuoteLF
## Interface
...
