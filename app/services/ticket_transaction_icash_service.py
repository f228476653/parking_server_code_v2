import time, datetime
from sqlalchemy import desc,text
import os,glob,sys
import zipfile
import shutil
import ftplib
from app.config.models import Trx_Data, ICashConfig, TicketTransactionFtpConfig
import operator
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.config.models import Account

class TicketTransactionICashService:
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
        self._file_directory_path = "D:\\test_use"
        # 正式環境
        # self._file_directory_path = "/home/pms_plus/file_directory/"
        self._process_path = os.path.join(self._file_directory_path, "ticket_transaction_files")
        self._card_type = "icash"
        self._now_date = datetime.date.today().strftime("%Y%m%d")
        self._user = user

    """ 場站交易檔包進壓縮檔 """
    async def pack(self, location):
        sql_customer = f"""SELECT distinct 
        a.customer_id, 
        a.icash_customer_tax_id,
        b.customer_code
        FROM 
        `ticket_transaction_ftp_config` AS a 
        LEFT JOIN 
        `customer` AS b 
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.status = 1 
        and a.card_type = '02'"""

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
                    `icash_config` AS a 
                    LEFT JOIN 
                    `customer` AS b 
                    ON 
                    a.customer_id = b.customer_id
                    LEFT JOIN 
                    `garage` AS c
                    ON 
                    a.garage_id = c.garage_id
                    WHERE 
                    a.status = 1 and 
                    a.customer_id = :customer_id"""

                    garage_list_count = await conn.execute(text(sql_garage), {'customer_id':str(customer_list[cl]['customer_id'])})
                    if garage_list_count.rowcount >0:
                        garage_code_list = {}

                        # 檔案上傳位置
                        upload_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "upload")
                        self.mkdirs(upload_path)

                        """ 門市主檔相關 BEGIN """
                        # 門市主檔檔名
                        ICMS_dat_name = "ICMS-" + str(customer_list[cl]['icash_customer_tax_id']) + "-" + self._now_date + ".dat"
                        ICMS_FILEOK_name = "ICMS-" + str(customer_list[cl]['icash_customer_tax_id']) + "-" + self._now_date + ".FILEOK"

                        ICMS_dat_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "ICMS_dat_path")
                        # 移除門市主檔資料夾及底下的檔案 (之後重新建立資料夾)
                        if os.path.isdir(ICMS_dat_path):
                            shutil.rmtree(ICMS_dat_path)
                        self.mkdirs(ICMS_dat_path)

                        ICMS_dat_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "ICMS_dat_backup_path", self._now_date)
                        self.mkdirs(ICMS_dat_backup_path)

                        # 開啟門市主檔寫檔 
                        ICMS_dat_output = open(os.path.join(ICMS_dat_path, ICMS_dat_name), 'w', encoding ='big5')
                        """ 門市主檔相關 END """

                        """ 場站壓縮檔全部放進壓縮檔 BEGIN """
                        generated_zip_all_in_one_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip_all_in_one_backup", self._now_date)
                        self.mkdirs(generated_zip_all_in_one_backup_path)

                        # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                        generated_zip_all_in_one_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip_all_in_one")
                        if os.path.isdir(generated_zip_all_in_one_path):
                            shutil.rmtree(generated_zip_all_in_one_path)
                        self.mkdirs(generated_zip_all_in_one_path)

                        # zip檔名、流水號
                        all_in_one_file_name = "ICTX-" + str(customer_list[cl]['icash_customer_tax_id']) + "-" + self._now_date + "-01"
                        zip_all_in_one_file_name = all_in_one_file_name + ".zip"
                        zip_all_in_one_FILEOK_name = all_in_one_file_name + ".FILEOK"

                        zip_all_in_one_file_path = os.path.join(generated_zip_all_in_one_path, zip_all_in_one_file_name)
                        zip_all_in_one_FILEOK_path = os.path.join(generated_zip_all_in_one_path, zip_all_in_one_FILEOK_name)

                        # 開啟場站壓縮檔全部放進壓縮檔寫檔 
                        zf_all_in_one = zipfile.ZipFile(zip_all_in_one_file_path, "w")
                        """ 場站壓縮檔全部放進壓縮檔 END """


                        # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                        generated_zip_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip")
                        if os.path.isdir(generated_zip_path):
                            shutil.rmtree(generated_zip_path)
                        self.mkdirs(generated_zip_path)

                        # 交易檔匯入資料庫
                        dat_files_import_db_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_import_db")
                        self.mkdirs(dat_files_import_db_path)
                        # 交易檔匯入資料庫備份
                        dat_files_import_db_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_import_db_backup", self._now_date)
                        self.mkdirs(dat_files_import_db_backup_path)

                        garage_list = [dict(row.items()) async for row in garage_list_count]
                        for gl in range(0, garage_list_count.rowcount):
                            # 場站代碼List
                            garage_code_list[str(garage_list[gl]['garage_code'])] = str(garage_list[gl]['garage_code'])

                            """ 場站交易檔放入場站壓縮檔 BEGIN"""
                            # device_ftp_path
                            device_ftp_path = os.path.join(self._directory_path, location, str(garage_list[gl]['customer_code']), str(garage_list[gl]['garage_code']), "transaction_files")
                            self.mkdirs(device_ftp_path)

                            # 交易檔匯入資料庫 (場站資料夾)
                            dat_files_import_db_garage_code_path = os.path.join(dat_files_import_db_path, str(garage_list[gl]['garage_code']))
                            self.mkdirs(dat_files_import_db_garage_code_path)

                            self.mkdirs(os.path.join(generated_zip_path, str(garage_list[gl]['garage_code']), str(garage_list[gl]['icash_garage_code'])))

                            generated_zip_backup_path = os.path.join(self._process_path, str(garage_list[gl]['customer_code']), self._card_type, "generated_zip_backup", self._now_date, str(garage_list[gl]['garage_code']), str(garage_list[gl]['icash_garage_code']))
                            self.mkdirs(generated_zip_backup_path)
                            files_from_device_path = os.path.join(self._process_path, str(garage_list[gl]['customer_code']), self._card_type, "files_from_device", self._now_date, str(garage_list[gl]['garage_code']))
                            self.mkdirs(files_from_device_path)

                            now_datetime = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                            zip_file_name = "STTX-" + now_datetime + ".zip"
                            zip_FILEOK_name = "STTX-" + now_datetime + ".FILEOK"

                            zip_file_path = os.path.join(generated_zip_path, str(garage_list[gl]['garage_code']), str(garage_list[gl]['icash_garage_code']), zip_file_name)
                            zip_FILEOK_path = os.path.join(generated_zip_path, str(garage_list[gl]['garage_code']), str(garage_list[gl]['icash_garage_code']), zip_FILEOK_name)

                            zf = zipfile.ZipFile(zip_file_path, "w")
                            for root, folders, files in os.walk(device_ftp_path):
                                for sfile in files:
                                    if(sfile.startswith("ICTX2LOG")):
                                        # Windows 測試
                                        root_split = root.split("\\")
                                        # 正式環境
                                        # root_split = root.split("/")

                                        aFile = os.path.join(root, sfile)
                                        zf.write(aFile, os.path.basename(sfile))
                                        shutil.copyfile(aFile, os.path.join(dat_files_import_db_garage_code_path, sfile))

                                        # device 設備資料夾
                                        self.mkdirs(os.path.join(files_from_device_path, root_split[len(root_split)-1]))
                                        shutil.move(aFile, os.path.join(files_from_device_path, root_split[len(root_split)-1], sfile))
                            zf.close()

                            # FILEOK內容為檔案的大小
                            zip_FILEOK_output = open(os.path.join(zip_FILEOK_path), 'w', encoding = 'utf8')
                            zip_FILEOK_output.write(str(os.path.getsize(zip_file_path)))
                            zip_FILEOK_output.close()

                            shutil.copyfile(zip_file_path, os.path.join(generated_zip_backup_path, zip_file_name))
                            shutil.copyfile(zip_FILEOK_path, os.path.join(generated_zip_backup_path, zip_FILEOK_name))
                            """ 場站交易檔放入場站壓縮檔 END """

                            """ 門市主檔寫檔 """
                            self.create_ICMS(garage_list[gl], ICMS_dat_output)
                    

                        """ 場站壓縮檔全部放進壓縮檔 & 檔案移動 & 備份處理 BEGIN """
                        # 場站壓縮檔全部放進壓縮檔寫檔
                        self.pack_all_in_one(os.path.join(generated_zip_path), zf_all_in_one)
                        zf_all_in_one.close()

                        if os.path.exists(os.path.join(zip_all_in_one_file_path)):
                            zip_all_in_one_FILEOK_output = open(os.path.join(zip_all_in_one_FILEOK_path), 'w', encoding = 'utf8')
                            zip_all_in_one_FILEOK_output.write(str(os.path.getsize(zip_all_in_one_file_path)))
                            zip_all_in_one_FILEOK_output.close()

                            shutil.copyfile(zip_all_in_one_file_path, os.path.join(generated_zip_all_in_one_backup_path, zip_all_in_one_file_name))
                            shutil.copyfile(zip_all_in_one_FILEOK_path, os.path.join(generated_zip_all_in_one_backup_path, zip_all_in_one_FILEOK_name))
                            shutil.copyfile(zip_all_in_one_file_path, os.path.join(upload_path, zip_all_in_one_file_name))
                            shutil.copyfile(zip_all_in_one_FILEOK_path, os.path.join(upload_path, zip_all_in_one_FILEOK_name))
                        """ 場站壓縮檔全部放進壓縮檔 & 檔案移動 & 備份處理  END """

                        """ 門市主檔FILEOK檔製作 & 檔案移動 & 備份處理 BEGIN """
                        # 門市主檔寫檔完成，關閉檔案
                        ICMS_dat_output.close()

                        # FILEOK內容為檔案的大小
                        if os.path.exists(os.path.join(ICMS_dat_path, ICMS_dat_name)):
                            ICMS_FILEOK_output = open(os.path.join(ICMS_dat_path, ICMS_FILEOK_name), 'w', encoding = 'utf8')
                            ICMS_FILEOK_output.write(str(os.path.getsize(os.path.join(ICMS_dat_path, ICMS_dat_name))))
                            ICMS_FILEOK_output.close()

                            shutil.copyfile(os.path.join(ICMS_dat_path, ICMS_dat_name), os.path.join(ICMS_dat_backup_path, ICMS_dat_name))
                            shutil.copyfile(os.path.join(ICMS_dat_path, ICMS_FILEOK_name), os.path.join(ICMS_dat_backup_path, ICMS_FILEOK_name))

                            shutil.copyfile(os.path.join(ICMS_dat_path, ICMS_dat_name), os.path.join(upload_path, ICMS_dat_name))
                            shutil.copyfile(os.path.join(ICMS_dat_path, ICMS_FILEOK_name), os.path.join(upload_path, ICMS_FILEOK_name))
                        """ 門市主檔FILEOK檔製作 & 檔案移動 & 備份處理 END """
                    
                        """ 票證交易資料匯入資料庫 BEGIN """
                        await self.data_import_db(zip_all_in_one_file_name, garage_code_list, dat_files_import_db_path, dat_files_import_db_backup_path)
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
        a.card_type ='02'"""

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
                        ftp_connection = ftplib.FTP()
                        ftp_connection.connect(str(customer_ftp_list[cfl]['ip_address']), int(customer_ftp_list[cfl]['ip_port']))
                        ftp_connection.login(str(customer_ftp_list[cfl]['account']), str(customer_ftp_list[cfl]['password']))

                        ticket_host_path = str(customer_ftp_list[cfl]['upload_path'])
                        ftp_connection.cwd(ticket_host_path)

                        # 交易檔
                        for root, folders, files in os.walk(upload_path):
                            for sfile in files:
                                if(sfile.startswith("ICTX-")):
                                    aFile = os.path.join(root, sfile)

                                    data = {}
                                    data['cal_status'] = "C"
                                    # where 條件
                                    # data['upload_zip_name'] = sfile
                                    ftp_connection.storbinary(f'STOR %s'%sfile, open(aFile, 'rb'))
                                    shutil.move(aFile, os.path.join(upload_backup_path, sfile))
                                    if (sfile.endswith(".zip")):
                                        trans = await conn.begin()
                                        try:
                                            rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.upload_zip_name == sfile))
                                        except Exception as e:
                                            print('有錯: ',e)
                                            await trans.rollback()
                                            raise
                                        else:
                                            await trans.commit()

                        # 門市主檔
                        for root, folders, files in os.walk(upload_path):
                            for sfile in files:
                                if(sfile.startswith("ICMS-")):
                                    aFile = os.path.join(root, sfile)
                                    ftp_connection.storbinary(f'STOR %s'%sfile, open(aFile, 'rb'))
                                    shutil.move(aFile, os.path.join(upload_backup_path, sfile))
                        
                        ftp_connection.close()
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
        a.status = 1 
        and a.card_type ='02'"""

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
                    customer_download_black_list_path = os.path.join(self._directory_path, location, str(customer_ftp_list[cfl]['customer_code']), "iCash.bl")
                    self.mkdirs(customer_download_black_list_path)

                    try:
                        ftp_connection = ftplib.FTP()
                        ftp_connection.connect(str(customer_ftp_list[cfl]['ip_address']), int(customer_ftp_list[cfl]['ip_port']))
                        ftp_connection.login(str(customer_ftp_list[cfl]['account']), str(customer_ftp_list[cfl]['password']))

                        ticket_host_path = str(customer_ftp_list[cfl]['download_path'])
                        ftp_connection.cwd(ticket_host_path)

                        # 回饋檔 & 剔退檔
                        if (operator.eq('feedback_files', download_file_type)):
                            fileList = ftp_connection.nlst()
                            for file in fileList:
                                if(file.startswith("ICSD") and file.endswith(".dat")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        ftp_connection.retrbinary('RETR %s'%file, open(os.path.join(download_path, file), "wb").write)
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(feedback_files_import_db_path, file))
                                elif(file.startswith("ICDC") and file.endswith(".dat")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        ftp_connection.retrbinary('RETR %s'%file, open(os.path.join(download_path, file), "wb").write)
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(feedback_files_import_db_path, file))
                        # 黑名單
                        elif (operator.eq('black_list', download_file_type)):
                            fileList = ftp_connection.nlst()
                            for file in fileList:
                                if(file.startswith("ICBL") and file.endswith(".zip")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        ftp_connection.retrbinary('RETR %s'%file, open(os.path.join(download_path, file), "wb").write)
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                        
                        ftp_connection.close()
                    except Exception as e:
                        print('Error:%s'% (e) )
        return "download"

    """ 場站壓縮檔全部放進壓縮檔 """
    def pack_all_in_one(self, generated_zip_path, zf_all_in_one):
        # 場站交易檔放入壓縮檔
        for root, folders, files in os.walk(generated_zip_path):
            for sfile in files:
                # Windows 測試
                root_split = root.split("\\")
                # 正式環境
                # root_split = root.split("/")

                aFile = os.path.join(root, sfile)
                zf_all_in_one.write(aFile, os.path.join(root_split[len(root_split)-1], sfile))


    """ 門市主檔寫檔 """
    # 特定字 Big5 編碼會有問題，導致寫檔失敗，例：碁
    def create_ICMS(self, data, ICMS_dat_output):
        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_code']), 8)))
        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_name']), 30)))

        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_abbreviated_name']), 10)))
        ICMS_dat_output.write(str(self.add_space((str(data['icash_garage_effective_begin_date']).replace("-","")), 8)))
        ICMS_dat_output.write(str(self.add_space((str(data['icash_garage_effective_end_date']).replace("-","")), 8)))

        ICMS_dat_output.write(str(self.add_space((str(data['icash_garage_opening_day']).replace("-","")), 8)))
        ICMS_dat_output.write(str(self.add_space((str(data['icash_garage_saleable_day']).replace("-","")), 8)))
        ICMS_dat_output.write(str(self.add_space((str(data['icash_garage_closing_day']).replace("-","")), 8)))

        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_postal_code']), 8)))
        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_address']), 60)))
        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_telephone_area_code']), 3)))

        ICMS_dat_output.write(str(self.add_space(str(data['icash_garage_telephone']), 12)))
        ICMS_dat_output.write("\n")

    """ 算字元長度，補齊需要的空白數 """
    def add_space(self, value, number):
        length = len(value)
        utf8_length = len(value.encode('utf-8'))
        length = (utf8_length - length)/2 + length
        return value + ("").ljust(number - int(length))

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

    """ 交易檔匯入資料庫 """
    async def data_import_db(self, zip_all_in_one_file_name, garage_code_list, dat_files_import_db_path, dat_files_import_db_backup_path):
        data = {}
        for root, folders, files in os.walk(dat_files_import_db_path):
            for sfile in files:
                # Windows 測試
                root_split = root.split("\\")
                # 正式環境
                # root_split = root.split("/")

                self.mkdirs(os.path.join(dat_files_import_db_backup_path, garage_code_list.get(root_split[len(root_split)-1])))

                aFile = os.path.join(root, sfile)

                content = open(aFile, 'r', encoding = "utf8")
                for line in content.readlines():
                    if len(line) == 328:
                        data['file_name'] = sfile
                        data['trx_date'] = line[25:33]
                        data['trx_time'] = line[33:39]
                        data['card_no'] = line[63:79]
                        data['txn_no'] = line[19:25]
                        data['trx_amt'] = line[79:87]
                        data['device_id'] = line[87:107]
                        data['trx_type'] = line[39:41]
                        # data['el_value'] = 
                        # data['cal_date'] = 
                        # data['cal_status'] = 
                        # data['cal_err_code'] = 
                        # data['trx_sub_type'] = 
                        data['garage_code'] = garage_code_list.get(root_split[len(root_split)-1])
                        data['upload_zip_name'] = zip_all_in_one_file_name
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
                shutil.move(aFile, os.path.join(dat_files_import_db_backup_path, garage_code_list.get(root_split[len(root_split)-1]), sfile))

    """ 回饋檔、剔退檔匯入資料庫 """
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
        a.card_type = '02' 
        AND a.status = 1"""
        
        async with self._db.acquire() as conn: 
            customer_list_query = await conn.execute(sql_customer)
            if customer_list_query.rowcount > 0:
                customer_list = [dict(row.items()) async for row in customer_list_query]
                for cl in range(0, customer_list_query.rowcount):          
                    # 回饋檔、剔退檔匯入資料庫
                    feedback_files_import_db_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "feedback_files_import_db")
                    self.mkdirs(feedback_files_import_db_path)
                    # 回饋檔、剔退檔匯入資料庫備份
                    feedback_files_import_db_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "feedback_files_import_db_backup", self._now_date)
                    self.mkdirs(feedback_files_import_db_backup_path)

                    data = {}
                    icash_garage_code_to_garage_code_list = await self.icash_garage_code_to_garage_code_list(str(customer_list[cl]['customer_id']))

                    # 剔退檔
                    for root, folders, files in os.walk(feedback_files_import_db_path):
                        for sfile in files:
                            if(sfile.startswith("ICDC-") and sfile.endswith(".dat")):
                                aFile = os.path.join(root, sfile)

                                content = open(aFile, 'r', encoding = "utf8")
                                for line in content.readlines():
                                    if len(line) == 130:
                                        # data['file_name'] = 
                                        # where 條件
                                        # data['trx_date'] = line[37:45]
                                        # where 條件
                                        # data['trx_time'] = line[45:51]
                                        # where 條件
                                        # data['card_no'] = line[75:91]
                                        # data['txn_no'] = 
                                        # where 條件
                                        # data['trx_amt'] = int(line[91:99])
                                        # data['device_id'] = 
                                        # where 條件
                                        # data['trx_type'] = line[51:53]
                                        # data['el_value'] = 
                                        data['cal_date'] = line[0:8]
                                        data['cal_status'] = "E"
                                        data['cal_err_code'] = line[8:12]
                                        # data['trx_sub_type'] = 
                                        # where 條件
                                        # data['garage_code'] = icash_garage_code_to_garage_code_list.get(line[20:28].strip())
                                        # data['upload_zip_name'] = 
                                        data['feedback_file_name'] = sfile

                                        trans = await conn.begin()
                                        try:
                                            rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.trx_date == line[37:45]).where(Trx_Data.c.trx_time == line[45:51]).where(Trx_Data.c.card_no == line[75:91]).where(Trx_Data.c.trx_amt == int(line[91:99])).where(Trx_Data.c.trx_type == line[51:53]).where(Trx_Data.c.garage_code == icash_garage_code_to_garage_code_list.get(line[20:28].strip())))
                                        except Exception as e:
                                            print('有錯: ',e)
                                            await trans.rollback()
                                            raise
                                        else:
                                            await trans.commit()
                                content.close()
                                shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, sfile))

                    # 回饋檔
                    for root, folders, files in os.walk(feedback_files_import_db_path):
                        for sfile in files:
                            if(sfile.startswith("ICSD-") and sfile.endswith(".dat")):
                                aFile = os.path.join(root, sfile)

                                content = open(aFile, 'r', encoding = "utf8")
                                for line in content.readlines():
                                    if len(line) == 76:
                                        # data['file_name'] = 
                                        # where 條件
                                        # data['trx_date'] = line[41:49]
                                        # where 條件
                                        # data['trx_time'] = line[49:55]
                                        # where 條件
                                        # data['card_no'] = line[19:35]
                                        # data['txn_no'] = 
                                        # where 條件
                                        # data['trx_amt'] = line[57:65].strip()
                                        # data['device_id'] = 
                                        # where 條件
                                        # data['trx_type'] = line[55:57]
                                        # data['el_value'] = 
                                        data['cal_date'] = line[0:8]
                                        data['cal_status'] = "F"
                                        data['cal_err_code'] = ""
                                        # data['trx_sub_type'] = 
                                        # where 條件
                                        # data['garage_code'] = icash_garage_code_to_garage_code_list.get(line[8:16].strip())
                                        # data['upload_zip_name'] = 
                                        data['feedback_file_name'] = sfile

                                        trans = await conn.begin()
                                        try:
                                            rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.trx_date == line[41:49]).where(Trx_Data.c.trx_time == line[49:55]).where(Trx_Data.c.card_no == line[19:35]).where(Trx_Data.c.trx_amt == line[57:65].strip()).where(Trx_Data.c.trx_type == line[55:57]).where(Trx_Data.c.garage_code == icash_garage_code_to_garage_code_list.get(line[8:16].strip())))
                                        except Exception as e:
                                            print('有錯: ',e)
                                            await trans.rollback()
                                            raise
                                        else:
                                            await trans.commit()
                                content.close()
                                shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, sfile))

    """ 門市對照碼對應 AcerITS場站代碼 """
    async def icash_garage_code_to_garage_code_list(self, customer_id):
        data = {}
        sql_icash_garage_code_list = f"""SELECT 
        a.icash_garage_code, 
        b.garage_code 
        FROM 
        `icash_config` AS a
        LEFT JOIN
        `garage` AS b
        ON
        a.garage_id = b.garage_id 
        WHERE 
        a.status = 1 and 
        a.customer_id = :customer_id'"""
        async with self._db.acquire() as conn: 
            icash_garage_code_list_query = await conn.execute(text(sql_icash_garage_code_list), {'customer_id':customer_id})
            if icash_garage_code_list_query.rowcount > 0:
                icash_garage_code_list = [dict(row.items()) async for row in icash_garage_code_list_query]
                for igcl in range(0, icash_garage_code_list_query.rowcount):
                    data[str(icash_garage_code_list[igcl]['icash_garage_code'])] = str(icash_garage_code_list[igcl]['garage_code'])
        return data

    """ 新增場站參數 """
    async def icash_insert_garage_parameter(self, data: dict, garage_code, customer_id, create_user_id):
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
                    rz =  await conn.execute(ICashConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 刪除場站參數 """
    async def icash_delete_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(ICashConfig.delete().where(ICashConfig.c.garage_id == garage_id))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新場站參數 (有啟用票種) """
    async def icash_update_garage_parameter_enabled_status(self, data: dict, garage_id: int, customer_id, user_id):
        sql = "SELECT * FROM `icash_config` WHERE garage_id = :garage_id"
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
                    rz =  await conn.execute(ICashConfig.update().values(data).where(ICashConfig.c.garage_id == garage_id))
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
                    rz =  await conn.execute(ICashConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢場站參數 """
    async def icash_query_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            result = await conn.execute(ICashConfig.select().where(ICashConfig.c.garage_id == garage_id))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]

    """ 更新場站參數 (未啟用票種) """
    async def icash_update_garage_parameter_disabled_status(self, garage_id: int, customer_id, update_user_id):
        sql = "SELECT * FROM `icash_config` WHERE garage_id = :garage_id"
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
                    rz =  await conn.execute(ICashConfig.update().values(data).where(ICashConfig.c.garage_id == garage_id))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 新增業者參數 """
    async def icash_insert_customer_parameter(self, data: dict, customer_code, create_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT `customer_id` FROM `customer` WHERE customer_code = :customer_code"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_code':customer_code})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = result[0]['customer_id']
                data['card_type'] = '02'
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
    async def icash_delete_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(TicketTransactionFtpConfig.delete().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "02"))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新業者參數 (有啟用票種) """
    async def icash_update_customer_parameter_enabled_status(self, data: dict, customer_id: int, user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '02'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = customer_id
                data['last_update_user_id'] = user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '02'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "02"))
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
                data['card_type'] = '02'

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
    async def icash_update_customer_parameter_disabled_status(self, customer_id: int, update_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '02'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data = {}
                data['customer_id'] = customer_id
                data['status'] = 0
                data['last_update_user_id'] = update_user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '02'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "02"))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢業者參數 """
    async def icash_query_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            result = await conn.execute(TicketTransactionFtpConfig.select().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "02"))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]