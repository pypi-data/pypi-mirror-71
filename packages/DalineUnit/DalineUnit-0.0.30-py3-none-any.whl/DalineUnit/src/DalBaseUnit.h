#ifndef DALBASEUNIT_H
#define DALBASEUNIT_H

#include <iostream>
#include <memory>
#include <string>
#include <list>
#include <map>
#include <thread>
#include <chrono>

#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
using namespace rapidjson;


class DalBaseUnitGRPC;


typedef std::string(*IF_Info)();
typedef std::string(*IF_Meta)(std::string, std::string);
typedef std::string(*IF_Data)(std::string, std::string);
typedef std::string(*IF_NewData)();

class  DalBaseUnit {
public:
	bool inprocess = false;
	std::string s_dataIF;
	std::list<std::thread> list_threads;
	Document dicMethod; // 
	

public:
	std::map<std::string, IF_Info> map_IFInfo; //
	std::map<std::string, IF_Meta> map_IFMeta; //
	std::map<std::string, IF_Data> map_IFData; // 
	std::map<std::string, IF_NewData> map_IFNewData; // 
	void logError();
	void logWarn();
	void logInfo();
	void quit();
	void start_frame();
	void run_new_data(IF_NewData p_if_newdata);
	static void newdata(std::string string_dicMeta, std::string string_dicData);
	static std::string Document2String(Document& documentin);
	static std::string Value2String(Value& valuein);
	std::string BindRequest(std::string s_request);
	

	DalBaseUnit();

	DalBaseUnitGRPC *m_pGRPC ;

	void run();
};

#endif // !DALBASEUNIT_H