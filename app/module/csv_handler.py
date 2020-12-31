import time, os

class CsvHandler():
    # TODO 改名換資料夾
    def export_csv(self, folder_path: dict, file_name: str, context: dict, customer_code: str, 
        garage_code: str, device_folder_name: str, folder_type: str):
        #print('目標路徑', folder_path)
        #print('檔名', file_name)
        #print('存入csv資料', context)
        #print('依場站代碼分類', garage_code)
        #print('依照類型再分子資料夾', folder_type)
        for i in folder_path:
            export_path = folder_path[i] + '/' + str(customer_code) + '/' + str(garage_code) + '/' + str(device_folder_name) + '/' + str(folder_type)
            print('路徑', export_path)
            if not os.path.isdir(export_path):
                # 依次建多層資料夾
                os.makedirs(export_path)
            f = open(export_path + '/' + file_name, 'w')
            for i in context:
                # switch.csv 手法和其他不一樣
                if file_name == 'switch.csv':
                    print(i, file= f)
                else:
                    print(i + ',' + str(context[i]), file= f)
            f.close()
        
    def get_datetime_format(self):
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    def export_fee_args_csv(self, folder_path: str, customer_code: str, garage_code: str,
          driveway: str, context: dict):
        print('最後一段')
        print(folder_path)
        # print(context)
        print(customer_code)
        print(garage_code)
        export_path = folder_path + '/' + str(customer_code) + '/' + str(garage_code) + '/' + str(driveway) + '/fee'
        print(export_path)
        if not os.path.isdir(export_path):
            os.makedirs(export_path)
        for keys in context:
            print(keys)
            f = open(export_path + '/' + keys, 'w')
            for i in context[keys]:
                print(i + ',' + str(context[keys][i]), file=f)
            f.close()

# test
def main():
    # a = CsvHandler()
    # b = {'Date': '2018-05-21 18:09:16', 'MarketCode': 'P21', 'Store_No': '192.168,1.1.1.1', 'Pos_No': '59', 'Cashier_No': 'A110'}
    # # b = b.items()
    # # 測試存iCash.csv
    # # date = a.get_datetime_format()
    # # print(b)
    # # data = {'Date': date, 'MarketCode': 'P21', 'Store_No': '12345678', 'Pos_No': '59', 'Cashier_No': 'A110'}
    # # b = data.items()
    # # print(b)
    # folder_path = '../module/test'
    # # c = os.path.isdir(folder_path)
    # a.export_csv(folder_path, 'haha.csv', b, 'garage_code', 'pv')
    # print('aa')
    # # a.export_csv(folder_path, 'haha.csv', b, 'garage_code', 'host')
    # # print('bb')
    # # path = os.path.abspath('.')
    # # print(path)
    print(os.getuid())

if __name__ == '__main__':
    main()

        
