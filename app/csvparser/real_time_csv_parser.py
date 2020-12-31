import csv, os, re, math ,json
from datetime import datetime, timedelta
from sqlalchemy.sql import select
from app.config.models import Garage ,Customer
from operator import itemgetter
from app.services.device_service import DeviceService
from app.services.systemlog_service import SystemlogService
class RealTimeCsvProcess():
   
    _db =None
    
    def __init__(self, db):
        self._db = db
        self._log_service = SystemlogService(self._db)
        self._syslog = {}

 
    # def real_time_transaction_process(self, location : str):
    #     files = os.listdir(location)
    #     pattern = "^\\d+_\\d+_\\d+\\.csv$"
    #     real_time_transaction_data = []
    #     for i in sorted(files,key= self.last_4chars):
    #         print(i)
    #         # if re.match(pattern,i):
    #         #     file_name_detail = []
    #         #     file_name_detail.append(i)    
    #         #     file_name_detail.append(i[8:16])
    #         #     x = open(location + '/'+ i,'r')
    #         #     temp = x.read().rstrip('\r\n').split(',')
    #         #     file_detail = file_name_detail + temp
    #         #     real_time_transaction_data.append(file_detail)
    #     return real_time_transaction_data

    # def last_4chars(self, x):
    #     return x[8:22]

    def real_time_transaction_process(self, location : str):
        pattern = "^[A-Za-z0-9]+_\\d+_\\d+.csv$"
        real_time_transaction_data = []
        for dirPath, dirNames, fileNames in os.walk(location):
            for n in fileNames:
                if re.match(pattern,n):
                    file_name_detail = []
                    file_name_detail.append(n)
                    file_name_detail.append(n[8:16])
                    x = open(os.path.join(dirPath,n),'r')
                    temp = x.read().rstrip('\r\n').split(',')
                    file_detail = file_name_detail + temp
                    real_time_transaction_data.append(file_detail)
        real_time_transaction_data = sorted(real_time_transaction_data, key = itemgetter(0))
        return real_time_transaction_data
    
  
    async def process_csv_data(self, parse_data : list, account_id : int):
        """ 負責解析資料 並且塞到裡面  """
        async with self._db.acquire() as conn:
            garage_id = await(await conn.execute(select([Garage.c.garage_id]).where(Garage.c.customer_garage_id == parse_data[14]))).scalar()
            garage_code = await(await conn.execute(select([Garage.c.garage_code]).where(Garage.c.customer_garage_id == parse_data[14]))).scalar()
            customer_id = await(await conn.execute(select([Garage.c.customer_id]).where(Garage.c.garage_id == garage_id))).scalar()
            data = await self.create_real_time_data(parse_data, account_id,garage_id,customer_id)
            in_or_out = parse_data[2]
            after_device = await self.get_device(data['real_time_transaction_bean'],in_or_out)
            data['parking_bean'] = self.create_parking_data(parse_data,garage_id,garage_code,after_device['parking_bean'],after_device['real_time_transaction_bean']['device_type'])
            data['real_time_transaction_bean'] = after_device['real_time_transaction_bean']
            self._syslog['create_account_id']=0
            self._syslog['event_id']=707
            self._syslog['event_message']= f"parse_data{parse_data} @ garage_id :{garage_id}/garage_code:{garage_code}/customer_id:{customer_id}"
            result = await self._log_service.addlog(self._syslog)
        return data
    
    async def get_device(self, real_time_transaction_bean ,in_or_out):
        device_service = DeviceService(self._db)
        device_data = await device_service.get_device_type_by_device_ip(real_time_transaction_bean['device_ip'],real_time_transaction_bean['garage_id'])
        parking_bean = {}
        if len(device_data) == 1:
            real_time_transaction_bean['device_type'] = device_data[0]['device_type']
            real_time_transaction_bean['device_id'] = device_data[0]['device_id']
            if in_or_out == '0':
                #in
                parking_bean['pv'] = device_data[0]['device_name']
            elif in_or_out == '1':
                parking_bean['pv_out'] = device_data[0]['device_name']
            if "4" is real_time_transaction_bean['device_type']:
                #ibox
                parking_bean['pv'] = device_data[0]['device_name']
                parking_bean['pv_out'] = device_data[0]['device_name']
        elif len(device_data) == 0 or len(device_data) > 1:
            # 設備還沒好，先寫死 等好了之後應該要改成 type:未知（'0'） 
            real_time_transaction_bean['device_type'] = '0'
            #raise PermissionError('錯了喔','找不到device ip')
        after_device = {"real_time_transaction_bean" :real_time_transaction_bean ,"parking_bean" :parking_bean}
        return after_device

    async def create_real_time_data(self, parse_data : list, account_id : int ,garage_id: int,customer_id):
        """ 組一個dict 方便在資料庫新增使用 """
        montior_log = {}
        # log Montior info 現在還沒用到 之後要用
        # montior_log['autoDeposit'] = "" if "0" == parse_data[24] else "[有開啟自動加值功能]"
        # montior_log['autoDepositCost'] = int(parse_data[25])
        # montior_log['paid_card_name'] = self.get_type_name(parse_data[7])
        # montior_log['car_type_name'] = self.get_type_name(parse_data[19])
        # montior_log['err_message'] = parse_data[26]

        einvoice_bean = {}
        parse_data.append(account_id)
        parse_data.append(datetime.utcnow())
        real_time_transaction_bean = ["in_or_out", "parking_type", "card_id_16", "in_or_out_datetime",
        "pay_datetime", "card_type", "receivable", "real_fees", "before_pay_balance", "is_disability",
        "vehicle_identification_number", "device_ip", "garage_id", "customer_id","discount_type", "discount_amount",
        "status_number", "vehicle_type", "einvoice", "einvoice_print_status", "tax_id_number", "card_id_appearance",
        "is_autoload", "autoload_amout","error_message","create_account_id", "create_date"]
        real_time_transaction_bean = dict(zip(real_time_transaction_bean, parse_data[2:]))
        real_time_transaction_bean['garage_id'] = garage_id
        real_time_transaction_bean['customer_id'] = 0 if customer_id is None else customer_id

        # # 目前用不到
        parking_in_out_bean = {}
        # parking_in_out_bean = {"state" : parse_data[2], "trans_type" : parse_data[3], "entry_time" : parse_data[5],
        # "exit_time" : parse_data[5], "car_number" : parse_data[12], "parking_id" : "", "update_time" : datetime.utcnow(),
        # "update_user" : "acer", "source_filename" : parse_data[0], "garage_code" : parse_data[14],
        # "csv_file_date" : parse_data[1]}
        # parking_in_out_bean['paid_type'] = "%02d" % (int(parse_data[7]))

        data = {"montior_log" : montior_log,"parse_data": parse_data,
        "parking_in_out_bean" : parking_in_out_bean,
        "einvoice_bean" : einvoice_bean, "real_time_transaction_bean" : real_time_transaction_bean}
        return data

    # def process_card_no(self, inner_code : str, outer_code : str, card_type : str):
    #     """ 依卡種處理 16進位和10進位卡號 """
    #     card_od_info = {'card_id16' : inner_code[0:8]}
    #     if('2' is card_type or '5' is card_type):
    #         card_od_info['card_id'] = outer_code
    #     else:
    #         temp = inner_code[6:] + inner_code[4:6] + inner_code[2:4] + inner_code[0:2]
    #         card_od_info['card_id'] = int(temp,16)
    #     return card_od_info
    
    def get_type_name(self, paid_type : str):
        """ 代號對照表 """
        return {"1" : "悠遊卡", "2" : "愛金卡", "3" : "一卡通", "5" : "有錢卡", "99" : "人工結帳", "01" : "汽車" , "02" : "機車" , "03" : "大客車"}.get(paid_type, "錯誤代碼")

    def create_parking_data(self ,parse_data,garage_id,garage_code,parking_bean,device_type):
        if "0" is parse_data[2]:
            parking_bean['exit_time'] = '0000-00-00 00:00:00'
            parking_bean['duration'] = 0
            parking_bean['note'] = ""
            parking_bean['exit_balance'] = 0
            parking_bean['settlement_type'] = 0
            parking_bean['txn_datetime'] = '0000-00-00 00:00:00'
            parking_bean['txn_amt'] = 0
            parking_bean['entry_mode'] = 1
            parking_bean['modified_date'] = datetime.utcnow()
            parking_bean['vehicle_type'] = parse_data[19]
            parking_bean['card_id'] =  parse_data[23]         
            parking_bean['card_id16'] = parse_data[4]
            parking_bean['enter_time'] = datetime.strptime(parse_data[5], '%Y%m%d%H%M%S')
            parking_bean['paid_time'] = datetime.strptime(parse_data[6], '%Y%m%d%H%M%S')
            parking_bean['fee'] = parse_data[8]
            parking_bean['real_fee'] = parse_data[9]
            parking_bean['paid_type'] = "%02d" % (int(parse_data[7]))
            parking_bean['entry_balance'] = parse_data[10]
            parking_bean['disability_mode'] = parse_data[11]
            parking_bean['card_autoload_flag'] = parse_data[24]   
            parking_bean['last_source_filename'] = parse_data[0]
            parking_bean['last_csv_file_date'] = parse_data[1]
            parking_bean['garage_id'] = garage_id
            parking_bean['garage_code'] = garage_code
        elif "1" is parse_data[2]:
            parking_bean['exit_time'] = datetime.strptime(parse_data[5], '%Y%m%d%H%M%S')
            parking_bean['card_id'] = parse_data[23]
            parking_bean['paid_time'] = datetime.strptime(parse_data[6], '%Y%m%d%H%M%S')
            parking_bean['exit_balance'] = parse_data[10]
            parking_bean['paid_type'] = "%02d" % (int(parse_data[7]))
            parking_bean['fee'] = parse_data[8]
            parking_bean['real_fee'] = parse_data[9]
            parking_bean['last_source_filename'] = parse_data[0]
            parking_bean['last_csv_file_date'] = parse_data[1]
            parking_bean['vehicle_identification_number'] = parse_data[12]
            parking_bean['einvoice'] = parse_data[20]
            parking_bean['einvoice_print_status'] = parse_data[21]
            parking_bean['garage_id'] = garage_id
            parking_bean['garage_code'] = garage_code
        # ibox
        if "4" is device_type:
            parking_bean['duration'] = 0
            parking_bean['note'] = ''
            parking_bean['settlement_type'] = 0
            parking_bean['txn_datetime'] = '0000-00-00 00:00:00'
            parking_bean['txn_amt'] = 0
            parking_bean['entry_mode'] = 1
            parking_bean['modified_date'] = datetime.utcnow()
            parking_bean['vehicle_type'] = parse_data[19]
            parking_bean['card_id16'] = parse_data[4]
            parking_bean['enter_time'] = datetime.strptime(parse_data[5], '%Y%m%d%H%M%S')
            parking_bean['entry_balance'] = parse_data[10]
            parking_bean['disability_mode'] = parse_data[11]
            parking_bean['card_autoload_flag'] = parse_data[24]   
        return parking_bean


# def main():
#     # test
#     # a = "../../csvs/real_time_transaction"
#     # b = RealTimeCsvProcess()
#     # c = b.real_time_transaction_process(a)
#     # for i in c:
#     #     print(i)
#     # a = b.process_csv_data(i,11)
#     # print(a['parking_in_out_record_bean'])
#     a ={"a":2}
#     print(bool(a));
#     if not a:
#         print('yes')
#     else:
#         print('no')

# if __name__ == "__main__":
#     main()
    
