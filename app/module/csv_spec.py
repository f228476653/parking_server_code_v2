
import time
import datetime

class CsvSpec():
    # TODO 改名換資料夾
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    ibox_pv_data_key = ['iCash.csv', 'iPass.csv', 'YHDP.csv', 'IPTable.csv', 'setting.csv',
    'switch.csv', 'PV.csv', 'PMS.csv', 'Car.csv', 'Receipt.csv']
    # ibox_service_data_key = ['iPass.csv', 'PMS.csv', 'PV.csv', 'YHDP.csv']
    def get_pv3_export_data(self, c_bean: dict, g_bean: dict, d_bean: dict):
        pass

    #   fee part

    def get_fee_args_export_csv_data(self, fee_rule: dict, fee_para1: dict, fee_para2: dict):
        # 組出費率csv檔
        fee_args_keys = ['Fee_Rule.csv', 'NormalDay.csv', 'Holiday.csv']
        result = [self.get_fee_rule_csv(fee_rule), self.get_fee_para_csv(fee_para1, 'normal_day'), self.get_fee_para_csv(fee_para2, 'holiday')]
        export_data = dict(zip(fee_args_keys, result))
        return export_data
    
    def get_fee_rule_csv(self, fee_rule: dict):
        result = {'New_Car_Hour': fee_rule['new_car_hour'], 'period': fee_rule['period'], 'NormalDay': fee_rule['normal_day'],
        'Holiday': fee_rule['holiday'], 'free_time': fee_rule['free_time'], 'mode': fee_rule['fee_mode']}
        print('現在處理FeeRule_csv', result)
        print('====================================')
        return result

    def get_fee_para_csv(self, fee_para: dict, para_day: str):
        result = {'1_HourPeriod_Fee': fee_para['hour_period_fee1'], '1_HourPeriod_Fee_Start': fee_para['hour_period_fee1_start'],
        '1_HourPeriod_Fee_End': fee_para['hour_period_fee1_end'], '2_HourPeriod_Fee': fee_para['hour_period_fee2'],
        '2_HourPeriod_Fee_Start': fee_para['hour_period_fee2_start'], '2_HourPeriod_Fee_End': fee_para['hour_period_fee2_end'],
        'Max_Fee': fee_para['max_fee'], 'Max_Fee_Hour': fee_para['max_hour'], 'special_rule': fee_para['special_rule'],
        'special_Fee_Start': fee_para['special_fee_start'], 'special_Fee_End': fee_para['special_fee_end'], 'special_Fee_Max': fee_para['special_fee_max'],
        'special_Fee_Hour': fee_para['special_fee_hour'], 'monthly_pass': fee_para['monthly_pass']}
        if para_day == 'normal_day':
            print('現在處理NormalDay_csv', result)
        elif para_day == 'holiday':
            print('現在處理Holiday_csv', result)
        print('====================================')
        return result

    # device_ibox Part
    def get_ibox_export_csv_data(self, c_data: dict, g_data: dict, d_data: dict, garage_code: str, customer_code: str, api_config: dict):
        export_data = {}
        result = [self.get_iCash_csv(c_data, g_data, d_data), self.get_iPass_csv(c_data, g_data, d_data),
        self.get_YHDP_csv(c_data), self.get_ip_table_csv(d_data), self.get_setting_csv(g_data, d_data),
        self.get_switch_csv(d_data), self.get_pv_csv(d_data), self.get_pms_csv(c_data, d_data, garage_code, customer_code, api_config), self.get_car_csv(),
        self.get_receipt_csv(g_data, d_data)]
        # service_result = [self.get_service_ipass_csv(c_data), self.get_service_pms_csv(c_data),
        # self.get_service_pv_csv(d_data), self.get_service_YHDP_csv(c_data)]
        export_data['pv'] = dict(zip(self.ibox_pv_data_key, result))
        # export_data['host'] = dict(zip(self.ibox_service_data_key, service_result))
        return export_data

    def get_iCash_csv(self, c_data: dict, g_data: dict, d_data: dict):
        result = {'MarketCode' : c_data['market_code'], 'Store_No': g_data['store_no'], 'Pos_No': d_data['pos_no'], 'Cashier_No': c_data['cashier_no']}
        print('現在處理iCash_csv', result)
        print('====================================')
        return result

    def get_iPass_csv(self, c_data: dict, g_data: dict, d_data: dict):
        result = {'SystemID' : c_data['system_id'], 'CompID':  c_data['comp_id'],
        'PLID': g_data['plid'], 'Machine': c_data['machine'], 'EXTERNAL_IP': d_data['external_ip'],
        'WaterLV_Host': c_data['ipass_water_lv_host'], 'WaterLV_Port': c_data['ipass_water_lv_port'],
        'Socket_IP': c_data['socket_ip']}
        print('現在處理iPass_csv', result)
        print('====================================')
        return result

    def get_YHDP_csv(self, c_data: dict):
        result = {'TransactionSystemID' : c_data['transaction_system_id'], 'LOC_ID':  c_data['loc_id'],
        'TransactionTerminalNO': c_data['transaction_terminal_no'], 'TID': c_data['tid'],
        'MID': c_data['mid'], 'WaterLV': c_data['YHDP_water_lv'], 'WaterLV_Host': c_data['YHDP_water_lv_host'],
        'WaterLV_Port': c_data['YHDP_water_lv_port'], 'NII': c_data['nii']}
        print('現在處理YHDP_csv', result)
        print('====================================')
        return result

    def get_ip_table_csv(self, d_data: dict):
        result = {'IPASS': 'smallpay.test.i-pass.com.tw,2222,park_41FF,9eef4187', 'CarIn': d_data['car_in'], 'CarOut': d_data['car_out']}        
        print('現在處理ip_table_csv', result)
        print('====================================')
        return result

    def get_setting_csv(self, g_data: dict, d_data: dict):
        result = {'Date': self.date, 'Station_InOut': d_data['station_inout'],
        'Printer': g_data['printer'], 'Store_No': g_data['store_no'],
        'Pos_No': d_data['pos_no'], 'Tax_ID_Num': g_data['tax_id_num'], 'NTP_Server': g_data['ntp_server']}
        print('現在處理setting_csv', result)
        print('====================================')
        return result

    def get_switch_csv(self, d_data: dict):
        # !!! 特別處理 !!!
        card_order = d_data['card_order'].split(',')
        data = [d_data['slot1'], d_data['slot2'], d_data['slot3'], d_data['slot4']]
        result = []
        for i in range(len(card_order)):
            result.append(card_order[i] + ',' + str(data[i]))
        print('現在處理switch_csv', result)
        print('====================================')
        return result

    def get_pv_csv(self, d_data: dict):
        result = {'IP': d_data['ip'], 'Gateway': d_data['gateway']}
        print('現在處理pv_csv', result)
        print('====================================')
        return result

    def get_pms_csv(self, c_data: dict, d_data:dict, garage_code: str, customer_code: str, api_config: dict):
        result = {'Host': c_data['host'], 'AcerStoreNo': garage_code, 'customerCode': customer_code, 'Position': d_data['driveway'],
            'API_url': api_config['API_url'], 'API_port': api_config['API_port'], 'API_account': api_config['API_account'], 'API_pwd': api_config['API_pwd']}
        print('現在處理pms_csv', result)
        print('====================================')
        return result

    def get_car_csv(self):
        result = {"CarNo": '        '}
        print('現在處理car_csv', result)
        print('====================================')
        return result

    def get_receipt_csv(self, g_data: dict, d_data: dict):
        result ={'Store_No': g_data['store_no'], 'Pos_No': d_data['eid_pos_no'], 'EID_Store_No': g_data['eid_store_no']}
        print('現在處理receipt_csv', result)
        print('====================================')
        return result

    # Service Part

    def get_service_ipass_csv(self, c_data: dict):
        if 'ipass_water_lv_host' in c_data and 'ipass_water_lv_port' in c_data:
            ipass_water_host = str(c_data['ipass_water_lv_host']) + "," + str(c_data['ipass_water_lv_port'])
        else:
            ipass_water_host = ' '
        result ={'iPass_Water_Host': ipass_water_host}
        print('現在處理service_ipass_csv', result)
        print('====================================')
        print(result)
        return result

    def get_service_pms_csv(self, c_data: dict):
        if 'ipass_water_lv_port' in c_data:
            YHDP_water_lv_port = c_data['YHDP_water_lv_port']
        else:
            YHDP_water_lv_port = ' '
        if 'ipass_water_lv_port' in c_data:
            ipass_water_lv_port = c_data['ipass_water_lv_port']
        else:
            ipass_water_lv_port = ' '
        result = {'PMS_Exchanger_Host': 'Not_Use', 'PMS_iPass_Listen_Port': ipass_water_lv_port,
        'PMS_YHDP_Listen_Port': YHDP_water_lv_port, 'PMS_ECC_Listen_Port': 'Not_Use'}
        print('現在處理service_pms_csv', result)
        print('====================================')
        return result
    
    def get_service_pv_csv(self, d_data: dict):
        result ={'Client_PV': d_data['client_pv'], 'TimeSyncPeriod': d_data['time_sync_period']}
        print('現在處理service_pv_csv', result)
        print('====================================')
        return result

    def get_service_YHDP_csv(self, c_data: dict):
        if 'YHDP_water_lv_host' in c_data and 'YHDP_water_lv_port' in c_data:
            YHDP_water_host = str(c_data['YHDP_water_lv_host']) + "," + str(c_data['YHDP_water_lv_port'])
        else:
            YHDP_water_host = ' '
        result ={'YHDP_Water_Host': YHDP_water_host}
        print('現在處理service_YHDP_csv', result)
        print('====================================')
        return result

