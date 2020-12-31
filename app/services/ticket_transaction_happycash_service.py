import time, datetime
from sqlalchemy import desc,text
import os,glob,sys
import zipfile
import shutil
import paramiko
from app.config.models import Trx_Data, HappyCashConfig, TicketTransactionFtpConfig
import operator
import csv
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.config.models import Account

class TicketTransactionHappyCashService:
    _db = None
    _log_service = None
    _syslog = None
    _directory_path = None
    _process_folder = None
    _card_type = None
    _now_date = None
    _file_directory_path = None
    _user = None

    def __init__(self, db, user: Account):
        self._db = db
        self._log_service = SystemlogService(db)
        self._syslog = {}
        self._directory_path = os.getcwd()
        # Windows 測試
        # self._file_directory_path = "D:\\test_use"
        # 正式環境
        self._file_directory_path = "/home/pms_plus/file_directory/"
        self._process_path = os.path.join(self._file_directory_path, "ticket_transaction_files")
        self._card_type = "happycash"
        self._now_date = datetime.date.today().strftime("%Y%m%d")
        self._user = user


    """ 交易檔包檔 """
    async def pack(self, location):
        sql_customer = f"""SELECT distinct 
        a.customer_id, 
        a.happycash_source_id,
        b.customer_code
        FROM 
        `ticket_transaction_ftp_config` AS a
        LEFT JOIN 
        `customer` AS b
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.status = 1 and 
        a.card_type = '05'"""

        async with self._db.acquire() as conn: 
            customer_list_query = await conn.execute(sql_customer)
            if customer_list_query.rowcount > 0:
                customer_list = [dict(row.items()) async for row in customer_list_query]
                for cl in range(0, customer_list_query.rowcount):
                    sql_garage = f"""SELECT 
                    a.*, 
                    b.customer_code,
                    c.garage_code 
                    FROM 
                    `happycash_config` AS a 
                    LEFT JOIN 
                    `customer` AS b 
                    ON 
                    a.customer_id = b.customer_id 
                    LEFT JOIN
                    `garage` AS c
                    ON
                    a.garage_id = c.garage_id
                    WHERE 
                    a.status = 1 
                    and a.customer_id = :customer_id"""

                    garage_list_count = await conn.execute(text(sql_garage), {'customer_id':str(customer_list[cl]['customer_id'])})
                    if garage_list_count.rowcount >0:
                        garage_code_list = {}

                        # 檔案上傳位置
                        upload_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "upload")
                        self.mkdirs(upload_path)

                        # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                        generated_dat_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_dat")
                        if os.path.isdir(generated_dat_path):
                            shutil.rmtree(generated_dat_path)
                        self.mkdirs(generated_dat_path)
                        # 移除需要包進壓縮檔的交易檔資料夾及底下的檔案 (之後重新建立資料夾)
                        dat_files_go_zip_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_go_zip")
                        if os.path.isdir(dat_files_go_zip_path):
                            shutil.rmtree(dat_files_go_zip_path)
                        self.mkdirs(dat_files_go_zip_path)

                        # 場站交易檔包入壓縮檔備份
                        dat_files_go_zip_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_go_zip_backup", self._now_date)
                        self.mkdirs(dat_files_go_zip_backup_path)

                        # 交易檔匯入資料庫
                        dat_files_import_db_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_import_db")
                        self.mkdirs(dat_files_import_db_path)
                        # 交易檔匯入資料庫備份
                        dat_files_import_db_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_import_db_backup", self._now_date)
                        self.mkdirs(dat_files_import_db_backup_path)

                        garage_list = [dict(row.items()) async for row in garage_list_count]
                        for gl in range(0, garage_list_count.rowcount):
                            # 場站代碼List
                            garage_code_list[str(garage_list[gl]['happycash_garage_code']).zfill(15)] = str(garage_list[gl]['garage_code'])

                            """ 場站交易檔包檔 BEGIN"""
                            # device_ftp_path
                            device_ftp_path = os.path.join(self._directory_path, location, str(garage_list[gl]['customer_code']), str(garage_list[gl]['garage_code']), "transaction_files")
                            self.mkdirs(device_ftp_path)

                            self.mkdirs(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code'])))

                            generated_dat_backup_path = os.path.join(self._process_path, str(garage_list[gl]['customer_code']), self._card_type, "generated_dat_backup", self._now_date, str(garage_list[gl]['garage_code']))
                            self.mkdirs(generated_dat_backup_path)
                            files_from_device_path = os.path.join(self._process_path, str(garage_list[gl]['customer_code']), self._card_type, "files_from_device", self._now_date, str(garage_list[gl]['garage_code']))
                            self.mkdirs(files_from_device_path)

                            # 取得今日dat檔案序號
                            file_seq = self.get_file_seq(generated_dat_backup_path, str(customer_list[cl]['happycash_source_id']), str(garage_list[gl]['happycash_garage_code']).zfill(15))

                            for root, folders, files in os.walk(device_ftp_path):
                                for sfile in files:
                                    if(sfile.startswith("TXN_PARK_")):
                                        # Windows 測試
                                        # root_split = root.split("\\")
                                        # 正式環境
                                        root_split = root.split("/")

                                        aFile = os.path.join(root, sfile)

                                        # device 設備資料夾
                                        self.mkdirs(os.path.join(files_from_device_path, root_split[len(root_split)-1]))
                                        # 空檔資料夾
                                        body_content_empty_path = os.path.join(files_from_device_path, root_split[len(root_split)-1], "body_content_empty")
                                        self.mkdirs(body_content_empty_path)
                                        # 一天最多包99檔案，超過數量未包檔檔案，依舊會留在csvs/in/{customer_code}/{garage_code}/transaction_files/底下
                                        # 此做該天未包檔檔案區分
                                        not_pack_path = os.path.join(files_from_device_path, root_split[len(root_split)-1], "not_pack")
                                        self.mkdirs(not_pack_path)

                                        content = self.open_files(os.path.join(self._directory_path, location, str(garage_list[gl]['customer_code']), str(garage_list[gl]['garage_code']), "transaction_files"), aFile)
                                        if not len(content) < 67:
                                            file_seq += 1
                                            # 一天最多包99個檔案
                                            if (file_seq < 100):
                                                content = self.add_header(content, file_seq)
                                                file_name = "TXN_PARK_" + str(customer_list[cl]['happycash_source_id']) + "_" + str(garage_list[gl]['happycash_garage_code']).zfill(15) + "_" + datetime.datetime.now().strftime('%Y%m%d%H') + "_" + str(file_seq).zfill(3) + ".DAT"
                                                self.generate_dat_file(file_name, content, str(garage_list[gl]['garage_code']), generated_dat_path, generated_dat_backup_path, dat_files_go_zip_path, dat_files_import_db_path)
                                                shutil.move(aFile, os.path.join(files_from_device_path, root_split[len(root_split)-1], sfile))
                                            else:
                                                print("包檔失敗原因：happyCash交易檔已包檔數量超過99個。業者：[" + str(garage_list[gl]['customer_code']) +"]，場站：[" + str(garage_list[gl]['garage_code']) + f"]，檔案名稱：[{aFile}]")
                                                shutil.copyfile(aFile, os.path.join(not_pack_path, sfile))
                                        # 空檔不包檔，僅作移動處理
                                        else:
                                            shutil.move(aFile, os.path.join(body_content_empty_path, sfile))

                    """ 場站包檔後交易檔全部放進壓縮檔 BEGIN """
                    generated_zip_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip_backup", self._now_date)
                    self.mkdirs(generated_zip_backup_path)

                    # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                    generated_zip_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip")
                    if os.path.isdir(generated_zip_path):
                        shutil.rmtree(generated_zip_path)
                    self.mkdirs(generated_zip_path)

                    # zip檔名、流水號
                    file_name = "TXN_PARK_" + str(customer_list[cl]['happycash_source_id']) + "_" + datetime.datetime.now().strftime('%Y%m%d%H') + "_" + self.get_zip_file_no_num(generated_zip_backup_path)
                    zip_file_name = file_name + ".ZIP"
                    zip_OK_name = zip_file_name + ".OK"

                    zip_file_path = os.path.join(generated_zip_path, zip_file_name)
                    zip_OK_path = os.path.join(generated_zip_path, zip_OK_name)

                    # 開啟場站包檔後交易檔全部放進壓縮檔寫檔 
                    zf = zipfile.ZipFile(zip_file_path, "w")
                    self.pack_all_in_one(dat_files_go_zip_path, dat_files_go_zip_backup_path, zf)
                    # 場站包檔後交易檔全部放進壓縮檔寫檔完成，關閉檔案
                    zf.close()

                    if os.path.exists(os.path.join(zip_file_path)):
                        self.create_OK_file(zip_file_path)

                        shutil.copyfile(zip_file_path, os.path.join(generated_zip_backup_path, zip_file_name))
                        shutil.copyfile(zip_OK_path, os.path.join(generated_zip_backup_path, zip_OK_name))
                        shutil.copyfile(zip_file_path, os.path.join(upload_path, zip_file_name))
                        shutil.copyfile(zip_OK_path, os.path.join(upload_path, zip_OK_name))
                    """ 場站包檔後交易檔全部放進壓縮檔 END """

                    """ 票證交易資料匯入資料庫 BEGIN """
                    await self.data_import_db(zip_file_name, garage_code_list, dat_files_import_db_path, dat_files_import_db_backup_path)
                    """ 票證交易資料匯入資料庫 END """
        return "pack"

    """ 交易檔上傳 """
    async def upload(self):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = f"""SELECT distinct 
        a.*, 
        b.customer_code 
        FROM 
        `ticket_transaction_ftp_config` AS a 
        LEFT JOIN 
        `customer` AS b 
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.status = 1 and 
        a.card_type ='05'"""

        async with self._db.acquire() as conn: 
            customer_ftp_list_query = await conn.execute(sql)
            if customer_ftp_list_query.rowcount > 0:
                customer_ftp_list = [dict(row.items()) async for row in customer_ftp_list_query]
                for cfl in range(0, customer_ftp_list_query.rowcount):
                    # 檔案上傳位置
                    upload_path = os.path.join(self._process_path, str(customer_ftp_list[cfl]['customer_code']), self._card_type, "upload")
                    self.mkdirs(upload_path)

                    # 檔案上傳備份位置
                    upload_backup_path = os.path.join(self._process_path, str(customer_ftp_list[cfl]['customer_code']), self._card_type, "upload_backup", self._now_date)
                    self.mkdirs(upload_backup_path)

                    try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(str(customer_ftp_list[cfl]['ip_address']), username = str(customer_ftp_list[cfl]['account']), password = str(customer_ftp_list[cfl]['password']), port = int(customer_ftp_list[cfl]['ip_port']))
                        sftp = client.open_sftp()

                        ticket_host_path = str(customer_ftp_list[cfl]['upload_path'])

                        # 交易檔
                        for root, folders, files in os.walk(upload_path):
                            for sfile in files:
                                if(sfile.startswith("TXN_PARK_")):
                                    aFile = os.path.join(root, sfile)

                                    data = {}
                                    data['cal_status'] = "C"
                                    # where 條件
                                    # data['upload_zip_name'] = sfile
                                    sftp.put(aFile, ticket_host_path + sfile)
                                    shutil.move(aFile, os.path.join(upload_backup_path, sfile))
                                    if (sfile.endswith(".ZIP")):
                                        trans = await conn.begin()
                                        try:
                                            rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.upload_zip_name == sfile))
                                        except Exception as e:
                                            print('有錯: ',e)
                                            await trans.rollback()
                                            raise
                                        else:
                                            await trans.commit()
                                
                                sftp.close()
                                client.close()
                    except Exception as e:
                        print('Error:%s'% (e) )    
        return "upload"

    """ 回饋檔 & 黑名單 下載 """
    async def download(self, location, download_file_type):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = f"""SELECT distinct 
        a.*, 
        b.customer_code 
        FROM 
        `ticket_transaction_ftp_config` AS a 
        LEFT JOIN 
        `customer` AS b 
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.status = 1 and 
        a.card_type ='05'"""

        async with self._db.acquire() as conn: 
            customer_ftp_list_query = await conn.execute(sql)
            if customer_ftp_list_query.rowcount > 0:
                customer_ftp_list = [dict(row.items()) async for row in customer_ftp_list_query]
                for cfl in range(0, customer_ftp_list_query.rowcount):
                    # 檔案下載位置
                    download_path = os.path.join(self._process_path, str(customer_ftp_list[cfl]['customer_code']), self._card_type, "download", download_file_type)
                    self.mkdirs(download_path)

                    # 回饋檔匯入資料庫
                    feedback_files_import_db_path = os.path.join(self._process_path, str(customer_ftp_list[cfl]['customer_code']), self._card_type, "feedback_files_import_db")
                    self.mkdirs(feedback_files_import_db_path)

                    # 供設備下載黑名單位置
                    customer_download_black_list_path = os.path.join(self._directory_path, location, str(customer_ftp_list[cfl]['customer_code']), "happyCash.bl")
                    self.mkdirs(customer_download_black_list_path)

                    try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(str(customer_ftp_list[cfl]['ip_address']), username = str(customer_ftp_list[cfl]['account']), password = str(customer_ftp_list[cfl]['password']), port = int(customer_ftp_list[cfl]['ip_port']))
                        sftp = client.open_sftp()

                        ticket_host_path = str(customer_ftp_list[cfl]['download_path'])

                        # 回饋檔
                        if (operator.eq('feedback_files', download_file_type)):
                            folderList = sftp.listdir(ticket_host_path)
                            for folder in folderList:
                                if not(folder.startswith("BLKLIST")):
                                    self.mkdirs(os.path.join(download_path, folder))
                                    fileList = sftp.listdir(ticket_host_path + folder)
                                    for file in fileList:
                                        if(file.startswith("TXNR_PARK_") and file.endswith(".CSV")):
                                            if not os.path.exists(os.path.join(download_path, folder, file)):
                                                sftp.get(ticket_host_path + folder + "/" + file, os.path.join(download_path, folder, file))
                                                shutil.copyfile(os.path.join(download_path, folder, file), os.path.join(feedback_files_import_db_path, folder, file))
                        # 黑名單
                        elif (operator.eq('black_list', download_file_type)):
                            fileList = sftp.listdir(ticket_host_path)
                            for file in fileList:
                                if(file.startswith("BLKLIST") and file.endswith(".DAT")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        sftp.get(ticket_host_path + file, os.path.join(download_path, file))
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                        
                        sftp.close()
                        client.close()
                    except Exception as e:
                        print('Error:%s'% (e) )
        return "download"
        
    """ 取得檔名流水號 """ 
    def get_file_seq(self, generated_dat_backup_path, source_id, happycash_garage_code):
        file_seq = 0
        if os.path.isdir(generated_dat_backup_path):
            # 算今天產了幾個檔，同一天不能重複序號
            for root,dirs,files in os.walk(generated_dat_backup_path):
                for each in files:
                    if(each.startswith(f'TXN_PARK_{source_id}_{happycash_garage_code}')):
                        file_seq += 1 
        return file_seq

    """ 讀取未包檔前檔案內容 """ 
    def open_files(self, file_path, file):
        content = ""
        with open(os.path.join(file_path, file), 'rb') as TXN_file:
            content = TXN_file.read().strip()
        return content

    """ header處理 """ 
    def add_header(self, content, file_seq):
        # 交易筆數
        data_count = (len(content)-66)/467
        # {:02x}就是以16進制輸出一個字符的ascii碼，而且\x後面一定佔兩位，不足兩位前面補0
        content_16 = ":".join("{:02x}".format(c) for c in content)
        content_array = content_16.split(":")
        total_amt_count = 0

        if data_count>0 and data_count.is_integer():
            for i in range(int(data_count)):
                # body的160,161
                # 各筆交易金額加總
                total_amt_count = total_amt_count + self.unit_amt((content_array[66+160+467*i-1]).replace('dc', ''), (content_array[66+161+467*i-1]).replace('dc', ''))
            content = self.replace_header_data(total_amt_count, data_count+1, content, file_seq)
        else:
            print (f'交易檔長度不對')
        return content

    """ 計算交易金額 """ 
    def unit_amt(self, no_160, no_161):
        unit_amt = 0
        unit_amt = int(no_161 + no_160, 16)
        return unit_amt

    """ 更改header內容 """ 
    def replace_header_data(self, total_amt_count, data_count, content, file_seq):
        total_amt_count = self.add_zero(12, total_amt_count)
        #總筆數
        data_count = self.add_zero(10, int(data_count))
        file_seq = self.add_zero(6, file_seq)
        data_count_byte = str.encode(data_count)
        file_seq_byte = str.encode(file_seq)
        total_amt_count_byte = str.encode(total_amt_count)
        content_after_excute = content[:10] + file_seq_byte + data_count_byte + total_amt_count_byte + content[38:]
        return content_after_excute

    """ 字數不足前方補0 """ 
    def add_zero(self, count, value):
        return(str(value).zfill(count))

    """ 產生包檔後交易檔 """ 
    def generate_dat_file(self, file_name, content, garage_code, generated_dat_path, generated_dat_backup_path, dat_files_go_zip_path, dat_files_import_db_path):  
        p = generated_dat_path + "/" + file_name.strip()
        a = str(file_name)
        with open(os.path.join(generated_dat_path, garage_code, file_name) , 'wb') as file_new:
            file_new.write(content)
        shutil.copyfile(os.path.join(generated_dat_path, garage_code, file_name), os.path.join(dat_files_go_zip_path, file_name))	
        shutil.copyfile(os.path.join(generated_dat_path, garage_code, file_name), os.path.join(generated_dat_backup_path, file_name))	
        shutil.copyfile(os.path.join(generated_dat_path, garage_code, file_name), os.path.join(dat_files_import_db_path, file_name))

    """ 場站交易檔全部放進壓縮檔 """
    def pack_all_in_one(self, dat_files_go_zip_path, dat_files_go_zip_backup_path, zf):
        # 場站交易檔放入壓縮檔
        for root, folders, files in os.walk(dat_files_go_zip_path):
            for sfile in files:
                aFile = os.path.join(root, sfile)

                zf.write(aFile, os.path.basename(sfile))
                shutil.copyfile(aFile, os.path.join(dat_files_go_zip_backup_path, sfile))

    """ 取得ZIP檔名流水號 """
    def get_zip_file_no_num(self, generated_zip_backup_path):
        zip_file_no_num = 51
        if os.path.exists(generated_zip_backup_path):
            filelist = os.listdir(generated_zip_backup_path)
            for file in filelist:
                if file.endswith(".ZIP"):
                    zip_file_no_num += 1
        zip_file_no_num = self.add_zero(3, zip_file_no_num)
        return zip_file_no_num

    """ 建立.OK檔案 """
    def create_OK_file(self, zip_file_name):
        file = open(f'{zip_file_name}.OK', 'w') 
        file.close()

    """ 建立多層目錄 """
    def mkdirs(self, path): 
        # 去除前方空格
        path = path.strip()
        # 去除尾巴 \ 符號
        path = path.rstrip("\\")

        # 判斷路徑是否存在
        # 存在     True
        # 不存在   False
        isExists = os.path.exists(path)
    
        # 判断结果
        if not isExists:
            # 建立目錄
            os.makedirs(path)
            # 如果不存在則建立目錄
            return True
        else:
            # 如果目錄存在則不建立
            return False

    def byte_to_str(self, bytes, order=0):
        """ 
            transfer bin > hex > ascii
            @param byte: convert target
            return convert to str
        """
        str1 = ''
        if order == 1:
            for i in bytes:
                str1 += hex(i).replace('0x','').zfill(2)
        else:
            for i in bytes[::-1]:
                # remove hex prefix"0x"
                str1 += hex(i).replace('0x','').zfill(2)
            str1 = 0 if str1.strip('0') == '' else int(str1,16)
        return str1

    """ 交易檔匯入資料庫 """
    async def data_import_db(self, zip_file_name, garage_code_list, dat_files_import_db_path, dat_files_import_db_backup_path):
        data = {}

        for root, folders, files in os.walk(dat_files_import_db_path):
            for sfile in files:
                if(sfile.startswith("TXN_PARK_") and sfile.endswith(".DAT")):
                    aFile = os.path.join(root, sfile)

                    content = open(aFile, 'rb')
                    content.seek(66, 0)
                    parse_data = content.read()
                    file_len = os.path.getsize(aFile) - 66
                    loop_time = int(file_len / 467)
                    for count in range(0, loop_time):
                        times = 467 * count       
                        unix_time = self.byte_to_str(parse_data[152 + times : 156 + times])
                        trx_date = datetime.datetime.utcfromtimestamp(unix_time)

                        data['file_name'] = sfile
                        data['trx_date'] = str(trx_date)[0 : 10].replace('-','')
                        data['trx_time'] = str(trx_date)[11 :].replace(':','')
                        data['card_no'] = self.byte_to_str(parse_data[384 + times : 392 + times],1)
                        data['txn_no'] = self.byte_to_str(parse_data[150 + times : 152 + times])
                        data['trx_amt'] = self.byte_to_str(parse_data[159 + times : 161 + times])
                        data['device_id'] = self.decimal_to_hex(self.byte_to_str(parse_data[165 + times : 169 + times]), 8)
                        data['trx_type'] = self.decimal_to_hex(self.byte_to_str(parse_data[156 + times : 157 + times]), 2)
                        data['el_value'] = self.byte_to_str(parse_data[161 + times : 163 + times])
                        # data['cal_date'] = 
                        # data['cal_status'] = 
                        # data['cal_err_code'] = 
                        # data['trx_sub_type'] = 
                        data['garage_code'] = garage_code_list.get(sfile[12:27])
                        data['upload_zip_name'] = zip_file_name
                        async with self._db.acquire() as conn: 
                            trans = await conn.begin()
                            try:
                                rz =  await conn.execute(Trx_Data.insert().values(data))
                            except Exception as e:
                                print('有錯: ',e)
                                await trans.rollback()
                                raise
                            else:
                                await trans.commit()
                    content.close()
                    shutil.move(aFile, os.path.join(dat_files_import_db_backup_path, sfile))

    """ decimal 轉 hexadecmial """
    def decimal_to_hex(self, value, count):
        hex_value = 0
        hex_value= ('{:02x}'.format(int(value))).upper()
        return hex_value.zfill(count)

    """ 回饋檔匯入資料庫 """
    async def feedback_data_import_db(self):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql_customer = f"""SELECT distinct 
        a.customer_id, 
        b.customer_code 
        FROM 
        `ticket_transaction_ftp_config` AS a 
        LEFT JOIN 
        `customer` AS b 
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.card_type = '05' AND 
        a.status = 1"""

        async with self._db.acquire() as conn: 
            customer_list_query = await conn.execute(sql_customer)
            if customer_list_query.rowcount > 0:
                customer_list = [dict(row.items()) async for row in customer_list_query]
                for cl in range(0, customer_list_query.rowcount):          
                    # 回饋檔匯入資料庫
                    feedback_files_import_db_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "feedback_files_import_db")
                    self.mkdirs(feedback_files_import_db_path)
                    # 回饋檔匯入資料庫備份
                    feedback_files_import_db_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "feedback_files_import_db_backup", self._now_date, "TXNR")
                    self.mkdirs(feedback_files_import_db_backup_path)                    

                    data = {}
                    for root, folders, files in os.walk(feedback_files_import_db_path):
                        for sfile in files:
                            if(sfile.startswith("TXNR_PARK_") and sfile.endswith(".CSV")):
                                # Windows 測試
                                # root_split = root.split("\\")
                                # 正式環境
                                root_split = root.split("/")

                                self.mkdirs(os.path.join(feedback_files_import_db_backup_path, root_split[len(root_split)-1]))

                                aFile = os.path.join(root, sfile)

                                csvfile = open(aFile, 'r', encoding = 'big5')
                                spamreader = csv.DictReader(csvfile)
                                for row in spamreader:
                                    # where 條件
                                    # data['file_name'] = row['小檔名稱']
                                    # where 條件
                                    # data['trx_date'] = str(row['交易日']).replace("/", "")
                                    # where 條件
                                    # data['trx_time'] = str(row['交易時間']).replace(":", "")
                                    # where 條件
                                    # data['card_no'] = row['卡號']
                                    # where 條件
                                    # data['txn_no'] = row['卡片交易序號']
                                    # where 條件
                                    # data['trx_amt'] = row['交易金額']
                                    # where 條件
                                    # data['device_id'] = row['設備號碼']
                                    # where 條件
                                    # data['trx_type'] = row['交通交易類型']
                                    # where 條件
                                    # data['el_value'] = row['交易後餘額']
                                    data['cal_date'] = row['清算日']
                                    data['cal_status'] = self.check_cal_status(row['遠鑫處理回覆碼'])
                                    data['cal_err_code'] = row['遠鑫處理回覆碼']
                                    # data['trx_sub_type'] = 
                                    # data['garage_code'] = 
                                    # data['upload_zip_name'] = 
                                    data['feedback_file_name'] = sfile

                                    trans = await conn.begin()
                                    try:
                                        rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.file_name == row['小檔名稱']).where(Trx_Data.c.trx_date == str(row['交易日']).replace("/", "")).where(Trx_Data.c.trx_time == str(row['交易時間']).replace(":", "")).where(Trx_Data.c.card_no == row['卡號']).where(Trx_Data.c.txn_no == row['卡片交易序號'][-2:]).where(Trx_Data.c.trx_amt == row['交易金額']).where(Trx_Data.c.device_id == row['設備號碼']).where(Trx_Data.c.trx_type == row['交通交易類型']).where(Trx_Data.c.el_value ==  row['交易後餘額']))
                                    except Exception as e:
                                        print('有錯: ',e)
                                        await trans.rollback()
                                        raise
                                    else:
                                        await trans.commit()
                                csvfile.close()
                                shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, root_split[len(root_split)-1], sfile))

    """ 遠鑫處理回覆碼 """
    def check_cal_status(self, data):
        cal_status = ""
        # 無錯誤
        if (operator.eq(data, "00")):
            cal_status = "F"
        else:
            cal_status = "E"
        return cal_status

    """ 新增場站參數 """
    async def happycash_insert_garage_parameter(self, data: dict, garage_code, customer_id, create_user_id):
        sql = "SELECT `garage_id` FROM `garage` WHERE garage_code = :garage_code"
        async with self._db.acquire() as conn:
            garage_id_query = await conn.execute(text(sql), {'garage_code':garage_code})
            if garage_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in garage_id_query]

                data['customer_id'] = customer_id
                data['garage_id'] = result[0]['garage_id']
                data['create_user_id'] = create_user_id
                data['create_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(HappyCashConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 刪除場站參數 """
    async def happycash_delete_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(HappyCashConfig.delete().where(HappyCashConfig.c.garage_id == garage_id))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新場站參數 (有啟用票種) """
    async def happycash_update_garage_parameter_enabled_status(self, data: dict, garage_id: int, customer_id, user_id):
        sql = "SELECT * FROM `happycash_config` WHERE garage_id = :garage_id"
        async with self._db.acquire() as conn:
            garage_id_query = await conn.execute(text(sql), {'garage_id':garage_id})
            if garage_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in garage_id_query]

                data['customer_id'] = customer_id
                data['garage_id'] = garage_id
                data['last_update_user_id'] = user_id
                data['last_update_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(HappyCashConfig.update().values(data).where(HappyCashConfig.c.garage_id == garage_id))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()
            elif(garage_id_query.rowcount == 0):
                data['customer_id'] = customer_id
                data['garage_id'] = garage_id
                data['create_user_id'] = user_id
                data['create_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(HappyCashConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢場站參數 """
    async def happycash_query_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            result = await conn.execute(HappyCashConfig.select().where(HappyCashConfig.c.garage_id == garage_id))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]

    """ 更新場站參數 (未啟用票種) """
    async def happycash_update_garage_parameter_disabled_status(self, garage_id: int, customer_id, update_user_id):
        sql = "SELECT * FROM `happycash_config` WHERE garage_id = :garage_id"
        async with self._db.acquire() as conn:
            garage_id_query = await conn.execute(text(sql), {'garage_id':garage_id})
            if garage_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in garage_id_query]

                data = {}
                data['customer_id'] = customer_id
                data['garage_id'] = garage_id
                data['status'] = 0
                data['last_update_user_id'] = update_user_id
                data['last_update_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(HappyCashConfig.update().values(data).where(HappyCashConfig.c.garage_id == garage_id))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 新增業者參數 """
    async def happycash_insert_customer_parameter(self, data: dict, customer_code, create_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT `customer_id` FROM `customer` WHERE customer_code = :customer_code"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_code':customer_code})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = result[0]['customer_id']
                data['card_type'] = '05'
                data['create_user_id'] = create_user_id
                data['create_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 刪除業者參數 """
    async def happycash_delete_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(TicketTransactionFtpConfig.delete().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "05"))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新業者參數 (有啟用票種) """
    async def happycash_update_customer_parameter_enabled_status(self, data: dict, customer_id: int, user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '05'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = customer_id
                data['last_update_user_id'] = user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '05'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "05"))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()
            elif(customer_id_query.rowcount == 0):
                data['customer_id'] = customer_id
                data['create_user_id'] = user_id
                data['create_time'] = datetime.datetime.now()
                data['card_type'] = '05'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 更新業者參數 (未啟用票種) """
    async def happycash_update_customer_parameter_disabled_status(self, customer_id: int, update_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '05'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data = {}
                data['customer_id'] = customer_id
                data['status'] = 0
                data['last_update_user_id'] = update_user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '05'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "05"))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢業者參數 """
    async def happycash_query_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            result = await conn.execute(TicketTransactionFtpConfig.select().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "05"))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]