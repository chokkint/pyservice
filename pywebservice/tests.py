# Create your tests here.
from pywebservice import bizfunc as bizfunc
import cx_Oracle
import demjson
# from django.db import connection
# cursor = connection.cursor()
def testOracle():
    conn = cx_Oracle.connect("ods_ctrl/ods_ctrl@chokkint.dsmynas.com:11521/ODS")
    cur = conn.cursor()
    r = cur.execute("select sysdate from dual")
    print(r.fetchall())



def test():
    data = {
        "odsBusiDt": "20200331",
        "odsBranchCode": "8879",
        "pdrMapList": [
            {
                "PD_ID": "1111",
                "PD_NAME": "J1a",
                "PD_VALUE": 0.0003,
                "R_BANK": 0.2,
                "R_NONE_BANK": 0.25
            },
            {
                "PD_ID": "222",
                "PD_NAME": "J1b",
                "PD_VALUE": 0.0003,
                "R_BANK": 0.2,
                "R_NONE_BANK": 0.25
            }
        ],
        "zMapList": [
            {
                "REC_PD_DATE": "20200630",
                "Z_UPPER_COMM": 0.0003,
                "Z_BASIC_COMM": 0.2,
                "Z_LOWER_COMM": 0.25,
                "Z_UPPER_HIGH": 0.0003,
                "Z_BASIC_HIGH": 0.2,
                "Z_LOWER_HIGH": 0.25,
                "Z_UPPER_BANK": 0.0003,
                "Z_BASIC_BANK": 0.2,
                "Z_LOWER_BANK": 0.25
            },
            {
                "REC_PD_DATE": "20200930",
                "Z_UPPER_COMM": 0.0003,
                "Z_BASIC_COMM": 0.2,
                "Z_LOWER_COMM": 0.25,
                "Z_UPPER_HIGH": 0.0003,
                "Z_BASIC_HIGH": 0.2,
                "Z_LOWER_HIGH": 0.25,
                "Z_UPPER_BANK": 0.0003,
                "Z_BASIC_BANK": 0.2,
                "Z_LOWER_BANK": 0.25
            }
        ]
    }
    # with open('../data.json', 'r', encoding='utf8')as fp:
    json_data = data
    print('这是文件中的json数据：', json_data)
    print('这是读取到文件数据的数据类型：', type(json_data))
    ret= {}
    ret['odsBusiDt'] = json_data['odsBusiDt']
    ret['odsBranchCode'] = json_data['odsBranchCode']
    pdAdjMapList = [];
    for pdr in json_data["pdrMapList"]:
        pdAdj={}
        pdAdj['PD_ID'] = pdr['PD_ID']
        pdAdj['PD_NAME'] = pdr['PD_NAME']
        pdAdj['PD_NONE_ADJ'] = pdr['PD_VALUE']
        for z in json_data["zMapList"]:
            pdAdj['REC_PD_DATE'] = z['REC_PD_DATE']
            pdAdj['PD_ADJ_UPPER_COMM'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_UPPER_COMM'])
            pdAdj['PD_ADJ_BASIC_COMM'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_BASIC_COMM'])
            pdAdj['PD_ADJ_LOWER_COMM'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_LOWER_COMM'])
            pdAdj['PD_ADJ_UPPER_HIGH'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_UPPER_HIGH'])
            pdAdj['PD_ADJ_BASIC_HIGH'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_BASIC_HIGH'])
            pdAdj['PD_ADJ_LOWER_HIGH'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_LOWER_HIGH'])
            pdAdj['PD_ADJ_UPPER_BANK'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_UPPER_BANK'])
            pdAdj['PD_ADJ_BASIC_BANK'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_BASIC_BANK'])
            pdAdj['PD_ADJ_LOWER_BANK'] = bizfunc.pd_forward(pdr['PD_VALUE'], pdr['R_NONE_BANK'], z['Z_LOWER_BANK'])
        pdAdjMapList.append(pdAdj)
    ret['pdAdjMapList'] = pdAdjMapList
    return ret

if __name__ == "__main__":

    a = "{ip:'121.79.50.68',address:'北京市 长城宽带'}"
    a =demjson.decode(a)
    print(a)
    testOracle()