# test
def main():
    # c = {'customer_ibox_args_id': 1, 'market_code': 'P21', 'cashier_no': 'A110', 'system_id': '42', 'comp_id': '29', 'machine': '4D3C2B1A', 'ipass_water_lv_host': '192.168.0.101', 'ipass_water_lv_port': 8988, 'socket_ip': '10.20.1.74', 'transaction_system_id': '00', 'loc_id': '02', 'transaction_terminal_no': '471F6241', 'tid': '00000002', 'mid': '0000000000000000', 'YHDP_water_lv': 3000, 'YHDP_water_lv_host': '192.168.0.101', 'YHDP_water_lv_port': 6666, 'nii': 667, 'host_ip': '192.168.35.129', 'host_port': '8000', 'host_user': 'root', 'host_pwd': '@@123qwe', 'update_time': datetime.datetime(2018, 7, 4, 13, 49, 27), 'update_user': 'root', 'customer_id': 0}
    # g = {'garage_ibox_args_id': 1, 'garage_code': '23400', 'store_no': '323', 'pos_no': 1, 'eid_store_no': '3346', 'plid': '01E1', 'printer': 1, 'tax_id_num': '86517413', 'ntp_server': '103.18.128.60', 'update_time': datetime.datetime(2018, 7, 4, 13, 49, 27), 'update_user': 'root', 'garage_id': 1}
    # d = {'device_ibox_args_id': 1, 'device_name': 'iBox一號', 'external_ip': '61.222.250.66', 'station_inout': 0, 'ECC': 1, 'iPass': 1, 'iCash': 0, 'YHDP': 1, 'ip': '192.168.0.102', 'mac_ip': '255.255.255.255', 'eid_pos_no': '346Z', 'client_pv': '192.168.53.201,192.168.53.202', 'time_sync_period': 24, 'update_time': datetime.datetime(2018, 7, 4, 14, 31, 54), 'update_user': 'root',
    #     'garage_id': 1, 'car_in': '', 'car_out': '192.168.0.102,0.0.0.0'}
    # a = CsvSpec()
    # ans = a.get_ibox_export_csv_data(c, g, d, '12002')
    # print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    # print(ans['host'])

    # card_order = d_data['card_order'].split(',')
    #     result =  {card_order[0]: d_data['slot1'], card_order[1]:  d_data['slot2'],
    #         card_order[2]: d_data['slot3'], card_order[3]: d_data['slot4']}

    # a = ['a', 'b','c','d']
    # b = ['1', '2','3','4']
    # c = {'a1' : a[0] + ',' + b[0], 'a2' : a[1] + ',' + b[1], 'a3' : a[2] + ',' + b[2], 'a4' : a[3] + ',' + b[3]}
    # print(c)
    # for i in c:
    #     print(str(c[i]))
    a = ['iCash', 'iPass', 'iCash', 'iC']
    for i in range(len(a)):
        print(i)

if __name__ == '__main__':
    main()
        
