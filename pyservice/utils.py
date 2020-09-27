import json
from bson import ObjectId,Decimal128
import decimal
import types
from datetime import date,datetime
import uuid
from django.db import connection

from pyservice.settings import logger
# logger.info("IndexHandler request Handler begin")

# Create your views here.
class DateJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        try :
            if isinstance(obj, datetime):
                return obj.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(obj, date):
                return obj.strftime("%Y-%m-%d")
            elif isinstance(obj, decimal.Decimal):
                return float(obj)
            elif isinstance(obj, Decimal128):
                return str(obj)
            elif isinstance(obj, ObjectId):
                return str(obj)
        except Exception as e:
            logger.error(e.args[0])
        return json.JSONEncoder.default(obj)



# class CJsonEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             if isinstance(obj, datetime.datetime):
#                 return obj.strftime('%Y-%m-%d %H:%M:%S')
#             elif isinstance(obj, date):
#                 return obj.strftime("%Y-%m-%d")
#             else:
#                 return json.JSONEncoder.default(self, obj)
#         except Exception as e:
#             print(e)

#对MongoDB返回对象使用
def createSuccessResultMongo(obj):
    if obj == None:
        jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: 'Success',
                               SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_SUCCESS,
                               SysConstants.DATASET_KEY: []}, cls=DateJsonEncoder)
    else:
        try:
            jsonObj = json.loads(obj)
            #print(jsonObj)
            jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: 'Success',
                                   SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_SUCCESS,
                                   SysConstants.DATASET_KEY: jsonObj}, cls=DateJsonEncoder)
        except Exception as e:
            jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: e,
                                   SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_ERROR,
                                   SysConstants.DATASET_KEY: []}, cls=DateJsonEncoder)
            # print(e)
            logger.error(e.args[0])
    return jsonlist

#对Mysql返回对象使用
def createSuccessResultMysql(obj):
    if obj == None:
        jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: 'Success',
                               SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_SUCCESS,
                               SysConstants.DATASET_KEY: []}, cls=DateJsonEncoder)
    else:
        try:
            data_set = []
            for i in obj.values():
                data_set.append(i)

            print(data_set)
            jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: 'Success',
                                   SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_SUCCESS,
                                   SysConstants.DATASET_KEY: data_set},cls=DateJsonEncoder)
        except Exception as e:
            jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: e,
                                   SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_ERROR,
                                   SysConstants.DATASET_KEY: []})
            # print(e)
            logger.error(e.args[0])
    return jsonlist

#手动SQL返回对象
def createSuccessResultSqlmt(sqlmt,obj):
    try:
        with connection.cursor() as cursor:
            if obj != None:
                cursor.execute(sqlmt, obj)
            else:
                cursor.execute(sqlmt)
            data_set = Dictfetchall(cursor)
            jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: 'Success',
                                   SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_SUCCESS,
                                   SysConstants.DATASET_KEY: data_set}, cls=DateJsonEncoder)

    except Exception as e:
        jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: e,
                               SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_ERROR,
                               SysConstants.DATASET_KEY: []}, cls=DateJsonEncoder)
        # print(e)
    return jsonlist

def createErrorResult(errmsg):
    jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: errmsg.args[0],
                           SysConstants.ERROR_CODE_KEY: SysConstants.ERROR_CODE_ERROR,
                           SysConstants.DATASET_KEY: []}, cls=DateJsonEncoder)
    # print(e)
    return jsonlist


def createResult(err_code, errmsg, obj):
    jsonlist = json.dumps({SysConstants.ERROR_MESSAGE_KEY: errmsg,
                           SysConstants.ERROR_CODE_KEY: err_code,
                           SysConstants.DATASET_KEY: obj}, cls=DateJsonEncoder)
    # print(jsonlist)
    return jsonlist

def createSimpleResult(obj):
    jsonlist = json.dumps(obj, cls=DateJsonEncoder)
    # print(jsonlist)
    return jsonlist

def getUUID():
    return "".join(str(uuid.uuid4()).split("-")).upper()

class SysConstants():
    DATASET_KEY = "DATASET"
    ERROR_CODE_KEY = "ERROR_CODE"
    ERROR_MESSAGE_KEY = "ERROR_MESSAGE"
    ERROR_CODE_ERROR = "ERROR"
    ERROR_CODE_EXISTED = "EXISTED"
    ERROR_CODE_SUCCESS = "SUCCESS"
    ERROR_CODE_NO_ACCESS = "NO_ACCESS"
    ERROR_CODE_SESSION_TIMEOUT = "SESSION_TIMEOUT"
    ERROR_CODE_UNKNOWN_EXCEPTIONS = "UNKNOWN_EXCEPTIONS"

# 将返回结果转换成字典
def Dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0].lower() for col in cursor.description]

    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def jsonPickValue(strjson,key):
    print(strjson)
    text1 = json.loads(strjson)
    for str in text1:
        print(str[key])
    value = text1[0][key]
    return value

def isUpdateValueNull(newVal,curVal):
    # print(newVal)
    if newVal != "null":
        return newVal
    else:
        return curVal

# 获取复杂嵌套list，json对应的下标（key）值
# 格式：keytag： "2.a"      dict_data：[{"a": "111", "b": 222}, "bbbb", {"a": "555", "b": 222}]
def get_nestdict_value(self, keytag, dict_data):
    if type(dict_data) not in [types.ListType, types.DictType]:  # 处理返回值为 "{}" ,"[]"情况
        dict_data = json.loads(dict_data)
        # dict_data = eval(dict_data)  # 效果同上
        # 处理 "a": "[]" 情况
    dict_data = self.dict_handle(dict_data)
    sname = keytag.strip()
    obj = scmd = realval = ""
    for i in sname.split("."):
        if i.is_numeric(i):
            obj = "%s[%s]" % (obj, i)
        else:
            if 'str(' in i:
                i = i[i.find('(') + 1:-1]  # 若有key为数字的，需要做str处理，编写格式为:{"data": {"1001": "A"}} --> data.str(1001)
            obj = "%s['%s']" % (obj, i)
    scmd = "%s%s" % ("dict_data", obj)
    try:
        realval = eval(scmd)
    except:
        return "[Failed]:cmd change error,eval(%s)" % scmd
    return realval

def str2date(str,date_format="%Y%m%d"):
    date = datetime.datetime.strptime(str, date_format)
    return date

def date2str(date,date_formate = "%Y%m%d"):
    str = date.strftime(date_formate)
    return str
def getNowToStr():
    return str(datetime.now())