import time, datetime
from sqlalchemy import desc,text
import os,glob,sys
import zipfile
import shutil
import paramiko
from app.config.models import Trx_Data, IPassConfig, TicketTransactionFtpConfig
import operator
from app.services.systemlog_service import SystemlogService
from app.config.system_event_type import SystemEventType
from app.config.models import Account

class TicketTransactionIPassService:
    _db = None
    _log_service = None
    _syslog = None
    _directory_path = None
    _process_folder = None
    _now_date = None
    _card_type = None
    _mac_jar_param_properties = None
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
        self._now_date = datetime.date.today().strftime("%Y%m%d")
        self._card_type = "ipass"
        self._mac_jar_param_properties= "param.properties"
        self._user = user


    """ 交易檔包檔 """
    async def pack(self, location):
        sql_customer = f"""SELECT distinct 
        a.customer_id, 
        a.ipass_company_id, 
        a.ipass_system_id,
        b.customer_code
        FROM 
        `ticket_transaction_ftp_config` AS a
        LEFT JOIN 
        `customer` AS b 
        ON 
        a.customer_id = b.customer_id 
        WHERE 
        a.status = 1 and 
        a.card_type = '03'"""

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
                    `ipass_config` AS a 
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

                        # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                        generated_dat_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_dat")
                        if os.path.isdir(generated_dat_path):
                            shutil.rmtree(generated_dat_path)
                        self.mkdirs(generated_dat_path)
                        # 移除壓MAC值之前資料夾及底下的檔案 (之後重新建立資料夾)
                        go_MAC_before_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "INPUT")
                        if os.path.isdir(go_MAC_before_path):
                            shutil.rmtree(go_MAC_before_path)
                        self.mkdirs(go_MAC_before_path)
                        # 移除壓MAC值之後資料夾及底下的檔案 (之後重新建立資料夾)
                        go_MAC_after_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "OUTPUT")
                        if os.path.isdir(go_MAC_after_path):
                            shutil.rmtree(go_MAC_after_path)
                        self.mkdirs(go_MAC_after_path)
                        # 移除需要包進壓縮檔的交易檔資料夾及底下的檔案 (之後重新建立資料夾)
                        dat_files_go_zip_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "dat_files_go_zip")
                        if os.path.isdir(dat_files_go_zip_path):
                            shutil.rmtree(dat_files_go_zip_path)
                        self.mkdirs(dat_files_go_zip_path)
                        
                        # 壓MAC值之後檔案備份
                        generated_dat_go_MAC_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_dat_go_MAC_backup")
                        self.mkdirs(generated_dat_go_MAC_backup_path)

                        # mac.jar 參數檔位置
                        mac_jar_param_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, self._mac_jar_param_properties)
                        self.create_mac_jac_param(mac_jar_param_path, go_MAC_before_path, go_MAC_after_path)
                        shutil.copyfile(os.path.join(self._directory_path, "mac.jar"), os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "mac.jar"))

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
                            garage_code_list[str(garage_list[gl]['ipass_garage_code_hexadecmial']).zfill(4)] = str(garage_list[gl]['garage_code'])

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
                            file_seq = self.get_file_seq(generated_dat_backup_path, str(garage_list[gl]['ipass_garage_code_hexadecmial']).zfill(4))
                            
                            for root, folders, files in os.walk(device_ftp_path):
                                for sfile in files:
                                    if(sfile.startswith("DPTI_")):
                                        # Windows 測試
                                        # root_split = root.split("\\")
                                        # 正式環境
                                        root_split = root.split("/")

                                        aFile = os.path.join(root, sfile)

                                        # device 設備資料夾
                                        self.mkdirs(os.path.join(files_from_device_path, root_split[len(root_split)-1]))
                                        # 一天最多包99檔案，超過數量未包檔檔案，依舊會留在csvs/in/{customer_code}/{garage_code}/transaction_files/底下
                                        # 此做該天未包檔檔案區分
                                        not_pack_path = os.path.join(files_from_device_path, root_split[len(root_split)-1], "not_pack")
                                        self.mkdirs(not_pack_path)
                                        
                                        file_seq += 1
                                        # 一天最多包99個檔案
                                        if (file_seq < 100):
                                            # 檔名
                                            file_name = "DPTI_" + str(garage_list[gl]['ipass_garage_code_hexadecmial']).zfill(4) + self._now_date + str(file_seq).zfill(2) + ".DAT"
                                            pms_generate_dat_file = open(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code']), file_name), 'w', encoding = 'utf8')
                                            # 檔頭
                                            header = ("HDPTI_" + str(garage_list[gl]['ipass_garage_code_hexadecmial']).zfill(4) + self._now_date + str(file_seq).zfill(2) + "05").ljust(48) + "\n"
                                            pms_generate_dat_file.write(header)
                                            # 檔身
                                            body_dat_file = open(aFile, 'r', encoding = "utf8")
                                            total_count = 0
                                            total_amount = 0

                                            for line in body_dat_file.readlines():
                                                if len(line) == 304:
                                                    total_count += 1
                                                    total_amount += int(line[51:57])
                                                pms_generate_dat_file.write(line)
                                            body_dat_file.close()
                                            # 檔尾
                                            trailer = self.add_trailer(total_count, total_amount)
                                            pms_generate_dat_file.write(trailer)
                                            pms_generate_dat_file.close()

                                            shutil.copyfile(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code']), file_name), os.path.join(generated_dat_backup_path, file_name))

                                            # 讀取原檔檔身內容，判斷是否空檔來確認是否壓MAC值
                                            content = self.open_files(aFile, os.path.join(self._directory_path, location, str(garage_list[gl]['customer_code']), str(garage_list[gl]['garage_code']), "transaction_files"))
                                            if not len(content) == 0:
                                                shutil.copyfile(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code']), file_name), os.path.join(go_MAC_before_path, file_name))
                                            else:
                                                shutil.copyfile(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code']), file_name), os.path.join(dat_files_go_zip_path, file_name))
                                                shutil.copyfile(os.path.join(generated_dat_path, str(garage_list[gl]['garage_code']), file_name), os.path.join(dat_files_import_db_path, file_name))

                                            shutil.move(aFile, os.path.join(files_from_device_path, root_split[len(root_split)-1], sfile))
                                        else:
                                            print("包檔失敗，原因：iPass交易檔已包檔數量超過99個。業者：[" + str(garage_list[gl]['customer_code']) +"]，場站：[" + str(garage_list[gl]['garage_code']) + f"]，檔案名稱：[{aFile}]")
                                            shutil.copyfile(aFile, os.path.join(not_pack_path, sfile))
                            
                            """ 移動自動加值檔案 BEGIN """
                            for root, folders, files in os.walk(device_ftp_path):
                                for sfile in files:
                                    if(sfile.startswith("OAAI_") or sfile.startswith("OATI_")):
                                        aFile = os.path.join(root, sfile)

                                        shutil.copyfile(aFile, os.path.join(upload_path, sfile))
                                        shutil.move(aFile, os.path.join(files_from_device_path, sfile))
                            """ 移動自動加值檔案 END """

                        # 壓MAC值
                        file_go_MAC_before_count = 0
                        for file_go_MAC_before in glob.glob(os.path.join(go_MAC_before_path, "*DPTI_*.DAT")):
                            file_go_MAC_before_count +=1

                        if file_go_MAC_before_count > 0:
                            x = os.system("java -jar " + os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "mac.jar"))

                            # 複製壓MAC值過後檔案
                            for root, folders, files in os.walk(go_MAC_after_path):
                                for sfile in files:
                                    if(sfile.startswith("DPTI_") or sfile.endswith("DAT")):
                                        aFile = os.path.join(root, sfile)
                                        shutil.copyfile(aFile, os.path.join(generated_dat_go_MAC_backup_path, sfile))
                                        shutil.copyfile(aFile, os.path.join(dat_files_go_zip_path, sfile))
                                        shutil.copyfile(aFile, os.path.join(dat_files_import_db_path, sfile))
                        """ 場站交易檔包檔 END"""

                    """ 場站包檔後交易檔全部放進壓縮檔 BEGIN """
                    generated_zip_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip_backup", self._now_date)
                    self.mkdirs(generated_zip_backup_path)

                    # 移除包檔資料夾及底下的檔案 (之後重新建立資料夾)
                    generated_zip_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "generated_zip")
                    if os.path.isdir(generated_zip_path):
                        shutil.rmtree(generated_zip_path)
                    self.mkdirs(generated_zip_path)

                    # zip檔名、流水號
                    file_name = "DPTI_" + str(customer_list[cl]['ipass_company_id']) + self._now_date + str(customer_list[cl]['ipass_system_id']) + self.get_zip_file_no_num(generated_zip_backup_path)
                    zip_file_name = file_name + ".ZIP"
                    zip_OK_name = zip_file_name + ".OK"

                    zip_file_path = os.path.join(generated_zip_path, zip_file_name)
                    zip_OK_path = os.path.join(generated_zip_path, zip_OK_name)

                    dat_files_go_zip_count = 0
                    for dat_files_go_zip in glob.glob(os.path.join(dat_files_go_zip_path, "*DPTI_*.DAT")):
                        dat_files_go_zip_count +=1

                    if dat_files_go_zip_count > 0:
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
        a.card_type ='03'"""
        
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
                                if(sfile.startswith("DPTI_")):
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

                        # 自動加值檔案
                        for root, folders, files in os.walk(upload_path):
                            for sfile in files:
                                if(sfile.startswith("OAAI_") or sfile.startswith("OATI_")):
                                    aFile = os.path.join(root, sfile)

                                    sftp.put(aFile, ticket_host_path + sfile)
                                    shutil.move(aFile, os.path.join(upload_backup_path, sfile))
                        
                        sftp.close()
                        client.close()
                    except Exception as e:
                        print('Error:%s'% (e) )
        return "upload"

    """ 回饋檔 & 黑名單 & 黑名單3小時增量檔 & 關閉自動加值名單 下載 """
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
        a.card_type ='03'"""

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

                    # 供設備下載黑名單3小時增量、黑名單、關閉自動加值名單位置
                    customer_download_black_list_path = os.path.join(self._directory_path, location, str(customer_ftp_list[cfl]['customer_code']), "iPass.bl")
                    self.mkdirs(customer_download_black_list_path)

                    try:
                        client = paramiko.SSHClient()
                        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        client.connect(str(customer_ftp_list[cfl]['ip_address']), username = str(customer_ftp_list[cfl]['account']), password = str(customer_ftp_list[cfl]['password']), port = int(customer_ftp_list[cfl]['ip_port']))
                        sftp = client.open_sftp()

                        ticket_host_path = str(customer_ftp_list[cfl]['download_path'])

                        # 回饋檔
                        if (operator.eq('feedback_files', download_file_type)):
                            fileList = sftp.listdir(ticket_host_path)
                            for file in fileList:
                                if(file.startswith("DPTR_") and file.endswith(".zip")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        sftp.get(ticket_host_path + file, os.path.join(download_path, file))
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(feedback_files_import_db_path, file))
                        # 黑名單 3小時增量檔
                        elif (operator.eq('black_list_KBLI', download_file_type)):
                            fileList = sftp.listdir(ticket_host_path)
                            for file in fileList:
                                if(file.startswith("KBLI_") and file.endswith(".ZIP")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        sftp.get(ticket_host_path + file, os.path.join(download_path, file))
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                        # 黑名單
                        elif (operator.eq('black_list_KBLN', download_file_type)):
                            fileList = sftp.listdir(ticket_host_path)
                            for file in fileList:
                                if(file.startswith("KBLN_") and file.endswith(".ZIP")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        sftp.get(ticket_host_path + file, os.path.join(download_path, file))
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                        # 關閉自動加值名單
                        elif (operator.eq('close_autoload_list', download_file_type)):
                            fileList = sftp.listdir(ticket_host_path)
                            for file in fileList:
                                if(file.startswith("KCAN_") and file.endswith(".ZIP")):
                                    if not os.path.exists(os.path.join(download_path, file)):
                                        sftp.get(ticket_host_path + file, os.path.join(download_path, file))
                                        shutil.copyfile(os.path.join(download_path, file), os.path.join(customer_download_black_list_path, file))
                        
                        sftp.close()
                        client.close()
                    except Exception as e:
                        print('Error:%s'% (e) )
        return "download"

    """ 取得檔名流水號 """
    def get_file_seq(self, generated_dat_backup_path, ipass_garage_code_hexadecmial):
        file_seq = 0
        if os.path.isdir(generated_dat_backup_path):
            # 算今天產了幾個檔，同一天不能重複序號
            for root, folders, files in os.walk(generated_dat_backup_path):
                for each in files:
                    if(each.startswith(f'DPTI_{ipass_garage_code_hexadecmial}')):
                        file_seq += 1 
        return file_seq

    """ 讀取未包檔前檔案檔身內容 """
    def open_files(self, file, path):
        content  = ""
        with open(os.path.join(path, file), 'r') as DPTI_file:
            content = DPTI_file.read()
            #print(content) 
        return content

    """ decimal 轉 hexadecmial """
    def decimal_to_hex(location_id):
        hex_location_id = 0
        hex_location_id = ('{:02x}'.format(int(location_id))).upper()
        return hex_location_id.zfill(4)

    """ 取得ZIP檔名流水號 """
    def get_zip_file_no_num(self, generated_zip_backup_path):
        zip_file_no_num = 51
        if os.path.isdir(generated_zip_backup_path):
            filelist = os.listdir(generated_zip_backup_path)
            for file in filelist:
                if file.endswith(".ZIP"):
                    zip_file_no_num += 1
        return str(zip_file_no_num).zfill(2)

    """ 建立.OK檔案 """
    def create_OK_file(self, zip_file_name):
        file = open(f'{zip_file_name}.OK', 'w') 
        file.close()

    """ 寫檔尾 """
    def add_trailer(self, total_count, total_amount):
        # Record Type
        trailer = "T"
        # MAC值
        trailer = trailer + ("").zfill(8)
        # 交易總筆數
        trailer = trailer + (str(total_count)).zfill(6)
        # 交易總金額
        trailer = trailer + (str(total_amount)).zfill(10)
        # 00 交易筆數
        trailer = trailer + ("").zfill(6)
        # 00 交易金額
        trailer = trailer + ("").zfill(10)
        # 03 交易筆數
        trailer = trailer + ("").zfill(6)
        # 10 交易筆數
        trailer = trailer + ("").zfill(6)
        # 11 交易筆數
        trailer = trailer + ("").zfill(6)
        # 11 交易金額
        trailer = trailer + ("").zfill(10)
        # 13 交易筆數
        trailer = trailer + ("").zfill(6)
        # 23 交易筆數
        trailer = trailer + ("").zfill(6)
        # 23 交易金額
        trailer = trailer + ("").zfill(10)
        # 52 交易筆數
        trailer = trailer + ("").zfill(6)
        # 52 交易金額
        trailer = trailer + ("").zfill(10)
        # 53 交易筆數
        trailer = trailer + ("").zfill(6)
        # 53 交易金額
        trailer = trailer + ("").zfill(10)
        # 90 交易筆數
        trailer = trailer + ("").zfill(6)
        # 91 交易筆數
        trailer = trailer + ("").zfill(6)
        # Reserved
        trailer = trailer + ("").ljust(123)
        # Record Separator
        trailer = trailer + "\n"
        return trailer

    """ 建立mac.jar的設定檔 """
    def create_mac_jac_param(self, mac_jar_param_path, go_MAC_before_path, go_MAC_after_path):
        mac_jar_param = open(mac_jar_param_path, 'w', encoding = "utf8")
        mac_jar_param.write("#\n")
        mac_jar_param.write("MAC_INPUT_DIR= ")

        # Windows 測試
        # mac_jar_param.write(str(go_MAC_before_path).replace("\\","\\\\"))
        # mac_jar_param.write("\\\\")
        # 正式環境
        mac_jar_param.write(str(go_MAC_before_path))
        mac_jar_param.write("/")

        mac_jar_param.write("\n")
        mac_jar_param.write("MAC_OUTPUT_DIR= ")

        # Windows 測試
        # mac_jar_param.write(str(go_MAC_after_path).replace("\\","\\\\"))
        # mac_jar_param.write("\\\\")
        # 正式環境
        mac_jar_param.write(str(go_MAC_after_path))
        mac_jar_param.write("/")

        mac_jar_param.write("\n")
        mac_jar_param.close()

    """ 場站壓縮檔全部放進壓縮檔 """
    def pack_all_in_one(self, dat_files_go_zip_path, dat_files_go_zip_backup_path, zf):
        # 場站交易檔放入壓縮檔
        for root, folders, files in os.walk(dat_files_go_zip_path):
            for sfile in files:
                aFile = os.path.join(root, sfile)

                zf.write(aFile, os.path.basename(sfile))
                shutil.copyfile(aFile, os.path.join(dat_files_go_zip_backup_path, sfile))

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
    async def data_import_db(self, zip_file_name, garage_code_list, dat_files_import_db_path,dat_files_import_db_backup_path):
        data = {}

        for root, folders, files in os.walk(dat_files_import_db_path):
            for sfile in files:
                if(sfile.startswith("DPTI_") and sfile.endswith("DAT")):
                    aFile = os.path.join(root, sfile)

                    content = open(aFile, 'r', encoding = "utf8")
                    for line in content.readlines():
                        if len(line) == 304:
                            data['file_name'] = sfile
                            data['trx_date'] = line[19:27]
                            data['trx_time'] = line[27:33]
                            data['card_no'] = line[69:101]
                            data['txn_no'] = line[101:107]
                            data['trx_amt'] = line[51:57]
                            data['device_id'] = line[35:43]
                            data['trx_type'] = line[33:35]
                            data['el_value'] = line[63:69]
                            # data['cal_date'] = 
                            # data['cal_status'] = 
                            # data['cal_err_code'] = 
                            data['trx_sub_type'] = line[107:109]
                            data['garage_code'] = garage_code_list.get(sfile[5:9])
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
        a.card_type = '03' AND 
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
                    feedback_files_import_db_backup_path = os.path.join(self._process_path, str(customer_list[cl]['customer_code']), self._card_type, "feedback_files_import_db_backup", self._now_date)
                    self.mkdirs(feedback_files_import_db_backup_path)

                    data = {}

                    for root, folders, files in os.walk(feedback_files_import_db_path):
                        for sfile in files:
                            if(sfile.startswith("DPTR_") and sfile.endswith("zip")):
                                aFile = os.path.join(root, sfile)

                                with zipfile.ZipFile(aFile, 'r') as myzip:
                                    myzip.extractall(feedback_files_import_db_path)
                                    myzip.close()
                                    shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, sfile))

                    for root, folders, files in os.walk(feedback_files_import_db_path):
                        for sfile in files:
                            if(sfile.startswith("DPTR_") and sfile.endswith("dat")):
                                aFile = os.path.join(root, sfile)

                                content = open(aFile, 'r', encoding = "utf8")
                                for line in content.readlines():
                                    if len(line) == 159:
                                        # where 條件
                                        # data['file_name'] = line[17:26]
                                        # where 條件
                                        # data['trx_date'] = line[74:82]
                                        # where 條件
                                        # data['trx_time'] = line[82:88]
                                        # where 條件
                                        # data['card_no'] = line[34:66]
                                        # data['txn_no'] = 
                                        # where 條件
                                        # data['trx_amt'] = line[88:98]
                                        # data['device_id'] = 
                                        # where 條件
                                        # data['trx_type'] = line[72:74]
                                        # data['el_value'] = 
                                        data['cal_date'] = line[98:106]
                                        data['cal_status'] = self.check_cal_status(line[148:149])
                                        data['cal_err_code'] = self.check_cal_err_code(line[63:69])
                                        # data['trx_sub_type'] = 
                                        # data['garage_code'] = 
                                        # data['upload_zip_name'] = 
                                        data['feedback_file_name'] = sfile

                                        trans = await conn.begin()
                                        try:
                                            rz =  await conn.execute(Trx_Data.update().values(data).where(Trx_Data.c.file_name.like('%' + line[17:26] + '%')).where(Trx_Data.c.trx_date == line[74:82]).where(Trx_Data.c.trx_time == line[82:88]).where(Trx_Data.c.card_no == line[34:66]).where(Trx_Data.c.trx_amt == line[88:98]).where(Trx_Data.c.trx_type == line[72:74]))
                                        except Exception as e:
                                            print('有錯: ',e)
                                            await trans.rollback()
                                            raise
                                        else:
                                            await trans.commit()
                                content.close()
                                shutil.move(aFile, os.path.join(feedback_files_import_db_backup_path, sfile))

    """ 清分錯誤代碼(驗證旗標) """
    def check_cal_err_code(self, data_hex):
        cal_err_code = ""
        # 全部均為0
        if (operator.eq(data_hex, "00000")):
            cal_err_code = "0"
        # 驗證旗標01清分
        elif (operator.eq(data_hex, "00001")):
            cal_err_code = "1"
        # 驗證旗標02重覆(不列入清分)
        elif (operator.eq(data_hex, "00002")):
            cal_err_code = "2"
        # 驗證旗標03 MAC
        elif (operator.eq(data_hex, "00004")):
            cal_err_code = "3"
        # 驗證旗標04 TAC
        elif (operator.eq(data_hex, "00008")):
            cal_err_code = "4"
        # 驗證旗標05資料格式錯誤
        elif (operator.eq(data_hex, "00010")):
            cal_err_code = "5"
        # 驗證旗標06測試卡(不列入清分)
        elif (operator.eq(data_hex, "00020")):
            cal_err_code = "6"
        # 驗證旗標07黑名單
        elif (operator.eq(data_hex, "00040")):
            cal_err_code = "7"
        # 驗證旗標08
        elif (operator.eq(data_hex, "00080")):
            cal_err_code = "8"
        # 驗證旗標09
        elif (operator.eq(data_hex, "00100")):
            cal_err_code = "9"
        # 驗證旗標10
        elif (operator.eq(data_hex, "00200")):
            cal_err_code = "10"
        # 驗證旗標11
        elif (operator.eq(data_hex, "00400")):
            cal_err_code = "11"
        # 驗證旗標12
        elif (operator.eq(data_hex, "00800")):
            cal_err_code = "12"
        # 驗證旗標13
        elif (operator.eq(data_hex, "01000")):
            cal_err_code = "13"
        # 驗證旗標14
        elif (operator.eq(data_hex, "02000")):
            cal_err_code = "14"
        # 驗證旗標15
        elif (operator.eq(data_hex, "04000")):
            cal_err_code = "15"
        # 驗證旗標16
        elif (operator.eq(data_hex, "08000")):
            cal_err_code = "16"
        # 驗證旗標17
        elif (operator.eq(data_hex, "10000")):
            cal_err_code = "17"
        # 驗證旗標18
        elif (operator.eq(data_hex, "20000")):
            cal_err_code = "18"
        # 驗證旗標19
        elif (operator.eq(data_hex, "40000")):
            cal_err_code = "19"
        # 驗證旗標20
        elif (operator.eq(data_hex, "80000")):
            cal_err_code = "20"
        return cal_err_code

    """ 總驗證結果 """
    def check_cal_status(self, data):
        cal_status = ""
        # 所有驗證旗標均為 0( 正確 )，列入帳款
        if (operator.eq(data, "0")):
            cal_status = "F"
        # 為暫先列入帳款，待後續判定處理之例外交易
        elif (operator.eq(data, "1")):
            cal_status = "E"
        # 為不列入帳款之交易
        elif (operator.eq(data, "N")):
            cal_status = "E"
        return cal_status

    """ 新增場站參數 """
    async def ipass_insert_garage_parameter(self, data: dict, garage_code, customer_id, create_user_id):
        sql = "SELECT `garage_id` FROM `garage` WHERE garage_code = :garage_code"
        async with self._db.acquire() as conn:
            garage_id_query = await conn.execute(text(sql), {'garage_code':garage_code})
            if garage_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in garage_id_query]

                data['customer_id'] = customer_id
                data['garage_id'] = result[0]['garage_id']
                data['ipass_garage_code_hexadecmial'] = str(data['ipass_garage_code_hexadecmial']).zfill(4)
                data['create_user_id'] = create_user_id
                data['create_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(IPassConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 刪除場站參數 """
    async def ipass_delete_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(IPassConfig.delete().where(IPassConfig.c.garage_id == garage_id))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新場站參數 (有啟用票種) """
    async def ipass_update_garage_parameter_enabled_status(self, data: dict, garage_id: int, customer_id, user_id):
        sql = "SELECT * FROM `ipass_config` WHERE garage_id = :garage_id"
        async with self._db.acquire() as conn:
            garage_id_query = await conn.execute(text(sql), {'garage_id':garage_id})
            if garage_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in garage_id_query]

                data['customer_id'] = customer_id
                data['garage_id'] = garage_id
                data['ipass_garage_code_hexadecmial'] = str(data['ipass_garage_code_hexadecmial']).zfill(4)
                data['last_update_user_id'] = user_id
                data['last_update_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(IPassConfig.update().values(data).where(IPassConfig.c.garage_id == garage_id))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()
            elif(garage_id_query.rowcount == 0):
                data['customer_id'] = customer_id
                data['garage_id'] = garage_id
                data['ipass_garage_code_hexadecmial'] = str(data['ipass_garage_code_hexadecmial']).zfill(4)
                data['create_user_id'] = user_id
                data['create_time'] = datetime.datetime.now()

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(IPassConfig.insert().values(data))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢場站參數 """
    async def ipass_query_garage_parameter(self, garage_id: int):
        async with self._db.acquire() as conn:
            result = await conn.execute(IPassConfig.select().where(IPassConfig.c.garage_id == garage_id))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]

    """ 更新場站參數 (未啟用票種) """
    async def ipass_update_garage_parameter_disabled_status(self, garage_id: int, customer_id, update_user_id):
        sql = "SELECT * FROM `ipass_config` WHERE garage_id = :garage_id"
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
                    rz =  await conn.execute(IPassConfig.update().values(data).where(IPassConfig.c.garage_id == garage_id))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 新增業者參數 """
    async def ipass_insert_customer_parameter(self, data: dict, customer_code, create_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT `customer_id` FROM `customer` WHERE customer_code = :customer_code"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_code':customer_code})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = result[0]['customer_id']
                data['card_type'] = '03'
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
    async def ipass_delete_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            trans = await conn.begin()
            try:
                rz =  await conn.execute(TicketTransactionFtpConfig.delete().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "03"))
            except Exception as e:
                print('有錯: ',e)
                await trans.rollback()
                raise
            else:
                await trans.commit()

    """ 更新業者參數 (有啟用票種) """
    async def ipass_update_customer_parameter_enabled_status(self, data: dict, customer_id: int, user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '03'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data['customer_id'] = customer_id
                data['last_update_user_id'] = user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '03'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "03"))
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
                data['card_type'] = '03'

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
    async def ipass_update_customer_parameter_disabled_status(self, customer_id: int, update_user_id):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        sql = "SELECT * FROM `ticket_transaction_ftp_config` WHERE customer_id = :customer_id AND card_type = '03'"
        async with self._db.acquire() as conn:
            customer_id_query = await conn.execute(text(sql), {'customer_id':customer_id})
            if customer_id_query.rowcount > 0:
                result = [dict(row.items()) async for row in customer_id_query]

                data = {}
                data['customer_id'] = customer_id
                data['status'] = 0
                data['last_update_user_id'] = update_user_id
                data['last_update_time'] = datetime.datetime.now()
                data['card_type'] = '03'

                trans = await conn.begin()
                try:
                    rz =  await conn.execute(TicketTransactionFtpConfig.update().values(data).where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "03"))
                except Exception as e:
                    print('有錯: ',e)
                    await trans.rollback()
                    raise
                else:
                    await trans.commit()

    """ 查詢業者參數 """
    async def ipass_query_customer_parameter(self, customer_id: int):
        # 01：悠遊卡, 02：愛金卡, 03：一卡通, 05：有錢卡
        async with self._db.acquire() as conn:
            result = await conn.execute(TicketTransactionFtpConfig.select().where(TicketTransactionFtpConfig.c.customer_id == customer_id).where(TicketTransactionFtpConfig.c.card_type == "03"))
            result = [dict(row.items()) async for row in result]
            return None if len(result) == 0 else result[0]