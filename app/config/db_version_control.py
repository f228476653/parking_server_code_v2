import subprocess
class DBVersionControl():
    
    engine = None
    # version_control mapping methods
    version = [1.0, 1.1, 1.11, 1.12, 1.3 ,1.31]

    def __init__(self, engine):
        self.engine = engine
    
    def is_correct_version_number(self, start, end= version[-1]):
        if start in self.version and end in self.version:
            return {"is_corrent": True, "index_start": self.version.index(start) + 1, "index_end": self.version.index(end)}
        else:
            return {"is_corrent": False, "version_start": start, "version_end": end}

    async def backup_db(self):
        pass
        # TODO 應該要輸入 一個參數 該參數為指定存放的路徑
        # TODO when prefix is 'backup'
        # subprocess.run(["mkdir", "指定路徑"])
        # subprocess.run(["my", "指定路徑"])
        # await conn.execute('')

    async def V0_0(self):
        # init 才會執行 刪掉已存在table
        async with self.engine.acquire() as conn:
            await conn.execute('DROP TABLE IF EXISTS device_ibox_args')
            await conn.execute('DROP TABLE IF EXISTS garage_ibox_args')
            await conn.execute('DROP TABLE IF EXISTS customer_map_card_case')
            await conn.execute('DROP TABLE IF EXISTS customer_ibox_args')
            await conn.execute('DROP TABLE IF EXISTS system_configuration') 
            await conn.execute('DROP TABLE IF EXISTS device_pv')
            await conn.execute('DROP TABLE IF EXISTS exit_config')
            await conn.execute('DROP TABLE IF EXISTS exit_type_config_detail')
            await conn.execute('DROP TABLE IF EXISTS account')
            await conn.execute('DROP TABLE IF EXISTS keystore')
            await conn.execute('DROP TABLE IF EXISTS license_info')
            await conn.execute('DROP TABLE IF EXISTS customer')
            await conn.execute('DROP TABLE IF EXISTS permission')
            await conn.execute('DROP TABLE IF EXISTS role')
            await conn.execute('DROP TABLE IF EXISTS map_role_permission')
            await conn.execute('DROP TABLE IF EXISTS garage')
            await conn.execute('DROP TABLE IF EXISTS garage_group')
            await conn.execute('DROP TABLE IF EXISTS entry_gate')
            await conn.execute('DROP TABLE IF EXISTS map_garage_to_garage_group')
            await conn.execute('DROP TABLE IF EXISTS map_garage_to_account')
            await conn.execute('DROP TABLE IF EXISTS map_garage_group_to_account')
            await conn.execute('DROP TABLE IF EXISTS system_log')
            await conn.execute('DROP TABLE IF EXISTS event')
            await conn.execute('DROP TABLE IF EXISTS trx_data')
            await conn.execute('DROP TABLE IF EXISTS parking')
            await conn.execute('DROP TABLE IF EXISTS ticket_provider')
            await conn.execute('DROP TABLE IF EXISTS map_garage_to_system_config')
            await conn.execute('DROP TABLE IF EXISTS system_config')            
            await conn.execute('DROP TABLE IF EXISTS lane')
            await conn.execute('DROP TABLE IF EXISTS driveway')
            await conn.execute('DROP TABLE IF EXISTS e_invoice_config')
            await conn.execute('DROP TABLE IF EXISTS real_time_transaction_data')
            await conn.execute('DROP TABLE IF EXISTS clock_time_card')
            await conn.execute('DROP TABLE IF EXISTS parking_in_out_record')
            await conn.execute('DROP TABLE IF EXISTS e_invoice_number_data')     
            await conn.execute('DROP TABLE IF EXISTS shift_checkout')
            await conn.execute('DROP TABLE IF EXISTS commutation_ticket_order')
            await conn.execute('DROP TABLE IF EXISTS commutation_ticket_config')
            await conn.execute('DROP TABLE IF EXISTS commutation_ticket_period_config')
            await conn.execute('DROP TABLE IF EXISTS garage_ftp_info')
            await conn.execute('DROP TABLE IF EXISTS device_event')
            await conn.execute('DROP TABLE IF EXISTS fee_rule')
            await conn.execute('DROP TABLE IF EXISTS fee_para')
            await conn.execute('DROP TABLE IF EXISTS pv3_log')
            await conn.execute('DROP TABLE IF EXISTS device_pv3_args')
            await conn.execute('DROP TABLE IF EXISTS garage_pv3_args')
            await conn.execute('DROP TABLE IF EXISTS customer_pv3_args')
            await conn.execute('DROP TABLE IF EXISTS ticket_transaction_ftp_config')
            await conn.execute('DROP TABLE IF EXISTS icash_config')
            await conn.execute('DROP TABLE IF EXISTS ipass_config')
            await conn.execute('DROP TABLE IF EXISTS happycash_config')
            await conn.execute('DROP TABLE IF EXISTS device_pad_args')
            await conn.execute('DROP TABLE IF EXISTS garage_pad_args')
            await conn.execute('DROP TABLE IF EXISTS customer_pad_args')
            await conn.execute('DROP TABLE IF EXISTS activation_code')
            await conn.execute('DROP TABLE IF EXISTS special_day')
            await conn.execute('DROP PROCEDURE IF EXISTS alter_table_ticket_transaction')
            await conn.execute('DROP TABLE IF EXISTS forget_password')
            

    async def v1_0(self):
        # pad-poc版本
        async with self.engine.acquire() as conn:
            await conn.execute(''' CREATE TABLE device_ibox_args (
                `device_ibox_args_id` int(10) auto_increment,
                `device_name` varchar(20) COMMENT '設備名稱 也是此設備資料夾名稱',
                `external_ip` varchar(20) COMMENT 'ibox external ip bind for iPass',
                `car_in` varchar(200) COMMENT '此站所有進場ip',
                `car_out` varchar(200) COMMENT '此站所有出場ip',
                `station_inout` int(5) COMMENT '該設置系統為進場或出場 1:in, 2:out',
                `ECC` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
                `iPass` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
                `iCash` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
                `YHDP` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
                `ip` varchar(200) COMMENT '設定該PV 主機IP 參數在開機時可以設定 IP Address',
                `mac_ip` varchar(20) COMMENT 'ibox mac ip',
                `eid_pos_no` varchar(20) COMMENT '立柱代碼 (for 發票EIDC 機制) 對應EIDC.txt 第三欄位',
                `update_time` datetime NOT NULL COMMENT '最後更新時間',
                `update_user` varchar(200) COMMENT '最後更新使用者',
                `garage_id` int(10),
                PRIMARY KEY  (`device_ibox_args_id`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE garage_ibox_args (
                `garage_ibox_args_id` int(10) auto_increment,
                `garage_code` varchar(10) COMMENT 'Acer ITS defined garage code',
                `store_no` varchar(20) COMMENT '場站代碼',
                `pos_no` int(10) COMMENT 'pos代碼 目前是取該車道IP最後一碼 ex:192.168.200.203 -> 003',
                `eid_store_no` varchar(20) COMMENT '此站所有出場ip',
                `plid` varchar(4) COMMENT '該設置系統為進場或出場 1:in, 2:out',
                `printer` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
                `tax_id_num` varchar(20) COMMENT '賣方統編',
                `ntp_server` varchar(20) COMMENT '校時',
                `update_time` datetime NOT NULL COMMENT '最後更新時間',
                `update_user` varchar(200) COMMENT '最後更新使用者',
                `garage_id` int(10),
                PRIMARY KEY  (`garage_ibox_args_id`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE customer_map_card_case (
                `customer_map_card_case_id` int(10) auto_increment,
                `device_type` varchar(20) COMMENT '設備類型 pad, pv3, iBox',
                `enable_card_case` int(10) COMMENT '客戶啟用卡種 0: 全關, 1:愛金, 2:一卡, 3:有錢, 4:愛金.一卡, 5:愛金.有錢, 6:一卡.有錢 7:三卡 ...之後悠遊卡在往後加',
                `customer_id` int(10),
                PRIMARY KEY  (`customer_map_card_case_id`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE customer_ibox_args (
                `customer_ibox_args_id` int(10) auto_increment,
                `market_code` varchar(3) COMMENT '特約機構代碼',
                `cashier_no` varchar(4) COMMENT '收銀員編號',
                `system_id` varchar(2) COMMENT '交易系統編號',
                `comp_id` varchar(2) COMMENT '停車場地點代碼/業者代碼',
                `machine` varchar(8) COMMENT '交易機器編碼',
                `ipass_water_lv_host` varchar(50) COMMENT '一卡通主機IP Host(須與主機端同步設定值須相同)',
                `ipass_water_lv_port` int(10) COMMENT '一卡通水位參數(須與主機端同步設定值須相同)',
                `socket_ip` varchar(50) COMMENT '參數設定 正式帶入172.21.1.101 測試帶入10.20.1.74',
                `transaction_system_id` varchar(2) COMMENT '交易系統編號',
                `loc_id` varchar(2) COMMENT '公司代碼',
                `transaction_terminal_no` varchar(8) COMMENT 'Terminal NO',
                `tid` varchar(8) COMMENT 'Terminal ID(BCD)',
                `mid` varchar(16) COMMENT '交易系統代碼',
                `YHDP_water_lv` int(10) COMMENT '水位參數',
                `YHDP_water_lv_host` varchar(50) COMMENT '遠鑫主機IP Host(須與主機端同步設定值須相同)',
                `YHDP_water_lv_port` int(5) COMMENT '遠鑫水位參數(須與主機端同步設定值須相同)',
                `nii` int(5) COMMENT '參數設定 正式帶入0688 測試 0667',
                `client_pv` varchar(50) COMMENT '設定同步時間 PV主機進站與出站IP',
                `time_sync_period` int(5) COMMENT '週期',
                `update_time` datetime NOT NULL COMMENT '最後更新時間',
                `update_user` varchar(200) COMMENT '最後更新使用者',
                `customer_id` int(5),
                PRIMARY KEY  (`customer_ibox_args_id`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE system_configuration (
                `key` varchar(50) NOT NULL COMMENT '系統配置名稱',
                `value` varchar(50) NOT NULL COMMENT '系統配置值',
                `description` varchar(100) NOT NULL COMMENT '用途描述',
                `config_group_name` varchar(50) NOT NULL COMMENT '系統配置群組名稱',
                PRIMARY KEY  (`key`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE device_pv (
                `device_pv_id` int(10) NOT NULL auto_increment,
                `garage_id` int(10) NOT NULL,
                `pv` varchar(128) NOT NULL,
                `type` varchar(1) NOT NULL,
                `pricing_scheme` int(2) NOT NULL COMMENT '計費規則',
                `pv_ip` varchar(64) NOT NULL,
                `pv_netmask` varchar(64) NOT NULL,
                `pv_gateway` varchar(64) NOT NULL,
                `pms_ip` varchar(64) NOT NULL,
                `pms_port` int(10) NOT NULL,
                `ecc_ip` varchar(64) NOT NULL,
                `ecc_port` int(10) NOT NULL,
                `in_out` int(1) NOT NULL,
                `aisle` varchar(10) NOT NULL,
                `auto_print_invoice` int(1) NOT NULL COMMENT '是否自動列印發票 0:不印, 1:要印',
                `pv_cutoff` varchar(4) NOT NULL,
                `MEntryB` varchar(10) NOT NULL,
                `MExitD` int(5) NOT NULL,
                `pv_version` varchar(20) NOT NULL,
                `last_response_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `response_type` varchar(4) NOT NULL default '00',
                `invoice_printer_status` varchar(2) NOT NULL default '00' COMMENT 'ref [invoice_printer_error_def].code',
                `pricing_scheme_disability` int(2) NOT NULL default '0' COMMENT '身障計費規則',
                `pv_response_confirm` tinyint(1) NOT NULL default '0' COMMENT 'PV是否回傳confirm(1:是-新連線,0:否-舊連線',
                `etag_flag` tinyint(1) NOT NULL default '0' COMMENT '是否為eTag車道(1:是,0:否)',
                `costrule_using_para` tinyint(1) NOT NULL default '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
                `lane_costrule_mode` tinyint(1) NOT NULL default '0' COMMENT '車道計費模式(1:複合, 0:單一)',
                `gate_control_mode` tinyint(1) NOT NULL default '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
                `lpr_lane` varchar(4) NOT NULL default '99' COMMENT '車辨車道代碼',
                `update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `update_account_id` int,
                PRIMARY KEY  (`device_pv_id`),
                UNIQUE KEY `pv` (`pv`),
                KEY `type` (`type`),
                KEY `pricing_scheme` (`pricing_scheme`),
                KEY `pv_ip` (`pv_ip`),
                KEY `MEntryB` (`MEntryB`),
                KEY `in_out` (`in_out`)
            ) DEFAULT CHARSET=utf8 ''')

            await conn.execute('''CREATE TABLE exit_config (
                exit_config_id SERIAL PRIMARY KEY,
                garage_id int, 
                description VARCHAR(100) DEFAULT '',
                is_configured int DEFAULT 0,
                disabled int DEFAULT 0,
                update_account_id int,
                update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
            ) DEFAULT CHARSET=utf8''')    

            await conn.execute('''CREATE TABLE exit_type_config_detail (
                exit_type_config_detail_id SERIAL PRIMARY KEY,
                exit_type VARCHAR(50) NOT NULL,
                exit_config_id int NOT NULL,
                exit_type_disabled int DEFAULT 0
            ) DEFAULT CHARSET=utf8''')           


            await conn.execute('''CREATE TABLE account (
                account_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                account VARCHAR(80) NOT NULL,
                customer_id int,
                password VARCHAR(500) NOT NULL,
                user_first_name VARCHAR(100) NULL,
                user_middle_name VARCHAR(100) NULL,
                user_last_name VARCHAR(100) NULL,
                email VARCHAR(100) NULL,
                mobile VARCHAR(100) NULL,
                role_id int,
                is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
                is_customer_root BOOLEAN NOT NULL DEFAULT FALSE
            ) DEFAULT CHARSET=utf8''')

            await conn.execute('''CREATE TABLE keystore (
                keystore_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                customer_id int,
                key_version VARCHAR(150) NOT NULL,
                key_type VARCHAR(150) NULL,
                fixed_account_total int NOT NULL DEFAULT 1,
                dynamic_account_total int NOT NULL DEFAULT 1,
                key_manager_email VARCHAR(255) NOT NULL,
                service_type VARCHAR(30) NOT NULL,
                note VARCHAR(255) NULL,
                start_date TIMESTAMP,
                end_date TIMESTAMP ,
                key_status VARCHAR(30) NOT NULL,
                key_validation_status VARCHAR(30) NULL,
                key_value VARCHAR(4000) NOT NULL
            ) DEFAULT CHARSET=utf8''')

            await conn.execute('''CREATE TABLE license_info (
                license_info_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                requested_keystore VARCHAR(2000) NULL,
                applied_keystore VARCHAR(2000) NULL,
                customer_id int,
                key_version VARCHAR(150) NOT NULL,
                key_type VARCHAR(150) NULL,
                fixed_account_total int NOT NULL DEFAULT 1,
                dyanmic_account_total int NOT NULL DEFAULT 1,
                key_manager_email VARCHAR(255) NOT NULL,
                service_type VARCHAR(30) NOT NULL,
                note VARCHAR(255) NULL,
                start_date TIMESTAMP ,
                end_date TIMESTAMP ,
                key_status VARCHAR(30) NOT NULL,
                key_string VARCHAR(2000) NOT NULL
            ) DEFAULT CHARSET=utf8''')

            await conn.execute('''CREATE TABLE customer (
                customer_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                company_english_name VARCHAR(255),
                company_union_number VARCHAR(15),
                customer_code VARCHAR(150) NOT NULL,
                company_name VARCHAR(150) NOT NULL,
                contact_username VARCHAR(150) NOT NULL,
                mobile VARCHAR(30) NULL,
                fax VARCHAR(30) NULL,
                phone_number1 VARCHAR(30) NULL,
                phone_number2 VARCHAR(30) NULL,
                email VARCHAR(100) NULL,
                customer_status int NULL COMMENT '閘門控制模式(1:active, 0:disabled)',
                note VARCHAR(255) NULL,
                contact_availible_datetime VARCHAR(255) NULL,
                contact_datetime VARCHAR(10),
                company_address VARCHAR(255)
            ) DEFAULT CHARSET=utf8''')


            await conn.execute('''CREATE TABLE permission (
                permission_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                name VARCHAR(50) NOT NULL,
                description VARCHAR(255) NULL,
                permission_type VARCHAR(255) NOT NULL,
                parent_id int,
                enable int Default 1
            ) DEFAULT CHARSET=utf8''')


            await conn.execute('''CREATE TABLE role (
                role_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                name VARCHAR(50) NOT NULL,
                description VARCHAR(255) NULL,
                role_type VARCHAR(30) NOT NULL,
                is_system_role int Default 0 COMMENT '只有is_superuser =1 的帳號才能夠選擇的角色',
                customer_id  int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE map_role_permission (
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                role_id int,
                permission_id int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE garage (
                garage_code VARCHAR(10) NOT NULL COMMENT 'Acer ITS defined garage code',
                garage_name VARCHAR(50) NULL,
                customer_id int,
                city_name VARCHAR(50) NULL,
                city_code VARCHAR(3) NULL,
                district VARCHAR(10) NULL,
                district_code VARCHAR(3) NULL,
                address1 VARCHAR(255) NULL,
                address2 VARCHAR(255) NULL,
                total_capacity int DEFAULT 0,
                sedan_capacity int DEFAULT 0,
                motocycle_capacity int DEFAULT 0,
                sedan_priority_pragnant_capacity int DEFAULT 0,
                motocycle_priority_pragnant_capacity int DEFAULT 0,
                sedan_priority_disability_capacity int DEFAULT 0,
                motocycle_priority_disability_capacity int DEFAULT 0,
                garage_lat VARCHAR(50),
                garage_lng VARCHAR(50),
                caculation_time_base_unit int DEFAULT 0 COMMENT '分:0/秒:1',
                charge_infomation VARCHAR(1000) NULL,
                supplementary_details VARCHAR(1000) NULL,
                business_hour_begin VARCHAR(5),
                business_hour_end VARCHAR(5),
                number_of_entrance int Default 0,
                number_of_exit int Default 0,
                number_of_driveway_in int Default 0,
                number_of_driveway_out int Default 0,
                management_type int Default 0 COMMENT '0:固定都有管理員/2:不定時巡視管理員/3:無管理員',
                garage_type int COMMENT '0:平面、1:車塔、2:機械、3:平面/機械混合、4:地下室',
                lot_type int COMMENT '室內還是室外停車場 室內:0/室外:1',
                establish_status int COMMENT '建置狀態 完成:0/建置中:1',
                max_clearance VARCHAR(5) COMMENT '車高限制',
                on_site_liaison VARCHAR(20) COMMENT '現場聯絡人',
                on_site_phone VARCHAR(20) COMMENT '現場聯絡電話',
                on_site_email VARCHAR(20) COMMENT '現場email',
                on_site_cell_phone VARCHAR(20) COMMENT '場站電話',
                customer_garage_id VARCHAR(20) COMMENT '客戶自己系統的場站id',
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                garage_id SERIAL PRIMARY KEY
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE garage_group (
                garage_group_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                garage_group_name VARCHAR(255) NULL,
                customer_id int,
                parent_id int,
                description VARCHAR(1000) NULL
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE entry_gate (
                entry_gate_id SERIAL PRIMARY KEY,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                customer_id int,
                garage_id int,
                entry_gate_sn int NULL,
                direction int DEFAULT 1 COMMENT 'entry_gate direction',
                has_e_envoicing int DEFAULT 1 COMMENT 'using electronic envoice',
                description VARCHAR(1000) NULL
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE map_garage_to_garage_group (
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                modified_date TIMESTAMP,
                create_account_id int,
                modified_account_id int,
                garage_id int,
                garage_group_id int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE map_garage_to_account (
                garage_id int,
                account_id int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE map_garage_group_to_account (
                garage_group_id int,
                account_id int
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE system_log (
                system_log_id SERIAL PRIMARY KEY,
                event_id int,
                create_account_id int,
                create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                event_message VARCHAR(255) NULL,
                query_string VARCHAR(255) NULL,
                field_1 VARCHAR(255)
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE event (
                event_id SERIAL PRIMARY KEY,
                SystemEventType int,
                event_subtype int,
                description VARCHAR(255) NULL
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('''CREATE TABLE trx_data (
                    import_date TIMESTAMP,
                    file_name varchar(54) NOT NULL default ' ',
                    trx_date varchar(8) NOT NULL default ' ',
                    trx_time varchar(6) NOT NULL default ' ',
                    card_no varchar(50) NOT NULL default ' ',
                    txn_no varchar(6) NOT NULL default '',
                    trx_amt int(11) default '0',
                    device_id varchar(10) default ' ',
                    trx_type varchar(2) default NULL,
                    trx_sub_type varchar(2) default NULL,
                    el_value int(11) default '0',
                    cal_date varchar(8) default ' ',
                    cal_status varchar(2) default ' ',
                    dept_id varchar(10) NOT NULL default '00',
                    unit_id varchar(2) NOT NULL default '02',
                    cal_err_code varchar(10) NOT NULL default '',
                    source_filename varchar(100),
                    garage_code varchar(20),
                    csv_file_date varchar(20),
                    trx_data_id SERIAL PRIMARY KEY,
                    create_date TIMESTAMP
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE parking (
                id int COMMENT '舊PMS parking_id',
                `pv` varchar(32) NOT NULL,
                `pv_out` varchar(32) NOT NULL,
                `card_id` varchar(32) NOT NULL,
                `card_id16` varchar(32) NOT NULL,
                `enter_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `exit_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `paid_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `duration` int(10) NOT NULL default '0',
                `fee` int(10) NOT NULL default '0',
                `real_fee` int(10) NOT NULL default '0',
                `note` text NOT NULL,
                `paid_type` varchar(2) NOT NULL default '00',
                `entry_balance` int(4) NOT NULL default '0' COMMENT '進場時卡片餘額',
                `exit_balance` int(4) NOT NULL default '0' COMMENT '出場時卡片餘額(扣款前)',
                `settlement_type` tinyint(3) NOT NULL default '0' COMMENT '1:待確認交易,2:ECC補寫log',
                `txn_datetime` datetime NOT NULL default '0000-00-00 00:00:00' COMMENT '待確認PV交易時間',
                `txn_amt` int(4) NOT NULL default '0' COMMENT '待確認交易金額',
                `disability_mode` tinyint(1) NOT NULL default '0' COMMENT '是否為身障計費(1:是,0:否)',
                `card_autoload_flag` tinyint(1) NOT NULL default '0' COMMENT '卡片自動加值FLAG',
                `entry_mode` tinyint(1) NOT NULL default '1' COMMENT '進場設備放行類別(0:無法辨識, 1:PV, 2:eTag, 3: 河南OBU, 4:車辨設備系統)',
                `last_source_filename` varchar(100),
                `garage_code` varchar(20),
                `last_csv_file_date` varchar(20),
                `parking_id` SERIAL PRIMARY KEY AUTO_INCREMENT,
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `vehicle_identification_number` varchar(10) default '000-0000',
                `modified_date` datetime COMMENT '資料修改日期',
                `vehicle_type` int(2) COMMENT '車類型 0:unknown,1:汽車,2:機車,3:卡車,4:腳踏車,5:沙石車,6:小貨車,7:休旅車,8:箱型車,9:電動機車,10:電動汽車,11:大客車,12:小巴,13:拖板車',
                `enter_account_id` int COMMENT '入場紀錄帳號',
                `exit_account_id` int COMMENT '出場紀錄帳號',
                `einvoice` varchar(20) COMMENT '電子發票號碼',
                `einvoice_use_status` tinyint(1) COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)'
                )DEFAULT CHARSET=utf8
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE ticket_provider (
                ticket_provider_id SERIAL PRIMARY KEY,
                company_name varchar(32) NOT NULL,
                type_id varchar(32) NOT NULL,
                ticket_provider_code varchar(32) NOT NULL COMMENT 'Acer ITS 定義票證業者代碼',
                provider_garage_code varchar(10)  COMMENT '場站編號(悠遊卡,一卡通)',
                provider_transaction_code varchar(10)  COMMENT '交易系統代碼(一卡通)',
                provider_system_code varchar(32) COMMENT '交易車種代碼(一卡通)',
                provider_transfer_code varchar(32) COMMENT '系統轉乘代碼(一卡通)',
                modified_account_id int,
                modified_date TIMESTAMP
                )DEFAULT CHARSET=utf8
            ''') 

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `map_garage_to_system_config` (
                `map_garage_to_system_config_id` int NOT NULL,
                `garage_id` int COMMENT '停車場站編號',
                `system_config_id` int COMMENT '系統設定編號',
                `modified_account_id` int,
                `modified_date` TIMESTAMP NOT NULL COMMENT '更新時間',
                PRIMARY KEY  (`map_garage_to_system_config_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='系統參數與停車廠站對應'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `system_config` (
                `report_title` varchar(60) NOT NULL COMMENT '報表名稱',
                `is_usb_mode_active` tinyint(1) unsigned NOT NULL default '0',
                `usb_version_id` varchar(4) NOT NULL,
                `pv_voice_value` varchar(2) NOT NULL default '0' COMMENT 'PV調整音量大小',
                `entry_balance_warning` int(4) NOT NULL default '0' COMMENT '進場餘額警示水位',
                `is_commutation_ticket_module_active` tinyint(1) NOT NULL default '0' COMMENT '定期票功能(1:啟用, 0:停用)',
                `commutation_ticket_sales_type` tinyint(1) NOT NULL default '0' COMMENT '1:只有汽車,2:只有機車,3:汽車+機車',
                `is_transfer_module_active` tinyint(1) NOT NULL default '0' COMMENT '轉乘優惠功能(1:啟用,0:停用)',
                `is_e_invoice_mode` tinyint(1) NOT NULL default '0' COMMENT '是否使用電子發票',
                `e_invoice_request_minimum` int(4) NOT NULL default '0' COMMENT '電子發票發動取號的最低數量',
                `is_java_server_mode` tinyint(1) NOT NULL default '0' COMMENT '是否為java socket server mode',
                `pv_alert_interval` int(4) NOT NULL default '0' COMMENT 'PV警告狀態顯示檢查間隔(單位:秒)',
                `monitor_response_time` int(10) unsigned NOT NULL COMMENT '監控不回應時間警示(單位:分鐘)',
                `is_calculator_parking_data` tinyint(1) NOT NULL default '0' COMMENT '更新PMS交易資料清分狀態',
                `is_check_accounting_and_email_notify` tinyint(1) NOT NULL default '0' COMMENT '自動對帳與發送通知',
                `is_support_multi_language` tinyint(1) NOT NULL default '0' COMMENT '是否開啟多國語言選取功能(1:是, 0:否)',
                `is_customize_disability_column_name` tinyint(1) NOT NULL default '0' COMMENT '身障計費試算欄位名稱是否客製(0:否, 1:是)',
                `is_invoice_record_number_mode` tinyint(1) NOT NULL default '0' COMMENT '是否啟用傳統發票號碼記錄',
                `invoice_paperroll_usable_number` int(4) NOT NULL default '0' COMMENT '發票紙捲可用張數',
                `invoice_alert_usable_number` int(4) NOT NULL default '0' COMMENT '發票紙捲剩餘張數警告通知',
                `is_commuter_ticket_check_entry_balance` tinyint(1) NOT NULL default '0' COMMENT '定期票進場是否檢查最低入場餘額',
                `is_fee_caculation_by_config` tinyint(1) NOT NULL default '0' COMMENT '計費規則參數化設定(1:啟用, 0:停用)',
                `is_human_pay_and_confirm_fix` tinyint(1) NOT NULL default '0' COMMENT '支援[人工結帳已付款]和[已扣款未回confirm狀態]旗標判定',
                `is_auto_add_value_card_check_entry_balance` tinyint(1) NOT NULL default '0' COMMENT '自動加值卡片檢查最低入場餘額(0:關,1:開)',
                `e_invoice_service_provider` tinyint(1) NOT NULL default '0' COMMENT '1:ChiefPay, 2:台灣聯通, 3:電子發票標準化介面',
                `is_support_gate_control` tinyint(1) NOT NULL default '0' COMMENT '是否支援遠端開閘',
                `acer_id` varchar(10),
                `config_name` varchar(60),
                `csv_file_date` varchar(10) COMMENT '解析csv檔案內容的資料來源日期',
                `modified_account_id` int,
                `modified_date` TIMESTAMP NOT NULL COMMENT '更新時間',
                `system_config_id` SERIAL PRIMARY KEY AUTO_INCREMENT 
                ) DEFAULT CHARSET=utf8 COMMENT='系統參數';
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `lane` (
                `garage_lane_id` int(10) NOT NULL,
                `pv` varchar(128) NOT NULL,
                `type` varchar(1) NOT NULL COMMENT '汽車道(c), 機車道(m)',
                `pricing_scheme` int(2) NOT NULL COMMENT '計費規則',
                `pv_ip` varchar(64) NOT NULL,
                `pv_netmask` varchar(64) NOT NULL,
                `pv_gateway` varchar(64) NOT NULL,
                `pms_ip` varchar(64) NOT NULL,
                `pms_port` int(10) NOT NULL,
                `ecc_ip` varchar(64) NOT NULL,
                `ecc_port` int(10) NOT NULL,
                `in_out` int(1) NOT NULL COMMENT '進或出車道 0:進, 1:出',
                `aisle` varchar(10) NOT NULL,
                `invoice` int(1) NOT NULL COMMENT '是否自動列印發票 0:不印, 1:要印',
                `cps_ip` varchar(64) NOT NULL,
                `pv_cutoff` varchar(4) NOT NULL COMMENT 'PV 的關機時間 Format: HHmm',
                `MEntryB` varchar(10) NOT NULL COMMENT'最小入場餘額 Format: 999.99',
                `MExitD` int(5) NOT NULL COMMENT'最長出場前緩衝時間',
                `pv_version` varchar(20) NOT NULL,
                `last_response_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `response_type` varchar(4) NOT NULL default '00',
                `invoice_printer_status` varchar(2) NOT NULL default '00' COMMENT 'ref [invoice_printer_error_def].code',
                `pricing_scheme_disability` int(2) NOT NULL default '0' COMMENT '身障計費規則',
                `pv_response_confirm` tinyint(1) NOT NULL default '0' COMMENT 'PV是否回傳confirm(1:是-新連線,0:否-舊連線',
                `etag_flag` tinyint(1) NOT NULL default '0' COMMENT '是否為eTag車道(1:是,0:否)',
                `costrule_using_para` tinyint(1) NOT NULL default '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
                `lane_costrule_mode` tinyint(1) NOT NULL default '0' COMMENT '車道計費模式(1:複合, 0:單一)',
                `gate_control_mode` tinyint(1) NOT NULL default '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
                `lpr_lane` varchar(4) NOT NULL default '99' COMMENT '車辨車道代碼',
                `source_filename` varchar(100),
                `garage_code` varchar(20),
                `csv_file_date` varchar(20),
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `lane_id` int(10) NOT NULL auto_increment,
                PRIMARY KEY  (`lane_id`),
                KEY `type` (`type`),
                KEY `pricing_scheme` (`pricing_scheme`),
                KEY `pv_ip` (`pv_ip`),
                KEY `MEntryB` (`MEntryB`),
                KEY `in_out` (`in_out`)
                ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `driveway` (
                `acer_id` varchar(5) NOT NULL COMMENT 'acer停車場編號',
                `pv_name` varchar(128) NOT NULL COMMENT 'PV 名稱',
                `type` varchar(1) NOT NULL COMMENT 'c:汽車道, m:機車道',
                `charge_rule` int(2)  COMMENT '計費規則',
                `pv_ip` varchar(64) NOT NULL COMMENT 'PV IP address',
                `pv_netmask` varchar(64) NOT NULL COMMENT 'PV Netmask address',
                `pv_gateway` varchar(64) COMMENT 'PV Default Gateway IP address',
                `pms_plus_ip` varchar(64) NOT NULL COMMENT 'PMS Plus IP',
                `pms_plus_port` int(10) NOT NULL COMMENT 'PMS Plus Port',
                `direction` int(1) NOT NULL COMMENT '車道方向 進或出車道 0:進, 1:出',
                `aisle` varchar(10) NOT NULL COMMENT '車道碼 如1,2,3,4 (車道序號)',
                `is_invoice_printing_enabled` int(1) NOT NULL COMMENT '是否自動列印發票 0:不印, 1:要印',
                `pv_turn_off_time` varchar(4) NOT NULL COMMENT 'PV 的關機時間 Format: HHmm',
                `minimun_entry_balance` varchar(10) NOT NULL COMMENT '最小入場餘額 Format: 999.99',
                `maximun_exit_buffer_minutes` int(5) NOT NULL COMMENT '最長出場前緩衝時間',
                `pv_version` varchar(20) NOT NULL COMMENT 'PV版本號碼',
                `pv_last_response_time` datetime NOT NULL COMMENT 'PV最後回應時間',
                `pv_response_type` varchar(4) NOT NULL default '00' COMMENT 'PV回應類型',
                `invoice_printer_status` varchar(2) NOT NULL default '00' COMMENT 'refer to [invoice_printer_error_def].code',
                `disability_charge_rule` int(2) NOT NULL default '0' COMMENT '身障計費規則',
                `is_etag_drvieway` tinyint(1) NOT NULL default '0' COMMENT '是否為eTag車道(1:是,0:否)',
                `is_charge_params_enabled` tinyint(1) NOT NULL default '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
                `driveway_charge_mode` tinyint(1) NOT NULL default '0' COMMENT '車道計費模式(1:複合, 0:單一)',
                `gate_control_mode` tinyint(1) NOT NULL default '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
                `car_recognition_driveway_code` varchar(4) NOT NULL default '99' COMMENT '車辨車道代碼',
                `driveway_id` SERIAL PRIMARY KEY AUTO_INCREMENT ,
                KEY `pv_name` (`pv_name`),
                KEY `type` (`type`),
                KEY `charge_rule` (`charge_rule`),
                KEY `pv_ip` (`pv_ip`),
                KEY `minimun_entry_balance` (`minimun_entry_balance`),
                KEY `direction` (`direction`)
                ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `real_time_transaction_data` (
                `real_time_transaction_data_id` int(11) NOT NULL auto_increment COMMENT '即時交易資料ID',
                `in_or_out` int(11) NOT NULL COMMENT '進離場類別(0:進場、1:離場)',
                `parking_type` int(11) NOT NULL default '0' COMMENT '臨時車或月租車(0:臨停車、1:月租車)',
                `card_id_16` varchar(30) NOT NULL COMMENT '票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)(卡內碼mifire)',
                `in_or_out_datetime` datetime NOT NULL COMMENT '進/出場日期時間 (ex. 201801082359)',
                `pay_datetime` datetime default NULL COMMENT '付費時間(ex. 201801082359)',
                `card_type` int(11) default NULL COMMENT '卡別(01:ECC,02:愛金,03:KRTC, /遠鑫:05 /99:人工結帳….).',
                `receivable` int(11) default NULL COMMENT '應收費用',
                `real_fees` int(11) default NULL COMMENT '實際費用',
                `before_pay_balance` int(11) default NULL COMMENT '卡片餘額(扣款前)   ',
                `is_disability` int(11) default '0' COMMENT '是否為身障計費(>0:身障計費規則id  0:否)',
                `vehicle_identification_number` varchar(10) NOT NULL COMMENT '車牌號碼',
                `pv_ip` varchar(15) NOT NULL COMMENT 'pv的ip',
                `garage_id` int(11)  COMMENT '場站代碼(acer define)',
                `customer_id` int(11) COMMENT '業者代碼(acer define)',
                `discount_type` int(11) default '0' COMMENT '0: 無優惠，1: 身障優惠，2: 折扣優惠',
                `discount_amount` int(11) default NULL COMMENT '優惠金額',
                `status_number` int(11) NOT NULL COMMENT '狀態碼，交易正常:0 異常:1',
                `vehicle_type` int(11) NOT NULL COMMENT '車種 0:unknown,1:汽車,2:機車,3:卡車,4:腳踏車,5:沙石車,6:小貨車,7:休旅車,8:箱型車,9:電動機車,10:電動汽車,11:大客車,12:小巴,13:拖板車',
                `einvoice` varchar(15) default NULL COMMENT '電子發票號碼',
                `einvoice_print_status` int(11) default NULL COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)',
                `tax_id_number` varchar(15) default NULL COMMENT '公司統編',
                `tax_id_number_buyer` varchar(15) default NULL COMMENT '買受人統編',
                `card_id_appearance` varchar(30) NOT NULL COMMENT '卡片卡號(卡片外碼)',
                `is_autoload` int(11) NOT NULL default '0' COMMENT '是否開啟自動加值功能(1:開啟,0:無)',
                `autoload_amout` int(11) NOT NULL default '0' COMMENT '自動加值金額 (default:0)',
                `error_message` varchar(500) NOT NULL default '' COMMENT '錯誤訊息(default:'')',
                `parking_id` int(11) NOT NULL COMMENT 'Parking資料ID',
                `create_account_id` int(11) default NULL,
                `create_date` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT 'create_date',
                `exit_type_config_detail_id` int(10)  COMMENT '出場設定id',
                `exit_type_config_detail_remarks` varchar(50) default NULL COMMENT '出場設定備註',
                `ibox_no` int(10) COMMENT 'IBox所使用的流水號',
                PRIMARY KEY  (`real_time_transaction_data_id`)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='即時交易資料' AUTO_INCREMENT=1
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `clock_time_card` (
                `id` int(11) NOT NULL auto_increment,
                `account_id` int(11) NOT NULL,
                `garage_id` int(11) NOT NULL,
                `customer_id` varchar(50) NOT NULL,
                `clock_in_time` datetime NOT NULL COMMENT '上班時間',
                `clock_out_time` datetime NOT NULL COMMENT '下班時間',
                `create_date` timestamp NULL default CURRENT_TIMESTAMP,
                `create_account_id` int(11) NOT NULL,
                PRIMARY KEY  (`id`)
                ) DEFAULT CHARSET=utf8 COMMENT='上下班打卡'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `parking_in_out_record` (
                `parking_in_out_record_id` int(11) NOT NULL,
                `state` varchar(2) NOT NULL COMMENT '進離場類別(0:進場、1:離場)',
                `trans_type` varchar(2) NOT NULL COMMENT '臨時車或月租車(0:臨停車、1:月租車)',
                `card_id` varchar(32) NOT NULL COMMENT '票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)',
                `entry_time` datetime NOT NULL COMMENT '進場日期時間',
                `exit_time` datetime NOT NULL COMMENT '離場日期時間',
                `car_number` varchar(16) NOT NULL COMMENT '車牌號碼',
                `parking_id` int(11) NOT NULL COMMENT '-->parking id',
                `paid_type` varchar(2) NOT NULL COMMENT '使用方式(票證、token、車辨...)',
                `update_time` datetime NOT NULL COMMENT '更新時間',
                `update_user` varchar(100) NOT NULL COMMENT '更新人員',
                `source_filename` varchar(100),
                `garage_code` varchar(20),
                `csv_file_date` varchar(20),
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `no` int(11) NOT NULL auto_increment COMMENT '流水號',
                PRIMARY KEY (`no`)
                ) DEFAULT CHARSET=utf8 COMMENT='PMS交易紀錄'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `e_invoice_number_data` (
                `no` bigint(20) NOT NULL,
                `tax_id` varchar(10) NOT NULL COMMENT '統編',
                `tax_id_buyer` varchar(10) default NULL COMMENT '買受人統編',
                `random_code` varchar(4) NOT NULL COMMENT '隨機碼',
                `use_year_month` varchar(6) NOT NULL COMMENT 'yyyyMM',
                `invoice_number` varchar(20) NOT NULL COMMENT '發票號碼',
                `einvoice_use_status` tinyint(1) NOT NULL default '0' COMMENT '0:印, 1:不印,2=存入載具,3=列印發票並打買受人統編',
                `donate_status` tinyint(1) NOT NULL default '0' COMMENT '捐贈狀態(0:不捐, 1:捐)',
                `sale_print_status` tinyint(1) NOT NULL default '0' COMMENT '銷貨清單列印狀態(0:不印, 1:印)',
                `preserve_code` varchar(20) default NULL COMMENT '愛心碼',
                `einvoice_device_no` varchar(20) default NULL COMMENT '載具編號',
                `txn_total_amt` int(4) NOT NULL default '0' COMMENT '交易金額',
                `invoice_amt` int(4) NOT NULL default '0' COMMENT '發票金額',
                `txn_date` varchar(8) default NULL COMMENT 'YYYYMMDD',
                `txn_time` varchar(6) default NULL COMMENT 'HHMMSS',
                `merchant_id` varchar(20) NOT NULL COMMENT '商家代號',
                `counter_id` varchar(20) NOT NULL COMMENT '門市(停車場)代號(舊PMS)',
                `pos_id` varchar(20) NOT NULL COMMENT '收銀機號',
                `batch_number` varchar(6) default NULL COMMENT '批號(車道編號)',
                `transaction_number` varchar(6) default NULL COMMENT '收銀機交易序號',
                `business_date` varchar(8) default NULL COMMENT '營業日',
                `process_status` tinyint(1) NOT NULL default '0' COMMENT '0:匯入, 1:銷售, 2:退貨(作廢), 3:折讓, 4:折讓取消, 5:註銷',
                `process_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `upload_status` tinyint(1) NOT NULL default '0' COMMENT '0:未上傳, 1:待上傳, 2:已上傳',
                `upload_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `use_status` tinyint(1) NOT NULL default '0' COMMENT '0:未使用, 1:已送出給PV',
                `use_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `sales_type` tinyint(1) NOT NULL default '0' COMMENT '0:parking id, 1:訂單',
                `sales_id` int(4) NOT NULL default '0' COMMENT 'parking id 或訂單id',
                `update_time` datetime NOT NULL default '0000-00-00 00:00:00',
                `update_user` varchar(100) NOT NULL,
                `source_filename` varchar(100),
                `garage_code` varchar(20),
                `csv_file_date` varchar(20),
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `garage_id` int NOT NULL,
                PRIMARY KEY  (`invoice_number`,`use_year_month`),
                KEY `proccess_status` (`process_status`),
                KEY `upload_status` (`upload_status`),
                KEY `use_status` (`use_status`),
                KEY `sales_id` (`sales_id`),
                KEY `counter_index` (`counter_id`,`tax_id`,`pos_id`,`merchant_id`)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8;
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `shift_checkout` (
                `checkout_no` varchar(20) NOT NULL COMMENT '結班條序號',
                `data_in_json` varchar(1000) NOT NULL COMMENT '結班資料in json type',
                `garage_id` int(11) NOT NULL COMMENT '場站ID',
                `customer_id` int(11) NOT NULL COMMENT '業者ID',
                `clock_in_time` datetime NOT NULL COMMENT '班別開始時間',
                `clock_out_time` datetime NOT NULL COMMENT '班別結束時間',
                `checkout_time` datetime NOT NULL COMMENT '結班時間',
                `checkout_amount` int(11) NOT NULL COMMENT '結帳（實收）金額',
                `number_of_vehicles` int(11) NOT NULL COMMENT '出場車輛數',
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_account_id` int(11) NOT NULL,
                `shift_checkout_id` int(11) NOT NULL auto_increment,
                PRIMARY KEY (`shift_checkout_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='平板結班資料'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `commutation_ticket_order` (
                `commutation_ticket_order_id` int(10) unsigned NOT NULL auto_increment,
                `card_id16` varchar(32) NOT NULL,
                `commutation_ticket_config_id` int(10) unsigned NOT NULL,
                `begin_date` datetime NOT NULL,
                `end_date` datetime NOT NULL,
                `customer_garage_id` varchar(32) NULL,
                `sale_amount` int(10) unsigned NOT NULL,
                `buyer_name` varchar(30) NOT NULL,
                `telephone` varchar(30) NOT NULL,
                `cellphone` varchar(30) ,
                `email` varchar(100) ,
                `address` varchar(100) ,
                `vehicle_plate_number` varchar(16) NOT NULL,
                `vehicle_color` varchar(16) ,
                `notes` varchar(200) NOT NULL,
                `order_status` int(3) unsigned NOT NULL default '1' COMMENT '1:售票, 2:註銷',
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `update_date` datetime default NULL,
                `update_reason` varchar(200) default NULL,
                `create_account_id` int(10) default '0' NOT NULL ,
                `update_account_id` int(10) default NULL,
                `garage_id` int(10) NOT NULL ,
                `customer_id` int(10) NOT NULL ,
                `unit_amount` int(10) default '1' COMMENT '買了幾個單位數量',
                `is_active` int(2) default '1' COMMENT '是否啟用',
                PRIMARY KEY (`commutation_ticket_order_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='定期票訂單'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `commutation_ticket_config` (
                `commutation_ticket_config_id` int(10) unsigned NOT NULL auto_increment,
                `commutation_ticket_config_name` varchar(60) NOT NULL COMMENT '票種名稱',
                `unit_sales` int(3) unsigned  NULL default '0' COMMENT '0:月, 1:天',
                `sales_num` int(10) unsigned NULL COMMENT '單位數量,ex :5 就是5天或5個月',
                `pay_amount` int(10) unsigned  NULL COMMENT '一單位多少錢',
                `vehicle_type` varchar(1) NULL COMMENT '車種類別(0:腳踏車,1:機車,2:重機,3:小型汽車sedan,4:wagon,5:truck,6: bus)',
                `customer_id` int(10) NOT NULL ,
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `update_date` datetime default NULL,
                `create_account_id` int(10) default '0' NOT NULL,
                `update_account_id` int(10) default NULL,
                `is_active` int(2) default '1' COMMENT '是否啟用',
                PRIMARY KEY  (`commutation_ticket_config_id`),
                key `commutation_ticket_config_id` (`commutation_ticket_config_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='定期票票種管理'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `commutation_ticket_period_config` (
                `commutation_ticket_period_config_id` int(10) unsigned NOT NULL auto_increment,
                `days_of_the_week`int(10) NOT NULL COMMENT '星期幾 (0-6)',
                `time_begin1` varchar(10) NOT NULL COMMENT '開始時間1',
                `time_end1` varchar(10) NOT NULL COMMENT '結束時間1',
                `time_begin2` varchar(10)  NULL COMMENT '開始時間2',
                `time_end2` varchar(10)  NULL COMMENT '結束時間2',
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `update_date` datetime default NULL,
                `create_account_id` int(10) default '0' NOT NULL,
                `update_account_id` int(10) default NULL,
                `commutation_ticket_config_id` int(10) NOT NULL COMMENT '票種id' ,
                `is_active` int(2) default '1' COMMENT '是否啟用',
                PRIMARY KEY  (`days_of_the_week` , `commutation_ticket_config_id`),
                key `commutation_ticket_period_config_id` (`commutation_ticket_period_config_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='定期票票種時段'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `garage_ftp_info` (
                `garage_code` varchar(20),
                `garage_name` varchar(20) NOT NULL COMMENT 'garage name',
                `ftp_ip` varchar(20) NOT NULL COMMENT 'ftp ip',
                `ftp_port` varchar(10)  NULL COMMENT 'ftp port',
                `ftp_userid` varchar(10)  NULL COMMENT 'fpt userid',
                `ftp_pwd` varchar(50)  NULL,
                `is_active` tinyint(3) NOT NULL default '0' COMMENT '0:啟用 1:停用',
                PRIMARY KEY  (`garage_code` ),
                key `garage_code` (`garage_code`)
                ) DEFAULT CHARSET=utf8 COMMENT='聯通各場站pms ftp 資料'
            ''')

            await conn.execute(''' CREATE TABLE customer_pv3_args (
            `customer_pv3_args_id` int(10) auto_increment,
            `market_code` varchar(3) COMMENT '特約機構代碼',
            `cashier_no` varchar(4) COMMENT '收銀員編號',
			`system_id` varchar(2) COMMENT '交易系統編號',
			`comp_id` varchar(2) COMMENT '停車場地點代碼/業者代碼',
			`machine` varchar(8) COMMENT '交易機器編碼',
			`ipass_water_lv_host` varchar(50) COMMENT '一卡通主機IP Host(須與主機端同步設定值須相同)',
			`ipass_water_lv_port` int(10) COMMENT '一卡通水位參數(須與主機端同步設定值須相同)',
			`socket_ip` varchar(50) COMMENT '參數設定 正式帶入172.21.1.101 測試帶入10.20.1.74',
            `transaction_system_id` varchar(2) COMMENT '交易系統編號',
			`loc_id` varchar(2) COMMENT '公司代碼',
			`transaction_terminal_no` varchar(8) COMMENT 'Terminal NO',
			`tid` varchar(8) COMMENT 'Terminal ID(BCD)',
			`mid` varchar(16) COMMENT '交易系統代碼',
			`YHDP_water_lv` int(10) COMMENT '水位參數',
			`YHDP_water_lv_host` varchar(50) COMMENT '遠鑫主機IP Host(須與主機端同步設定值須相同)',
			`YHDP_water_lv_port` int(5) COMMENT '遠鑫水位參數(須與主機端同步設定值須相同)',
			`nii` int(5) COMMENT '參數設定 正式帶入0688 測試 0667',
            `client_pv` varchar(50) COMMENT '設定同步時間 PV主機進站與出站IP',
            `time_sync_period` int(5) COMMENT '週期',
            `update_time` datetime NOT NULL COMMENT '最後更新時間',
            `update_user` varchar(200) COMMENT '最後更新使用者',
            `customer_id` int(5),
             PRIMARY KEY  (`customer_pv3_args_id`)
            ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE device_pv3_args (
            `device_pv3_args_id` int(10) auto_increment,
            `device_name` varchar(20) COMMENT '設備名稱 也是此設備資料夾名稱',
            `external_ip` varchar(20) COMMENT 'ibox external ip bind for iPass',
            `car_in` varchar(200) COMMENT '此站所有進場ip',
            `car_out` varchar(200) COMMENT '此站所有出場ip',
            `station_inout` int(5) COMMENT '該設置系統為進場或出場 1:in, 2:out',
            `ECC` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
            `iPass` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
            `iCash` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
            `YHDP` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
            `ip` varchar(200) COMMENT '設定該PV 主機IP 參數在開機時可以設定 IP Address',
            `mac_ip` varchar(20) COMMENT 'ibox mac ip',
            `eid_pos_no` varchar(20) COMMENT '立柱代碼 (for 發票EIDC 機制) 對應EIDC.txt 第三欄位',
            `update_time` datetime NOT NULL COMMENT '最後更新時間',
            `update_user` varchar(200) COMMENT '最後更新使用者',
            `garage_id` int(10),
             PRIMARY KEY  (`device_pv3_args_id`)
            ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' CREATE TABLE fee_rule (
            `fee_rule_id` int(10) auto_increment,
            `new_car_hour` int(10) COMMENT '場站初始以小時計費的時數',
            `period` int(10) COMMENT '多少分鐘計費一次(層級低於new_car_hour 需要new_car_hour時數結束 才會開始計算period參數)',
            `normal_day` varchar(200) COMMENT '調整特定日期 設定為平日',
            `holiday` varchar(200) COMMENT '調整特定日期 設定為假日',
            `free_time` int(5) COMMENT '贈送分鐘數',
            `fee_mode` int(5) COMMENT '費率計算模式 0: 當日最高計費模式 1: 24小時最高計費模式 2: 12小時最高計費模式 3: 單次計費模式 4: 單次計費(每天00:00:00重製) 5:單次計費(進場24小時後重製) 6:單次計費(進場12小時候重製)',
            `update_time` datetime NOT NULL COMMENT '最後更新時間',
            `update_user` varchar(200) COMMENT '最後更新使用者',
            `garage_id` int(10) COMMENT '對應場站PRIMARY KEY',
             PRIMARY KEY  (`fee_rule_id`)
            ) DEFAULT CHARSET=utf8  ''')

            await conn.execute(''' CREATE TABLE fee_para (
            `fee_para_id` int(10) auto_increment,
            `fee_para_mode` varchar(20) COMMENT '區分 平日 normal_day 還是假日 holiday',
            `hour_period_fee1` int(10) COMMENT '區段一收費價格',
            `hour_period_fee1_start` int(10) COMMENT '區段一起始時間',
            `hour_period_fee1_end` int(5) COMMENT '區段一結束時間',
            `hour_period_fee2` int(5) COMMENT '區段二收費價格',
            `hour_period_fee2_start` int(5) COMMENT '區段二起始時間',
            `hour_period_fee2_end` int(5) COMMENT '區段二結束時間',
            `max_fee` int(5) COMMENT '最高收費價格',
            `max_hour` int(5) COMMENT '最高計費時數',
            `special_rule` int(5) COMMENT '特別費率模式 0:關閉特別費率 1:啟用(截尾模式) 2:啟用(推遲模式)',
            `special_fee_start` int(5) COMMENT '特別費率起始時間',
            `special_fee_end` int(5) COMMENT '特別費率結束時間',
            `special_fee_max` int(5) COMMENT '特最高收費金額',
            `special_fee_hour` int(5) COMMENT '特別費率最高計費時數',
            `monthly_pass` int(5) COMMENT '!! 目前尚未使用 都給0 !! 月票模式 0:關閉特別費率 1:啟用(截尾模式) 2:啟用(推遲模式)',
            `update_time` datetime NOT NULL COMMENT '最後更新時間',
            `update_user` varchar(200) COMMENT '最後更新使用者',
            `fee_rule_id` int(10) COMMENT '對應費率規則 PRIMARY KEY',
             PRIMARY KEY  (`fee_para_id`)
            ) DEFAULT CHARSET=utf8 ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `pv3_log` (
            `pv3_log_id` int(10) unsigned NOT NULL auto_increment,
            `customer_id` int default NULL,
            `customer_garage_code` varchar(20) default NULL,
            `garage_code` varchar(20) default NULL,
            `ip_address` varchar(20),
            `mac_address` varchar(20),
            `category` varchar(20) COMMENT '自訂分類',
            `log_type` varchar(20) COMMENT '自訂類型',
            `message` varchar(20) NULL COMMENT '標準訊息',
            `field_1` varchar(20) NULL COMMENT '自訂訊息1',
            `field_2` varchar(20)  NULL,
            `field_3` varchar(20)  NULL,
            `field_4` varchar(50)  NULL,
            `field_5` varchar(2000)  NULL,
            `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY  (`pv3_log_id` ),
            key `pv3_log_id` (`pv3_log_id`)
            ) DEFAULT CHARSET=utf8 COMMENT='pv3錯誤及時訊息'
            ''')

            await conn.execute(''' CREATE TABLE garage_pv3_args (
            `garage_PV3_args_id` int(10) auto_increment,
            `garage_code` varchar(10) COMMENT 'Acer ITS defined garage code',
            `store_no` varchar(20) COMMENT '場站代碼',
            `pos_no` int(10) COMMENT 'pos代碼 目前是取該車道IP最後一碼 ex:192.168.200.203 -> 003',
            `eid_store_no` varchar(20) COMMENT '此站所有出場ip',
            `plid` varchar(4) COMMENT '該設置系統為進場或出場 1:in, 2:out',
            `printer` int(5) COMMENT '1為開啟SAM Card 讀取 0為關閉SAM Card讀取',
            `tax_id_num` varchar(20) COMMENT '賣方統編',
            `ntp_server` varchar(20) COMMENT '校時',
            `update_time` datetime NOT NULL COMMENT '最後更新時間',
            `update_user` varchar(200) COMMENT '最後更新使用者',
            `garage_id` int(10),
             PRIMARY KEY  (`garage_PV3_args_id`)
            ) DEFAULT CHARSET=utf8 ''')

            await conn.execute(''' ALTER TABLE trx_data ADD COLUMN  `update_date` datetime AFTER `cal_err_code` ''')
            await conn.execute(''' ALTER TABLE parking CHANGE `einvoice_use_status` `einvoice_print_status` tinyint(1) COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)' ''')
            await conn.execute(''' ALTER TABLE parking ADD COLUMN  `garage_id` int COMMENT '場站ID' ''')
            await conn.execute(''' ALTER TABLE parking ADD COLUMN  `record_status` tinyint(1) DEFAULT 1 COMMENT '此紀錄狀態 (1 = 正常, 0＝作廢（退費）)' AFTER `einvoice_print_status`  ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data change `pv_ip` `device_ip` varchar(15) NOT NULL COMMENT 'device_ip' ''')
            await conn.execute(''' ALTER TABLE e_invoice_number_data CHANGE `einvoice_use_status` `einvoice_print_status` tinyint(1) NOT NULL DEFAULT 0 COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)' ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data ADD COLUMN  `record_status` int(10) COMMENT '此紀錄狀態,0:作廢,1:正常' default 1  AFTER `ibox_no`  ''')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW parking_view AS SELECT `b`.`garage_code` AS `garage_code`, `b`.`id` AS `id`, `a`.`pv` AS `pv`, `b`.`pv_out` AS `pv_out`, `a`.`type` AS `type`, `a`.`pricing_scheme` AS `pricing_scheme`, `a`.`pricing_scheme_disability` AS `pricing_scheme_disability`, `b`.`card_id` AS `card_id`, `b`.`card_id16` AS `card_id16`, `b`.`enter_time` AS `enter_time`, `b`.`exit_time` AS `exit_time`, `b`.`paid_time` AS `paid_time`, `b`.`fee` AS `fee`, `b`.`real_fee` AS `real_fee`, `b`.`note` AS `note`, `b`.`paid_type` AS `paid_type`, `b`.`entry_balance` AS `entry_balance`, `b`.`exit_balance` AS `exit_balance`, `b`.`settlement_type` AS `settlement_type`, `b`.`disability_mode` AS `disability_mode`, `c`.`customer_id` AS `customer_id` FROM ((`parking` `b` LEFT JOIN `lane` `a` ON (((`a`.`pv` = `b`.`pv`) AND (`a`.`garage_code` = `b`.`garage_code`)))) LEFT JOIN `garage` `c` ON ((`a`.`garage_code` = `c`.`garage_code`)))')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''INSERT INTO `garage_ftp_info` VALUES ('081', '瑞二', '192.168.41.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('323', '汐科', '192.168.198.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('247', '大世界', '192.168.185.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('229', '阿曼TIT場', '192.168.173.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('084', '衡陽', '192.168.96.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('275', '日月潭中興', '192.168.33.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('132', '里昂', '192.168.91.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('357', '台中福星', '10.1.24.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('359', '昌隆', '10.1.26.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('349', '永科停一', '192.168.209.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('350', '永科停三', '192.168.210.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('351', '永科停四', '192.168.211.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('352', '永科停五', '192.168.212.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('353', '永科停六', '192.168.213.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('354', '永科停七', '192.168.214.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('355', '永科停八', '192.168.215.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('356', '桃園高明', '10.1.23.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('360', '台中文心', '10.1.27.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('361', '台南小北商場', '192.168.153.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('363', '力行', '172.16.21.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('321', '麗林', '192.168.196.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('341', '文化三', '10.1.22.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('347', '民視', '192.168.208.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('020', '克強', '192.168.135.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('034', '中興', '192.168.71.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('039', '安東', '192.168.62.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('079', '建國', '192.168.74.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('120', '成功', '192.168.54.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('151', '文德', '192.168.63.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('171', '文成', '192.168.63.210', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('254', '石潭', '192.168.192.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('296', '山仔頂', '192.168.164.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('210', '醒吾', '192.168.151.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('259', '宜蘭礁溪', '192.168.42.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('261', '光華商場', '192.168.82.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('082', '南京場', '192.168.55.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('346', '南門場', '192.168.53.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('031', '大千場', '192.168.57.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('324', '天祥場', '192.168.199.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('145', '行天宮場', '192.168.109.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('083', '前瞻場', '192.168.56.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('158', '博仁醫院場', '192.168.113.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('262', '士林官邸', '192.168.59.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('056', '統領', '192.168.75.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('272', '士商', '192.168.77.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('271', '桃園頂好', '192.168.99.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('234', '文湖', '192.168.170.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('246', '長慶', '192.168.184.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('255', '松山慈惠堂', '192.168.193.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('290', '宜蘭健康', '192.168.128.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('245', '頭份信東', '192.168.183.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('116', '大湳', '192.168.84.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('220', '中壢仁海宮', '192.168.161.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('115', '中壢長春', '192.168.51.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('301', '中壢新街', '192.168.107.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('243', '中壢環中', '192.168.182.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('207', '延平', '192.168.148.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('237', '桃園大有', '192.168.176.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('242', '桃園同安', '192.168.181.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('114', '桃園國際', '192.168.52.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('203', '桃園復興', '192.168.142.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('342', '桃園晶宴', '192.168.44.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('117', '龍潭', '192.168.86.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('252', '龜山', '192.168.190.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('131', '介壽', '192.168.89.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('133', '三峽', '192.168.92.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('330', '北大', '192.168.203.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('269', '土城中一', '192.168.98.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('250', '秀山', '192.168.188.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('052', '永一', '192.168.35.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('336', '汐止福德', '192.168.197.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('263', '四川路', '192.168.61.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('284', '府中', '192.168.121.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('316', '長江', '192.168.162.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('325', '華江', '192.168.115.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('307', '林口', '192.168.126.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('311', '淡大', '192.168.110.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('111', '淡水', '192.168.49.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('256', '關渡', '192.168.194.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('159', '安康', '192.168.114.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('195', '中莊', '192.168.132.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('218', '中華', '192.168.159.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('197', '中誠', '192.168.134.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('327', '榮華', '192.168.200.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('178', '頭前', '192.168.129.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('113', '重陽', '192.168.95.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('304', '台中清泉崗', '192.168.40.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('308', '第一廣場 ', '192.168.60.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('287', '台中昌平', '192.168.125.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('294', '台中逢甲', '192.168.156.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('235', '台中福雅', '192.168.174.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('278', '台灣大道', '192.168.117.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('198', '台中大忠', '192.168.139.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('344', '台中大益', '192.168.46.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('276', '台中五權三', '192.168.102.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('238', '台中大昌', '192.168.177.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('282', '台中大新', '192.168.45.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('348', '台中潭子', '192.168.133.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('295', '台南樹林', '192.168.81.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('326', '台南永康', '192.168.68.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('317', '台南安中', '192.168.130.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('216', '台南忠義', '192.168.157.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('309', '台南小東', '192.168.90.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('303', '台南東一', '192.168.94.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('302', '台南東和', '192.168.31.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('319', '台南莊敬', '192.168.141.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('297', '台南富農', '192.168.166.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('286', '台南裕農', '192.168.123.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('265', '埔里忠孝', '192.168.58.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('233', '埔里', '192.168.171.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('257', '南投草屯', '192.168.37.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('168', '高雄大順', '192.168.124.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('331', '高雄鼎義', '192.168.83.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('318', '高雄澄清', '192.168.140.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('312', '高雄寶三', '192.168.111.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('315', '高雄頂豐', '192.168.120.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('298', '台中綠園道', '192.168.144.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('313', '嘉義嘉南', '192.168.112.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('314', '嘉義嘉東', '192.168.118.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('340', '員林員生', '192.168.205.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('232', '員林華成', '192.168.169.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('285', '員榮', '192.168.122.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('240', '彰化永樂', '192.168.179.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('369', '臥龍', '10.1.30.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('268', '東方巨人', '192.168.85.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('291', '新竹公道五', '192.168.143.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('367', '新台五', '192.168.178.200', '21', 'transfer', 'transfer', 1);
                INSERT INTO `garage_ftp_info` VALUES ('370', '南投竹山', '10.1.31.200', '21', 'transfer', 'transfer', 0);
                INSERT INTO `garage_ftp_info` VALUES ('371', '高雄岡山', '10.1.32.200', '21', 'transfer', 'transfer', 0);
                        ''')

    async def v1_1(self):
        # 台灣聯通目前版本
        async with self.engine.acquire() as conn:
            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `device_event` (
                `device_event_id` int(10) unsigned NOT NULL auto_increment,
                `event_category` varchar(30) NOT NULL COMMENT '事件群組',
                `event_type` varchar(30) NOT NULL COMMENT '事件類型',
                `message` varchar(2000) COMMENT '事件訊息',
                `event_source` varchar(200) COMMENT '訊息來源',
                `source_ip_address` varchar(20) COMMENT '來源IP',
                `field_01` text COMMENT '特定欄位01',
                `field_02` varchar(200) COMMENT '特定欄位02',
                `field_03` varchar(200) COMMENT '特定欄位03',
                `field_04` varchar(200) COMMENT '特定欄位',
                `field_05` varchar(200) COMMENT '特定欄位',
                `update_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY  (`device_event_id`),
                key `device_event_id` (`device_event_id`)
                ) DEFAULT CHARSET=utf8 COMMENT='設備訊息log'
            ''')

            await conn.execute(''' ALTER TABLE real_time_transaction_data change `device_ip` `device_ip` varchar(15) NULL COMMENT 'device_ip' ''')
            await conn.execute(''' ALTER TABLE e_invoice_number_data CHANGE `einvoice_print_status` `einvoice_print_status` tinyint(1) NULL COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)' ''')
            await conn.execute(''' ALTER TABLE lane ADD COLUMN  `garage_id` int(10) COMMENT 'garage_id' AFTER `csv_file_date` ''')

    async def v1_11(self):
        async with self.engine.acquire() as conn:

            await conn.execute(''' 
            ALTER TABLE customer_ibox_args ADD COLUMN host_ip varchar(20) COMMENT 'aws ip';  
            ALTER TABLE customer_ibox_args ADD COLUMN host_port varchar(20) COMMENT 'aws port';
            ALTER TABLE customer_ibox_args ADD COLUMN host_user varchar(20) COMMENT 'aws account';
            ALTER TABLE customer_ibox_args ADD COLUMN host_pwd varchar(20) COMMENT 'aws password';
            ALTER TABLE device_ibox_args DROP COLUMN car_in;
            ALTER TABLE device_ibox_args DROP COLUMN car_out;
            ALTER TABLE customer_ibox_args DROP COLUMN client_pv;
            ALTER TABLE customer_ibox_args DROP COLUMN time_sync_period;
            ALTER TABLE device_ibox_args ADD COLUMN client_pv varchar(50) COMMENT '設定同步時間 PV主機進站與出站IP';
            ALTER TABLE device_ibox_args ADD COLUMN time_sync_period int(5) COMMENT '週期';
            ALTER TABLE device_ibox_args ADD COLUMN type varchar(20) COMMENT '設備類型 c:汽車 m:機車' AFTER `device_name`;
            ALTER TABLE device_pv3_args ADD COLUMN type varchar(20) COMMENT '設備類型 c:汽車 m:機車' AFTER `device_name`;
            ALTER TABLE garage_ibox_args CHANGE `pos_no` `pos_no` varchar(10) COMMENT 'pos代碼 目前是取該車道IP最後一碼 ex:192.168.200.203 -> 003';
            ALTER TABLE customer_ibox_args CHANGE `nii` `nii` varchar(5) COMMENT '參數設定 正式帶入0688 測試 0667';
            ''')

            await conn.execute(''' ALTER TABLE device_ibox_args CHANGE `mac_ip` `gateway` varchar(20) ''')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW device_view AS select pv as device_name, type, pv_ip as ip, pricing_scheme, pricing_scheme_disability, garage_code from lane union all select device_name, type, ip, "null" as pricing_scheme, "null" as pricing_scheme_disability, g.garage_code from device_ibox_args d left join garage g on d.garage_id = g.garage_id')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW new_parking_view AS SELECT `b`.`garage_code`, `b`.`id`, `a`.`device_name`, `b`.`pv_out`, `a`.`type`, `a`.`pricing_scheme`, `a`.`pricing_scheme_disability`, `b`.`card_id`, `b`.`card_id16`, `b`.`enter_time`, `b`.`exit_time`, `b`.`paid_time`, `b`.`fee`, `b`.`real_fee`, `b`.`note`, `b`.`paid_type`, `b`.`entry_balance`, `b`.`exit_balance`, `b`.`settlement_type`, `b`.`disability_mode`, `c`.`customer_id` FROM ((`parking` `b` LEFT JOIN `device_view` `a` ON (((`a`.`device_name` = `b`.`pv`) AND (`a`.`garage_code` = `b`.`garage_code`)))) LEFT JOIN `garage` `c` ON ((`a`.`garage_code` = `c`.`garage_code`)))')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue1` AS select left(`new_parking_view`.`paid_time`,10) AS `parking_date`,`new_parking_view`.`real_fee` AS `fee`,`new_parking_view`.`type` AS `type`,`new_parking_view`.`paid_type` AS `paid_type`,`new_parking_view`.`pv_out` AS `pv_out`,count(0) AS `cnt`, `new_parking_view`.`garage_code` from `new_parking_view` group by left(`new_parking_view`.`exit_time`,10),`new_parking_view`.`real_fee`,`new_parking_view`.`type`,`new_parking_view`.`paid_type`,`new_parking_view`.`pv_out`, `new_parking_view`.`garage_code` order by left(`new_parking_view`.`exit_time`,10),`new_parking_view`.`real_fee`')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue` AS select `day_revenue1`.`parking_date` AS `parking_date`,`day_revenue1`.`fee` AS `fee`,`day_revenue1`.`paid_type` AS `paid_type`,`day_revenue1`.`pv_out` AS `pv_out`,`day_revenue1`.`cnt` AS `cnt`,(`day_revenue1`.`fee` * `day_revenue1`.`cnt`) AS `subtotal`, `day_revenue1`.`garage_code` from `day_revenue1`')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum` AS select `day_revenue`.`parking_date` AS `parking_date`,`day_revenue`.`paid_type` AS `paid_type`,`day_revenue`.`pv_out` AS `pv_out`,sum(`day_revenue`.`cnt`) AS `total_cnt`,sum(`day_revenue`.`subtotal`) AS `total`, `day_revenue`.`garage_code` from `day_revenue` group by `day_revenue`.`parking_date`,`day_revenue`.`paid_type`,`day_revenue`.`pv_out`, `day_revenue`.`garage_code`')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_type` AS select `day_revenue1`.`parking_date` AS `parking_date`,`day_revenue1`.`fee` AS `fee`,`day_revenue1`.`paid_type` AS `paid_type`,`day_revenue1`.`pv_out` AS `pv_out`,`day_revenue1`.`cnt` AS `cnt`,(`day_revenue1`.`fee` * `day_revenue1`.`cnt`) AS `subtotal`,`day_revenue1`.`type` AS `type`, `day_revenue1`.`garage_code` from `day_revenue1`')
            await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum_type` AS select `day_revenue_type`.`parking_date` AS `parking_date`,sum(`day_revenue_type`.`cnt`) AS `total_cnt`,sum(`day_revenue_type`.`subtotal`) AS `total`,`day_revenue_type`.`type` AS `type`,`day_revenue_type`.`paid_type` AS `paid_type`,`day_revenue_type`.`pv_out` AS `pv_out`, `day_revenue_type`.`garage_code` from `day_revenue_type` group by `day_revenue_type`.`parking_date`,`day_revenue_type`.`type`,`day_revenue_type`.`paid_type`,`day_revenue_type`.`pv_out`, `day_revenue_type`.`garage_code`')
            # await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue0` AS select left(`parking_view`.`paid_time`,10) AS `parking_date`,`parking_view`.`real_fee` AS `fee`,`parking_view`.`type` AS `type`,`parking_view`.`paid_type` AS `paid_type`,`parking_view`.`pv_out` AS `pv_out`,count(0) AS `cnt`, `parking_view`.`garage_code` from `parking_view` group by left(`parking_view`.`exit_time`,10),`parking_view`.`real_fee`,`parking_view`.`type`,`parking_view`.`paid_type`,`parking_view`.`pv_out` order by left(`parking_view`.`exit_time`,10),`parking_view`.`real_fee`')
            # await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue` AS select `day_revenue0`.`parking_date` AS `parking_date`,`day_revenue0`.`fee` AS `fee`,`day_revenue0`.`paid_type` AS `paid_type`,`day_revenue0`.`pv_out` AS `pv_out`,`day_revenue0`.`cnt` AS `cnt`,(`day_revenue0`.`fee` * `day_revenue0`.`cnt`) AS `subtotal`, `day_revenue0`.`garage_code` from `day_revenue0`')
            # await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum` AS select `day_revenue`.`parking_date` AS `parking_date`,`day_revenue`.`paid_type` AS `paid_type`,`day_revenue`.`pv_out` AS `pv_out`,sum(`day_revenue`.`cnt`) AS `total_cnt`,sum(`day_revenue`.`subtotal`) AS `total`, `day_revenue`.`garage_code` from `day_revenue` group by `day_revenue`.`parking_date`,`day_revenue`.`paid_type`,`day_revenue`.`pv_out`')
            # await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_type` AS select `day_revenue0`.`parking_date` AS `parking_date`,`day_revenue0`.`fee` AS `fee`,`day_revenue0`.`paid_type` AS `paid_type`,`day_revenue0`.`pv_out` AS `pv_out`,`day_revenue0`.`cnt` AS `cnt`,(`day_revenue0`.`fee` * `day_revenue0`.`cnt`) AS `subtotal`,`day_revenue0`.`type` AS `type`, `day_revenue0`.`garage_code` from `day_revenue0`')
            # await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum_type` AS select `day_revenue_type`.`parking_date` AS `parking_date`,sum(`day_revenue_type`.`cnt`) AS `total_cnt`,sum(`day_revenue_type`.`subtotal`) AS `total`,`day_revenue_type`.`type` AS `type`,`day_revenue_type`.`paid_type` AS `paid_type`,`day_revenue_type`.`pv_out` AS `pv_out`, `day_revenue_type`.`garage_code` from `day_revenue_type` group by `day_revenue_type`.`parking_date`,`day_revenue_type`.`type`,`day_revenue_type`.`paid_type`,`day_revenue_type`.`pv_out`')
            await conn.execute(''' ALTER TABLE real_time_transaction_data CHANGE `record_status` `record_status` int(10) COMMENT '此紀錄狀態,0:作廢,1:正常,2:補開' default 1 ''')
            await conn.execute(''' ALTER TABLE parking CHANGE `record_status` `record_status` int(10) DEFAULT 1 COMMENT '此紀錄狀態,0:作廢,1:正常,2:補開'  ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data ADD COLUMN device_type int(5) DEFAULT 0 COMMENT '設備種類, 0:未知,1:pv3,2:pv,3:pad,4:ibox,5:abs' AFTER `ibox_no`; ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data ADD COLUMN device_id int(5) COMMENT '設備ID' AFTER `ibox_no`; ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data change COLUMN card_id_appearance card_id_appearance varchar(255) NOT NULL COMMENT '卡片卡號(卡片外碼)'; ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `ticket_transaction_ftp_config` (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `customer_id` int(10) NOT NULL,
                `card_type` varchar(2) NOT NULL,
                `ip_address` varchar(50) NOT NULL,
                `ip_port` int(5) NOT NULL,
                `account` varchar(50) NOT NULL,
                `password` varchar(50) NOT NULL,
                `upload_path` varchar(100) NOT NULL,
                `download_path` varchar(100) NOT NULL,
                `status` tinyint(1) NOT NULL,
                `create_user_id` int(10),
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `last_update_user_id` int(10) DEFAULT NULL,
                `last_update_time` datetime DEFAULT NULL,
                PRIMARY KEY (`id`)
                ) DEFAULT CHARSET=utf8 COMMENT='票證公司FTP設定'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `icash_config` (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `customer_id` int(10) NOT NULL COMMENT 'Acer ITS 業者ID',
                `garage_code` varchar(20) NOT NULL COMMENT 'Acer ITS 場站代碼',
                `icash_customer_tax_id` varchar(8) NOT NULL COMMENT 'iCash 特約機構統編',
                `icash_garage_code` varchar(8) NOT NULL COMMENT '門市對照碼',
                `icash_garage_name` varchar(30) NOT NULL COMMENT '門市全名',
                `icash_garage_abbreviated_name` varchar(10) NOT NULL COMMENT '門市簡稱',
                `icash_garage_effective_begin_date` int(8) NOT NULL COMMENT '生效起日',
                `icash_garage_effective_end_date` int(8) NOT NULL COMMENT '生效迄日',
                `icash_garage_opening_day` int(8) NOT NULL COMMENT '開幕日',
                `icash_garage_saleable_day` int(8) NOT NULL COMMENT '可販售日',
                `icash_garage_closing_day` int(8) NOT NULL COMMENT '關店日',
                `icash_garage_postal_code` varchar(8) NOT NULL COMMENT '郵遞區號',
                `icash_garage_address` varchar(60) NOT NULL COMMENT '地址',
                `icash_garage_telephone_area_code` varchar(3) NOT NULL COMMENT '電話區域碼',
                `icash_garage_telephone` varchar(12) NOT NULL COMMENT '電話',
                `status` tinyint(1) NOT NULL COMMENT '0:停用, 1:啟用',
                `create_user_id` int(10),
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `last_update_user_id` int(10) DEFAULT NULL,
                `last_update_time` datetime DEFAULT NULL,
                PRIMARY KEY (`id`)
                ) DEFAULT CHARSET=utf8 COMMENT='iCash票證交易檔設定'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `ipass_config` (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `customer_id` int(10) NOT NULL COMMENT 'Acer ITS 業者ID',
                `garage_code` varchar(20) NOT NULL COMMENT 'Acer ITS 場站代碼',
                `ipass_company_id` varchar(4) NOT NULL COMMENT 'iPass 業者代碼',
                `ipass_system_id` varchar(2) NOT NULL COMMENT 'iPass 系統類型代碼',
                `ipass_garage_code_decimal` int(5) NOT NULL COMMENT 'iPass 場站代碼(Dec)',
                `ipass_garage_code_hexadecmial` varchar(4) NOT NULL COMMENT 'iPass 場站代碼(Hex)',
                `status` tinyint(1) NOT NULL COMMENT '0:停用, 1:啟用',
                `create_user_id` int(10),
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `last_update_user_id` int(10) DEFAULT NULL,
                `last_update_time` datetime DEFAULT NULL,
                PRIMARY KEY (`id`)
                ) DEFAULT CHARSET=utf8 COMMENT='iPass票證交易檔設定'
            ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `happycash_config` (
                `id` int(10) NOT NULL AUTO_INCREMENT,
                `customer_id` int(10) NOT NULL COMMENT 'Acer ITS 業者ID',
                `garage_code` varchar(20) NOT NULL COMMENT 'Acer ITS 場站代碼',
                `happycash_source_id` varchar(2) NOT NULL COMMENT 'happycash 業者代碼',
                `happycash_garage_code` varchar(15) NOT NULL COMMENT 'happycash 場站代碼',
                `status` tinyint(1) NOT NULL COMMENT '0:停用, 1:啟用',
                `create_user_id` int(10),
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `last_update_user_id` int(10) DEFAULT NULL,
                `last_update_time` datetime DEFAULT NULL,
                PRIMARY KEY (`id`)
                ) DEFAULT CHARSET=utf8 COMMENT='happyCash票證交易檔設定'
            ''')

            await conn.execute(''' ALTER TABLE `trx_data` CHANGE COLUMN `device_id` `device_id` VARCHAR(20) NULL DEFAULT ' '; ''')
            await conn.execute(''' ALTER TABLE `trx_data` ADD COLUMN `upload_zip_name` VARCHAR(50) NULL AFTER `create_date`; ''')
            await conn.execute(''' ALTER TABLE `trx_data` ADD COLUMN `feedback_file_name` VARCHAR(50) NULL AFTER `upload_zip_name`; ''')

             
            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute(''' CREATE TABLE device_pad_args (
                `device_pad_args_id` int(10) auto_increment,
                `device_name` varchar(20) COMMENT '設備名稱',
                `android_id` varchar(50) COMMENT '設備android id',
                `pos_no` varchar(20) ,
                `device_ip` varchar(50) ,
                `device_key` varchar(50) COMMENT '啟動碼用',
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_user_id`  int(10)  COMMENT '新增使用者',
                `update_time` datetime  NULL COMMENT '最後更新時間',
                `update_user_id`  int(10)  COMMENT '最後更新使用者',
                `garage_id` int(10),
                PRIMARY KEY  (`device_pad_args_id`)
                ) DEFAULT CHARSET=utf8 ''')
                
            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute(''' CREATE TABLE garage_pad_args (
                `garage_pad_args_id` int(10) auto_increment,
                `garage_code` varchar(10) COMMENT 'Acer ITS defined garage code',
                `prepayment` tinyint(1) COMMENT '是否預付 1:true/0:false',
				`e_invoice_config_id`  int(10)  COMMENT '此場站使用發票設定id',
				`create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_user_id`  int(10)  COMMENT '新增使用者',
                `update_time` datetime NULL COMMENT '最後更新時間',
                `update_user_id` int(10) COMMENT '最後更新使用者',
                `garage_id` int(10),
                PRIMARY KEY  (`garage_pad_args_id`)
                ) DEFAULT CHARSET=utf8 ''')

            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute(''' CREATE TABLE customer_pad_args (
                `customer_ibox_args_id` int(10) auto_increment,
				`create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_user_id`  int(10)  COMMENT '新增使用者',
                `update_time` datetime  NULL COMMENT '最後更新時間',
                `update_user_id` int(10) COMMENT '最後更新使用者',
                `customer_id` int(10),
                PRIMARY KEY  (`customer_ibox_args_id`)
                ) DEFAULT CHARSET=utf8 ''')
            await conn.execute('SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO"')
            await conn.execute('''CREATE TABLE `activation_code` (
                `activation_code_id` INT NOT NULL AUTO_INCREMENT,
                `garage_id` INT NOT NULL,
                `device_key` VARCHAR(45) NOT NULL,
                `activation_code` VARCHAR(45) NOT NULL,
                `is_used` int(10) default '0' NOT NULL,
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_account_id` INT NULL,
                PRIMARY KEY (`activation_code_id`),
                UNIQUE INDEX `activation_code_UNIQUE` (`activation_code` ASC));
            ''')

            await conn.execute(''' ALTER TABLE system_log change COLUMN event_message event_message varchar(20000); ''')
            await conn.execute(''' ALTER TABLE garage_ibox_args CHANGE `plid` `plid` varchar(4) COMMENT '一卡通停車場代碼' ''')
            await conn.execute(''' ALTER TABLE fee_rule CHANGE `normal_day` `normal_day` varchar(500) COMMENT '調整特定日期 設定為平日' ''')
            await conn.execute(''' ALTER TABLE fee_rule CHANGE `holiday` `holiday` varchar(500) COMMENT '調整特定日期 設定為假日' ''')
            await conn.execute(''' ALTER TABLE device_ibox_args CHANGE `iCash` `slot1` int(5) COMMENT '卡槽1: 1為開啟SAM Card 讀取 0為關閉SAM Card讀取' ''')
            await conn.execute(''' ALTER TABLE device_ibox_args CHANGE `iPass` `slot2` int(5) COMMENT '卡槽2: 1為開啟SAM Card 讀取 0為關閉SAM Card讀取' ''')
            await conn.execute(''' ALTER TABLE device_ibox_args CHANGE `YHDP` `slot3` int(5) COMMENT '卡槽3: 1為開啟SAM Card 讀取 0為關閉SAM Card讀取' ''')
            await conn.execute(''' ALTER TABLE device_ibox_args CHANGE `ecc` `slot4` int(5) COMMENT '卡槽4: 1為開啟SAM Card 讀取 0為關閉SAM Card讀取' ''')
            await conn.execute(''' ALTER TABLE device_ibox_args ADD COLUMN card_order varchar(50) COMMENT '卡種順序' ''')
            await conn.execute('''
                CREATE TABLE special_day (
                special_day_id SERIAL PRIMARY KEY,
                date VARCHAR(20),
                year INT COMMENT '年分',
                day_type INT COMMENT '日期類型 1:假日 2:平日',
                day_description VARCHAR(50) COMMENT '日期描述'
                ) DEFAULT CHARSET=utf8
            ''')
            await conn.execute(''' 
                insert into special_day (date, year, day_type, day_description) values ("2018/2/15", 2018, 1, "除夕");
                insert into special_day (date, year, day_type, day_description) values ("2018/2/16", 2018, 1, "春節");
                insert into special_day (date, year, day_type, day_description) values ("2018/2/19", 2018, 1, "初四");
                insert into special_day (date, year, day_type, day_description) values ("2018/2/28", 2018, 1, "和平紀念日");
                insert into special_day (date, year, day_type, day_description) values ("2018/4/4", 2018, 1, "兒童節");
                insert into special_day (date, year, day_type, day_description) values ("2018/4/5", 2018, 1, "清明節");
                insert into special_day (date, year, day_type, day_description) values ("2018/4/6", 2018, 1, "清明連假");
                insert into special_day (date, year, day_type, day_description) values ("2018/5/1", 2018, 1, "勞動節");
                insert into special_day (date, year, day_type, day_description) values ("2018/6/18", 2018, 1, "端午節");
                insert into special_day (date, year, day_type, day_description) values ("2018/9/24", 2018, 1, "中秋節");
                insert into special_day (date, year, day_type, day_description) values ("2018/10/10", 2018, 1, "國慶日");
                insert into special_day (date, year, day_type, day_description) values ("2018/12/31", 2018, 1, "元旦連假");
                insert into special_day (date, year, day_type, day_description) values ("2018/12/22", 2018, 2, "元旦連假補假");
            ''')
            await conn.execute('''ALTER TABLE `device_pad_args` ADD COLUMN `car_type` VARCHAR(15) NULL DEFAULT 'c' COMMENT 'c:car/m:motocycle' AFTER `garage_id`;''')

            await conn.execute(''' DROP VIEW IF EXISTS device_view;
            CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost`
            SQL SECURITY DEFINER VIEW device_view AS
            select pv as device_name, type, pv_ip as ip, pricing_scheme, pricing_scheme_disability, garage_code , lane_id as device_id , '2'  as device_type ,garage_id,pv_ip as device_key
            from lane
            union all
            select device_name, type, ip, "null" as pricing_scheme, "null" as pricing_scheme_disability, g.garage_code ,device_ibox_args_id as device_id , '4'  as device_type,g.garage_id,ip as device_key
            from device_ibox_args d left join garage g on d.garage_id = g.garage_id
            union all
            select device_name, type, ip, "null" as pricing_scheme, "null" as pricing_scheme_disability, g.garage_code ,device_pv3_args_id as device_id ,'1'  as device_type,g.garage_id,ip as device_key
            from device_pv3_args p left join garage g on p.garage_id = g.garage_id
            union all
            select device_name, car_type as type, device_ip as ip, "null" as pricing_scheme, "null" as pricing_scheme_disability, g.garage_code ,device_pad_args_id as device_id ,'3'  as device_type,g.garage_id,device_key
            from device_pad_args pa left join garage g on pa.garage_id = g.garage_id ''')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW new_parking_view AS SELECT `b`.`garage_code`, `b`.`id`, `a`.`device_name`, `b`.`pv_out`, `a`.`type`, `a`.`pricing_scheme`, `a`.`pricing_scheme_disability`, `b`.`card_id`, `b`.`card_id16`, `b`.`enter_time`, `b`.`exit_time`, `b`.`paid_time`, `b`.`fee`, `b`.`real_fee`, `b`.`note`, `b`.`paid_type`, `b`.`entry_balance`, `b`.`exit_balance`, `b`.`settlement_type`, `b`.`disability_mode`, `c`.`customer_id` FROM ((`parking` `b` LEFT JOIN `device_view` `a` ON (((`a`.`device_name` = `b`.`pv`) AND (`a`.`garage_code` = `b`.`garage_code`)))) LEFT JOIN `garage` `c` ON ((`a`.`garage_code` = `c`.`garage_code`)))')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue1` AS select left(`new_parking_view`.`paid_time`,10) AS `parking_date`,`new_parking_view`.`real_fee` AS `fee`,`new_parking_view`.`type` AS `type`,`new_parking_view`.`paid_type` AS `paid_type`,`new_parking_view`.`pv_out` AS `pv_out`,count(0) AS `cnt`, `new_parking_view`.`garage_code` from `new_parking_view` group by left(`new_parking_view`.`exit_time`,10),`new_parking_view`.`real_fee`,`new_parking_view`.`type`,`new_parking_view`.`paid_type`,`new_parking_view`.`pv_out`, `new_parking_view`.`garage_code` order by left(`new_parking_view`.`exit_time`,10),`new_parking_view`.`real_fee`')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue` AS select `day_revenue1`.`parking_date` AS `parking_date`,`day_revenue1`.`fee` AS `fee`,`day_revenue1`.`paid_type` AS `paid_type`,`day_revenue1`.`pv_out` AS `pv_out`,`day_revenue1`.`cnt` AS `cnt`,(`day_revenue1`.`fee` * `day_revenue1`.`cnt`) AS `subtotal`, `day_revenue1`.`garage_code` from `day_revenue1`')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum` AS select `day_revenue`.`parking_date` AS `parking_date`,`day_revenue`.`paid_type` AS `paid_type`,`day_revenue`.`pv_out` AS `pv_out`,sum(`day_revenue`.`cnt`) AS `total_cnt`,sum(`day_revenue`.`subtotal`) AS `total`, `day_revenue`.`garage_code` from `day_revenue` group by `day_revenue`.`parking_date`,`day_revenue`.`paid_type`,`day_revenue`.`pv_out`, `day_revenue`.`garage_code`')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_type` AS select `day_revenue1`.`parking_date` AS `parking_date`,`day_revenue1`.`fee` AS `fee`,`day_revenue1`.`paid_type` AS `paid_type`,`day_revenue1`.`pv_out` AS `pv_out`,`day_revenue1`.`cnt` AS `cnt`,(`day_revenue1`.`fee` * `day_revenue1`.`cnt`) AS `subtotal`,`day_revenue1`.`type` AS `type`, `day_revenue1`.`garage_code` from `day_revenue1`')
        await conn.execute('CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_revenue_sum_type` AS select `day_revenue_type`.`parking_date` AS `parking_date`,sum(`day_revenue_type`.`cnt`) AS `total_cnt`,sum(`day_revenue_type`.`subtotal`) AS `total`,`day_revenue_type`.`type` AS `type`,`day_revenue_type`.`paid_type` AS `paid_type`,`day_revenue_type`.`pv_out` AS `pv_out`, `day_revenue_type`.`garage_code` from `day_revenue_type` group by `day_revenue_type`.`parking_date`,`day_revenue_type`.`type`,`day_revenue_type`.`paid_type`,`day_revenue_type`.`pv_out`, `day_revenue_type`.`garage_code`')
        await conn.execute('''
            ALTER TABLE exit_type_config_detail ADD COLUMN `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
            ALTER TABLE exit_type_config_detail ADD COLUMN `update_time` TIMESTAMP ;
        ''')

    async def v1_12(self):
        async with self.engine.acquire() as conn:
            await conn.execute("ALTER TABLE garage_ibox_args DROP COLUMN pos_no;")
            await conn.execute("ALTER TABLE device_ibox_args ADD COLUMN pos_no varchar(10) COMMENT 'pos代碼 目前是取該車道IP最後一碼 ex:192.168.200.203 -> 003';")

    async def v1_3(self):
        async with self.engine.acquire() as conn:
            await conn.execute('''
                CREATE TABLE `e_invoice_config` (
                `e_invoice_config_id` int(4) NOT NULL auto_increment COMMENT '流水號',
                `eidc_merchant_code` varchar(20) NOT NULL COMMENT 'EIDC用場站編號',
                `merchant_id` varchar(20) NOT NULL COMMENT '業者場站編號/門市代碼',
                `cashier_id` varchar(20) NOT NULL COMMENT '收銀機編號/pos_no',
                `garage_name` varchar(20) NOT NULL COMMENT '停車場名稱',
                `acer_garage_id` varchar(20) NOT NULL COMMENT 'acer的場次編號5碼',
                `tax_id` varchar(10) NOT NULL COMMENT '賣方統編',
                `qrcode_encrypt_key` varchar(32) NOT NULL default 'acer_pms_aes_key' COMMENT '產生QR code的AES KEY',
                `set_execute_time` datetime default '2014-01-01 00:00:00' COMMENT '執行起日',
                `txn_file_upload_flag` tinyint(4) COMMENT '是否產生/更新交易檔案(0:否, 1:是)',
                `txn_file_upload_interval` int(4) COMMENT '產生/更新交易檔案時間間隔',
                `txn_file_import_folder` varchar(100) COMMENT '匯入交易檔案預設路徑',
                `txn_file_upload_folder` varchar(100) COMMENT '產生/更新交易檔案預設路徑',
                `txn_file_backup_folder` varchar(100) COMMENT '產生/更新交易檔案備份路徑',
                `web_url` varchar(1000)  COMMENT '電子發票後台網址',
                `web_api_key` varchar(1000)  COMMENT '電子發票後台啟動碼',
                `web_login_account` varchar(100)  COMMENT '電子發票後台登入帳號',
                `web_login_pwd` varchar(100) COMMENT '電子發票後台登入密碼',
                `ftp_upload_address` varchar(100) COMMENT '上傳發票交易交易檔ftp位置',
                `ftp_upload_port` varchar(100)  COMMENT '上傳發票交易ftp port',
                `ftp_login_account` varchar(100)  COMMENT 'ftp帳號',
                `ftp_login_pwd` varchar(100)  COMMENT 'ftp密碼',
                `ftp_down_path` varchar(100)  COMMENT 'ftp download path',
                `ftp_up_path` varchar(100) COMMENT 'ftp updateload path',
                `customer_id` int(10) NOT NULL ,
                `is_used` int(10) default 1 NOT NULL COMMENT '是否使用' ,
                `create_time` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `create_user_id` int(10)  COMMENT '新增使用者',
                `update_time` datetime  COMMENT '更新時間',
                `update_user_id` int(10)  COMMENT '更新使用者',
                PRIMARY KEY  (`e_invoice_config_id`)
                ) ENGINE=MyISAM  DEFAULT CHARSET=utf8 COMMENT='電子發票設定 ' AUTO_INCREMENT=1 ;
            ''')
            await conn.execute(''' ALTER TABLE fee_rule ADD COLUMN car_type varchar(20) COMMENT '車道類型 c:汽車, m:機車, t:大客車' ''')
            await conn.execute(''' ALTER TABLE fee_rule ADD COLUMN fee_args_name varchar(20) COMMENT '費率名稱' ''')
            await conn.execute(''' 
                insert into system_configuration values ('API_url', 'ec2-35-163-187-179.us-west-2.compute.amazonaws.com', 'API 網址', 'API_config');
                insert into system_configuration values ('API_port', '84', 'API port號', 'API_config');
                insert into system_configuration values ('API_account', 'root', 'API 帳號', 'API_config');
                insert into system_configuration values ('API_pwd', '@@123qwe', 'API密碼', 'API_config');
            ''')

            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_sedan int COMMENT '汽車剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_suv int COMMENT 'UV剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_bicycle int COMMENT '腳踏車剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_motocycle int COMMENT '機車剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_truck int COMMENT '卡車剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_bus int COMMENT '客運剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_total int COMMENT '總剩餘車位' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN gov_id varchar(30) COMMENT '政府id' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_update_account_id int COMMENT '剩餘車位更新帳號' ''')
            await conn.execute(''' ALTER TABLE garage ADD COLUMN current_capacity_updatetime timestamp COMMENT '更新日期' ''')
            await conn.execute("CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@localhost SQL SECURITY DEFINER VIEW day_enter_flow AS select pv, left(enter_time, 13) AS enter_date, count(0) AS cnt ,garage_code from parking  group by left(enter_time, 13), garage_code;")
            await conn.execute("CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@localhost SQL SECURITY DEFINER VIEW day_exit_flow AS select pv, left(exit_time,13) AS exit_date, count(0) AS cnt, garage_code from parking where (exit_time > '0000-00-00 00:00:00') group by left(exit_time,13), garage_code;")
            await conn.execute("CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `day_usage` AS select `a`.`pv` AS `pv`,`a`.`enter_date` AS `enter_date`,`b`.`exit_date` AS `exit_date`, if(isnull(`a`.`cnt`),0,`a`.`cnt`) AS `enter_cnt`, if(isnull(`b`.`cnt`),0,`b`.`cnt`) AS `exit_cnt`,(if(isnull(`a`.`cnt`),0,`a`.`cnt`) - if(isnull(`b`.`cnt`),0,`b`.`cnt`)) AS `cnt`, `a`.`garage_code` AS `garage_code` from (`day_enter_flow` `a` left join `day_exit_flow` `b`  on(((`a`.`enter_date` = `b`.`exit_date`) and (`a`.`garage_code` = `b`.`garage_code`)))) union select `a`.`pv` AS `pv`,`a`.`enter_date` AS `enter_date`,`b`.`exit_date` AS `exit_date`, if(isnull(`a`.`cnt`),0,`a`.`cnt`) AS `a_cnt`,if(isnull(`b`.`cnt`),0,`b`.`cnt`) AS `b_cnt`, (if(isnull(`a`.`cnt`),0,`a`.`cnt`) - if(isnull(`b`.`cnt`),0,`b`.`cnt`)) AS `cnt`,`b`.`garage_code` AS `garage_code` from (`day_exit_flow` `b` left join `day_enter_flow` `a` on(((`a`.`enter_date` = `b`.`exit_date`) and (`a`.`garage_code` = `b`.`garage_code`))));")
            await conn.execute("CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW hour_car_cnt AS select if(isnull(day_usage.enter_date),day_usage.exit_date,day_usage.enter_date) AS the_hour, sum(day_usage.cnt) AS car_sum, day_usage.garage_code from day_usage group by if(isnull(day_usage.enter_date),day_usage.exit_date,day_usage.enter_date),day_usage.garage_code")
            await conn.execute("CREATE OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `hour_car_csum` AS select `b`.`the_hour` AS `the_hour`,`b`.`car_sum` AS `car_sum`,(select sum(`a`.`car_sum`) AS `sum(``a``.``car_sum``)` from `hour_car_cnt` `a` where (`a`.`the_hour` <= `b`.`the_hour` and a.garage_code = b.garage_code)) AS `car_csum`, garage_code from `hour_car_cnt` `b`;")
            await conn.execute("""
                DROP view IF EXISTS new_parking_view ;
                CREATE 
                    ALGORITHM = UNDEFINED 
                    DEFINER = `root`@`localhost` 
                    SQL SECURITY DEFINER
                VIEW `new_parking_view` AS
                    SELECT 
                        `b`.`garage_code` AS `garage_code`,
                        `b`.`id` AS `id`,
                        `a`.`device_name` AS `device_name`,
                        `b`.`pv_out` AS `pv_out`,
                        `a`.`type` AS `type`,
                        `a`.`pricing_scheme` AS `pricing_scheme`,
                        `a`.`pricing_scheme_disability` AS `pricing_scheme_disability`,
                        `b`.`card_id` AS `card_id`,
                        `b`.`card_id16` AS `card_id16`,
                        `b`.`enter_time` AS `enter_time`,
                        `b`.`exit_time` AS `exit_time`,
                        `b`.`paid_time` AS `paid_time`,
                        `b`.`fee` AS `fee`,
                        `b`.`real_fee` AS `real_fee`,
                        `b`.`note` AS `note`,
                        `b`.`paid_type` AS `paid_type`,
                        `b`.`entry_balance` AS `entry_balance`,
                        `b`.`exit_balance` AS `exit_balance`,
                        `b`.`settlement_type` AS `settlement_type`,
                        `b`.`disability_mode` AS `disability_mode`,
                        `c`.`customer_id` AS `customer_id`,
                        `b`.`record_status` AS `record_status`
                    FROM
                        ((`parking` `b`
                        LEFT JOIN `device_view` `a` ON (((`a`.`device_name` = `b`.`pv`)
                            AND (`a`.`garage_code` = `b`.`garage_code`))))
                        LEFT JOIN `garage` `c` ON ((`a`.`garage_code` = `c`.`garage_code`)))
            """)
            await conn.execute("""
                DROP view IF EXISTS day_revenue1 ;
                CREATE 
                    ALGORITHM = UNDEFINED 
                    DEFINER = `root`@`localhost` 
                    SQL SECURITY DEFINER
                VIEW `day_revenue1` AS
                    SELECT 
                        LEFT(`new_parking_view`.`paid_time`, 10) AS `parking_date`,
                        `new_parking_view`.`real_fee` AS `fee`,
                        `new_parking_view`.`type` AS `type`,
                        `new_parking_view`.`paid_type` AS `paid_type`,
                        `new_parking_view`.`pv_out` AS `pv_out`,
                        COUNT(0) AS `cnt`,
                        `new_parking_view`.`garage_code` AS `garage_code`
                    FROM
                        `new_parking_view`
                    WHERE
                        ((`new_parking_view`.`record_status` <> '0')
                            AND (`new_parking_view`.`record_status` <> '2'))
                    GROUP BY LEFT(`new_parking_view`.`exit_time`, 10) , `new_parking_view`.`real_fee` , `new_parking_view`.`type` , `new_parking_view`.`paid_type` , `new_parking_view`.`pv_out` , `new_parking_view`.`garage_code`
                    ORDER BY LEFT(`new_parking_view`.`exit_time`, 10) , `new_parking_view`.`real_fee`
            """)

            await conn.execute('''
                CREATE PROCEDURE alter_table_ticket_transaction() 
                BEGIN
                IF NOT EXISTS( SELECT NULL
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ticket_transaction_ftp_config'
                            AND column_name = 'icash_customer_tax_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ticket_transaction_ftp_config` ADD COLUMN `icash_customer_tax_id` VARCHAR(8) NULL COMMENT 'iCash 特約機構統編' AFTER `download_path`;
                END IF;
                IF NOT EXISTS( SELECT NULL
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ticket_transaction_ftp_config'
                            AND column_name = 'ipass_company_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ticket_transaction_ftp_config` ADD COLUMN `ipass_company_id` VARCHAR(4) NULL COMMENT 'iPass 業者代碼' AFTER `icash_customer_tax_id`;
                END IF;
                IF NOT EXISTS( SELECT NULL
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ticket_transaction_ftp_config'
                            AND column_name = 'ipass_system_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ticket_transaction_ftp_config` ADD COLUMN `ipass_system_id` VARCHAR(2) NULL COMMENT 'iPass 系統類型代碼' AFTER `ipass_company_id`;
                END IF;
                IF NOT EXISTS( SELECT NULL
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ticket_transaction_ftp_config'
                            AND column_name = 'happycash_source_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ticket_transaction_ftp_config` ADD COLUMN `happycash_source_id` VARCHAR(2) NULL COMMENT 'happycash 業者代碼' AFTER `ipass_system_id`;
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'icash_config'
                            AND column_name = 'icash_customer_tax_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `icash_config` DROP COLUMN `icash_customer_tax_id`;
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'icash_config'
                            AND column_name = 'garage_code'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `icash_config` CHANGE COLUMN `garage_code` `garage_id` int(10) NOT NULL COMMENT 'Acer ITS 場站ID',
                ADD UNIQUE INDEX `garage_id_UNIQUE` (`garage_id` ASC);
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ipass_config'
                            AND column_name = 'ipass_system_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ipass_config` DROP COLUMN `ipass_system_id`;
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ipass_config'
                            AND column_name = 'ipass_company_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ipass_config` DROP COLUMN `ipass_company_id`;
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'ipass_config'
                            AND column_name = 'garage_code'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `ipass_config` CHANGE COLUMN `garage_code` `garage_id` int(10) NOT NULL COMMENT 'Acer ITS 場站ID',
                ADD UNIQUE INDEX `garage_id_UNIQUE` (`garage_id` ASC);
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'happycash_config'
                            AND column_name = 'happycash_source_id'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `happycash_config` DROP COLUMN `happycash_source_id`;
                END IF;
                IF EXISTS( SELECT *
                            FROM INFORMATION_SCHEMA.COLUMNS
                            WHERE table_name = 'happycash_config'
                            AND column_name = 'garage_code'
                            AND TABLE_SCHEMA = (SELECT database()) )  THEN
                ALTER TABLE `happycash_config` CHANGE COLUMN `garage_code` `garage_id` int(10) NOT NULL COMMENT 'Acer ITS 場站ID',
                ADD UNIQUE INDEX `garage_id_UNIQUE` (`garage_id` ASC);
                END IF;
                ALTER TABLE `ticket_transaction_ftp_config` CHANGE COLUMN `customer_id` `customer_id` int(10) NOT NULL COMMENT 'Acer ITS 業者ID',
                CHANGE COLUMN `card_type` `card_type` varchar(2) NOT NULL COMMENT '交易票種',
                CHANGE COLUMN `ip_address` `ip_address` varchar(50) NOT NULL COMMENT 'FTP主機',
                CHANGE COLUMN `ip_port` `ip_port` int(5) NOT NULL COMMENT 'FTP port',
                CHANGE COLUMN `account` `account` varchar(50) NOT NULL COMMENT 'FTP帳號',
                CHANGE COLUMN `password` `password` varchar(50) NOT NULL COMMENT 'FTP密碼',
                CHANGE COLUMN `upload_path` `upload_path` varchar(100) NOT NULL COMMENT '檔案上傳路徑',
                CHANGE COLUMN `download_path` `download_path` varchar(100) NOT NULL COMMENT '檔案下載路徑';
                END ;''')
            await conn.execute('''CALL alter_table_ticket_transaction; ''')
            await conn.execute('''DROP PROCEDURE alter_table_ticket_transaction; ''')
            await conn.execute(''' ALTER TABLE real_time_transaction_data CHANGE `record_status` `record_status` int(10) COMMENT '此紀錄狀態,0:作廢,1:正常,2:補開(補開是因為晚上結班前會讓所有車子以零元出場 隔天車主來取車時再以補開開一張有金額的發票)' default 1 ''')
            await conn.execute(''' ALTER TABLE parking CHANGE `record_status` `record_status` int(10) DEFAULT 1 COMMENT '此紀錄狀態,0:作廢,1:正常,2:補開(補開是因為晚上結班前會讓所有車子以零元出場 隔天車主來取車時再以補開開一張有金額的發票)'  ''')
            await conn.execute('''
                ALTER TABLE e_invoice_config DROP COLUMN txn_file_upload_flag;


                ALTER TABLE e_invoice_config 
                DROP COLUMN web_login_account;


                ALTER TABLE e_invoice_config 
                DROP COLUMN web_login_pwd;


                ALTER TABLE e_invoice_config 
                DROP COLUMN ftp_login_account;


                ALTER TABLE e_invoice_config 
                DROP COLUMN ftp_login_pwd;


                ALTER TABLE e_invoice_config 
                DROP COLUMN ftp_down_path;


                ALTER TABLE e_invoice_config 
                DROP COLUMN ftp_up_path;


                ALTER TABLE e_invoice_config 
                CHANGE COLUMN txn_file_import_folder txn_file_import_folder VARCHAR(100) DEFAULT NULL COMMENT '取號檔路徑';


                ALTER TABLE e_invoice_config 
                CHANGE COLUMN customer_id customer_id VARCHAR(10) NOT NULL;


                ALTER TABLE e_invoice_config 
                ADD COLUMN txn_file_upload_via VARCHAR(10) DEFAULT NULL COMMENT '如何上傳發票交易檔(0:API/1:FTP)';


                ALTER TABLE e_invoice_config 
                ADD COLUMN txn_file_generate_flag VARCHAR(10) DEFAULT NULL COMMENT '是否產生/更新交易檔案(0:否, 1:是)';


                ALTER TABLE e_invoice_config 
                ADD COLUMN api_txn_upload_url VARCHAR(1000) DEFAULT NULL COMMENT '上傳交易檔後台ＡＰＩ啟動碼';


                ALTER TABLE e_invoice_config 
                ADD COLUMN api_txn_upload_key VARCHAR(1000) DEFAULT NULL COMMENT '上傳交易檔ＡＰＩ ＫＥＹ';


                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_upload_login_account VARCHAR(100) DEFAULT NULL COMMENT 'ftp帳號';


                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_upload_login_pwd VARCHAR(100) DEFAULT NULL COMMENT 'ftp updateload path';


                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_upload_path VARCHAR(100) DEFAULT NULL;


                ALTER TABLE e_invoice_config 
                ADD COLUMN txn_file_upload_setting VARCHAR(10) DEFAULT NULL COMMENT '交易檔案上傳方式(0:由發票廠商程式上傳/1:由場站上傳發票廠商/2:由場站上傳PMS+,PMS+上傳發票廠商)';


                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_get_number_address VARCHAR(100) DEFAULT NULL COMMENT '取號FTP主機位置';


                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_get_number_login_pwd VARCHAR(100) DEFAULT NULL COMMENT '取號FTP密碼';

                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_get_number_port VARCHAR(100) DEFAULT NULL COMMENT '取號FTP PORT';

                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_get_number_login_account VARCHAR(100) DEFAULT NULL COMMENT '取號FTP帳號';

                ALTER TABLE e_invoice_config 
                ADD COLUMN ftp_get_number_down_path VARCHAR(100) DEFAULT NULL COMMENT '下載發票取號檔FTP位置';

                ALTER TABLE e_invoice_config 
                ADD COLUMN get_number_setting VARCHAR(10) DEFAULT NULL COMMENT '取號方式(0:由發票廠商程式配號/1:由場站下載配號檔/2:由PMS+下載配號檔傳至場站)';


                ALTER TABLE e_invoice_config 
                ADD COLUMN get_number_via VARCHAR(10) DEFAULT NULL COMMENT '如何取號(0:API/1:FTP)';

 
                ALTER TABLE e_invoice_config 
                ADD COLUMN api_get_number_url VARCHAR(1000) DEFAULT NULL COMMENT '取號API網址';


                ALTER TABLE e_invoice_config 
                ADD COLUMN api_get_number_key VARCHAR(1000) DEFAULT NULL COMMENT 'EY';


                ALTER TABLE e_invoice_config 
                ADD COLUMN einvoice_company VARCHAR(20) DEFAULT NULL COMMENT '發票廠商';


                ALTER TABLE e_invoice_config 
                MODIFY txn_file_upload_via VARCHAR(10) DEFAULT NULL COMMENT '如何上傳發票交易檔(0:API/1:FTP)' AFTER set_execute_time;
                ALTER TABLE e_invoice_config 
                MODIFY txn_file_generate_flag VARCHAR(10) DEFAULT NULL COMMENT '是否產生/更新交易檔案(0:否, 1:是)' AFTER txn_file_upload_via;
                ALTER TABLE e_invoice_config 
                MODIFY ftp_upload_address VARCHAR(100) DEFAULT NULL COMMENT '上傳發票交易交易檔ftp位置' AFTER api_txn_upload_key;
                ALTER TABLE e_invoice_config 
                MODIFY ftp_upload_port VARCHAR(100) DEFAULT NULL COMMENT '上傳發票交易ftp port' AFTER ftp_upload_address;
                ALTER TABLE e_invoice_config 
                MODIFY customer_id VARCHAR(10) NOT NULL AFTER api_get_number_key;
                ALTER TABLE e_invoice_config 
                MODIFY is_used INT(10) NOT NULL DEFAULT 1 COMMENT '是否使用' AFTER customer_id;
                ALTER TABLE e_invoice_config 
                MODIFY create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP AFTER is_used;
                ALTER TABLE e_invoice_config 
                MODIFY create_user_id INT(10) DEFAULT NULL COMMENT '新增使用者' AFTER create_time;
                ALTER TABLE e_invoice_config 
                MODIFY update_time DATETIME DEFAULT NULL COMMENT '更新時間' AFTER create_user_id;
                ALTER TABLE e_invoice_config 
                MODIFY update_user_id INT(10) DEFAULT NULL COMMENT '更新使用者' AFTER update_time;
                ALTER TABLE e_invoice_config 
                CHANGE `web_url` `web_url` varchar(1000) DEFAULT NULL COMMENT '電子發票後台網址(上傳＆下載相同web_url時用,因為平板更新不易,所以這個欄不可以刪)';
                ALTER TABLE e_invoice_config 
                CHANGE `web_api_key` `web_api_key` varchar(1000) DEFAULT NULL COMMENT '電子發票後台啟動碼(上傳＆下載相同啟動碼時用,因為平板更新不易,所以這個欄不可以刪)';
            
                ALTER TABLE e_invoice_config 
                DROP COLUMN eidc_merchant_code;
                ALTER TABLE e_invoice_config 
                DROP merchant_id;
                ALTER TABLE e_invoice_config 
                DROP cashier_id;
                ALTER TABLE e_invoice_config 
                DROP garage_name;
                ALTER TABLE e_invoice_config 
                DROP acer_garage_id;
                ALTER TABLE e_invoice_config 
                DROP set_execute_time;

                CREATE or replace
                    ALGORITHM = UNDEFINED 
                    DEFINER = `root`@`localhost` 
                    SQL SECURITY DEFINER
                VIEW `device_view` AS
                    SELECT 
                        `lane`.`pv` AS `device_name`,
                        `lane`.`type` AS `type`,
                        `lane`.`pv_ip` AS `ip`,
                        `lane`.`pricing_scheme` AS `pricing_scheme`,
                        `lane`.`pricing_scheme_disability` AS `pricing_scheme_disability`,
                        `lane`.`garage_code` AS `garage_code`,
                        `lane`.`lane_id` AS `device_id`,
                        '2' AS `device_type`,
                        `lane`.`garage_id` AS `garage_id`,
                        `lane`.`pv_ip` AS `device_key`
                    FROM
                        `lane` 
                    UNION ALL SELECT 
                        `d`.`device_name` AS `device_name`,
                        `d`.`type` AS `type`,
                        `d`.`ip` AS `ip`,
                        'null' AS `pricing_scheme`,
                        'null' AS `pricing_scheme_disability`,
                        `g`.`garage_code` AS `garage_code`,
                        `d`.`device_ibox_args_id` AS `device_id`,
                        '4' AS `device_type`,
                        `g`.`garage_id` AS `garage_id`,
                        `d`.`ip` AS `device_key`
                    FROM
                        (`device_ibox_args` `d`
                        LEFT JOIN `garage` `g` ON ((`d`.`garage_id` = `g`.`garage_id`))) 
                    UNION ALL SELECT 
                        `p`.`device_name` AS `device_name`,
                        `p`.`type` AS `type`,
                        `p`.`ip` AS `ip`,
                        'null' AS `pricing_scheme`,
                        'null' AS `pricing_scheme_disability`,
                        `g`.`garage_code` AS `garage_code`,
                        `p`.`device_pv3_args_id` AS `device_id`,
                        '1' AS `device_type`,
                        `g`.`garage_id` AS `garage_id`,
                        `p`.`ip` AS `device_key`
                    FROM
                        (`device_pv3_args` `p`
                        LEFT JOIN `garage` `g` ON ((`p`.`garage_id` = `g`.`garage_id`))) 
                    UNION ALL SELECT 
                        `pa`.`device_name` AS `device_name`,
                        'm' AS `type`,
                        `pa`.`device_ip` AS `ip`,
                        'null' AS `pricing_scheme`,
                        'null' AS `pricing_scheme_disability`,
                        `g`.`garage_code` AS `garage_code`,
                        `pa`.`device_pad_args_id` AS `device_id`,
                        '3' AS `device_type`,
                        `g`.`garage_id` AS `garage_id`,
                        `pa`.`device_key` AS `device_key`
                    FROM
                        (`device_pad_args` `pa`
                        LEFT JOIN `garage` `g` ON ((`pa`.`garage_id` = `g`.`garage_id`)));
            ''')
            

    async def v1_31(self):
        async with self.engine.acquire() as conn:
            await conn.execute(''' CREATE TABLE `forget_password` (
                `no` int(4) NOT NULL auto_increment COMMENT '流水號',
                `account_id` INT NOT NULL COMMENT '申請帳號ID',
                `account` VARCHAR(50) NOT NULL COMMENT '申請帳號',
                `email` VARCHAR(200)  NOT NULL COMMENT '申請ＥＭＡＩＬ',
                `token` VARCHAR(1000)  NOT NULL COMMENT '申請ＴＯＫＥＮ',
                `create_date` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                `expiration_date` DATETIME  COMMENT '申請有效日期',
                `has_change_pwd` INT DEFAULT 0 COMMENT '是否有修改密碼',
                PRIMARY KEY (`no`));

                CREATE TRIGGER `expiration_date_insert_trigger` BEFORE INSERT ON `forget_password` FOR EACH ROW SET NEW.`expiration_date` = NOW() + INTERVAL 10 MINUTE;

            ''')

            await conn.execute('''
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `customer_id` `garaga_id` VARCHAR(10) NOT NULL ;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `txn_file_upload_via` `txn_file_upload_via` VARCHAR(10) NULL DEFAULT NULL COMMENT '如何上傳發票交易檔(0:API/1:FTP/2:先傳至ＰＭＳ＋,再由ＰＭＳ＋上傳)' ;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `api_txn_upload_url` `api_txn_upload_url` VARCHAR(1000) NULL DEFAULT NULL COMMENT '上傳交易檔後台ＡＰＩ ＵＲＬ' ;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `ftp_upload_address` `ftp_upload_address` VARCHAR(100) NULL DEFAULT NULL COMMENT '上傳發票交易交易檔ftp host' ;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `ftp_upload_login_pwd` `ftp_upload_login_pwd` VARCHAR(100) NULL DEFAULT NULL COMMENT 'ftp pwd' ;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `ftp_get_number_address` `ftp_get_number_address` VARCHAR(100) NULL DEFAULT NULL COMMENT '取號FTP host' ;
                ALTER TABLE `e_invoice_config` 
                DROP COLUMN `get_number_via`;
                ALTER TABLE `e_invoice_config` 
                CHANGE COLUMN `api_get_number_key` `api_get_number_key` VARCHAR(1000) NULL DEFAULT NULL COMMENT 'get number Api key' ;
            ''')

            await conn.execute('''
                ALTER TABLE `real_time_transaction_data` 
                CHANGE COLUMN `create_date` `create_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'create_date' ;
            ''')
