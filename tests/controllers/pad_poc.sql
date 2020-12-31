-- MySQL dump 10.13  Distrib 5.5.59, for Linux (x86_64)
--
-- Host: localhost    Database: pmsplus_pad_poc
-- ------------------------------------------------------
-- Server version	5.5.59

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account` (
  `account_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `account` varchar(80) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `password` varchar(500) NOT NULL,
  `user_first_name` varchar(100) DEFAULT NULL,
  `user_middle_name` varchar(100) DEFAULT NULL,
  `user_last_name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(100) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `is_customer_root` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `account_id` (`account_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'2018-05-21 07:08:05','2018-05-25 06:55:14',1,2,'system',0,'$pbkdf2-sha256$200000$8947hzBmLEUopRRC6J2ztg$5qb603F5riLOvnLwaHxOTBESmgvk2h1PZRvH41g1tH0','系統',NULL,'system',NULL,NULL,1,1,0),(2,'2018-05-21 07:08:05','2018-05-22 02:05:20',1,2,'root',0,'$pbkdf2-sha256$200000$8947hzBmLEUopRRC6J2ztg$5qb603F5riLOvnLwaHxOTBESmgvk2h1PZRvH41g1tH0','root',NULL,'admin',NULL,NULL,1,1,0),(3,'2018-05-21 10:24:58','2018-06-01 07:59:54',2,2,'guard_user_1',1,'$pbkdf2-sha256$200000$S0kpJYTQGmOMkfIeY4zx3g$TfS6uPnpOsrDFjdcP9UPiSbpJ8qxgaWyiQdM.keW6gs','王',NULL,'振民',NULL,NULL,2,0,1),(4,'2018-05-21 11:54:41','2018-06-01 08:00:02',2,2,'guard_user_2',1,'$pbkdf2-sha256$200000$YExJqdU653xvDYHQWsvZmw$rNdU.wzWVDbJWnWFuapHEHjVk63Fx5xY.kfcOotNw3s','Fang',NULL,'Amy',NULL,NULL,3,0,0),(5,'2018-06-01 03:14:48','2018-06-01 08:00:09',3,2,'guard_user_3',1,'$pbkdf2-sha256$200000$cE6pdQ4BoBTi/P./V.qd0w$9LMYJNW7SidiFagHCmtKr6dhDUmEEEMlBISLLWbbfc8','Kitty',NULL,'Yen',NULL,NULL,3,0,0),(6,'2018-06-01 08:00:48','2018-06-01 08:00:48',2,NULL,'user1',1,'$pbkdf2-sha256$200000$eC8lRAiBcO79/x8jBCAkpA$EZMWqUHjgWhep10M6CdgL4/zlt5L4DvSFhg4.kuKyO8',NULL,NULL,NULL,NULL,NULL,2,0,1);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clock_time_card`
--

DROP TABLE IF EXISTS `clock_time_card`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clock_time_card` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `account_id` int(11) NOT NULL,
  `garage_id` int(11) NOT NULL,
  `customer_id` varchar(50) NOT NULL,
  `clock_in_time` datetime NOT NULL COMMENT '上班時間',
  `clock_out_time` datetime NOT NULL COMMENT '下班時間',
  `create_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `create_account_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='上下班打卡';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clock_time_card`
--

LOCK TABLES `clock_time_card` WRITE;
/*!40000 ALTER TABLE `clock_time_card` DISABLE KEYS */;
/*!40000 ALTER TABLE `clock_time_card` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customer` (
  `customer_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `company_english_name` varchar(255) DEFAULT NULL,
  `company_union_number` varchar(15) DEFAULT NULL,
  `customer_code` varchar(150) NOT NULL,
  `company_name` varchar(150) NOT NULL,
  `contact_username` varchar(150) NOT NULL,
  `mobile` varchar(30) DEFAULT NULL,
  `fax` varchar(30) DEFAULT NULL,
  `phone_number1` varchar(30) DEFAULT NULL,
  `phone_number2` varchar(30) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `customer_status` int(11) DEFAULT NULL COMMENT '閘門控制模式(1:active, 0:disabled)',
  `note` varchar(255) DEFAULT NULL,
  `contact_availible_datetime` varchar(255) DEFAULT NULL,
  `contact_datetime` varchar(10) DEFAULT NULL,
  `company_address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  UNIQUE KEY `customer_id` (`customer_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (0,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,NULL,'800101','8001','Acer ITS','root',NULL,NULL,'02-26963690#8301',NULL,NULL,1,NULL,NULL,NULL,NULL),(1,'2018-05-21 10:23:35','2018-05-21 10:23:35',2,2,NULL,'72962808','8003','禾典實業有限公司','王振民',NULL,NULL,'02-27098677',NULL,NULL,1,NULL,NULL,'1','台北市中山區林森北路566號B2');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_ibox`
--

DROP TABLE IF EXISTS `device_ibox`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_ibox` (
  `device_pv3_ibox_id` int(10) NOT NULL AUTO_INCREMENT,
  `market_code` varchar(3) NOT NULL COMMENT '特約機構代碼',
  `store_no` varchar(8) NOT NULL COMMENT '場站代碼',
  `pos_no` varchar(3) NOT NULL COMMENT '立柱代碼',
  `cashier_no` varchar(4) NOT NULL COMMENT '收銀員編號',
  PRIMARY KEY (`device_pv3_ibox_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_ibox`
--

LOCK TABLES `device_ibox` WRITE;
/*!40000 ALTER TABLE `device_ibox` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_ibox` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `device_pv`
--

DROP TABLE IF EXISTS `device_pv`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `device_pv` (
  `device_pv_id` int(10) NOT NULL AUTO_INCREMENT,
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
  `last_response_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `response_type` varchar(4) NOT NULL DEFAULT '00',
  `invoice_printer_status` varchar(2) NOT NULL DEFAULT '00' COMMENT 'ref [invoice_printer_error_def].code',
  `pricing_scheme_disability` int(2) NOT NULL DEFAULT '0' COMMENT '身障計費規則',
  `pv_response_confirm` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'PV是否回傳confirm(1:是-新連線,0:否-舊連線',
  `etag_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否為eTag車道(1:是,0:否)',
  `costrule_using_para` tinyint(1) NOT NULL DEFAULT '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
  `lane_costrule_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '車道計費模式(1:複合, 0:單一)',
  `gate_control_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
  `lpr_lane` varchar(4) NOT NULL DEFAULT '99' COMMENT '車辨車道代碼',
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_account_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`device_pv_id`),
  UNIQUE KEY `pv` (`pv`),
  KEY `type` (`type`),
  KEY `pricing_scheme` (`pricing_scheme`),
  KEY `pv_ip` (`pv_ip`),
  KEY `MEntryB` (`MEntryB`),
  KEY `in_out` (`in_out`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `device_pv`
--

LOCK TABLES `device_pv` WRITE;
/*!40000 ALTER TABLE `device_pv` DISABLE KEYS */;
/*!40000 ALTER TABLE `device_pv` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `driveway`
--

DROP TABLE IF EXISTS `driveway`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `driveway` (
  `acer_id` varchar(5) NOT NULL COMMENT 'acer停車場編號',
  `pv_name` varchar(128) NOT NULL COMMENT 'PV 名稱',
  `type` varchar(1) NOT NULL COMMENT 'c:汽車道, m:機車道',
  `charge_rule` int(2) DEFAULT NULL COMMENT '計費規則',
  `pv_ip` varchar(64) NOT NULL COMMENT 'PV IP address',
  `pv_netmask` varchar(64) NOT NULL COMMENT 'PV Netmask address',
  `pv_gateway` varchar(64) DEFAULT NULL COMMENT 'PV Default Gateway IP address',
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
  `pv_response_type` varchar(4) NOT NULL DEFAULT '00' COMMENT 'PV回應類型',
  `invoice_printer_status` varchar(2) NOT NULL DEFAULT '00' COMMENT 'refer to [invoice_printer_error_def].code',
  `disability_charge_rule` int(2) NOT NULL DEFAULT '0' COMMENT '身障計費規則',
  `is_etag_drvieway` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否為eTag車道(1:是,0:否)',
  `is_charge_params_enabled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
  `driveway_charge_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '車道計費模式(1:複合, 0:單一)',
  `gate_control_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
  `car_recognition_driveway_code` varchar(4) NOT NULL DEFAULT '99' COMMENT '車辨車道代碼',
  `driveway_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`driveway_id`),
  UNIQUE KEY `driveway_id` (`driveway_id`),
  KEY `pv_name` (`pv_name`),
  KEY `type` (`type`),
  KEY `charge_rule` (`charge_rule`),
  KEY `pv_ip` (`pv_ip`),
  KEY `minimun_entry_balance` (`minimun_entry_balance`),
  KEY `direction` (`direction`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `driveway`
--

LOCK TABLES `driveway` WRITE;
/*!40000 ALTER TABLE `driveway` DISABLE KEYS */;
/*!40000 ALTER TABLE `driveway` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_invoice_config`
--

DROP TABLE IF EXISTS `e_invoice_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_invoice_config` (
  `e_invoice_config_id` int(4) NOT NULL AUTO_INCREMENT COMMENT '流水號',
  `invoicing_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '-1:預設未使用, 0:PMS->PV',
  `eidc_merchant_code` varchar(20) NOT NULL COMMENT 'EIDC用場站編號',
  `merchant_id` varchar(20) NOT NULL COMMENT '場站編號',
  `cashier_id` varchar(20) NOT NULL COMMENT '收銀機編號',
  `garage_name` varchar(20) NOT NULL COMMENT '停車場名稱',
  `pos_id` varchar(20) NOT NULL COMMENT 'acer的PMS場次編號',
  `tax_id` varchar(10) NOT NULL COMMENT '賣方統編',
  `qrcode_encrypt_key` varchar(32) NOT NULL DEFAULT 'acer_pms_aes_key' COMMENT '產生QR code的AES KEY',
  `set_execute_time` datetime NOT NULL DEFAULT '2014-01-01 00:00:00',
  `txn_file_upload_flag` tinyint(4) NOT NULL DEFAULT '1' COMMENT '是否產生/更新交易檔案(0:否, 1:是)',
  `txn_file_upload_interval` int(4) NOT NULL DEFAULT '30' COMMENT '產生/更新交易檔案時間間隔',
  `txn_file_import_folder` varchar(100) NOT NULL COMMENT '匯入交易檔案預設路徑',
  `txn_file_upload_folder` varchar(100) NOT NULL COMMENT '產生/更新交易檔案預設路徑',
  `txn_file_backup_folder` varchar(100) NOT NULL COMMENT '產生/更新交易檔案備份路徑',
  `update_time` datetime NOT NULL COMMENT '更新時間',
  `update_user` varchar(100) NOT NULL COMMENT '更新使用者',
  PRIMARY KEY (`e_invoice_config_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='電子發票設定 (電子發票標準化介面)';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_invoice_config`
--

LOCK TABLES `e_invoice_config` WRITE;
/*!40000 ALTER TABLE `e_invoice_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `e_invoice_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `e_invoice_number_data`
--

DROP TABLE IF EXISTS `e_invoice_number_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `e_invoice_number_data` (
  `no` bigint(20) NOT NULL,
  `tax_id` varchar(10) NOT NULL COMMENT '統編',
  `tax_id_buyer` varchar(10) DEFAULT NULL COMMENT '買受人統編',
  `random_code` varchar(4) NOT NULL COMMENT '隨機碼',
  `use_year_month` varchar(6) NOT NULL COMMENT 'yyyyMM',
  `invoice_number` varchar(20) NOT NULL COMMENT '發票號碼',
  `einvoice_use_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:印, 1:不印,2=存入載具,3=列印發票並打買受人統編',
  `donate_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '捐贈狀態(0:不捐, 1:捐)',
  `sale_print_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '銷貨清單列印狀態(0:不印, 1:印)',
  `preserve_code` varchar(20) DEFAULT NULL COMMENT '愛心碼',
  `einvoice_device_no` varchar(20) DEFAULT NULL COMMENT '載具編號',
  `txn_total_amt` int(4) NOT NULL DEFAULT '0' COMMENT '交易金額',
  `invoice_amt` int(4) NOT NULL DEFAULT '0' COMMENT '發票金額',
  `txn_date` varchar(8) DEFAULT NULL COMMENT 'YYYYMMDD',
  `txn_time` varchar(6) DEFAULT NULL COMMENT 'HHMMSS',
  `merchant_id` varchar(20) NOT NULL COMMENT '商家代號',
  `counter_id` varchar(20) NOT NULL COMMENT '門市(停車場)代號(舊PMS)',
  `pos_id` varchar(20) NOT NULL COMMENT '收銀機號',
  `batch_number` varchar(6) DEFAULT NULL COMMENT '批號(車道編號)',
  `transaction_number` varchar(6) DEFAULT NULL COMMENT '收銀機交易序號',
  `business_date` varchar(8) DEFAULT NULL COMMENT '營業日',
  `process_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:匯入, 1:銷售, 2:退貨(作廢), 3:折讓, 4:折讓取消, 5:註銷',
  `process_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `upload_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:未上傳, 1:待上傳, 2:已上傳',
  `upload_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `use_status` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:未使用, 1:已送出給PV',
  `use_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `sales_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '0:parking id, 1:訂單',
  `sales_id` int(4) NOT NULL DEFAULT '0' COMMENT 'parking id 或訂單id',
  `update_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `update_user` varchar(100) NOT NULL,
  `source_filename` varchar(100) DEFAULT NULL,
  `garage_code` varchar(20) DEFAULT NULL,
  `csv_file_date` varchar(20) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `garage_id` int(11) NOT NULL,
  PRIMARY KEY (`invoice_number`,`use_year_month`),
  KEY `proccess_status` (`process_status`),
  KEY `upload_status` (`upload_status`),
  KEY `use_status` (`use_status`),
  KEY `sales_id` (`sales_id`),
  KEY `counter_index` (`counter_id`,`tax_id`,`pos_id`,`merchant_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `e_invoice_number_data`
--

LOCK TABLES `e_invoice_number_data` WRITE;
/*!40000 ALTER TABLE `e_invoice_number_data` DISABLE KEYS */;
INSERT INTO `e_invoice_number_data` VALUES (0,'54641988','','7075','201806','QW00105650',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'1',NULL,1,'2018-05-21 18:44:30',2,'2018-05-21 18:44:40',1,'2018-05-21 18:44:30',0,1,'2018-05-21 18:44:40','2',NULL,'1',NULL,'2018-05-21 10:44:41',0),(0,'54641988','','0977','201806','QW00105651',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'2',NULL,1,'2018-05-22 00:07:27',2,'2018-05-22 00:07:35',1,'2018-05-22 00:07:27',0,4,'2018-05-22 00:07:35','2',NULL,'1',NULL,'2018-05-21 16:41:08',0),(0,'54641988','','9065','201806','QW00105850',0,0,0,'','1234',20,20,NULL,NULL,'1','1','1234',NULL,'1',NULL,1,'2018-05-22 10:35:13',2,'2018-05-22 10:36:05',1,'2018-05-22 10:35:13',0,10,'2018-05-22 10:36:05','4',NULL,'1',NULL,'2018-05-22 02:36:06',0),(0,'54641988','','0248','201806','QW00105851',0,0,0,'','1234',20,20,NULL,NULL,'1','1','1234',NULL,'2',NULL,1,'2018-05-22 10:39:15',2,'2018-05-22 10:41:02',1,'2018-05-22 10:39:15',0,13,'2018-05-22 10:41:02','4',NULL,'1',NULL,'2018-05-22 02:41:03',0),(0,'54641988','','4314','201806','QW00105852',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'3',NULL,1,'2018-05-22 10:47:56',2,'2018-05-22 10:49:15',1,'2018-05-22 10:47:56',0,15,'2018-05-22 10:49:15','4',NULL,'1',NULL,'2018-05-22 02:49:16',0),(0,'54641988','56788998','3635','201806','QW00106050',3,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'1',NULL,1,'2018-05-25 18:09:54',2,'2018-05-25 18:10:58',1,'2018-05-25 18:09:54',0,20,'2018-05-25 18:10:58','2',NULL,'1',NULL,'2018-05-25 10:11:00',0),(0,'54641988','12345678','2834','201806','QW00106450',3,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'1',NULL,1,'2018-05-30 15:15:16',2,'2018-05-30 15:16:34',1,'2018-05-30 15:15:16',0,32,'2018-05-30 15:16:34','4',NULL,'1',NULL,'2018-05-30 07:16:30',0),(0,'54641988','','5409','201806','QW00106451',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'2',NULL,1,'2018-05-30 15:21:58',2,'2018-05-30 15:23:14',1,'2018-05-30 15:21:58',0,31,'2018-05-30 15:23:14','4',NULL,'1',NULL,'2018-05-30 07:24:16',0),(0,'54641988','','4664','201806','QW00106452',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'3',NULL,1,'2018-05-30 15:32:30',2,'2018-05-30 15:41:35',1,'2018-05-30 15:32:30',0,34,'2018-05-30 15:41:35','4',NULL,'1',NULL,'2018-05-30 07:41:32',0),(0,'54641988','','9000','201806','QW00106453',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'4',NULL,1,'2018-05-30 15:44:50',2,'2018-05-30 15:45:23',1,'2018-05-30 15:44:50',0,36,'2018-05-30 15:45:23','4',NULL,'1',NULL,'2018-05-30 07:45:19',0),(0,'54641988','','6889','201806','QW00107050',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'1',NULL,1,'2018-06-01 16:02:49',2,'2018-06-01 16:03:33',1,'2018-06-01 16:02:49',0,53,'2018-06-01 16:03:33','2',NULL,'1',NULL,'2018-06-01 08:03:34',0),(0,'54641988','','0403','201806','QW00107051',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'2',NULL,1,'2018-06-01 16:19:58',2,'2018-06-01 16:20:30',1,'2018-06-01 16:19:58',0,56,'2018-06-01 16:20:30','5',NULL,'1',NULL,'2018-06-01 08:20:31',0),(0,'54641988','','6471','201806','QW00107052',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'3',NULL,1,'2018-06-01 16:44:40',2,'2018-06-01 16:45:03',1,'2018-06-01 16:44:40',0,57,'2018-06-01 16:45:03','5',NULL,'1',NULL,'2018-06-01 08:45:04',0),(0,'54641988','','8902','201806','QW00107053',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'4',NULL,1,'2018-06-01 17:28:46',2,'2018-06-01 17:29:06',1,'2018-06-01 17:28:46',0,54,'2018-06-01 17:29:06','5',NULL,'1',NULL,'2018-06-01 09:29:06',0),(0,'54641988','22027475','0320','201806','QW00107054',3,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'5',NULL,1,'2018-06-01 19:12:48',2,'2018-06-01 19:13:02',1,'2018-06-01 19:12:48',0,60,'2018-06-01 19:13:02','5',NULL,'1',NULL,'2018-06-01 11:13:03',0),(0,'54641988','','2014','201806','QW00107055',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'6',NULL,1,'2018-06-01 19:42:22',2,'2018-06-01 19:42:33',1,'2018-06-01 19:42:22',0,58,'2018-06-01 19:42:33','5',NULL,'1',NULL,'2018-06-01 11:42:33',0),(0,'54641988','','2967','201806','QW00107056',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'7',NULL,1,'2018-06-01 20:03:12',2,'2018-06-01 20:03:20',1,'2018-06-01 20:03:12',0,65,'2018-06-01 20:03:20','5',NULL,'1',NULL,'2018-06-01 12:03:20',0),(0,'54641988','','7270','201806','QW00107057',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'8',NULL,1,'2018-06-01 20:16:05',2,'2018-06-01 20:16:13',1,'2018-06-01 20:16:05',0,63,'2018-06-01 20:16:13','5',NULL,'1',NULL,'2018-06-01 12:16:14',0),(0,'54641988','','0246','201806','QW00107058',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'9',NULL,1,'2018-06-01 20:39:32',2,'2018-06-01 20:39:41',1,'2018-06-01 20:39:32',0,68,'2018-06-01 20:39:41','5',NULL,'1',NULL,'2018-06-01 12:39:42',0),(0,'54641988','','3157','201806','QW00107059',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'10',NULL,1,'2018-06-01 20:42:26',2,'2018-06-01 20:42:33',1,'2018-06-01 20:42:26',0,66,'2018-06-01 20:42:33','5',NULL,'1',NULL,'2018-06-01 12:42:34',0),(0,'54641988','','3651','201806','QW00107060',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'11',NULL,1,'2018-06-01 20:59:48',2,'2018-06-01 20:59:55',1,'2018-06-01 20:59:48',0,64,'2018-06-01 20:59:55','5',NULL,'1',NULL,'2018-06-01 12:59:56',0),(0,'54641988','','7921','201806','QW00107061',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'12',NULL,1,'2018-06-01 21:00:33',2,'2018-06-01 21:00:40',1,'2018-06-01 21:00:33',0,69,'2018-06-01 21:00:40','5',NULL,'1',NULL,'2018-06-01 13:00:40',0),(0,'54641988','','3083','201806','QW00107062',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'13',NULL,1,'2018-06-01 21:30:03',2,'2018-06-01 21:30:10',1,'2018-06-01 21:30:03',0,62,'2018-06-01 21:30:10','5',NULL,'1',NULL,'2018-06-01 13:30:11',0),(0,'54641988','','6856','201806','QW00107063',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'14',NULL,1,'2018-06-01 21:33:31',2,'2018-06-01 21:33:38',1,'2018-06-01 21:33:31',0,71,'2018-06-01 21:33:38','5',NULL,'1',NULL,'2018-06-01 13:33:39',0),(0,'54641988','','8565','201806','QW00107064',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'15',NULL,1,'2018-06-01 21:40:08',2,'2018-06-01 21:41:30',1,'2018-06-01 21:40:08',0,61,'2018-06-01 21:41:30','5',NULL,'1',NULL,'2018-06-01 13:41:31',0),(0,'54641988','','0545','201806','QW00107065',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'16',NULL,1,'2018-06-01 22:06:31',2,'2018-06-01 22:06:39',1,'2018-06-01 22:06:31',0,72,'2018-06-01 22:06:39','5',NULL,'1',NULL,'2018-06-01 14:06:40',0),(0,'54641988','','3625','201806','QW00107066',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'17',NULL,1,'2018-06-01 22:16:35',2,'2018-06-01 22:16:43',1,'2018-06-01 22:16:35',0,67,'2018-06-01 22:16:43','5',NULL,'1',NULL,'2018-06-01 14:16:43',0),(0,'54641988','','8848','201806','QW00107067',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'18',NULL,1,'2018-06-01 22:37:27',2,'2018-06-01 22:37:34',1,'2018-06-01 22:37:27',0,70,'2018-06-01 22:37:34','5',NULL,'1',NULL,'2018-06-01 14:37:35',0),(0,'54641988','','5276','201806','QW00107068',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'19',NULL,1,'2018-06-02 08:29:14',2,'2018-06-02 08:30:31',1,'2018-06-02 08:29:14',0,73,'2018-06-02 08:30:31','5',NULL,'1',NULL,'2018-06-02 00:30:31',0),(0,'54641988','','5389','201806','QW00107069',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'20',NULL,1,'2018-06-02 08:30:56',2,'2018-06-02 08:31:38',1,'2018-06-02 08:30:56',0,76,'2018-06-02 08:31:38','5',NULL,'1',NULL,'2018-06-02 00:31:39',0),(0,'54641988','','5702','201806','QW00107070',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'21',NULL,1,'2018-06-02 11:31:15',2,'2018-06-02 11:31:40',1,'2018-06-02 11:31:15',0,77,'2018-06-02 11:31:40','5',NULL,'1',NULL,'2018-06-02 03:31:42',0),(0,'54641988','','2909','201806','QW00107071',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'22',NULL,1,'2018-06-02 12:46:03',2,'2018-06-02 12:46:21',1,'2018-06-02 12:46:03',0,84,'2018-06-02 12:46:21','5',NULL,'1',NULL,'2018-06-02 04:46:22',0),(0,'54641988','','0840','201806','QW00107072',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'23',NULL,1,'2018-06-02 12:47:34',2,'2018-06-02 12:47:44',1,'2018-06-02 12:47:34',0,80,'2018-06-02 12:47:44','5',NULL,'1',NULL,'2018-06-02 04:47:46',0),(0,'54641988','24968418','0790','201806','QW00107073',3,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'24',NULL,1,'2018-06-02 12:50:02',2,'2018-06-02 12:50:38',1,'2018-06-02 12:50:02',0,78,'2018-06-02 12:50:38','5',NULL,'1',NULL,'2018-06-02 04:50:40',0),(0,'54641988','','9457','201806','QW00107074',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'25',NULL,1,'2018-06-02 12:54:22',2,'2018-06-02 12:54:33',1,'2018-06-02 12:54:22',0,81,'2018-06-02 12:54:33','5',NULL,'1',NULL,'2018-06-02 04:54:35',0),(0,'54641988','','0859','201806','QW00107075',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'26',NULL,1,'2018-06-02 13:04:15',2,'2018-06-02 13:04:29',1,'2018-06-02 13:04:15',0,85,'2018-06-02 13:04:29','5',NULL,'1',NULL,'2018-06-02 05:04:30',0),(0,'54641988','','1149','201806','QW00107076',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'27',NULL,1,'2018-06-02 14:06:28',2,'2018-06-02 14:06:37',1,'2018-06-02 14:06:28',0,89,'2018-06-02 14:06:37','5',NULL,'1',NULL,'2018-06-02 06:06:39',0),(0,'54641988','','8203','201806','QW00107077',0,0,0,'','1234',140,140,NULL,NULL,'1','1','1234',NULL,'28',NULL,1,'2018-06-02 14:25:14',2,'2018-06-02 14:25:27',1,'2018-06-02 14:25:14',0,79,'2018-06-02 14:25:27','5',NULL,'1',NULL,'2018-06-02 06:25:29',0),(0,'54641988','','8125','201806','QW00107078',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'29',NULL,1,'2018-06-02 14:28:11',2,'2018-06-02 14:28:20',1,'2018-06-02 14:28:11',0,82,'2018-06-02 14:28:20','5',NULL,'1',NULL,'2018-06-02 06:28:21',0),(0,'54641988','','0316','201806','QW00107079',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'30',NULL,1,'2018-06-02 14:37:44',2,'2018-06-02 14:37:53',1,'2018-06-02 14:37:44',0,87,'2018-06-02 14:37:53','5',NULL,'1',NULL,'2018-06-02 06:37:55',0),(0,'54641988','','3869','201806','QW00107080',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'31',NULL,1,'2018-06-02 15:00:21',2,'2018-06-02 15:00:33',1,'2018-06-02 15:00:21',0,83,'2018-06-02 15:00:33','5',NULL,'1',NULL,'2018-06-02 07:00:35',0),(0,'54641988','','7665','201806','QW00107081',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'32',NULL,1,'2018-06-02 15:30:44',2,'2018-06-02 15:30:52',1,'2018-06-02 15:30:44',0,92,'2018-06-02 15:30:52','5',NULL,'1',NULL,'2018-06-02 07:30:53',0),(0,'54641988','','7322','201806','QW00107082',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'33',NULL,1,'2018-06-02 16:18:15',2,'2018-06-02 16:23:17',1,'2018-06-02 16:18:15',0,99,'2018-06-02 16:23:17','5',NULL,'1',NULL,'2018-06-02 08:23:18',0),(0,'54641988','','0934','201806','QW00107083',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'34',NULL,1,'2018-06-02 16:44:08',2,'2018-06-02 16:44:22',1,'2018-06-02 16:44:08',0,74,'2018-06-02 16:44:22','5',NULL,'1',NULL,'2018-06-02 08:44:23',0),(0,'54641988','','1279','201806','QW00107084',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'35',NULL,1,'2018-06-02 16:51:06',2,'2018-06-02 16:51:18',1,'2018-06-02 16:51:06',0,96,'2018-06-02 16:51:18','5',NULL,'1',NULL,'2018-06-02 08:51:19',0),(0,'54641988','','7361','201806','QW00107085',0,0,0,'','1234',160,160,NULL,NULL,'1','1','1234',NULL,'36',NULL,1,'2018-06-02 17:19:39',2,'2018-06-02 17:19:47',1,'2018-06-02 17:19:39',0,88,'2018-06-02 17:19:47','5',NULL,'1',NULL,'2018-06-02 09:19:48',0),(0,'54641988','','3117','201806','QW00107086',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'37',NULL,1,'2018-06-02 18:16:53',2,'2018-06-02 18:17:02',1,'2018-06-02 18:16:53',0,102,'2018-06-02 18:17:02','5',NULL,'1',NULL,'2018-06-02 10:17:04',0),(0,'54641988','','8628','201806','QW00107087',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'38',NULL,1,'2018-06-02 18:17:40',2,'2018-06-02 18:17:48',1,'2018-06-02 18:17:40',0,98,'2018-06-02 18:17:48','5',NULL,'1',NULL,'2018-06-02 10:17:49',0),(0,'54641988','','9821','201806','QW00107088',0,0,0,'','1234',140,140,NULL,NULL,'1','1','1234',NULL,'39',NULL,1,'2018-06-02 18:17:59',2,'2018-06-02 18:18:09',1,'2018-06-02 18:17:59',0,91,'2018-06-02 18:18:09','5',NULL,'1',NULL,'2018-06-02 10:18:11',0),(0,'54641988','','8575','201806','QW00107089',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'40',NULL,1,'2018-06-02 18:42:45',2,'2018-06-02 18:45:41',1,'2018-06-02 18:42:45',0,95,'2018-06-02 18:45:41','5',NULL,'1',NULL,'2018-06-02 10:45:43',0),(0,'54641988','','6639','201806','QW00107090',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'41',NULL,1,'2018-06-02 18:45:59',2,'2018-06-02 18:46:09',1,'2018-06-02 18:45:59',0,86,'2018-06-02 18:46:09','5',NULL,'1',NULL,'2018-06-02 10:46:11',0),(0,'54641988','','6262','201806','QW00107091',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'42',NULL,1,'2018-06-02 19:03:59',2,'2018-06-02 19:04:08',1,'2018-06-02 19:03:59',0,103,'2018-06-02 19:04:08','5',NULL,'1',NULL,'2018-06-02 11:04:09',0),(0,'54641988','','7679','201806','QW00107092',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'43',NULL,1,'2018-06-02 19:24:11',2,'2018-06-02 19:24:20',1,'2018-06-02 19:24:11',0,101,'2018-06-02 19:24:20','5',NULL,'1',NULL,'2018-06-02 11:24:22',0),(0,'54641988','','4804','201806','QW00107093',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'44',NULL,1,'2018-06-02 19:36:41',2,'2018-06-02 19:36:48',1,'2018-06-02 19:36:41',0,106,'2018-06-02 19:36:48','5',NULL,'1',NULL,'2018-06-02 11:36:50',0),(0,'54641988','','8666','201806','QW00107094',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'45',NULL,1,'2018-06-02 20:06:42',2,'2018-06-02 20:06:49',1,'2018-06-02 20:06:42',0,104,'2018-06-02 20:06:49','5',NULL,'1',NULL,'2018-06-02 12:06:51',0),(0,'54641988','','8787','201806','QW00107095',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'46',NULL,1,'2018-06-02 20:06:52',2,'2018-06-02 20:06:59',1,'2018-06-02 20:06:52',0,105,'2018-06-02 20:06:59','5',NULL,'1',NULL,'2018-06-02 12:07:01',0),(0,'54641988','','2678','201806','QW00107096',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'47',NULL,1,'2018-06-02 20:24:24',2,'2018-06-02 20:24:32',1,'2018-06-02 20:24:24',0,107,'2018-06-02 20:24:32','5',NULL,'1',NULL,'2018-06-02 12:24:34',0),(0,'54641988','','4374','201806','QW00107097',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'48',NULL,1,'2018-06-02 20:51:34',2,'2018-06-02 20:51:55',1,'2018-06-02 20:51:34',0,-1,'2018-06-02 20:51:55','5',NULL,'1',NULL,'2018-06-02 12:51:57',0),(0,'54641988','','1854','201806','QW00107098',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'49',NULL,1,'2018-06-02 20:52:19',2,'2018-06-02 20:52:27',1,'2018-06-02 20:52:19',0,-1,'2018-06-02 20:52:27','5',NULL,'1',NULL,'2018-06-02 12:52:29',0),(0,'54641988','','8285','201806','QW00107099',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'50',NULL,1,'2018-06-02 20:53:00',2,'2018-06-02 20:53:08',1,'2018-06-02 20:53:00',0,-1,'2018-06-02 20:53:08','5',NULL,'1',NULL,'2018-06-02 12:53:10',0),(0,'54641988','','7236','201806','QW00107100',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'51',NULL,1,'2018-06-02 20:53:41',0,'0000-00-00 00:00:00',1,'2018-06-02 20:53:41',0,90,'0000-00-00 00:00:00','',NULL,'1',NULL,'2018-06-02 12:54:19',0),(0,'54641988','','1848','201806','QW00107101',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'52',NULL,1,'2018-06-02 20:58:33',2,'2018-06-02 20:58:46',1,'2018-06-02 20:58:33',0,-1,'2018-06-02 20:58:46','5',NULL,'1',NULL,'2018-06-02 12:58:48',0),(0,'54641988','','8661','201806','QW00107102',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'53',NULL,1,'2018-06-02 21:03:28',2,'2018-06-02 21:03:40',1,'2018-06-02 21:03:28',0,-1,'2018-06-02 21:03:40','5',NULL,'1',NULL,'2018-06-02 13:03:42',0),(0,'54641988','','5995','201806','QW00107103',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'54',NULL,1,'2018-06-02 21:05:41',2,'2018-06-02 21:08:25',1,'2018-06-02 21:05:41',0,-1,'2018-06-02 21:08:25','5',NULL,'1',NULL,'2018-06-02 13:08:27',0),(0,'54641988','','6723','201806','QW00107104',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'55',NULL,1,'2018-06-02 21:21:14',2,'2018-06-02 21:21:24',1,'2018-06-02 21:21:14',0,109,'2018-06-02 21:21:24','5',NULL,'1',NULL,'2018-06-02 13:21:26',0),(0,'54641988','','6223','201806','QW00107105',0,0,0,'','1234',160,160,NULL,NULL,'1','1','1234',NULL,'56',NULL,1,'2018-06-02 21:34:17',2,'2018-06-02 21:34:47',1,'2018-06-02 21:34:17',0,100,'2018-06-02 21:34:47','5',NULL,'1',NULL,'2018-06-02 13:34:49',0),(0,'54641988','','6457','201806','QW00107106',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'57',NULL,1,'2018-06-02 21:39:07',2,'2018-06-02 21:39:16',1,'2018-06-02 21:39:07',0,108,'2018-06-02 21:39:16','5',NULL,'1',NULL,'2018-06-02 13:39:18',0),(0,'54641988','','9548','201806','QW00107107',0,0,0,'','1234',160,160,NULL,NULL,'1','1','1234',NULL,'58',NULL,1,'2018-06-03 11:26:29',2,'2018-06-03 11:26:53',1,'2018-06-03 11:26:29',0,111,'2018-06-03 11:26:53','5',NULL,'1',NULL,'2018-06-03 03:26:53',0),(0,'54641988','','3109','201806','QW00107108',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'59',NULL,1,'2018-06-03 11:29:12',2,'2018-06-03 11:29:31',1,'2018-06-03 11:29:12',0,112,'2018-06-03 11:29:31','5',NULL,'1',NULL,'2018-06-03 03:29:31',0),(0,'54641988','','2142','201806','QW00107109',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'60',NULL,1,'2018-06-03 13:06:37',2,'2018-06-03 13:06:48',1,'2018-06-03 13:06:37',0,122,'2018-06-03 13:06:48','5',NULL,'1',NULL,'2018-06-03 05:06:48',0),(0,'54641988','','2346','201806','QW00107110',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'61',NULL,1,'2018-06-03 13:49:58',2,'2018-06-03 13:50:07',1,'2018-06-03 13:49:58',0,116,'2018-06-03 13:50:07','5',NULL,'1',NULL,'2018-06-03 05:50:07',0),(0,'54641988','','3712','201806','QW00107111',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'62',NULL,1,'2018-06-03 13:52:38',2,'2018-06-03 13:52:45',1,'2018-06-03 13:52:38',0,115,'2018-06-03 13:52:45','5',NULL,'1',NULL,'2018-06-03 05:52:46',0),(0,'54641988','','4594','201806','QW00107112',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'63',NULL,1,'2018-06-03 13:53:40',2,'2018-06-03 13:53:47',1,'2018-06-03 13:53:40',0,125,'2018-06-03 13:53:47','5',NULL,'1',NULL,'2018-06-03 05:53:47',0),(0,'54641988','','4414','201806','QW00107113',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'64',NULL,1,'2018-06-03 13:54:03',2,'2018-06-03 13:54:23',1,'2018-06-03 13:54:03',0,121,'2018-06-03 13:54:23','5',NULL,'1',NULL,'2018-06-03 05:54:24',0),(0,'54641988','','8182','201806','QW00107114',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'65',NULL,1,'2018-06-03 14:22:10',2,'2018-06-03 14:22:17',1,'2018-06-03 14:22:10',0,113,'2018-06-03 14:22:17','5',NULL,'1',NULL,'2018-06-03 06:22:18',0),(0,'54641988','','3793','201806','QW00107115',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'66',NULL,1,'2018-06-03 14:23:06',2,'2018-06-03 14:23:14',1,'2018-06-03 14:23:06',0,123,'2018-06-03 14:23:14','5',NULL,'1',NULL,'2018-06-03 06:23:15',0),(0,'54641988','','0316','201806','QW00107116',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'67',NULL,1,'2018-06-03 14:29:31',2,'2018-06-03 14:29:39',1,'2018-06-03 14:29:31',0,131,'2018-06-03 14:29:39','5',NULL,'1',NULL,'2018-06-03 06:29:40',0),(0,'54641988','','4993','201806','QW00107117',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'68',NULL,1,'2018-06-03 14:31:20',2,'2018-06-03 14:31:26',1,'2018-06-03 14:31:20',0,114,'2018-06-03 14:31:26','5',NULL,'1',NULL,'2018-06-03 06:31:27',0),(0,'54641988','','0694','201806','QW00107118',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'69',NULL,1,'2018-06-03 14:38:02',2,'2018-06-03 14:38:09',1,'2018-06-03 14:38:02',0,117,'2018-06-03 14:38:09','5',NULL,'1',NULL,'2018-06-03 06:38:10',0),(0,'54641988','','1894','201806','QW00107119',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'70',NULL,1,'2018-06-03 14:40:09',2,'2018-06-03 14:40:16',1,'2018-06-03 14:40:09',0,128,'2018-06-03 14:40:16','5',NULL,'1',NULL,'2018-06-03 06:40:16',0),(0,'54641988','','5351','201806','QW00107120',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'71',NULL,1,'2018-06-03 14:47:42',2,'2018-06-03 14:47:49',1,'2018-06-03 14:47:42',0,120,'2018-06-03 14:47:49','5',NULL,'1',NULL,'2018-06-03 06:47:50',0),(0,'54641988','','9846','201806','QW00107121',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'72',NULL,1,'2018-06-03 14:56:51',2,'2018-06-03 14:57:00',1,'2018-06-03 14:56:51',0,126,'2018-06-03 14:57:00','5',NULL,'1',NULL,'2018-06-03 06:57:01',0),(0,'54641988','','2133','201806','QW00107122',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'73',NULL,1,'2018-06-03 15:08:58',2,'2018-06-03 15:09:10',1,'2018-06-03 15:08:58',0,129,'2018-06-03 15:09:10','5',NULL,'1',NULL,'2018-06-03 07:09:11',0),(0,'54641988','','4858','201806','QW00107123',0,0,0,'','1234',140,140,NULL,NULL,'1','1','1234',NULL,'74',NULL,1,'2018-06-03 15:17:26',2,'2018-06-03 15:17:38',1,'2018-06-03 15:17:26',0,118,'2018-06-03 15:17:38','5',NULL,'1',NULL,'2018-06-03 07:17:39',0),(0,'54641988','','1305','201806','QW00107124',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'75',NULL,1,'2018-06-03 16:24:25',2,'2018-06-03 16:24:39',1,'2018-06-03 16:24:25',0,132,'2018-06-03 16:24:39','5',NULL,'1',NULL,'2018-06-03 08:24:39',0),(0,'54641988','','5695','201806','QW00107125',0,0,0,'','1234',160,160,NULL,NULL,'1','1','1234',NULL,'76',NULL,1,'2018-06-03 16:39:08',2,'2018-06-03 16:39:17',1,'2018-06-03 16:39:08',0,127,'2018-06-03 16:39:17','5',NULL,'1',NULL,'2018-06-03 08:39:17',0),(0,'54641988','','3087','201806','QW00107126',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'77',NULL,1,'2018-06-03 16:43:48',2,'2018-06-03 16:43:56',1,'2018-06-03 16:43:48',0,134,'2018-06-03 16:43:56','5',NULL,'1',NULL,'2018-06-03 08:43:57',0),(0,'54641988','','2502','201806','QW00107127',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'78',NULL,1,'2018-06-03 17:19:00',0,'0000-00-00 00:00:00',1,'2018-06-03 17:19:00',0,137,'0000-00-00 00:00:00','',NULL,'1',NULL,'2018-06-03 09:19:10',0),(0,'54641988','','6108','201806','QW00107128',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'79',NULL,1,'2018-06-03 17:19:21',2,'2018-06-03 17:19:31',1,'2018-06-03 17:19:21',0,-1,'2018-06-03 17:19:31','5',NULL,'1',NULL,'2018-06-03 09:19:31',0),(0,'54641988','','6094','201806','QW00107129',0,0,0,'','1234',160,160,NULL,NULL,'1','1','1234',NULL,'80',NULL,1,'2018-06-03 17:25:33',2,'2018-06-03 17:25:42',1,'2018-06-03 17:25:33',0,130,'2018-06-03 17:25:42','5',NULL,'1',NULL,'2018-06-03 09:25:43',0),(0,'54641988','','1821','201806','QW00107130',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'81',NULL,1,'2018-06-03 17:39:40',2,'2018-06-03 17:39:55',1,'2018-06-03 17:39:40',0,139,'2018-06-03 17:39:55','5',NULL,'1',NULL,'2018-06-03 09:39:55',0),(0,'54641988','','1318','201806','QW00107131',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'82',NULL,1,'2018-06-03 17:57:05',2,'2018-06-03 17:57:15',1,'2018-06-03 17:57:05',0,119,'2018-06-03 17:57:15','5',NULL,'1',NULL,'2018-06-03 09:57:16',0),(0,'54641988','','9804','201806','QW00107132',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'83',NULL,1,'2018-06-03 18:21:27',2,'2018-06-03 18:21:36',1,'2018-06-03 18:21:27',0,124,'2018-06-03 18:21:36','5',NULL,'1',NULL,'2018-06-03 10:21:37',0),(0,'54641988','','8911','201806','QW00107133',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'84',NULL,1,'2018-06-03 18:22:57',2,'2018-06-03 18:23:06',1,'2018-06-03 18:22:57',0,142,'2018-06-03 18:23:06','5',NULL,'1',NULL,'2018-06-03 10:23:07',0),(0,'54641988','','8354','201806','QW00107134',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'85',NULL,1,'2018-06-03 18:46:34',2,'2018-06-03 18:46:57',1,'2018-06-03 18:46:34',0,141,'2018-06-03 18:46:57','5',NULL,'1',NULL,'2018-06-03 10:46:58',0),(0,'54641988','','3757','201806','QW00107135',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'86',NULL,1,'2018-06-03 18:51:27',2,'2018-06-03 18:51:38',1,'2018-06-03 18:51:27',0,140,'2018-06-03 18:51:38','5',NULL,'1',NULL,'2018-06-03 10:51:38',0),(0,'54641988','','1489','201806','QW00107136',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'87',NULL,1,'2018-06-03 19:00:07',2,'2018-06-03 19:01:03',1,'2018-06-03 19:00:07',0,145,'2018-06-03 19:01:03','5',NULL,'1',NULL,'2018-06-03 11:01:03',0),(0,'54641988','','4552','201806','QW00107137',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'88',NULL,1,'2018-06-03 19:07:34',2,'2018-06-03 19:07:41',1,'2018-06-03 19:07:34',0,133,'2018-06-03 19:07:41','5',NULL,'1',NULL,'2018-06-03 11:07:42',0),(0,'54641988','','6473','201806','QW00107138',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'89',NULL,1,'2018-06-03 19:09:16',2,'2018-06-03 19:09:23',1,'2018-06-03 19:09:16',0,147,'2018-06-03 19:09:23','5',NULL,'1',NULL,'2018-06-03 11:09:24',0),(0,'54641988','','4381','201806','QW00107139',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'90',NULL,1,'2018-06-03 19:39:13',2,'2018-06-03 19:39:23',1,'2018-06-03 19:39:13',0,138,'2018-06-03 19:39:23','5',NULL,'1',NULL,'2018-06-03 11:39:24',0),(0,'54641988','','9279','201806','QW00107140',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'91',NULL,1,'2018-06-03 19:56:00',2,'2018-06-03 19:56:10',1,'2018-06-03 19:56:00',0,135,'2018-06-03 19:56:10','5',NULL,'1',NULL,'2018-06-03 11:56:11',0),(0,'54641988','','0705','201806','QW00107141',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'92',NULL,1,'2018-06-03 20:05:39',2,'2018-06-03 20:05:52',1,'2018-06-03 20:05:39',0,149,'2018-06-03 20:05:52','5',NULL,'1',NULL,'2018-06-03 12:05:53',0),(0,'54641988','','7486','201806','QW00107142',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'93',NULL,1,'2018-06-03 20:09:13',2,'2018-06-03 20:10:01',1,'2018-06-03 20:09:13',0,136,'2018-06-03 20:10:01','5',NULL,'1',NULL,'2018-06-03 12:10:02',0),(0,'54641988','','0868','201806','QW00107143',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'94',NULL,1,'2018-06-03 20:12:42',2,'2018-06-03 20:13:03',1,'2018-06-03 20:12:42',0,148,'2018-06-03 20:13:03','5',NULL,'1',NULL,'2018-06-03 12:13:04',0),(0,'54641988','','1388','201806','QW00107144',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'95',NULL,1,'2018-06-03 20:13:16',2,'2018-06-03 20:13:24',1,'2018-06-03 20:13:16',0,151,'2018-06-03 20:13:24','5',NULL,'1',NULL,'2018-06-03 12:13:25',0),(0,'54641988','','9900','201806','QW00107145',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'96',NULL,1,'2018-06-03 20:15:41',2,'2018-06-03 20:15:52',1,'2018-06-03 20:15:41',0,150,'2018-06-03 20:15:52','5',NULL,'1',NULL,'2018-06-03 12:15:53',0),(0,'54641988','','1762','201806','QW00107146',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'97',NULL,1,'2018-06-03 20:17:13',0,'0000-00-00 00:00:00',1,'2018-06-03 20:17:13',0,144,'0000-00-00 00:00:00','',NULL,'1',NULL,'2018-06-03 12:17:21',0),(0,'54641988','','5170','201806','QW00107147',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'98',NULL,1,'2018-06-03 20:20:06',2,'2018-06-03 20:20:14',1,'2018-06-03 20:20:06',0,-1,'2018-06-03 20:20:14','5',NULL,'1',NULL,'2018-06-03 12:20:15',0),(0,'54641988','','9202','201806','QW00107148',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'99',NULL,1,'2018-06-03 20:20:35',0,'0000-00-00 00:00:00',1,'2018-06-03 20:20:35',0,153,'0000-00-00 00:00:00','',NULL,'1',NULL,'2018-06-03 12:20:51',0),(0,'54641988','','4102','201806','QW00107149',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'100',NULL,1,'2018-06-03 20:30:26',2,'2018-06-03 20:30:41',1,'2018-06-03 20:30:26',0,-1,'2018-06-03 20:30:41','5',NULL,'1',NULL,'2018-06-03 12:30:41',0),(0,'54641988','','3480','201806','QW00107150',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'101',NULL,1,'2018-06-03 20:50:09',2,'2018-06-03 20:50:17',1,'2018-06-03 20:50:09',0,146,'2018-06-03 20:50:17','5',NULL,'1',NULL,'2018-06-03 12:50:17',0),(0,'54641988','','3408','201806','QW00107151',0,0,0,'','1234',140,140,NULL,NULL,'1','1','1234',NULL,'102',NULL,1,'2018-06-03 21:02:37',2,'2018-06-03 21:03:30',1,'2018-06-03 21:02:37',0,143,'2018-06-03 21:03:30','5',NULL,'1',NULL,'2018-06-03 13:03:31',0),(0,'54641988','','8807','201806','QW00107152',0,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'103',NULL,1,'2018-06-03 21:28:21',2,'2018-06-03 21:28:35',1,'2018-06-03 21:28:21',0,152,'2018-06-03 21:28:35','5',NULL,'1',NULL,'2018-06-03 13:28:36',0),(0,'54641988','','4726','201806','QW00107153',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'104',NULL,1,'2018-06-04 07:10:48',2,'2018-06-04 07:11:21',1,'2018-06-04 07:10:48',0,154,'2018-06-04 07:11:21','5',NULL,'1',NULL,'2018-06-03 23:11:22',0),(0,'54641988','','0510','201806','QW00107154',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'105',NULL,1,'2018-06-04 08:21:38',2,'2018-06-04 08:21:52',1,'2018-06-04 08:21:38',0,155,'2018-06-04 08:21:52','5',NULL,'1',NULL,'2018-06-04 00:21:52',0),(0,'54641988','','3445','201806','QW00107155',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'106',NULL,1,'2018-06-04 11:11:38',2,'2018-06-04 11:11:51',1,'2018-06-04 11:11:38',0,156,'2018-06-04 11:11:51','5',NULL,'1',NULL,'2018-06-04 03:11:52',0),(0,'54641988','','4840','201806','QW00107156',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'107',NULL,1,'2018-06-04 12:21:32',2,'2018-06-04 12:21:46',1,'2018-06-04 12:21:32',0,159,'2018-06-04 12:21:46','5',NULL,'1',NULL,'2018-06-04 04:21:46',0),(0,'54641988','','7274','201806','QW00107157',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'108',NULL,1,'2018-06-04 12:26:59',2,'2018-06-04 12:27:06',1,'2018-06-04 12:26:59',0,158,'2018-06-04 12:27:06','5',NULL,'1',NULL,'2018-06-04 04:27:07',0),(0,'54641988','','4165','201806','QW00107158',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'109',NULL,1,'2018-06-04 13:01:27',2,'2018-06-04 13:01:40',1,'2018-06-04 13:01:27',0,161,'2018-06-04 13:01:40','5',NULL,'1',NULL,'2018-06-04 05:01:40',0),(0,'54641988','','3619','201806','QW00107159',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'110',NULL,1,'2018-06-04 14:04:38',2,'2018-06-04 14:04:46',1,'2018-06-04 14:04:38',0,163,'2018-06-04 14:04:46','5',NULL,'1',NULL,'2018-06-04 06:04:46',0),(0,'54641988','','4840','201806','QW00107160',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'111',NULL,1,'2018-06-04 14:14:05',2,'2018-06-04 14:14:12',1,'2018-06-04 14:14:05',0,164,'2018-06-04 14:14:12','5',NULL,'1',NULL,'2018-06-04 06:14:13',0),(0,'54641988','','4918','201806','QW00107161',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'112',NULL,1,'2018-06-04 14:22:35',2,'2018-06-04 14:22:42',1,'2018-06-04 14:22:35',0,165,'2018-06-04 14:22:42','5',NULL,'1',NULL,'2018-06-04 06:22:43',0),(0,'54641988','','7682','201806','QW00107162',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'113',NULL,1,'2018-06-04 14:24:49',2,'2018-06-04 14:24:55',1,'2018-06-04 14:24:49',0,160,'2018-06-04 14:24:55','5',NULL,'1',NULL,'2018-06-04 06:24:56',0),(0,'54641988','','7637','201806','QW00107163',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'114',NULL,1,'2018-06-04 16:33:17',2,'2018-06-04 16:33:24',1,'2018-06-04 16:33:17',0,167,'2018-06-04 16:33:24','5',NULL,'1',NULL,'2018-06-04 08:33:25',0),(0,'54641988','16145734','7625','201806','QW00107164',3,0,0,'','1234',100,100,NULL,NULL,'1','1','1234',NULL,'115',NULL,1,'2018-06-04 17:26:03',2,'2018-06-04 17:26:15',1,'2018-06-04 17:26:03',0,166,'2018-06-04 17:26:15','5',NULL,'1',NULL,'2018-06-04 09:26:16',0),(0,'54641988','','5937','201806','QW00107165',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'116',NULL,1,'2018-06-04 18:16:03',2,'2018-06-04 18:16:11',1,'2018-06-04 18:16:03',0,169,'2018-06-04 18:16:11','5',NULL,'1',NULL,'2018-06-04 10:16:12',0),(0,'54641988','','2356','201806','QW00107166',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'117',NULL,1,'2018-06-04 18:53:58',2,'2018-06-04 18:54:07',1,'2018-06-04 18:53:58',0,170,'2018-06-04 18:54:07','5',NULL,'1',NULL,'2018-06-04 10:54:08',0),(0,'54641988','','7909','201806','QW00107167',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'118',NULL,1,'2018-06-04 20:02:31',2,'2018-06-04 20:02:39',1,'2018-06-04 20:02:31',0,177,'2018-06-04 20:02:39','5',NULL,'1',NULL,'2018-06-04 12:02:40',0),(0,'54641988','','6810','201806','QW00107168',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'119',NULL,1,'2018-06-04 20:08:32',2,'2018-06-04 20:08:38',1,'2018-06-04 20:08:32',0,176,'2018-06-04 20:08:38','5',NULL,'1',NULL,'2018-06-04 12:08:39',0),(0,'54641988','','9530','201806','QW00107169',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'120',NULL,1,'2018-06-04 20:25:54',2,'2018-06-04 20:26:01',1,'2018-06-04 20:25:54',0,174,'2018-06-04 20:26:01','5',NULL,'1',NULL,'2018-06-04 12:26:02',0),(0,'54641988','','4104','201806','QW00107170',0,0,0,'','1234',60,60,NULL,NULL,'1','1','1234',NULL,'121',NULL,1,'2018-06-04 20:28:51',2,'2018-06-04 20:28:58',1,'2018-06-04 20:28:51',0,172,'2018-06-04 20:28:58','5',NULL,'1',NULL,'2018-06-04 12:28:59',0),(0,'54641988','','1429','201806','QW00107171',0,0,0,'','1234',40,40,NULL,NULL,'1','1','1234',NULL,'122',NULL,1,'2018-06-04 20:35:20',2,'2018-06-04 20:35:27',1,'2018-06-04 20:35:20',0,175,'2018-06-04 20:35:27','5',NULL,'1',NULL,'2018-06-04 12:35:27',0),(0,'54641988','','2111','201806','QW00107172',0,0,0,'','1234',80,80,NULL,NULL,'1','1','1234',NULL,'123',NULL,1,'2018-06-04 20:51:51',2,'2018-06-04 20:51:58',1,'2018-06-04 20:51:51',0,171,'2018-06-04 20:51:58','5',NULL,'1',NULL,'2018-06-04 12:51:59',0),(0,'54641988','54773875','8510','201806','QW00107173',3,0,0,'','1234',180,180,NULL,NULL,'1','1','1234',NULL,'124',NULL,1,'2018-06-04 21:10:36',2,'2018-06-04 21:11:06',1,'2018-06-04 21:10:36',0,168,'2018-06-04 21:11:06','5',NULL,'1',NULL,'2018-06-04 13:11:07',0),(0,'54641988','','1785','201806','QW00107174',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'125',NULL,1,'2018-06-04 22:01:29',2,'2018-06-04 22:01:36',1,'2018-06-04 22:01:29',0,173,'2018-06-04 22:01:36','5',NULL,'1',NULL,'2018-06-04 14:01:37',0),(0,'54641988','','6177','201806','QW00107175',0,0,0,'','1234',120,120,NULL,NULL,'1','1','1234',NULL,'126',NULL,1,'2018-06-04 22:08:06',2,'2018-06-04 22:08:14',1,'2018-06-04 22:08:06',0,-1,'2018-06-04 22:08:14','5',NULL,'1',NULL,'2018-06-04 14:08:15',0),(0,'54641988','','9984','201806','QW00107176',0,0,0,'','1234',170,170,NULL,NULL,'1','1','1234',NULL,'127',NULL,1,'2018-06-05 07:49:53',2,'2018-06-05 07:50:20',1,'2018-06-05 07:49:53',0,178,'2018-06-05 07:50:20','5',NULL,'1',NULL,'2018-06-04 23:50:20',0);
/*!40000 ALTER TABLE `e_invoice_number_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `entry_gate`
--

DROP TABLE IF EXISTS `entry_gate`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry_gate` (
  `entry_gate_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `garage_id` int(11) DEFAULT NULL,
  `entry_gate_sn` int(11) DEFAULT NULL,
  `direction` int(11) DEFAULT '1' COMMENT 'entry_gate direction',
  `has_e_envoicing` int(11) DEFAULT '1' COMMENT 'using electronic envoice',
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`entry_gate_id`),
  UNIQUE KEY `entry_gate_id` (`entry_gate_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entry_gate`
--

LOCK TABLES `entry_gate` WRITE;
/*!40000 ALTER TABLE `entry_gate` DISABLE KEYS */;
/*!40000 ALTER TABLE `entry_gate` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `event_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `SystemEventType` int(11) DEFAULT NULL,
  `event_subtype` int(11) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`event_id`),
  UNIQUE KEY `event_id` (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exit_config`
--

DROP TABLE IF EXISTS `exit_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exit_config` (
  `exit_config_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `garage_id` int(11) DEFAULT NULL,
  `description` varchar(100) DEFAULT '',
  `is_configured` int(11) DEFAULT '0',
  `disabled` int(11) DEFAULT '0',
  `update_account_id` int(11) DEFAULT NULL,
  `update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`exit_config_id`),
  UNIQUE KEY `exit_config_id` (`exit_config_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exit_config`
--

LOCK TABLES `exit_config` WRITE;
/*!40000 ALTER TABLE `exit_config` DISABLE KEYS */;
INSERT INTO `exit_config` VALUES (1,1,'',0,0,NULL,'2018-05-21 11:44:36');
/*!40000 ALTER TABLE `exit_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exit_type_config_detail`
--

DROP TABLE IF EXISTS `exit_type_config_detail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `exit_type_config_detail` (
  `exit_type_config_detail_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `exit_type` varchar(50) NOT NULL,
  `exit_config_id` int(11) NOT NULL,
  `exit_type_disabled` int(11) DEFAULT '0',
  PRIMARY KEY (`exit_type_config_detail_id`),
  UNIQUE KEY `exit_type_config_detail_id` (`exit_type_config_detail_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exit_type_config_detail`
--

LOCK TABLES `exit_type_config_detail` WRITE;
/*!40000 ALTER TABLE `exit_type_config_detail` DISABLE KEYS */;
INSERT INTO `exit_type_config_detail` VALUES (1,'正常出場',1,0),(2,'預收',1,0),(3,'貴賓車',1,0),(4,'過夜車',1,0),(5,'輸入錯誤',1,0),(6,'客人突然不停',1,0),(7,'清場不明原因離場',1,0),(8,'長租',1,0),(9,'短租',1,0),(10,'住宿',1,0),(11,'用餐',1,0),(12,'其他',1,0);
/*!40000 ALTER TABLE `exit_type_config_detail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garage`
--

DROP TABLE IF EXISTS `garage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `garage` (
  `garage_code` varchar(10) NOT NULL COMMENT 'Acer ITS defined garage code',
  `garage_name` varchar(50) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `city_name` varchar(50) DEFAULT NULL,
  `city_code` varchar(3) DEFAULT NULL,
  `district` varchar(10) DEFAULT NULL,
  `district_code` varchar(3) DEFAULT NULL,
  `address1` varchar(255) DEFAULT NULL,
  `address2` varchar(255) DEFAULT NULL,
  `total_capacity` int(11) DEFAULT '0',
  `sedan_capacity` int(11) DEFAULT '0',
  `motocycle_capacity` int(11) DEFAULT '0',
  `sedan_priority_pragnant_capacity` int(11) DEFAULT '0',
  `motocycle_priority_pragnant_capacity` int(11) DEFAULT '0',
  `sedan_priority_disability_capacity` int(11) DEFAULT '0',
  `motocycle_priority_disability_capacity` int(11) DEFAULT '0',
  `garage_lat` varchar(50) DEFAULT NULL,
  `garage_lng` varchar(50) DEFAULT NULL,
  `caculation_time_base_unit` int(11) DEFAULT '0' COMMENT '分:0/秒:1',
  `charge_infomation` varchar(1000) DEFAULT NULL,
  `supplementary_details` varchar(1000) DEFAULT NULL,
  `business_hour_begin` varchar(5) DEFAULT NULL,
  `business_hour_end` varchar(5) DEFAULT NULL,
  `number_of_entrance` int(11) DEFAULT '0',
  `number_of_exit` int(11) DEFAULT '0',
  `number_of_driveway_in` int(11) DEFAULT '0',
  `number_of_driveway_out` int(11) DEFAULT '0',
  `management_type` int(11) DEFAULT '0' COMMENT '0:固定都有管理員/2:不定時巡視管理員/3:無管理員',
  `garage_type` int(11) DEFAULT NULL COMMENT '0:平面、1:車塔、2:機械、3:平面/機械混合、4:地下室',
  `lot_type` int(11) DEFAULT NULL COMMENT '室內還是室外停車場 室內:0/室外:1',
  `establish_status` int(11) DEFAULT NULL COMMENT '建置狀態 完成:0/建置中:1',
  `max_clearance` varchar(5) DEFAULT NULL COMMENT '車高限制',
  `on_site_liaison` varchar(20) DEFAULT NULL COMMENT '現場聯絡人',
  `on_site_phone` varchar(20) DEFAULT NULL COMMENT '現場聯絡電話',
  `on_site_email` varchar(20) DEFAULT NULL COMMENT '現場email',
  `on_site_cell_phone` varchar(20) DEFAULT NULL COMMENT '場站電話',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `garage_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `customer_garage_id` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`garage_id`),
  UNIQUE KEY `garage_id` (`garage_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garage`
--

LOCK TABLES `garage` WRITE;
/*!40000 ALTER TABLE `garage` DISABLE KEYS */;
INSERT INTO `garage` VALUES ('1','晴美站',1,'台北市',NULL,'中正區',NULL,'台北市中山區林森北路566號B2',NULL,38,38,0,0,0,0,0,NULL,NULL,0,NULL,NULL,NULL,NULL,1,1,1,1,1,0,1,0,NULL,'王振民','02-27098677',NULL,'0911078001','2018-05-21 10:30:14','2018-06-02 05:21:07',3,2,1,'R17'),('test','123',NULL,'台北市',NULL,NULL,NULL,NULL,NULL,0,0,0,0,0,0,0,NULL,NULL,1,NULL,NULL,NULL,NULL,0,0,0,0,1,NULL,1,0,NULL,NULL,NULL,NULL,NULL,'2018-05-23 04:18:32','2018-06-01 07:26:49',3,2,2,'R17');
/*!40000 ALTER TABLE `garage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `garage_group`
--

DROP TABLE IF EXISTS `garage_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `garage_group` (
  `garage_group_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `garage_group_name` varchar(255) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `description` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`garage_group_id`),
  UNIQUE KEY `garage_group_id` (`garage_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `garage_group`
--

LOCK TABLES `garage_group` WRITE;
/*!40000 ALTER TABLE `garage_group` DISABLE KEYS */;
INSERT INTO `garage_group` VALUES (1,'2018-05-21 10:27:25','2018-05-21 10:27:25',2,2,'中山區',1,NULL,'中山區場站'),(2,'2018-05-21 10:27:51','2018-05-21 10:27:51',3,NULL,'信義區',1,NULL,'信義區場站'),(3,'2018-05-23 09:51:15','2018-05-23 09:51:15',3,NULL,'test',NULL,NULL,NULL);
/*!40000 ALTER TABLE `garage_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `keystore`
--

DROP TABLE IF EXISTS `keystore`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `keystore` (
  `keystore_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `key_version` varchar(150) NOT NULL,
  `key_type` varchar(150) DEFAULT NULL,
  `fixed_account_total` int(11) NOT NULL DEFAULT '1',
  `dynamic_account_total` int(11) NOT NULL DEFAULT '1',
  `key_manager_email` varchar(255) NOT NULL,
  `service_type` varchar(30) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `start_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `key_status` varchar(30) NOT NULL,
  `key_validation_status` varchar(30) DEFAULT NULL,
  `key_value` varchar(4000) NOT NULL,
  PRIMARY KEY (`keystore_id`),
  UNIQUE KEY `keystore_id` (`keystore_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `keystore`
--

LOCK TABLES `keystore` WRITE;
/*!40000 ALTER TABLE `keystore` DISABLE KEYS */;
/*!40000 ALTER TABLE `keystore` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lane`
--

DROP TABLE IF EXISTS `lane`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `lane` (
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
  `MEntryB` varchar(10) NOT NULL COMMENT '最小入場餘額 Format: 999.99',
  `MExitD` int(5) NOT NULL COMMENT '最長出場前緩衝時間',
  `pv_version` varchar(20) NOT NULL,
  `last_response_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `response_type` varchar(4) NOT NULL DEFAULT '00',
  `invoice_printer_status` varchar(2) NOT NULL DEFAULT '00' COMMENT 'ref [invoice_printer_error_def].code',
  `pricing_scheme_disability` int(2) NOT NULL DEFAULT '0' COMMENT '身障計費規則',
  `pv_response_confirm` tinyint(1) NOT NULL DEFAULT '0' COMMENT 'PV是否回傳confirm(1:是-新連線,0:否-舊連線',
  `etag_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否為eTag車道(1:是,0:否)',
  `costrule_using_para` tinyint(1) NOT NULL DEFAULT '0' COMMENT '計費規則是否使用參數化(1:是,0:否)',
  `lane_costrule_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '車道計費模式(1:複合, 0:單一)',
  `gate_control_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '閘門控制模式(0:維持, 1:開門)',
  `lpr_lane` varchar(4) NOT NULL DEFAULT '99' COMMENT '車辨車道代碼',
  `source_filename` varchar(100) DEFAULT NULL,
  `garage_code` varchar(20) DEFAULT NULL,
  `csv_file_date` varchar(20) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lane_id` int(10) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`lane_id`),
  KEY `type` (`type`),
  KEY `pricing_scheme` (`pricing_scheme`),
  KEY `pv_ip` (`pv_ip`),
  KEY `MEntryB` (`MEntryB`),
  KEY `in_out` (`in_out`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lane`
--

LOCK TABLES `lane` WRITE;
/*!40000 ALTER TABLE `lane` DISABLE KEYS */;
/*!40000 ALTER TABLE `lane` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `license_info`
--

DROP TABLE IF EXISTS `license_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `license_info` (
  `license_info_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `requested_keystore` varchar(2000) DEFAULT NULL,
  `applied_keystore` varchar(2000) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `key_version` varchar(150) NOT NULL,
  `key_type` varchar(150) DEFAULT NULL,
  `fixed_account_total` int(11) NOT NULL DEFAULT '1',
  `dyanmic_account_total` int(11) NOT NULL DEFAULT '1',
  `key_manager_email` varchar(255) NOT NULL,
  `service_type` varchar(30) NOT NULL,
  `note` varchar(255) DEFAULT NULL,
  `start_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `key_status` varchar(30) NOT NULL,
  `key_string` varchar(2000) NOT NULL,
  PRIMARY KEY (`license_info_id`),
  UNIQUE KEY `license_info_id` (`license_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `license_info`
--

LOCK TABLES `license_info` WRITE;
/*!40000 ALTER TABLE `license_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `license_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_garage_group_to_account`
--

DROP TABLE IF EXISTS `map_garage_group_to_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `map_garage_group_to_account` (
  `garage_group_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_garage_group_to_account`
--

LOCK TABLES `map_garage_group_to_account` WRITE;
/*!40000 ALTER TABLE `map_garage_group_to_account` DISABLE KEYS */;
INSERT INTO `map_garage_group_to_account` VALUES (2,2),(1,2),(1,1),(1,3),(1,5);
/*!40000 ALTER TABLE `map_garage_group_to_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_garage_to_account`
--

DROP TABLE IF EXISTS `map_garage_to_account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `map_garage_to_account` (
  `garage_id` int(11) DEFAULT NULL,
  `account_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_garage_to_account`
--

LOCK TABLES `map_garage_to_account` WRITE;
/*!40000 ALTER TABLE `map_garage_to_account` DISABLE KEYS */;
/*!40000 ALTER TABLE `map_garage_to_account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_garage_to_garage_group`
--

DROP TABLE IF EXISTS `map_garage_to_garage_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `map_garage_to_garage_group` (
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `garage_id` int(11) DEFAULT NULL,
  `garage_group_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_garage_to_garage_group`
--

LOCK TABLES `map_garage_to_garage_group` WRITE;
/*!40000 ALTER TABLE `map_garage_to_garage_group` DISABLE KEYS */;
INSERT INTO `map_garage_to_garage_group` VALUES ('2018-05-23 09:51:15','2018-05-23 09:51:15',NULL,NULL,1,3),('2018-05-24 03:56:17','2018-05-24 03:56:17',NULL,NULL,1,1);
/*!40000 ALTER TABLE `map_garage_to_garage_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_garage_to_system_config`
--

DROP TABLE IF EXISTS `map_garage_to_system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `map_garage_to_system_config` (
  `map_garage_to_system_config_id` int(11) NOT NULL,
  `garage_id` int(11) DEFAULT NULL COMMENT '停車場站編號',
  `system_config_id` int(11) DEFAULT NULL COMMENT '系統設定編號',
  `modified_account_id` int(11) DEFAULT NULL,
  `modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
  PRIMARY KEY (`map_garage_to_system_config_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系統參數與停車廠站對應';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_garage_to_system_config`
--

LOCK TABLES `map_garage_to_system_config` WRITE;
/*!40000 ALTER TABLE `map_garage_to_system_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `map_garage_to_system_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `map_role_permission`
--

DROP TABLE IF EXISTS `map_role_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `map_role_permission` (
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  `permission_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `map_role_permission`
--

LOCK TABLES `map_role_permission` WRITE;
/*!40000 ALTER TABLE `map_role_permission` DISABLE KEYS */;
INSERT INTO `map_role_permission` VALUES ('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,1),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,2),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,3),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,4),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,5),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,6),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,11),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,12),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,13),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,21),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,22),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,23),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,191),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,192),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,193),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,31),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,32),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,33),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,41),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,42),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,43),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,51),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,52),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,53),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,54),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,61),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,62),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,63),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,65),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,64),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,66),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,67),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,71),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,72),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,73),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,74),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,75),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,81),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,82),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,83),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,91),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,92),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,93),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,111),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,112),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,113),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,121),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,122),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,123),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,131),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,132),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,133),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,141),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,142),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,143),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,144),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,151),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,152),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,153),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,154),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,161),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,162),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,163),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,163),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,181),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,1,182),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,1),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,2),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,3),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,4),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,5),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,6),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,11),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,12),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,13),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,31),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,32),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,33),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,91),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,92),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,93),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,111),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,112),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,113),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,131),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,143),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,181),('2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,2,182),('2018-05-21 10:26:31','2018-05-21 10:26:31',NULL,NULL,3,131),('2018-05-21 10:26:31','2018-05-21 10:26:31',NULL,NULL,3,143),('2018-05-21 10:26:31','2018-05-21 10:26:31',NULL,NULL,3,181),('2018-05-21 10:26:31','2018-05-21 10:26:31',NULL,NULL,3,182);
/*!40000 ALTER TABLE `map_role_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking`
--

DROP TABLE IF EXISTS `parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parking` (
  `id` int(11) DEFAULT NULL COMMENT '舊PMS parking_id',
  `pv` varchar(32) NOT NULL,
  `pv_out` varchar(32) NOT NULL,
  `card_id` varchar(32) NOT NULL,
  `card_id16` varchar(32) NOT NULL,
  `enter_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `exit_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `paid_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `duration` int(10) NOT NULL DEFAULT '0',
  `fee` int(10) NOT NULL DEFAULT '0',
  `real_fee` int(10) NOT NULL DEFAULT '0',
  `note` text NOT NULL,
  `paid_type` varchar(2) NOT NULL DEFAULT '00',
  `entry_balance` int(4) NOT NULL DEFAULT '0' COMMENT '進場時卡片餘額',
  `exit_balance` int(4) NOT NULL DEFAULT '0' COMMENT '出場時卡片餘額(扣款前)',
  `settlement_type` tinyint(3) NOT NULL DEFAULT '0' COMMENT '1:待確認交易,2:ECC補寫log',
  `txn_datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00' COMMENT '待確認PV交易時間',
  `txn_amt` int(4) NOT NULL DEFAULT '0' COMMENT '待確認交易金額',
  `disability_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否為身障計費(1:是,0:否)',
  `card_autoload_flag` tinyint(1) NOT NULL DEFAULT '0' COMMENT '卡片自動加值FLAG',
  `entry_mode` tinyint(1) NOT NULL DEFAULT '1' COMMENT '進場設備放行類別(0:無法辨識, 1:PV, 2:eTag, 3: 河南OBU, 4:車辨設備系統)',
  `last_source_filename` varchar(100) DEFAULT NULL,
  `garage_code` varchar(20) DEFAULT NULL,
  `last_csv_file_date` varchar(20) DEFAULT NULL,
  `parking_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `vehicle_identification_number` varchar(10) DEFAULT '000-0000',
  `modified_date` datetime DEFAULT NULL COMMENT '資料修改日期',
  `vehicle_type` int(2) DEFAULT NULL COMMENT '車類型 0:unknown,1:sedan,2:motocycle,3:truck,4:bus',
  `enter_account_id` int(11) DEFAULT NULL COMMENT '入場紀錄帳號',
  `exit_account_id` int(11) DEFAULT NULL COMMENT '出場紀錄帳號',
  `einvoice` varchar(20) DEFAULT NULL COMMENT '電子發票號碼',
  `einvoice_use_status` tinyint(1) DEFAULT NULL COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)',
  PRIMARY KEY (`parking_id`),
  UNIQUE KEY `parking_id` (`parking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=180 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking`
--

LOCK TABLES `parking` WRITE;
/*!40000 ALTER TABLE `parking` DISABLE KEYS */;
INSERT INTO `parking` VALUES (NULL,'進場','出場','666666','666666','2018-06-01 15:59:22','2018-06-01 16:09:01','0000-00-00 00:00:00',0,40,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,52,'2018-06-01 07:59:42','34576',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 16:00:04','2018-06-01 16:02:49','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,53,'2018-06-01 08:00:29','92298',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 16:01:59','2018-06-01 17:28:46','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,54,'2018-06-01 08:02:16','702727',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 16:07:56','2018-06-01 16:08:24','0000-00-00 00:00:00',0,40,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,55,'2018-06-01 08:08:05','836004',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 16:19:05','2018-06-01 16:19:58','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,56,'2018-06-01 08:19:26','123408',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 16:43:55','2018-06-01 16:44:40','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,57,'2018-06-01 08:44:18','123409',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 17:03:10','2018-06-01 19:42:22','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,58,'2018-06-01 09:03:19','116720',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 17:31:44','2018-06-01 17:31:58','0000-00-00 00:00:00',0,40,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,59,'2018-06-01 09:31:52','AKT-8077',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 18:24:27','2018-06-01 19:12:48','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,60,'2018-06-01 10:24:37','125038',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 18:42:37','2018-06-01 21:40:08','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,61,'2018-06-01 10:42:47','963308',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 18:52:37','2018-06-01 21:30:03','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,62,'2018-06-01 10:52:46','828337',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:19:54','2018-06-01 20:16:05','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,63,'2018-06-01 11:20:05','890338',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:25:18','2018-06-01 20:59:48','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,64,'2018-06-01 11:25:26','955811',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:29:48','2018-06-01 20:03:12','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,65,'2018-06-01 11:29:59','936719',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:35:04','2018-06-01 20:42:26','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,66,'2018-06-01 11:35:13','153715',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:40:49','2018-06-01 22:16:35','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,67,'2018-06-01 11:40:57','768816',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 19:57:11','2018-06-01 20:39:32','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,68,'2018-06-01 11:57:23','035720',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 20:31:30','2018-06-01 21:00:33','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,69,'2018-06-01 12:31:37','225538',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 20:59:05','2018-06-01 22:37:27','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,70,'2018-06-01 12:59:13','808719',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 21:05:33','2018-06-01 21:33:31','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,71,'2018-06-01 13:05:40','846511',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-01 21:32:44','2018-06-01 22:06:31','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,72,'2018-06-01 13:32:53','203637',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 08:02:43','2018-06-02 08:29:14','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,73,'2018-06-02 00:03:09','263105',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 08:03:30','2018-06-02 16:44:08','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,74,'2018-06-02 00:03:41','239803',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 08:22:23','2018-06-02 08:26:35','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,75,'2018-06-02 00:26:28','473306',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 08:30:39','2018-06-02 08:30:56','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,76,'2018-06-02 00:30:53','473306',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 08:34:45','2018-06-02 11:31:15','0000-00-00 00:00:00',0,120,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,77,'2018-06-02 01:50:38','253305',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 10:45:54','2018-06-02 12:50:02','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,78,'2018-06-02 02:46:07','806004',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 11:04:19','2018-06-02 14:25:14','0000-00-00 00:00:00',0,140,140,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,79,'2018-06-02 03:04:30','675707',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 11:20:47','2018-06-02 12:47:34','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,80,'2018-06-02 03:20:57','011908',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 11:43:22','2018-06-02 12:54:22','0000-00-00 00:00:00',0,60,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,81,'2018-06-02 03:58:54','500011',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 11:59:41','2018-06-02 14:28:11','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,82,'2018-06-02 04:16:23','581812',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 12:17:11','2018-06-02 15:00:21','0000-00-00 00:00:00',0,120,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,83,'2018-06-02 04:38:03','739515',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 12:43:39','2018-06-02 12:46:03','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,84,'2018-06-02 04:43:49','173616',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 12:56:30','2018-06-02 13:04:15','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,85,'2018-06-02 05:02:04','063111',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 13:04:45','2018-06-02 18:45:59','0000-00-00 00:00:00',0,170,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,86,'2018-06-02 05:22:33','973805',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 13:27:25','2018-06-02 14:37:44','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,87,'2018-06-02 05:27:33','755010',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 13:37:54','2018-06-02 17:19:39','0000-00-00 00:00:00',0,160,160,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,88,'2018-06-02 05:38:04','253909',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 13:39:10','2018-06-02 14:06:27','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,89,'2018-06-02 05:46:17','881004',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 13:46:42','2018-06-02 20:53:41','0000-00-00 00:00:00',0,170,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,90,'2018-06-02 06:01:20','617908',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 14:06:46','2018-06-02 18:17:59','0000-00-00 00:00:00',0,170,140,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,91,'2018-06-02 06:09:14','082237',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 14:34:17','2018-06-02 15:30:44','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,92,'2018-06-02 06:34:27','501612',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 15:07:21','2018-06-02 15:28:47','0000-00-00 00:00:00',0,40,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,93,'2018-06-02 07:07:35','963804',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 15:21:59','2018-06-02 21:09:18','0000-00-00 00:00:00',0,170,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,94,'2018-06-02 07:22:10','972007',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 15:36:01','2018-06-02 18:42:45','0000-00-00 00:00:00',0,140,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,95,'2018-06-02 07:36:08','130012',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 15:41:36','2018-06-02 16:51:06','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,96,'2018-06-02 07:41:49','922810',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 15:59:44','2018-06-02 16:08:10','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,97,'2018-06-02 08:00:02','WQ-1222',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 16:04:41','2018-06-02 18:17:40','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,98,'2018-06-02 08:05:26','687513',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 16:18:03','2018-06-02 16:18:15','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,99,'2018-06-02 08:18:12','AA-123',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 17:27:05','2018-06-02 21:34:17','0000-00-00 00:00:00',0,170,160,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,100,'2018-06-02 09:27:15','811910',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 17:33:03','2018-06-02 19:24:11','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,101,'2018-06-02 09:33:12','588003',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 17:44:27','2018-06-02 18:16:53','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,102,'2018-06-02 09:44:36','588909',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 18:28:23','2018-06-02 19:03:59','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,103,'2018-06-02 10:28:32','315537',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 18:32:45','2018-06-02 20:06:42','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,104,'2018-06-02 10:32:58','999738',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 18:50:51','2018-06-02 20:06:52','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,105,'2018-06-02 10:50:59','166808',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 18:55:35','2018-06-02 19:36:40','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,106,'2018-06-02 10:55:44','619205',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 19:23:55','2018-06-02 20:24:24','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,107,'2018-06-02 11:24:05','577904',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 20:02:38','2018-06-02 21:39:07','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,108,'2018-06-02 12:02:47','900237',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-02 20:09:27','2018-06-02 21:21:14','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,109,'2018-06-02 12:09:39','515738',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 07:22:27','2018-06-03 09:12:02','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,110,'2018-06-02 23:23:08','050508',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 07:48:51','2018-06-03 11:26:29','0000-00-00 00:00:00',0,160,160,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,111,'2018-06-02 23:49:04','595807',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 10:47:10','2018-06-03 11:29:12','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,112,'2018-06-03 02:47:20','318608',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 11:58:17','2018-06-03 14:22:10','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,113,'2018-06-03 03:58:28','669608',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:04:21','2018-06-03 14:31:20','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,114,'2018-06-03 04:04:31','838807',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:08:07','2018-06-03 13:52:38','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,115,'2018-06-03 04:08:17','696706',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:11:30','2018-06-03 13:49:58','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,116,'2018-06-03 04:11:39','388304',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:15:40','2018-06-03 14:38:01','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,117,'2018-06-03 04:15:51','718911',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:17:15','2018-06-03 15:17:26','0000-00-00 00:00:00',0,140,140,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,118,'2018-06-03 04:17:24','799903',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:22:24','2018-06-03 17:57:05','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,119,'2018-06-03 04:22:34','763805',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:26:59','2018-06-03 14:47:42','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,120,'2018-06-03 04:27:08','363701',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:30:55','2018-06-03 13:54:03','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,121,'2018-06-03 04:31:04','158909',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:35:13','2018-06-03 13:06:37','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,122,'2018-06-03 04:35:23','020620',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:37:18','2018-06-03 14:23:06','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,123,'2018-06-03 04:37:47','951812',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:53:15','2018-06-03 18:21:27','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,124,'2018-06-03 04:53:25','968519',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 12:58:29','2018-06-03 13:53:40','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,125,'2018-06-03 04:58:38','698113',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:01:33','2018-06-03 14:56:51','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,126,'2018-06-03 05:01:43','845914',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:08:23','2018-06-03 16:39:08','0000-00-00 00:00:00',0,160,160,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,127,'2018-06-03 05:08:35','096010',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:19:25','2018-06-03 14:40:09','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,128,'2018-06-03 05:19:37','755820',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:25:26','2018-06-03 15:08:58','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,129,'2018-06-03 05:25:36','026515',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:36:18','2018-06-03 17:25:33','0000-00-00 00:00:00',0,160,160,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,130,'2018-06-03 05:36:27','352316',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 13:41:51','2018-06-03 14:29:31','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,131,'2018-06-03 05:42:02','285823',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 14:09:32','2018-06-03 16:24:25','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,132,'2018-06-03 06:09:41','099904',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 14:15:11','2018-06-03 19:07:33','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,133,'2018-06-03 06:15:22','039906',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 14:20:15','2018-06-03 16:43:48','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,134,'2018-06-03 06:20:28','186109',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 14:33:34','2018-06-03 19:56:00','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,135,'2018-06-03 06:33:43','026112',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 15:36:41','2018-06-03 20:09:13','0000-00-00 00:00:00',0,170,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,136,'2018-06-03 07:36:56','159517',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 15:44:05','2018-06-03 17:19:00','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,137,'2018-06-03 07:45:53','581737',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 16:47:31','2018-06-03 19:39:13','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,138,'2018-06-03 08:47:42','506109',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 16:53:56','2018-06-03 17:39:40','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,139,'2018-06-03 08:54:10','719738',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 17:00:20','2018-06-03 18:51:27','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,140,'2018-06-03 09:02:01','186818',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 17:04:56','2018-06-03 18:46:34','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,141,'2018-06-03 09:07:01','165610',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 17:24:12','2018-06-03 18:22:57','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,142,'2018-06-03 09:25:13','582537',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 17:45:14','2018-06-03 21:02:37','0000-00-00 00:00:00',0,140,140,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,143,'2018-06-03 09:47:10','509001',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:06:55','2018-06-03 20:17:13','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,144,'2018-06-03 10:09:00','909838',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:10:21','2018-06-03 19:00:07','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,145,'2018-06-03 10:14:02','286225',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:26:38','2018-06-03 20:50:08','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,146,'2018-06-03 10:29:00','110237',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:31:50','2018-06-03 19:09:16','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,147,'2018-06-03 10:34:06','256626',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:37:13','2018-06-03 20:12:42','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,148,'2018-06-03 10:39:31','033728',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:42:43','2018-06-03 20:05:39','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,149,'2018-06-03 10:44:36','580919',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 18:58:15','2018-06-03 20:15:41','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,150,'2018-06-03 10:59:18','636518',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 19:07:50','2018-06-03 20:13:16','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,151,'2018-06-03 11:08:51','366620',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 19:16:13','2018-06-03 21:28:21','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,152,'2018-06-03 11:16:21','313806',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-03 19:27:20','2018-06-03 20:20:35','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,153,'2018-06-03 11:29:24','680210',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 07:10:11','2018-06-04 07:10:48','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,154,'2018-06-03 23:10:38','595808',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 08:21:22','2018-06-04 08:21:38','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,155,'2018-06-04 00:21:32','473307',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 10:23:00','2018-06-04 11:11:38','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,156,'2018-06-04 02:23:14','209616',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 11:48:04','2018-06-04 22:17:46','0000-00-00 00:00:00',0,170,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,157,'2018-06-04 03:48:25','883233',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 11:50:56','2018-06-04 12:26:59','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,158,'2018-06-04 03:51:09','990504',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 12:15:09','2018-06-04 12:21:32','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,159,'2018-06-04 04:15:18','179616',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 12:30:57','2018-06-04 14:24:49','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,160,'2018-06-04 04:31:08','707104',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 12:39:46','2018-06-04 13:01:27','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,161,'2018-06-04 04:39:56','750715',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 12:44:03','2018-06-04 13:21:43','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,162,'2018-06-04 04:44:13','268003',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 13:06:26','2018-06-04 14:04:38','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,163,'2018-06-04 05:06:35','389315',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 13:16:09','2018-06-04 14:14:05','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,164,'2018-06-04 05:16:19','821011',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 13:32:06','2018-06-04 14:22:35','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,165,'2018-06-04 05:32:15','326503',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 15:08:23','2018-06-04 17:26:03','0000-00-00 00:00:00',0,100,100,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,166,'2018-06-04 07:08:31','666715',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 15:42:04','2018-06-04 16:33:16','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,167,'2018-06-04 07:42:12','588919',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 17:04:34','2018-06-04 21:10:36','0000-00-00 00:00:00',0,170,180,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,168,'2018-06-04 09:04:42','058819',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 17:49:51','2018-06-04 18:16:03','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,169,'2018-06-04 09:49:58','662620',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 18:18:30','2018-06-04 18:53:58','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,170,'2018-06-04 10:18:38','352737',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 18:53:47','2018-06-04 20:51:51','0000-00-00 00:00:00',0,80,80,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,171,'2018-06-04 10:53:55','298808',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 19:05:13','2018-06-04 20:28:51','0000-00-00 00:00:00',0,60,60,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,172,'2018-06-04 11:05:21','092737',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 19:20:57','2018-06-04 22:01:29','0000-00-00 00:00:00',0,120,120,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,173,'2018-06-04 11:21:05','607238',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 19:43:37','2018-06-04 20:25:54','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,174,'2018-06-04 11:43:44','723220',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 20:01:18','2018-06-04 20:35:20','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,175,'2018-06-04 12:01:25','136916',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 20:01:38','2018-06-04 20:08:32','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,176,'2018-06-04 12:01:50','683712',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-04 20:02:20','2018-06-04 20:02:31','0000-00-00 00:00:00',0,40,40,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,177,'2018-06-04 12:02:28','179616',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-05 07:49:40','2018-06-05 07:49:53','0000-00-00 00:00:00',0,40,170,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,178,'2018-06-04 23:49:51','595838',NULL,NULL,NULL,NULL,NULL,NULL),(NULL,'進場','出場','666666','666666','2018-06-05 11:15:57','2018-06-05 11:17:11','0000-00-00 00:00:00',0,40,0,'','00',0,0,0,'0000-00-00 00:00:00',0,0,0,1,NULL,'1',NULL,179,'2018-06-05 03:16:41','8563',NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `parking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking_in_out_record`
--

DROP TABLE IF EXISTS `parking_in_out_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `parking_in_out_record` (
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
  `source_filename` varchar(100) DEFAULT NULL,
  `garage_code` varchar(20) DEFAULT NULL,
  `csv_file_date` varchar(20) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `no` int(11) NOT NULL AUTO_INCREMENT COMMENT '流水號',
  PRIMARY KEY (`no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='PMS交易紀錄';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking_in_out_record`
--

LOCK TABLES `parking_in_out_record` WRITE;
/*!40000 ALTER TABLE `parking_in_out_record` DISABLE KEYS */;
/*!40000 ALTER TABLE `parking_in_out_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `parking_view`
--

DROP TABLE IF EXISTS `parking_view`;
/*!50001 DROP VIEW IF EXISTS `parking_view`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `parking_view` (
  `garage_code` tinyint NOT NULL,
  `id` tinyint NOT NULL,
  `pv` tinyint NOT NULL,
  `pv_out` tinyint NOT NULL,
  `type` tinyint NOT NULL,
  `pricing_scheme` tinyint NOT NULL,
  `pricing_scheme_disability` tinyint NOT NULL,
  `card_id` tinyint NOT NULL,
  `card_id16` tinyint NOT NULL,
  `enter_time` tinyint NOT NULL,
  `exit_time` tinyint NOT NULL,
  `paid_time` tinyint NOT NULL,
  `fee` tinyint NOT NULL,
  `real_fee` tinyint NOT NULL,
  `note` tinyint NOT NULL,
  `paid_type` tinyint NOT NULL,
  `entry_balance` tinyint NOT NULL,
  `exit_balance` tinyint NOT NULL,
  `settlement_type` tinyint NOT NULL,
  `disability_mode` tinyint NOT NULL,
  `customer_id` tinyint NOT NULL
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `permission`
--

DROP TABLE IF EXISTS `permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `permission` (
  `permission_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `permission_type` varchar(10) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `enable` int(11) DEFAULT '1',
  PRIMARY KEY (`permission_id`),
  UNIQUE KEY `permission_id` (`permission_id`)
) ENGINE=InnoDB AUTO_INCREMENT=194 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `permission`
--

LOCK TABLES `permission` WRITE;
/*!40000 ALTER TABLE `permission` DISABLE KEYS */;
INSERT INTO `permission` VALUES (1,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'維運管理','維運管理功能群組','group',0,1),(2,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳號管理','帳號管理功能','page',1,1),(3,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳號修改','帳號管理修改功能','page_featu',2,1),(4,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳號刪除','帳號管理刪除功能ˊ','page_featu',2,1),(5,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳號場站指派','帳號管理場站指派','page_featu',2,1),(6,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳號角色指派','帳號管理角色指派','page_featu',2,1),(11,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'角色管理','角色管理功能','page',0,1),(12,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'角色修改','角色管理修改功能','page_featu',11,1),(13,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'角色刪除','角色管理刪除功能ˊ','page_featu',11,1),(21,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶管理','客戶管理功能','page',0,1),(22,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶基本設定修改','客戶管理修改功能','page_featu',21,1),(23,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶刪除','客戶管理刪除功能ˊ','page_featu',21,1),(31,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站管理','場站管理功能','page',0,1),(32,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站基本設定修改','場站管理修改功能','page_featu',31,1),(33,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站刪除','場站管理刪除功能ˊ','page_featu',31,1),(41,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'票證設定管理','票證設定管理功能','page_featu',31,1),(42,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'票證設定修改','票證設定修改功能','page_featu',41,1),(43,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'票證設定刪除','票證設定刪除功能ˊ','page_featu',41,1),(51,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'設備管理','設備管理','page_featu',31,1),(52,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'設備新增','設備新增功能ˊ','page_featu',51,1),(53,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'設備修改','設備修改功能ˊ','page_featu',51,1),(54,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'設備刪除','設備刪除功能ˊ','page_featu',51,1),(61,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票','定期票','page_featu',31,1),(62,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票新增','定期票新增','page_featu',61,1),(63,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票修改','定期票修改','page_featu',61,1),(64,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票刪除','定期票刪除','page_featu',61,1),(65,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票產出dat','定期票產出dat','page_featu',61,1),(66,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票匯入','定期票匯入','page_featu',61,1),(67,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'定期票匯出','定期票匯出','page_featu',61,1),(71,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站行事曆','場站行事曆','page_featu',31,1),(72,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站行事曆新增','場站行事曆新增','page_featu',71,1),(73,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站行事曆修改','場站行事曆修改','page_featu',71,1),(74,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站行事曆刪除','場站行事曆刪除','page_featu',71,1),(75,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站行事曆產出dat','場站行事曆產出dat','page_featu',71,1),(81,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'發票設定管理','發票設定管理功能','page_featu',31,1),(82,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'發票設定修改','發票設定修改功能','page_featu',81,1),(83,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'發票設定刪除','發票設定刪除功能ˊ','page_featu',81,1),(91,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'出場設定管理','出場設定功能','page',31,1),(92,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'出場設定修改','出場設定修改功能','page_featu',91,1),(93,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'出場啟用停用切換','出場啟用停用切換功能ˊ','page_featu',91,1),(101,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'車道設定管理','車道設定功能','page',31,1),(102,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'車道設定修改','車道設定修改功能','page_featu',101,1),(103,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'車道刪除','車道刪除功能ˊ','page_featu',101,1),(111,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站群組管理','場站群組管理功能','page',0,1),(112,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站群組基本設定修改','場站群組管理修改功能','page_featu',111,1),(113,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'場站群組刪除','場站群組管理刪除功能ˊ','page_featu',111,1),(121,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'授權金鑰管理','授權金鑰管理','page',0,1),(122,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'授權金鑰基本設定修改','授權金鑰基本設定修改','page_featu',121,1),(123,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'授權金鑰刪除','授權金鑰刪除','page_featu',122,1),(131,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳務管理','帳務管理群組','group',0,1),(132,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳務查詢','帳務查詢功能','page',131,1),(133,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'帳務報表訂閱','帳務報表訂閱','page_featu',131,0),(141,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'PV即時交易資料查詢','PV即時交易資料查詢功能','page',0,1),(142,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'PV3即時交易資料查詢','PV3即時交易資料查詢功能','page',131,1),(143,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'平板即時交易資料查詢','平板即時交易資料查詢功能','page',131,1),(144,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'IBox即時交易資料查詢','IBox即時交易資料查詢功能','page',131,1),(151,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'儀表板','儀表板群組','group',0,1),(152,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'資源分析','資源分析','page',151,1),(153,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'營收分析','營收分析','page',151,1),(154,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'交易分析','交易分析','page',151,1),(161,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'計費設定管理','計費設定管理','page',0,1),(162,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'計費設定新增','計費設定新增','page_featu',161,1),(163,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'計費設定修改','計費設定修改','page_featu',161,1),(164,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'計費設定刪除','計費設定刪除','page_featu',161,1),(181,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'報表','報表群組','group',0,1),(182,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'結班報表','結班報表','page',181,1),(191,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶行事曆匯入','客戶行事曆匯入','page_featu',21,1),(192,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶行事曆匯出','客戶行事曆匯出','page_featu',21,1),(193,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'客戶行事曆產出dat','客戶行事曆產出dat','page_featu',21,1);
/*!40000 ALTER TABLE `permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `real_time_transaction_data`
--

DROP TABLE IF EXISTS `real_time_transaction_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `real_time_transaction_data` (
  `real_time_transaction_data_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '即時交易資料ID',
  `in_or_out` int(11) NOT NULL COMMENT '進離場類別(0:進場、1:離場)',
  `parking_type` int(11) NOT NULL DEFAULT '0' COMMENT '臨時車或月租車(0:臨停車、1:月租車)',
  `card_id_16` varchar(30) NOT NULL COMMENT '票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)(卡內碼mifire)',
  `in_or_out_datetime` datetime NOT NULL COMMENT '進/出場日期時間 (ex. 201801082359)',
  `pay_datetime` datetime DEFAULT NULL COMMENT '付費時間(ex. 201801082359)',
  `card_type` int(11) DEFAULT NULL COMMENT '卡別(01:ECC,02:愛金,03:KRTC, /遠鑫:05 /99:人工結帳….).',
  `receivable` int(11) DEFAULT NULL COMMENT '應收費用',
  `real_fees` int(11) DEFAULT NULL COMMENT '實際費用',
  `before_pay_balance` int(11) DEFAULT NULL COMMENT '卡片餘額(扣款前)   ',
  `is_disability` int(11) DEFAULT '0' COMMENT '是否為身障計費(>0:身障計費規則id  0:否)',
  `vehicle_identification_number` varchar(10) NOT NULL COMMENT '車牌號碼',
  `pv_ip` varchar(15) NOT NULL COMMENT 'pv的ip',
  `garage_id` varchar(10) DEFAULT 'acer' COMMENT '場站代碼(acer)',
  `customer_id` varchar(10) DEFAULT 'acer' COMMENT '業者代碼(acer)',
  `discount_type` int(11) DEFAULT '0' COMMENT '0: 無優惠，1: 身障優惠，2: 折扣優惠',
  `discount_amount` int(11) DEFAULT NULL COMMENT '優惠金額',
  `status_number` int(11) NOT NULL COMMENT '狀態碼，交易正常:0 異常:1',
  `vehicle_type` int(11) NOT NULL COMMENT '車種(汽車sedan:01,機車:02,大客車:03,腳踏車:04,卡車:05)',
  `einvoice` varchar(15) DEFAULT NULL COMMENT '電子發票號碼',
  `einvoice_print_status` int(11) DEFAULT NULL COMMENT '發票狀態列印 (1=列印紙本發票,2=存入載具,3=列印紙本發票並打買受人統編)',
  `tax_id_number` varchar(15) DEFAULT NULL COMMENT '買受人統編',
  `card_id_appearance` varchar(30) NOT NULL COMMENT '卡片卡號(卡片外碼)',
  `is_autoload` int(11) NOT NULL DEFAULT '0' COMMENT '是否開啟自動加值功能(1:開啟,0:無)',
  `autoload_amout` int(11) NOT NULL DEFAULT '0' COMMENT '自動加值金額 (default:0)',
  `error_message` varchar(500) NOT NULL DEFAULT '' COMMENT '錯誤訊息(default:'')',
  `parking_id` int(11) NOT NULL COMMENT 'Parking資料ID',
  `create_account_id` int(11) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'create_date',
  `exit_type_config_detail_id` int(10) DEFAULT NULL COMMENT '出場設定id',
  `exit_type_config_detail_remarks` varchar(50) DEFAULT NULL COMMENT '出場設定備註',
  `ibox_no` int(10) DEFAULT NULL COMMENT 'IBOX 流水號',
  `tax_id_number_buyer` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`real_time_transaction_data_id`)
) ENGINE=MyISAM AUTO_INCREMENT=345 DEFAULT CHARSET=utf8 COMMENT='即時交易資料';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `real_time_transaction_data`
--

LOCK TABLES `real_time_transaction_data` WRITE;
/*!40000 ALTER TABLE `real_time_transaction_data` DISABLE KEYS */;
INSERT INTO `real_time_transaction_data` VALUES (79,0,0,'666666','2018-06-01 15:59:22','0000-00-00 00:00:00',NULL,0,0,NULL,0,'34576','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',52,2,'2018-06-01 07:59:42',0,'',NULL,NULL),(80,0,0,'666666','2018-06-01 16:00:04','0000-00-00 00:00:00',NULL,0,0,NULL,0,'92298','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',53,2,'2018-06-01 08:00:29',0,'',NULL,NULL),(81,0,0,'666666','2018-06-01 16:01:59','0000-00-00 00:00:00',NULL,0,0,NULL,0,'702727','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',54,2,'2018-06-01 08:02:16',0,'',NULL,NULL),(82,1,0,'666666','2018-06-01 16:02:49','0000-00-00 00:00:00',NULL,40,40,NULL,0,'92298','127.0.0.1','1','1',NULL,NULL,0,6,'QW00107050',0,'54641988','666666',0,0,'',53,2,'2018-06-01 08:03:34',6,'',NULL,NULL),(83,0,0,'666666','2018-06-01 16:07:56','0000-00-00 00:00:00',NULL,0,0,NULL,0,'836004','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',55,2,'2018-06-01 08:08:05',0,'',NULL,NULL),(84,1,0,'666666','2018-06-01 16:08:24','0000-00-00 00:00:00',NULL,40,0,NULL,0,'836004','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',55,2,'2018-06-01 08:08:36',6,'',NULL,NULL),(85,1,0,'666666','2018-06-01 16:09:01','0000-00-00 00:00:00',NULL,40,0,NULL,0,'34576','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',52,2,'2018-06-01 08:09:12',6,'',NULL,NULL),(86,0,0,'666666','2018-06-01 16:19:05','0000-00-00 00:00:00',NULL,0,0,NULL,0,'123408','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',56,5,'2018-06-01 08:19:26',0,'',NULL,NULL),(87,1,0,'666666','2018-06-01 16:19:58','0000-00-00 00:00:00',NULL,40,40,NULL,0,'123408','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107051',0,'54641988','666666',0,0,'',56,5,'2018-06-01 08:20:31',1,'',NULL,NULL),(88,0,0,'666666','2018-06-01 16:43:55','0000-00-00 00:00:00',NULL,0,0,NULL,0,'123409','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',57,5,'2018-06-01 08:44:18',0,'',NULL,NULL),(89,1,0,'666666','2018-06-01 16:44:40','0000-00-00 00:00:00',NULL,40,40,NULL,0,'123409','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107052',0,'54641988','666666',0,0,'',57,5,'2018-06-01 08:45:04',1,'',NULL,NULL),(90,0,0,'666666','2018-06-01 17:03:10','0000-00-00 00:00:00',NULL,0,0,NULL,0,'116720','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',58,5,'2018-06-01 09:03:19',0,'',NULL,NULL),(91,1,0,'666666','2018-06-01 17:28:46','0000-00-00 00:00:00',NULL,60,60,NULL,0,'702727','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107053',0,'54641988','666666',0,0,'',54,5,'2018-06-01 09:29:06',1,'',NULL,NULL),(92,0,0,'666666','2018-06-01 17:31:44','0000-00-00 00:00:00',NULL,0,0,NULL,0,'AKT-8077','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',59,5,'2018-06-01 09:31:52',0,'',NULL,NULL),(93,1,0,'666666','2018-06-01 17:31:58','0000-00-00 00:00:00',NULL,40,0,NULL,0,'AKT-8077','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',59,5,'2018-06-01 09:32:17',5,'',NULL,NULL),(94,0,0,'666666','2018-06-01 18:24:27','0000-00-00 00:00:00',NULL,0,0,NULL,0,'125038','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',60,5,'2018-06-01 10:24:37',0,'',NULL,NULL),(95,0,0,'666666','2018-06-01 18:42:37','0000-00-00 00:00:00',NULL,0,0,NULL,0,'963308','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',61,5,'2018-06-01 10:42:47',0,'',NULL,NULL),(96,0,0,'666666','2018-06-01 18:52:37','0000-00-00 00:00:00',NULL,0,0,NULL,0,'828337','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',62,5,'2018-06-01 10:52:46',0,'',NULL,NULL),(97,1,0,'666666','2018-06-01 19:12:48','0000-00-00 00:00:00',NULL,40,40,NULL,0,'125038','127.0.0.1','1','1',NULL,NULL,0,6,'QW00107054',3,'54641988','666666',0,0,'',60,5,'2018-06-01 11:13:03',1,'',NULL,NULL),(98,0,0,'666666','2018-06-01 19:19:54','0000-00-00 00:00:00',NULL,0,0,NULL,0,'890338','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',63,5,'2018-06-01 11:20:05',0,'',NULL,NULL),(99,0,0,'666666','2018-06-01 19:25:18','0000-00-00 00:00:00',NULL,0,0,NULL,0,'955811','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',64,5,'2018-06-01 11:25:26',0,'',NULL,NULL),(100,0,0,'666666','2018-06-01 19:29:48','0000-00-00 00:00:00',NULL,0,0,NULL,0,'936719','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',65,5,'2018-06-01 11:29:59',0,'',NULL,NULL),(101,0,0,'666666','2018-06-01 19:35:04','0000-00-00 00:00:00',NULL,0,0,NULL,0,'153715','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',66,5,'2018-06-01 11:35:13',0,'',NULL,NULL),(102,0,0,'666666','2018-06-01 19:40:49','0000-00-00 00:00:00',NULL,0,0,NULL,0,'768816','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',67,5,'2018-06-01 11:40:57',0,'',NULL,NULL),(103,1,0,'666666','2018-06-01 19:42:22','0000-00-00 00:00:00',NULL,120,120,NULL,0,'116720','127.0.0.1','1','1',NULL,NULL,0,6,'QW00107055',0,'54641988','666666',0,0,'',58,5,'2018-06-01 11:42:33',1,'',NULL,NULL),(104,0,0,'666666','2018-06-01 19:57:11','0000-00-00 00:00:00',NULL,0,0,NULL,0,'035720','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',68,5,'2018-06-01 11:57:23',0,'',NULL,NULL),(105,1,0,'666666','2018-06-01 20:03:12','0000-00-00 00:00:00',NULL,40,40,NULL,0,'936719','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107056',0,'54641988','666666',0,0,'',65,5,'2018-06-01 12:03:20',1,'',NULL,NULL),(106,1,0,'666666','2018-06-01 20:16:05','0000-00-00 00:00:00',NULL,40,40,NULL,0,'890338','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107057',0,'54641988','666666',0,0,'',63,5,'2018-06-01 12:16:14',1,'',NULL,NULL),(107,0,0,'666666','2018-06-01 20:31:30','0000-00-00 00:00:00',NULL,0,0,NULL,0,'225538','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',69,5,'2018-06-01 12:31:37',0,'',NULL,NULL),(108,1,0,'666666','2018-06-01 20:39:32','0000-00-00 00:00:00',NULL,40,40,NULL,0,'035720','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107058',0,'54641988','666666',0,0,'',68,5,'2018-06-01 12:39:42',1,'',NULL,NULL),(109,1,0,'666666','2018-06-01 20:42:26','0000-00-00 00:00:00',NULL,60,60,NULL,0,'153715','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107059',0,'54641988','666666',0,0,'',66,5,'2018-06-01 12:42:34',1,'',NULL,NULL),(110,0,0,'666666','2018-06-01 20:59:05','0000-00-00 00:00:00',NULL,0,0,NULL,0,'808719','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',70,5,'2018-06-01 12:59:13',0,'',NULL,NULL),(111,1,0,'666666','2018-06-01 20:59:48','0000-00-00 00:00:00',NULL,80,80,NULL,0,'955811','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107060',0,'54641988','666666',0,0,'',64,5,'2018-06-01 12:59:56',1,'',NULL,NULL),(112,1,0,'666666','2018-06-01 21:00:33','0000-00-00 00:00:00',NULL,40,40,NULL,0,'225538','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107061',0,'54641988','666666',0,0,'',69,5,'2018-06-01 13:00:40',1,'',NULL,NULL),(113,0,0,'666666','2018-06-01 21:05:33','0000-00-00 00:00:00',NULL,0,0,NULL,0,'846511','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',71,5,'2018-06-01 13:05:40',0,'',NULL,NULL),(114,1,0,'666666','2018-06-01 21:30:03','0000-00-00 00:00:00',NULL,120,120,NULL,0,'828337','127.0.0.1','1','1',NULL,NULL,0,6,'QW00107062',0,'54641988','666666',0,0,'',62,5,'2018-06-01 13:30:11',1,'',NULL,NULL),(115,0,0,'666666','2018-06-01 21:32:44','0000-00-00 00:00:00',NULL,0,0,NULL,0,'203637','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',72,5,'2018-06-01 13:32:53',0,'',NULL,NULL),(116,1,0,'666666','2018-06-01 21:33:31','0000-00-00 00:00:00',NULL,40,40,NULL,0,'846511','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107063',0,'54641988','666666',0,0,'',71,5,'2018-06-01 13:33:39',1,'',NULL,NULL),(117,1,0,'666666','2018-06-01 21:40:08','0000-00-00 00:00:00',NULL,120,120,NULL,0,'963308','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107064',0,'54641988','666666',0,0,'',61,5,'2018-06-01 13:41:31',1,'',NULL,NULL),(118,1,0,'666666','2018-06-01 22:06:31','0000-00-00 00:00:00',NULL,40,40,NULL,0,'203637','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107065',0,'54641988','666666',0,0,'',72,5,'2018-06-01 14:06:40',1,'',NULL,NULL),(119,1,0,'666666','2018-06-01 22:16:35','0000-00-00 00:00:00',NULL,120,120,NULL,0,'768816','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107066',0,'54641988','666666',0,0,'',67,5,'2018-06-01 14:16:43',1,'',NULL,NULL),(120,1,0,'666666','2018-06-01 22:37:27','0000-00-00 00:00:00',NULL,80,80,NULL,0,'808719','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107067',0,'54641988','666666',0,0,'',70,5,'2018-06-01 14:37:35',1,'',NULL,NULL),(121,0,0,'666666','2018-06-02 08:02:43','0000-00-00 00:00:00',NULL,0,0,NULL,0,'263105','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',73,5,'2018-06-02 00:03:09',0,'',NULL,NULL),(122,0,0,'666666','2018-06-02 08:03:30','0000-00-00 00:00:00',NULL,0,0,NULL,0,'239803','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',74,5,'2018-06-02 00:03:41',0,'',NULL,NULL),(123,0,0,'666666','2018-06-02 08:22:23','0000-00-00 00:00:00',NULL,0,0,NULL,0,'473306','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',75,5,'2018-06-02 00:26:28',0,'',NULL,NULL),(124,1,0,'666666','2018-06-02 08:26:35','0000-00-00 00:00:00',NULL,40,40,NULL,0,'473306','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',75,5,'2018-06-02 00:28:41',5,'',NULL,NULL),(125,1,0,'666666','2018-06-02 08:29:14','0000-00-00 00:00:00',NULL,40,40,NULL,0,'263105','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107068',0,'54641988','666666',0,0,'',73,5,'2018-06-02 00:30:31',1,'',NULL,NULL),(126,0,0,'666666','2018-06-02 08:30:39','0000-00-00 00:00:00',NULL,0,0,NULL,0,'473306','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',76,5,'2018-06-02 00:30:53',0,'',NULL,NULL),(127,1,0,'666666','2018-06-02 08:30:56','0000-00-00 00:00:00',NULL,40,170,NULL,0,'473306','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107069',0,'54641988','666666',0,0,'',76,5,'2018-06-02 00:31:39',12,'一日車',NULL,NULL),(128,0,0,'666666','2018-06-02 08:34:45','0000-00-00 00:00:00',NULL,0,0,NULL,0,'253305','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',77,5,'2018-06-02 01:50:38',0,'',NULL,NULL),(129,0,0,'666666','2018-06-02 10:45:54','0000-00-00 00:00:00',NULL,0,0,NULL,0,'806004','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',78,5,'2018-06-02 02:46:07',0,'',NULL,NULL),(130,0,0,'666666','2018-06-02 11:04:19','0000-00-00 00:00:00',NULL,0,0,NULL,0,'675707','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',79,5,'2018-06-02 03:04:30',0,'',NULL,NULL),(131,0,0,'666666','2018-06-02 11:20:47','0000-00-00 00:00:00',NULL,0,0,NULL,0,'011908','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',80,5,'2018-06-02 03:20:57',0,'',NULL,NULL),(132,1,0,'666666','2018-06-02 11:31:15','0000-00-00 00:00:00',NULL,120,80,NULL,0,'253305','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107070',0,'54641988','666666',0,0,'',77,5,'2018-06-02 03:31:42',1,'',NULL,NULL),(133,0,0,'666666','2018-06-02 11:43:22','0000-00-00 00:00:00',NULL,0,0,NULL,0,'500011','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',81,5,'2018-06-02 03:58:54',0,'',NULL,NULL),(134,0,0,'666666','2018-06-02 11:59:41','0000-00-00 00:00:00',NULL,0,0,NULL,0,'581812','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',82,5,'2018-06-02 04:16:23',0,'',NULL,NULL),(135,0,0,'666666','2018-06-02 12:17:11','0000-00-00 00:00:00',NULL,0,0,NULL,0,'739515','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',83,5,'2018-06-02 04:38:03',0,'',NULL,NULL),(136,0,0,'666666','2018-06-02 12:43:39','0000-00-00 00:00:00',NULL,0,0,NULL,0,'173616','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',84,5,'2018-06-02 04:43:49',0,'',NULL,NULL),(137,1,0,'666666','2018-06-02 12:46:03','0000-00-00 00:00:00',NULL,40,170,NULL,0,'173616','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107071',0,'54641988','666666',0,0,'',84,5,'2018-06-02 04:46:22',2,'',NULL,NULL),(138,1,0,'666666','2018-06-02 12:47:34','0000-00-00 00:00:00',NULL,60,60,NULL,0,'011908','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107072',0,'54641988','666666',0,0,'',80,5,'2018-06-02 04:47:46',1,'',NULL,NULL),(139,1,0,'666666','2018-06-02 12:50:02','0000-00-00 00:00:00',NULL,100,100,NULL,0,'806004','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107073',3,'54641988','666666',0,0,'',78,5,'2018-06-02 04:50:40',1,'',NULL,NULL),(140,1,0,'666666','2018-06-02 12:54:22','0000-00-00 00:00:00',NULL,60,40,NULL,0,'500011','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107074',0,'54641988','666666',0,0,'',81,5,'2018-06-02 04:54:35',1,'',NULL,NULL),(141,0,0,'666666','2018-06-02 12:56:30','0000-00-00 00:00:00',NULL,0,0,NULL,0,'063111','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',85,5,'2018-06-02 05:02:04',0,'',NULL,NULL),(142,1,0,'666666','2018-06-02 13:04:15','0000-00-00 00:00:00',NULL,40,170,NULL,0,'063111','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107075',0,'54641988','666666',0,0,'',85,5,'2018-06-02 05:04:30',2,'',NULL,NULL),(143,0,0,'666666','2018-06-02 13:04:45','0000-00-00 00:00:00',NULL,0,0,NULL,0,'973805','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',86,5,'2018-06-02 05:22:33',0,'',NULL,NULL),(144,0,0,'666666','2018-06-02 13:27:25','0000-00-00 00:00:00',NULL,0,0,NULL,0,'755010','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',87,5,'2018-06-02 05:27:33',0,'',NULL,NULL),(145,0,0,'666666','2018-06-02 13:37:54','0000-00-00 00:00:00',NULL,0,0,NULL,0,'253909','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',88,5,'2018-06-02 05:38:04',0,'',NULL,NULL),(146,0,0,'666666','2018-06-02 13:39:10','0000-00-00 00:00:00',NULL,0,0,NULL,0,'881004','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',89,5,'2018-06-02 05:46:17',0,'',NULL,NULL),(147,0,0,'666666','2018-06-02 13:46:42','0000-00-00 00:00:00',NULL,0,0,NULL,0,'617908','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',90,5,'2018-06-02 06:01:20',0,'',NULL,NULL),(148,1,0,'666666','2018-06-02 14:06:27','0000-00-00 00:00:00',NULL,40,40,NULL,0,'881004','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107076',0,'54641988','666666',0,0,'',89,5,'2018-06-02 06:06:39',1,'',NULL,NULL),(149,0,0,'666666','2018-06-02 14:06:46','0000-00-00 00:00:00',NULL,0,0,NULL,0,'082237','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',91,5,'2018-06-02 06:09:14',0,'',NULL,NULL),(150,1,0,'666666','2018-06-02 14:25:14','0000-00-00 00:00:00',NULL,140,140,NULL,0,'675707','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107077',0,'54641988','666666',0,0,'',79,5,'2018-06-02 06:25:29',1,'',NULL,NULL),(151,1,0,'666666','2018-06-02 14:28:11','0000-00-00 00:00:00',NULL,100,100,NULL,0,'581812','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107078',0,'54641988','666666',0,0,'',82,5,'2018-06-02 06:28:21',1,'',NULL,NULL),(152,0,0,'666666','2018-06-02 14:34:17','0000-00-00 00:00:00',NULL,0,0,NULL,0,'501612','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',92,5,'2018-06-02 06:34:27',0,'',NULL,NULL),(153,1,0,'666666','2018-06-02 14:37:44','0000-00-00 00:00:00',NULL,60,60,NULL,0,'755010','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107079',0,'54641988','666666',0,0,'',87,5,'2018-06-02 06:37:55',1,'',NULL,NULL),(154,1,0,'666666','2018-06-02 15:00:21','0000-00-00 00:00:00',NULL,120,100,NULL,0,'739515','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107080',0,'54641988','666666',0,0,'',83,5,'2018-06-02 07:00:35',1,'',NULL,NULL),(155,0,0,'666666','2018-06-02 15:07:21','0000-00-00 00:00:00',NULL,0,0,NULL,0,'963804','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',93,5,'2018-06-02 07:07:35',0,'',NULL,NULL),(156,0,0,'666666','2018-06-02 15:21:59','0000-00-00 00:00:00',NULL,0,0,NULL,0,'972007','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',94,5,'2018-06-02 07:22:10',0,'',NULL,NULL),(157,1,0,'666666','2018-06-02 15:28:47','0000-00-00 00:00:00',NULL,40,0,NULL,0,'963804','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',93,5,'2018-06-02 07:29:21',12,'車頭太高',NULL,NULL),(158,1,0,'666666','2018-06-02 15:30:44','0000-00-00 00:00:00',NULL,40,40,NULL,0,'501612','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107081',0,'54641988','666666',0,0,'',92,5,'2018-06-02 07:30:53',1,'',NULL,NULL),(159,0,0,'666666','2018-06-02 15:36:01','0000-00-00 00:00:00',NULL,0,0,NULL,0,'130012','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',95,5,'2018-06-02 07:36:08',0,'',NULL,NULL),(160,0,0,'666666','2018-06-02 15:41:36','0000-00-00 00:00:00',NULL,0,0,NULL,0,'922810','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',96,5,'2018-06-02 07:41:49',0,'',NULL,NULL),(161,0,0,'666666','2018-06-02 15:59:44','0000-00-00 00:00:00',NULL,0,0,NULL,0,'WQ-1222','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',97,5,'2018-06-02 08:00:02',0,'',NULL,NULL),(162,0,0,'666666','2018-06-02 16:04:41','0000-00-00 00:00:00',NULL,0,0,NULL,0,'687513','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',98,5,'2018-06-02 08:05:26',0,'',NULL,NULL),(163,1,0,'666666','2018-06-02 16:08:10','0000-00-00 00:00:00',NULL,40,40,NULL,0,'WQ-1222','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',97,5,'2018-06-02 08:08:50',12,'測試',NULL,NULL),(164,0,0,'666666','2018-06-02 16:18:03','0000-00-00 00:00:00',NULL,0,0,NULL,0,'AA-123','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',99,5,'2018-06-02 08:18:12',0,'',NULL,NULL),(165,1,0,'666666','2018-06-02 16:18:15','0000-00-00 00:00:00',NULL,40,170,NULL,0,'AA-123','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107082',0,'54641988','666666',0,0,'',99,5,'2018-06-02 08:23:18',2,'測試',NULL,NULL),(166,1,0,'666666','2018-06-02 16:44:08','0000-00-00 00:00:00',NULL,170,170,NULL,0,'239803','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107083',0,'54641988','666666',0,0,'',74,5,'2018-06-02 08:44:23',2,'',NULL,NULL),(167,1,0,'666666','2018-06-02 16:51:06','0000-00-00 00:00:00',NULL,60,60,NULL,0,'922810','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107084',0,'54641988','666666',0,0,'',96,5,'2018-06-02 08:51:19',1,'',NULL,NULL),(168,1,0,'666666','2018-06-02 17:19:39','0000-00-00 00:00:00',NULL,160,160,NULL,0,'253909','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107085',0,'54641988','666666',0,0,'',88,5,'2018-06-02 09:19:48',1,'',NULL,NULL),(169,0,0,'666666','2018-06-02 17:27:05','0000-00-00 00:00:00',NULL,0,0,NULL,0,'811910','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',100,5,'2018-06-02 09:27:15',0,'',NULL,NULL),(170,0,0,'666666','2018-06-02 17:33:03','0000-00-00 00:00:00',NULL,0,0,NULL,0,'588003','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',101,5,'2018-06-02 09:33:12',0,'',NULL,NULL),(171,0,0,'666666','2018-06-02 17:44:27','0000-00-00 00:00:00',NULL,0,0,NULL,0,'588909','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',102,5,'2018-06-02 09:44:36',0,'',NULL,NULL),(172,1,0,'666666','2018-06-02 18:16:53','0000-00-00 00:00:00',NULL,40,40,NULL,0,'588909','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107086',0,'54641988','666666',0,0,'',102,5,'2018-06-02 10:17:04',1,'',NULL,NULL),(173,1,0,'666666','2018-06-02 18:17:40','0000-00-00 00:00:00',NULL,100,100,NULL,0,'687513','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107087',0,'54641988','666666',0,0,'',98,5,'2018-06-02 10:17:49',1,'',NULL,NULL),(174,1,0,'666666','2018-06-02 18:17:59','0000-00-00 00:00:00',NULL,170,140,NULL,0,'082237','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107088',0,'54641988','666666',0,0,'',91,5,'2018-06-02 10:18:11',1,'',NULL,NULL),(175,0,0,'666666','2018-06-02 18:28:23','0000-00-00 00:00:00',NULL,0,0,NULL,0,'315537','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',103,5,'2018-06-02 10:28:32',0,'',NULL,NULL),(176,0,0,'666666','2018-06-02 18:32:45','0000-00-00 00:00:00',NULL,0,0,NULL,0,'999738','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',104,5,'2018-06-02 10:32:58',0,'',NULL,NULL),(177,1,0,'666666','2018-06-02 18:42:45','0000-00-00 00:00:00',NULL,140,60,NULL,0,'130012','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107089',0,'54641988','666666',0,0,'',95,5,'2018-06-02 10:45:43',1,'',NULL,NULL),(178,1,0,'666666','2018-06-02 18:45:59','0000-00-00 00:00:00',NULL,170,100,NULL,0,'973805','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107090',0,'54641988','666666',0,0,'',86,5,'2018-06-02 10:46:11',1,'',NULL,NULL),(179,0,0,'666666','2018-06-02 18:50:51','0000-00-00 00:00:00',NULL,0,0,NULL,0,'166808','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',105,5,'2018-06-02 10:50:59',0,'',NULL,NULL),(180,0,0,'666666','2018-06-02 18:55:35','0000-00-00 00:00:00',NULL,0,0,NULL,0,'619205','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',106,5,'2018-06-02 10:55:44',0,'',NULL,NULL),(181,1,0,'666666','2018-06-02 19:03:59','0000-00-00 00:00:00',NULL,40,40,NULL,0,'315537','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107091',0,'54641988','666666',0,0,'',103,5,'2018-06-02 11:04:09',1,'',NULL,NULL),(182,0,0,'666666','2018-06-02 19:23:55','0000-00-00 00:00:00',NULL,0,0,NULL,0,'577904','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',107,5,'2018-06-02 11:24:05',0,'',NULL,NULL),(183,1,0,'666666','2018-06-02 19:24:11','0000-00-00 00:00:00',NULL,80,80,NULL,0,'588003','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107092',0,'54641988','666666',0,0,'',101,5,'2018-06-02 11:24:22',1,'',NULL,NULL),(184,1,0,'666666','2018-06-02 19:36:40','0000-00-00 00:00:00',NULL,40,40,NULL,0,'619205','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107093',0,'54641988','666666',0,0,'',106,5,'2018-06-02 11:36:50',1,'',NULL,NULL),(185,0,0,'666666','2018-06-02 20:02:38','0000-00-00 00:00:00',NULL,0,0,NULL,0,'900237','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',108,5,'2018-06-02 12:02:47',0,'',NULL,NULL),(186,1,0,'666666','2018-06-02 20:06:42','0000-00-00 00:00:00',NULL,80,80,NULL,0,'999738','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107094',0,'54641988','666666',0,0,'',104,5,'2018-06-02 12:06:51',1,'',NULL,NULL),(187,1,0,'666666','2018-06-02 20:06:52','0000-00-00 00:00:00',NULL,60,60,NULL,0,'166808','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107095',0,'54641988','666666',0,0,'',105,5,'2018-06-02 12:07:01',1,'',NULL,NULL),(188,0,0,'666666','2018-06-02 20:09:27','0000-00-00 00:00:00',NULL,0,0,NULL,0,'515738','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',109,5,'2018-06-02 12:09:39',0,'',NULL,NULL),(189,1,0,'666666','2018-06-02 20:24:24','0000-00-00 00:00:00',NULL,60,60,NULL,0,'577904','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107096',0,'54641988','666666',0,0,'',107,5,'2018-06-02 12:24:34',1,'',NULL,NULL),(190,1,0,'666666','2018-06-02 20:51:34','0000-00-00 00:00:00',NULL,60,60,NULL,0,'577904','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(191,1,0,'666666','2018-06-02 20:52:19','0000-00-00 00:00:00',NULL,60,60,NULL,0,'577904','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(192,1,0,'666666','2018-06-02 20:53:00','0000-00-00 00:00:00',NULL,60,60,NULL,0,'577904','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(193,1,0,'666666','2018-06-02 20:53:41','0000-00-00 00:00:00',NULL,170,80,NULL,0,'617908','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107100',0,'54641988','666666',0,0,'',90,5,'2018-06-02 12:54:19',1,'',NULL,NULL),(194,1,0,'666666','2018-06-02 20:58:33','0000-00-00 00:00:00',NULL,170,80,NULL,0,'617908','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(195,1,0,'666666','2018-06-02 21:03:28','0000-00-00 00:00:00',NULL,170,80,NULL,0,'617908','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(196,1,0,'666666','2018-06-02 21:05:41','0000-00-00 00:00:00',NULL,170,80,NULL,0,'617908','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',5,'',NULL,NULL),(197,1,0,'666666','2018-06-02 21:09:18','0000-00-00 00:00:00',NULL,170,80,NULL,0,'972007','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',94,5,'2018-06-02 13:09:47',1,'',NULL,NULL),(198,1,0,'666666','2018-06-02 21:21:14','0000-00-00 00:00:00',NULL,60,60,NULL,0,'515738','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107104',0,'54641988','666666',0,0,'',109,5,'2018-06-02 13:21:26',1,'',NULL,NULL),(199,1,0,'666666','2018-06-02 21:34:17','0000-00-00 00:00:00',NULL,170,160,NULL,0,'811910','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107105',0,'54641988','666666',0,0,'',100,5,'2018-06-02 13:34:49',1,'',NULL,NULL),(200,1,0,'666666','2018-06-02 21:39:07','0000-00-00 00:00:00',NULL,80,80,NULL,0,'900237','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107106',0,'54641988','666666',0,0,'',108,5,'2018-06-02 13:39:18',1,'',NULL,NULL),(201,0,0,'666666','2018-06-03 07:22:27','0000-00-00 00:00:00',NULL,0,0,NULL,0,'050508','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',110,5,'2018-06-02 23:23:08',0,'',NULL,NULL),(202,0,0,'666666','2018-06-03 07:48:51','0000-00-00 00:00:00',NULL,0,0,NULL,0,'595807','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',111,5,'2018-06-02 23:49:04',0,'',NULL,NULL),(203,1,0,'666666','2018-06-03 09:12:02','0000-00-00 00:00:00',NULL,80,80,NULL,0,'050508','127.0.0.1','1','1',NULL,NULL,0,6,NULL,NULL,NULL,'666666',0,0,'',110,5,'2018-06-03 01:12:27',1,'',NULL,NULL),(204,0,0,'666666','2018-06-03 10:47:10','0000-00-00 00:00:00',NULL,0,0,NULL,0,'318608','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',112,5,'2018-06-03 02:47:20',0,'',NULL,NULL),(205,1,0,'666666','2018-06-03 11:26:29','0000-00-00 00:00:00',NULL,160,160,NULL,0,'595807','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107107',0,'54641988','666666',0,0,'',111,5,'2018-06-03 03:26:53',1,'',NULL,NULL),(206,1,0,'666666','2018-06-03 11:29:12','0000-00-00 00:00:00',NULL,40,40,NULL,0,'318608','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107108',0,'54641988','666666',0,0,'',112,5,'2018-06-03 03:29:31',1,'',NULL,NULL),(207,0,0,'666666','2018-06-03 11:58:17','0000-00-00 00:00:00',NULL,0,0,NULL,0,'669608','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',113,5,'2018-06-03 03:58:28',0,'',NULL,NULL),(208,0,0,'666666','2018-06-03 12:04:21','0000-00-00 00:00:00',NULL,0,0,NULL,0,'838807','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',114,5,'2018-06-03 04:04:31',0,'',NULL,NULL),(209,0,0,'666666','2018-06-03 12:08:07','0000-00-00 00:00:00',NULL,0,0,NULL,0,'696706','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',115,5,'2018-06-03 04:08:17',0,'',NULL,NULL),(210,0,0,'666666','2018-06-03 12:11:30','0000-00-00 00:00:00',NULL,0,0,NULL,0,'388304','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',116,5,'2018-06-03 04:11:39',0,'',NULL,NULL),(211,0,0,'666666','2018-06-03 12:15:40','0000-00-00 00:00:00',NULL,0,0,NULL,0,'718911','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',117,5,'2018-06-03 04:15:51',0,'',NULL,NULL),(212,0,0,'666666','2018-06-03 12:17:15','0000-00-00 00:00:00',NULL,0,0,NULL,0,'799903','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',118,5,'2018-06-03 04:17:24',0,'',NULL,NULL),(213,0,0,'666666','2018-06-03 12:22:24','0000-00-00 00:00:00',NULL,0,0,NULL,0,'763805','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',119,5,'2018-06-03 04:22:34',0,'',NULL,NULL),(214,0,0,'666666','2018-06-03 12:26:59','0000-00-00 00:00:00',NULL,0,0,NULL,0,'363701','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',120,5,'2018-06-03 04:27:08',0,'',NULL,NULL),(215,0,0,'666666','2018-06-03 12:30:55','0000-00-00 00:00:00',NULL,0,0,NULL,0,'158909','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',121,5,'2018-06-03 04:31:04',0,'',NULL,NULL),(216,0,0,'666666','2018-06-03 12:35:13','0000-00-00 00:00:00',NULL,0,0,NULL,0,'020620','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',122,5,'2018-06-03 04:35:23',0,'',NULL,NULL),(217,0,0,'666666','2018-06-03 12:37:18','0000-00-00 00:00:00',NULL,0,0,NULL,0,'951812','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',123,5,'2018-06-03 04:37:47',0,'',NULL,NULL),(218,0,0,'666666','2018-06-03 12:53:15','0000-00-00 00:00:00',NULL,0,0,NULL,0,'968519','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',124,5,'2018-06-03 04:53:25',0,'',NULL,NULL),(219,0,0,'666666','2018-06-03 12:58:29','0000-00-00 00:00:00',NULL,0,0,NULL,0,'698113','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',125,5,'2018-06-03 04:58:38',0,'',NULL,NULL),(220,0,0,'666666','2018-06-03 13:01:33','0000-00-00 00:00:00',NULL,0,0,NULL,0,'845914','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',126,5,'2018-06-03 05:01:43',0,'',NULL,NULL),(221,1,0,'666666','2018-06-03 13:06:37','0000-00-00 00:00:00',NULL,40,40,NULL,0,'020620','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107109',0,'54641988','666666',0,0,'',122,5,'2018-06-03 05:06:48',1,'',NULL,NULL),(222,0,0,'666666','2018-06-03 13:08:23','0000-00-00 00:00:00',NULL,0,0,NULL,0,'096010','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',127,5,'2018-06-03 05:08:35',0,'',NULL,NULL),(223,0,0,'666666','2018-06-03 13:19:25','0000-00-00 00:00:00',NULL,0,0,NULL,0,'755820','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',128,5,'2018-06-03 05:19:37',0,'',NULL,NULL),(224,0,0,'666666','2018-06-03 13:25:26','0000-00-00 00:00:00',NULL,0,0,NULL,0,'026515','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',129,5,'2018-06-03 05:25:36',0,'',NULL,NULL),(225,0,0,'666666','2018-06-03 13:36:18','0000-00-00 00:00:00',NULL,0,0,NULL,0,'352316','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',130,5,'2018-06-03 05:36:27',0,'',NULL,NULL),(226,0,0,'666666','2018-06-03 13:41:51','0000-00-00 00:00:00',NULL,0,0,NULL,0,'285823','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',131,5,'2018-06-03 05:42:02',0,'',NULL,NULL),(227,1,0,'666666','2018-06-03 13:49:58','0000-00-00 00:00:00',NULL,80,80,NULL,0,'388304','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107110',0,'54641988','666666',0,0,'',116,5,'2018-06-03 05:50:07',1,'',NULL,NULL),(228,1,0,'666666','2018-06-03 13:52:38','0000-00-00 00:00:00',NULL,80,80,NULL,0,'696706','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107111',0,'54641988','666666',0,0,'',115,5,'2018-06-03 05:52:46',1,'',NULL,NULL),(229,1,0,'666666','2018-06-03 13:53:40','0000-00-00 00:00:00',NULL,40,40,NULL,0,'698113','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107112',0,'54641988','666666',0,0,'',125,5,'2018-06-03 05:53:47',1,'',NULL,NULL),(230,1,0,'666666','2018-06-03 13:54:03','0000-00-00 00:00:00',NULL,60,60,NULL,0,'158909','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107113',0,'54641988','666666',0,0,'',121,5,'2018-06-03 05:54:24',1,'',NULL,NULL),(231,0,0,'666666','2018-06-03 14:09:32','0000-00-00 00:00:00',NULL,0,0,NULL,0,'099904','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',132,5,'2018-06-03 06:09:41',0,'',NULL,NULL),(232,0,0,'666666','2018-06-03 14:15:11','0000-00-00 00:00:00',NULL,0,0,NULL,0,'039906','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',133,5,'2018-06-03 06:15:22',0,'',NULL,NULL),(233,0,0,'666666','2018-06-03 14:20:15','0000-00-00 00:00:00',NULL,0,0,NULL,0,'186109','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',134,5,'2018-06-03 06:20:28',0,'',NULL,NULL),(234,1,0,'666666','2018-06-03 14:22:10','0000-00-00 00:00:00',NULL,100,100,NULL,0,'669608','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107114',0,'54641988','666666',0,0,'',113,5,'2018-06-03 06:22:18',1,'',NULL,NULL),(235,1,0,'666666','2018-06-03 14:23:06','0000-00-00 00:00:00',NULL,80,80,NULL,0,'951812','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107115',0,'54641988','666666',0,0,'',123,5,'2018-06-03 06:23:15',1,'',NULL,NULL),(236,1,0,'666666','2018-06-03 14:29:31','0000-00-00 00:00:00',NULL,40,40,NULL,0,'285823','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107116',0,'54641988','666666',0,0,'',131,5,'2018-06-03 06:29:40',1,'',NULL,NULL),(237,1,0,'666666','2018-06-03 14:31:20','0000-00-00 00:00:00',NULL,100,100,NULL,0,'838807','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107117',0,'54641988','666666',0,0,'',114,5,'2018-06-03 06:31:27',1,'',NULL,NULL),(238,0,0,'666666','2018-06-03 14:33:34','0000-00-00 00:00:00',NULL,0,0,NULL,0,'026112','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',135,5,'2018-06-03 06:33:43',0,'',NULL,NULL),(239,1,0,'666666','2018-06-03 14:38:01','0000-00-00 00:00:00',NULL,100,100,NULL,0,'718911','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107118',0,'54641988','666666',0,0,'',117,5,'2018-06-03 06:38:10',1,'',NULL,NULL),(240,1,0,'666666','2018-06-03 14:40:09','0000-00-00 00:00:00',NULL,60,60,NULL,0,'755820','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107119',0,'54641988','666666',0,0,'',128,5,'2018-06-03 06:40:16',1,'',NULL,NULL),(241,1,0,'666666','2018-06-03 14:47:42','0000-00-00 00:00:00',NULL,100,100,NULL,0,'363701','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107120',0,'54641988','666666',0,0,'',120,5,'2018-06-03 06:47:50',1,'',NULL,NULL),(242,1,0,'666666','2018-06-03 14:56:51','0000-00-00 00:00:00',NULL,80,80,NULL,0,'845914','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107121',0,'54641988','666666',0,0,'',126,5,'2018-06-03 06:57:01',1,'',NULL,NULL),(243,1,0,'666666','2018-06-03 15:08:58','0000-00-00 00:00:00',NULL,80,80,NULL,0,'026515','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107122',0,'54641988','666666',0,0,'',129,5,'2018-06-03 07:09:11',1,'',NULL,NULL),(244,1,0,'666666','2018-06-03 15:17:26','0000-00-00 00:00:00',NULL,140,140,NULL,0,'799903','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107123',0,'54641988','666666',0,0,'',118,5,'2018-06-03 07:17:39',1,'',NULL,NULL),(245,0,0,'666666','2018-06-03 15:36:41','0000-00-00 00:00:00',NULL,0,0,NULL,0,'159517','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',136,5,'2018-06-03 07:36:56',0,'',NULL,NULL),(246,0,0,'666666','2018-06-03 15:44:05','0000-00-00 00:00:00',NULL,0,0,NULL,0,'581737','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',137,5,'2018-06-03 07:45:53',0,'',NULL,NULL),(247,1,0,'666666','2018-06-03 16:24:25','0000-00-00 00:00:00',NULL,100,100,NULL,0,'099904','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107124',0,'54641988','666666',0,0,'',132,5,'2018-06-03 08:24:39',1,'',NULL,NULL),(248,1,0,'666666','2018-06-03 16:39:08','0000-00-00 00:00:00',NULL,160,160,NULL,0,'096010','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107125',0,'54641988','666666',0,0,'',127,5,'2018-06-03 08:39:17',1,'',NULL,NULL),(249,1,0,'666666','2018-06-03 16:43:48','0000-00-00 00:00:00',NULL,100,100,NULL,0,'186109','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107126',0,'54641988','666666',0,0,'',134,5,'2018-06-03 08:43:57',1,'',NULL,NULL),(250,0,0,'666666','2018-06-03 16:47:31','0000-00-00 00:00:00',NULL,0,0,NULL,0,'506109','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',138,5,'2018-06-03 08:47:42',0,'',NULL,NULL),(251,0,0,'666666','2018-06-03 16:53:56','0000-00-00 00:00:00',NULL,0,0,NULL,0,'719738','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',139,5,'2018-06-03 08:54:10',0,'',NULL,NULL),(252,0,0,'666666','2018-06-03 17:00:20','0000-00-00 00:00:00',NULL,0,0,NULL,0,'186818','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',140,5,'2018-06-03 09:02:01',0,'',NULL,NULL),(253,0,0,'666666','2018-06-03 17:04:56','0000-00-00 00:00:00',NULL,0,0,NULL,0,'165610','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',141,5,'2018-06-03 09:07:01',0,'',NULL,NULL),(254,1,0,'666666','2018-06-03 17:19:00','0000-00-00 00:00:00',NULL,80,80,NULL,0,'581737','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107127',0,'54641988','666666',0,0,'',137,5,'2018-06-03 09:19:10',1,'',NULL,NULL),(255,1,0,'666666','2018-06-03 17:19:21','0000-00-00 00:00:00',NULL,80,80,NULL,0,'581737','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(256,0,0,'666666','2018-06-03 17:24:12','0000-00-00 00:00:00',NULL,0,0,NULL,0,'582537','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',142,5,'2018-06-03 09:25:13',0,'',NULL,NULL),(257,1,0,'666666','2018-06-03 17:25:33','0000-00-00 00:00:00',NULL,160,160,NULL,0,'352316','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107129',0,'54641988','666666',0,0,'',130,5,'2018-06-03 09:25:43',1,'',NULL,NULL),(258,1,0,'666666','2018-06-03 17:39:40','0000-00-00 00:00:00',NULL,40,40,NULL,0,'719738','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107130',0,'54641988','666666',0,0,'',139,5,'2018-06-03 09:39:55',1,'',NULL,NULL),(259,0,0,'666666','2018-06-03 17:45:14','0000-00-00 00:00:00',NULL,0,0,NULL,0,'509001','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',143,5,'2018-06-03 09:47:10',0,'',NULL,NULL),(260,1,0,'666666','2018-06-03 17:57:05','0000-00-00 00:00:00',NULL,170,170,NULL,0,'763805','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107131',0,'54641988','666666',0,0,'',119,5,'2018-06-03 09:57:16',1,'',NULL,NULL),(261,0,0,'666666','2018-06-03 18:06:55','0000-00-00 00:00:00',NULL,0,0,NULL,0,'909838','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',144,5,'2018-06-03 10:09:00',0,'',NULL,NULL),(262,0,0,'666666','2018-06-03 18:10:21','0000-00-00 00:00:00',NULL,0,0,NULL,0,'286225','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',145,5,'2018-06-03 10:14:02',0,'',NULL,NULL),(263,1,0,'666666','2018-06-03 18:21:27','0000-00-00 00:00:00',NULL,170,170,NULL,0,'968519','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107132',0,'54641988','666666',0,0,'',124,5,'2018-06-03 10:21:37',1,'',NULL,NULL),(264,1,0,'666666','2018-06-03 18:22:57','0000-00-00 00:00:00',NULL,40,40,NULL,0,'582537','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107133',0,'54641988','666666',0,0,'',142,5,'2018-06-03 10:23:07',1,'',NULL,NULL),(265,0,0,'666666','2018-06-03 18:26:38','0000-00-00 00:00:00',NULL,0,0,NULL,0,'110237','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',146,5,'2018-06-03 10:29:00',0,'',NULL,NULL),(266,0,0,'666666','2018-06-03 18:31:50','0000-00-00 00:00:00',NULL,0,0,NULL,0,'256626','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',147,5,'2018-06-03 10:34:06',0,'',NULL,NULL),(267,0,0,'666666','2018-06-03 18:37:13','0000-00-00 00:00:00',NULL,0,0,NULL,0,'033728','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',148,5,'2018-06-03 10:39:31',0,'',NULL,NULL),(268,0,0,'666666','2018-06-03 18:42:43','0000-00-00 00:00:00',NULL,0,0,NULL,0,'580919','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',149,5,'2018-06-03 10:44:36',0,'',NULL,NULL),(269,1,0,'666666','2018-06-03 18:46:34','0000-00-00 00:00:00',NULL,80,80,NULL,0,'165610','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107134',0,'54641988','666666',0,0,'',141,5,'2018-06-03 10:46:58',1,'',NULL,NULL),(270,1,0,'666666','2018-06-03 18:51:27','0000-00-00 00:00:00',NULL,80,80,NULL,0,'186818','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107135',0,'54641988','666666',0,0,'',140,5,'2018-06-03 10:51:38',1,'',NULL,NULL),(271,0,0,'666666','2018-06-03 18:58:15','0000-00-00 00:00:00',NULL,0,0,NULL,0,'636518','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',150,5,'2018-06-03 10:59:18',0,'',NULL,NULL),(272,1,0,'666666','2018-06-03 19:00:07','0000-00-00 00:00:00',NULL,40,40,NULL,0,'286225','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107136',0,'54641988','666666',0,0,'',145,5,'2018-06-03 11:01:03',1,'',NULL,NULL),(273,1,0,'666666','2018-06-03 19:07:33','0000-00-00 00:00:00',NULL,170,170,NULL,0,'039906','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107137',0,'54641988','666666',0,0,'',133,5,'2018-06-03 11:07:42',1,'',NULL,NULL),(274,0,0,'666666','2018-06-03 19:07:50','0000-00-00 00:00:00',NULL,0,0,NULL,0,'366620','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',151,5,'2018-06-03 11:08:51',0,'',NULL,NULL),(275,1,0,'666666','2018-06-03 19:09:16','0000-00-00 00:00:00',NULL,40,40,NULL,0,'256626','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107138',0,'54641988','666666',0,0,'',147,5,'2018-06-03 11:09:24',1,'',NULL,NULL),(276,0,0,'666666','2018-06-03 19:16:13','0000-00-00 00:00:00',NULL,0,0,NULL,0,'313806','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',152,5,'2018-06-03 11:16:21',0,'',NULL,NULL),(277,0,0,'666666','2018-06-03 19:27:20','0000-00-00 00:00:00',NULL,0,0,NULL,0,'680210','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',153,5,'2018-06-03 11:29:24',0,'',NULL,NULL),(278,1,0,'666666','2018-06-03 19:39:13','0000-00-00 00:00:00',NULL,120,120,NULL,0,'506109','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107139',0,'54641988','666666',0,0,'',138,5,'2018-06-03 11:39:24',1,'',NULL,NULL),(279,1,0,'666666','2018-06-03 19:56:00','0000-00-00 00:00:00',NULL,170,170,NULL,0,'026112','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107140',0,'54641988','666666',0,0,'',135,5,'2018-06-03 11:56:11',1,'',NULL,NULL),(280,1,0,'666666','2018-06-03 20:05:39','0000-00-00 00:00:00',NULL,60,60,NULL,0,'580919','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107141',0,'54641988','666666',0,0,'',149,5,'2018-06-03 12:05:53',1,'',NULL,NULL),(281,1,0,'666666','2018-06-03 20:09:13','0000-00-00 00:00:00',NULL,170,170,NULL,0,'159517','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107142',0,'54641988','666666',0,0,'',136,5,'2018-06-03 12:10:02',1,'',NULL,NULL),(282,1,0,'666666','2018-06-03 20:12:42','0000-00-00 00:00:00',NULL,80,80,NULL,0,'033728','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107143',0,'54641988','666666',0,0,'',148,5,'2018-06-03 12:13:04',1,'',NULL,NULL),(283,1,0,'666666','2018-06-03 20:13:16','0000-00-00 00:00:00',NULL,60,60,NULL,0,'366620','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107144',0,'54641988','666666',0,0,'',151,5,'2018-06-03 12:13:25',1,'',NULL,NULL),(284,1,0,'666666','2018-06-03 20:15:41','0000-00-00 00:00:00',NULL,60,60,NULL,0,'636518','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107145',0,'54641988','666666',0,0,'',150,5,'2018-06-03 12:15:53',1,'',NULL,NULL),(285,1,0,'666666','2018-06-03 20:17:13','0000-00-00 00:00:00',NULL,100,100,NULL,0,'909838','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107146',0,'54641988','666666',0,0,'',144,5,'2018-06-03 12:17:21',1,'',NULL,NULL),(286,1,0,'666666','2018-06-03 20:20:06','0000-00-00 00:00:00',NULL,100,100,NULL,0,'909838','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(287,1,0,'666666','2018-06-03 20:20:35','0000-00-00 00:00:00',NULL,40,40,NULL,0,'680210','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107148',0,'54641988','666666',0,0,'',153,5,'2018-06-03 12:20:51',1,'',NULL,NULL),(288,1,0,'666666','2018-06-03 20:30:26','0000-00-00 00:00:00',NULL,60,60,NULL,0,'680210','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(289,1,0,'666666','2018-06-03 20:50:08','0000-00-00 00:00:00',NULL,100,100,NULL,0,'110237','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107150',0,'54641988','666666',0,0,'',146,5,'2018-06-03 12:50:17',1,'',NULL,NULL),(290,1,0,'666666','2018-06-03 21:02:37','0000-00-00 00:00:00',NULL,140,140,NULL,0,'509001','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107151',0,'54641988','666666',0,0,'',143,5,'2018-06-03 13:03:31',1,'',NULL,NULL),(291,1,0,'666666','2018-06-03 21:28:21','0000-00-00 00:00:00',NULL,100,100,NULL,0,'313806','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107152',0,'54641988','666666',0,0,'',152,5,'2018-06-03 13:28:36',1,'',NULL,NULL),(292,0,0,'666666','2018-06-04 07:10:11','0000-00-00 00:00:00',NULL,0,0,NULL,0,'595808','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',154,5,'2018-06-03 23:10:38',0,'',NULL,NULL),(293,1,0,'666666','2018-06-04 07:10:48','0000-00-00 00:00:00',NULL,40,170,NULL,0,'595808','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107153',0,'54641988','666666',0,0,'',154,5,'2018-06-03 23:11:22',1,'',NULL,NULL),(294,0,0,'666666','2018-06-04 08:21:22','0000-00-00 00:00:00',NULL,0,0,NULL,0,'473307','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',155,5,'2018-06-04 00:21:32',0,'',NULL,NULL),(295,1,0,'666666','2018-06-04 08:21:38','0000-00-00 00:00:00',NULL,40,170,NULL,0,'473307','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107154',0,'54641988','666666',0,0,'',155,5,'2018-06-04 00:21:52',1,'',NULL,NULL),(296,0,0,'666666','2018-06-04 10:23:00','0000-00-00 00:00:00',NULL,0,0,NULL,0,'209616','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',156,5,'2018-06-04 02:23:14',0,'',NULL,NULL),(297,1,0,'666666','2018-06-04 11:11:38','0000-00-00 00:00:00',NULL,40,40,NULL,0,'209616','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107155',0,'54641988','666666',0,0,'',156,5,'2018-06-04 03:11:52',1,'',NULL,NULL),(298,0,0,'666666','2018-06-04 11:48:04','0000-00-00 00:00:00',NULL,0,0,NULL,0,'883233','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',157,5,'2018-06-04 03:48:25',0,'',NULL,NULL),(299,0,0,'666666','2018-06-04 11:50:56','0000-00-00 00:00:00',NULL,0,0,NULL,0,'990504','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',158,5,'2018-06-04 03:51:09',0,'',NULL,NULL),(300,0,0,'666666','2018-06-04 12:15:09','0000-00-00 00:00:00',NULL,0,0,NULL,0,'179616','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',159,5,'2018-06-04 04:15:18',0,'',NULL,NULL),(301,1,0,'666666','2018-06-04 12:21:32','0000-00-00 00:00:00',NULL,40,170,NULL,0,'179616','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107156',0,'54641988','666666',0,0,'',159,5,'2018-06-04 04:21:46',1,'',NULL,NULL),(302,1,0,'666666','2018-06-04 12:26:59','0000-00-00 00:00:00',NULL,40,40,NULL,0,'990504','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107157',0,'54641988','666666',0,0,'',158,5,'2018-06-04 04:27:07',1,'',NULL,NULL),(303,0,0,'666666','2018-06-04 12:30:57','0000-00-00 00:00:00',NULL,0,0,NULL,0,'707104','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',160,5,'2018-06-04 04:31:08',0,'',NULL,NULL),(304,0,0,'666666','2018-06-04 12:39:46','0000-00-00 00:00:00',NULL,0,0,NULL,0,'750715','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',161,5,'2018-06-04 04:39:56',0,'',NULL,NULL),(305,0,0,'666666','2018-06-04 12:44:03','0000-00-00 00:00:00',NULL,0,0,NULL,0,'268003','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',162,5,'2018-06-04 04:44:13',0,'',NULL,NULL),(306,1,0,'666666','2018-06-04 13:01:27','0000-00-00 00:00:00',NULL,40,40,NULL,0,'750715','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107158',0,'54641988','666666',0,0,'',161,5,'2018-06-04 05:01:40',1,'',NULL,NULL),(307,0,0,'666666','2018-06-04 13:06:26','0000-00-00 00:00:00',NULL,0,0,NULL,0,'389315','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',163,5,'2018-06-04 05:06:35',0,'',NULL,NULL),(308,0,0,'666666','2018-06-04 13:16:09','0000-00-00 00:00:00',NULL,0,0,NULL,0,'821011','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',164,5,'2018-06-04 05:16:19',0,'',NULL,NULL),(309,1,0,'666666','2018-06-04 13:21:43','0000-00-00 00:00:00',NULL,40,40,NULL,0,'268003','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',162,5,'2018-06-04 05:21:53',1,'',NULL,NULL),(310,0,0,'666666','2018-06-04 13:32:06','0000-00-00 00:00:00',NULL,0,0,NULL,0,'326503','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',165,5,'2018-06-04 05:32:15',0,'',NULL,NULL),(311,1,0,'666666','2018-06-04 14:04:38','0000-00-00 00:00:00',NULL,40,40,NULL,0,'389315','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107159',0,'54641988','666666',0,0,'',163,5,'2018-06-04 06:04:46',1,'',NULL,NULL),(312,1,0,'666666','2018-06-04 14:14:05','0000-00-00 00:00:00',NULL,40,40,NULL,0,'821011','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107160',0,'54641988','666666',0,0,'',164,5,'2018-06-04 06:14:13',1,'',NULL,NULL),(313,1,0,'666666','2018-06-04 14:22:35','0000-00-00 00:00:00',NULL,40,40,NULL,0,'326503','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107161',0,'54641988','666666',0,0,'',165,5,'2018-06-04 06:22:43',1,'',NULL,NULL),(314,1,0,'666666','2018-06-04 14:24:49','0000-00-00 00:00:00',NULL,80,80,NULL,0,'707104','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107162',0,'54641988','666666',0,0,'',160,5,'2018-06-04 06:24:56',1,'',NULL,NULL),(315,0,0,'666666','2018-06-04 15:08:23','0000-00-00 00:00:00',NULL,0,0,NULL,0,'666715','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',166,5,'2018-06-04 07:08:31',0,'',NULL,NULL),(316,0,0,'666666','2018-06-04 15:42:04','0000-00-00 00:00:00',NULL,0,0,NULL,0,'588919','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',167,5,'2018-06-04 07:42:12',0,'',NULL,NULL),(317,1,0,'666666','2018-06-04 16:33:16','0000-00-00 00:00:00',NULL,40,40,NULL,0,'588919','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107163',0,'54641988','666666',0,0,'',167,5,'2018-06-04 08:33:25',1,'',NULL,NULL),(318,0,0,'666666','2018-06-04 17:04:34','0000-00-00 00:00:00',NULL,0,0,NULL,0,'058819','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',168,5,'2018-06-04 09:04:42',0,'',NULL,NULL),(319,1,0,'666666','2018-06-04 17:26:03','0000-00-00 00:00:00',NULL,100,100,NULL,0,'666715','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107164',3,'54641988','666666',0,0,'',166,5,'2018-06-04 09:26:16',1,'',NULL,NULL),(320,0,0,'666666','2018-06-04 17:49:51','0000-00-00 00:00:00',NULL,0,0,NULL,0,'662620','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',169,5,'2018-06-04 09:49:58',0,'',NULL,NULL),(321,1,0,'666666','2018-06-04 18:16:03','0000-00-00 00:00:00',NULL,40,40,NULL,0,'662620','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107165',0,'54641988','666666',0,0,'',169,5,'2018-06-04 10:16:12',1,'',NULL,NULL),(322,0,0,'666666','2018-06-04 18:18:30','0000-00-00 00:00:00',NULL,0,0,NULL,0,'352737','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',170,5,'2018-06-04 10:18:38',0,'',NULL,NULL),(323,0,0,'666666','2018-06-04 18:53:47','0000-00-00 00:00:00',NULL,0,0,NULL,0,'298808','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',171,5,'2018-06-04 10:53:55',0,'',NULL,NULL),(324,1,0,'666666','2018-06-04 18:53:58','0000-00-00 00:00:00',NULL,40,40,NULL,0,'352737','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107166',0,'54641988','666666',0,0,'',170,5,'2018-06-04 10:54:08',1,'',NULL,NULL),(325,0,0,'666666','2018-06-04 19:05:13','0000-00-00 00:00:00',NULL,0,0,NULL,0,'092737','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',172,5,'2018-06-04 11:05:21',0,'',NULL,NULL),(326,0,0,'666666','2018-06-04 19:20:57','0000-00-00 00:00:00',NULL,0,0,NULL,0,'607238','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',173,5,'2018-06-04 11:21:05',0,'',NULL,NULL),(327,0,0,'666666','2018-06-04 19:43:37','0000-00-00 00:00:00',NULL,0,0,NULL,0,'723220','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',174,5,'2018-06-04 11:43:44',0,'',NULL,NULL),(328,0,0,'666666','2018-06-04 20:01:18','0000-00-00 00:00:00',NULL,0,0,NULL,0,'136916','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',175,5,'2018-06-04 12:01:25',0,'',NULL,NULL),(329,0,0,'666666','2018-06-04 20:01:38','0000-00-00 00:00:00',NULL,0,0,NULL,0,'683712','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',176,5,'2018-06-04 12:01:50',0,'',NULL,NULL),(330,0,0,'666666','2018-06-04 20:02:20','0000-00-00 00:00:00',NULL,0,0,NULL,0,'179616','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',177,5,'2018-06-04 12:02:28',0,'',NULL,NULL),(331,1,0,'666666','2018-06-04 20:02:31','0000-00-00 00:00:00',NULL,40,40,NULL,0,'179616','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107167',0,'54641988','666666',0,0,'',177,5,'2018-06-04 12:02:40',1,'',NULL,NULL),(332,1,0,'666666','2018-06-04 20:08:32','0000-00-00 00:00:00',NULL,40,40,NULL,0,'683712','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107168',0,'54641988','666666',0,0,'',176,5,'2018-06-04 12:08:39',1,'',NULL,NULL),(333,1,0,'666666','2018-06-04 20:25:54','0000-00-00 00:00:00',NULL,40,40,NULL,0,'723220','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107169',0,'54641988','666666',0,0,'',174,5,'2018-06-04 12:26:02',1,'',NULL,NULL),(334,1,0,'666666','2018-06-04 20:28:51','0000-00-00 00:00:00',NULL,60,60,NULL,0,'092737','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107170',0,'54641988','666666',0,0,'',172,5,'2018-06-04 12:28:59',1,'',NULL,NULL),(335,1,0,'666666','2018-06-04 20:35:20','0000-00-00 00:00:00',NULL,40,40,NULL,0,'136916','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107171',0,'54641988','666666',0,0,'',175,5,'2018-06-04 12:35:27',1,'',NULL,NULL),(336,1,0,'666666','2018-06-04 20:51:51','0000-00-00 00:00:00',NULL,80,80,NULL,0,'298808','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107172',0,'54641988','666666',0,0,'',171,5,'2018-06-04 12:51:59',1,'',NULL,NULL),(337,1,0,'666666','2018-06-04 21:10:36','0000-00-00 00:00:00',NULL,170,180,NULL,0,'058819','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107173',3,'54641988','666666',0,0,'',168,5,'2018-06-04 13:11:07',1,'',NULL,NULL),(338,1,0,'666666','2018-06-04 22:01:29','0000-00-00 00:00:00',NULL,120,120,NULL,0,'607238','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107174',0,'54641988','666666',0,0,'',173,5,'2018-06-04 14:01:37',1,'',NULL,NULL),(339,1,0,'666666','2018-06-04 22:08:06','0000-00-00 00:00:00',NULL,120,120,NULL,0,'607238','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107175',0,'54641988','666666',0,0,'',-1,5,'2018-06-04 14:08:15',1,'',NULL,NULL),(340,1,0,'666666','2018-06-04 22:17:46','0000-00-00 00:00:00',NULL,170,0,NULL,0,'883233','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',157,5,'2018-06-04 14:17:59',1,'',NULL,NULL),(341,0,0,'666666','2018-06-05 07:49:40','0000-00-00 00:00:00',NULL,0,0,NULL,0,'595838','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',178,5,'2018-06-04 23:49:51',0,'',NULL,NULL),(342,1,0,'666666','2018-06-05 07:49:53','0000-00-00 00:00:00',NULL,40,170,NULL,0,'595838','127.0.0.1','1','1',NULL,NULL,0,1,'QW00107176',0,'54641988','666666',0,0,'',178,5,'2018-06-04 23:50:20',1,'',NULL,NULL),(343,0,0,'666666','2018-06-05 11:15:57','0000-00-00 00:00:00',NULL,0,0,NULL,0,'8563','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',179,2,'2018-06-05 03:16:41',0,'',NULL,NULL),(344,1,0,'666666','2018-06-05 11:17:11','0000-00-00 00:00:00',NULL,40,0,NULL,0,'8563','127.0.0.1','1','1',NULL,NULL,0,1,NULL,NULL,NULL,'666666',0,0,'',179,2,'2018-06-05 03:17:26',5,'',NULL,NULL);
/*!40000 ALTER TABLE `real_time_transaction_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `role_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modified_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `create_account_id` int(11) DEFAULT NULL,
  `modified_account_id` int(11) DEFAULT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `role_type` varchar(30) NOT NULL,
  `is_system_role` int(11) DEFAULT '0' COMMENT '只有is_superuser =1 的帳號才能夠選擇的角色',
  `customer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`role_id`),
  UNIQUE KEY `role_id` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'root_admin','root admin role','root_admin',1,0),(2,'2018-05-21 07:08:05','2018-05-21 07:08:05',0,NULL,'pad_admin','admin role','pad_admin',1,1),(3,'2018-05-21 10:26:31','2018-05-21 10:26:31',3,NULL,'管理員','管理員權限','',NULL,1);
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shift_checkout`
--

DROP TABLE IF EXISTS `shift_checkout`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shift_checkout` (
  `checkout_no` varchar(20) NOT NULL COMMENT '結班條序號',
  `data_in_json` varchar(255) NOT NULL COMMENT '結班資料in json type',
  `garage_id` int(11) NOT NULL COMMENT '場站ID',
  `customer_id` int(11) NOT NULL COMMENT '業者ID',
  `clock_in_time` datetime NOT NULL COMMENT '班別開始時間',
  `clock_out_time` datetime NOT NULL COMMENT '班別結束時間',
  `checkout_time` datetime NOT NULL COMMENT '結班時間',
  `checkout_amount` int(11) NOT NULL COMMENT '結帳金額',
  `number_of_vehicles` int(11) NOT NULL COMMENT '出場車輛數',
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `create_account_id` int(11) NOT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8 COMMENT='平板結班資料';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shift_checkout`
--

LOCK TABLES `shift_checkout` WRITE;
/*!40000 ALTER TABLE `shift_checkout` DISABLE KEYS */;
INSERT INTO `shift_checkout` VALUES ('120180521001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"QW00105650~QW00105650\",\"numCarIn\":1,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\"',1,1,'2018-05-21 18:43:57','2018-05-21 18:44:44','2018-05-21 18:44:44',40,1,'2018-05-21 10:44:50',2,1),('120180522001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":2,\"numCarNotOut\":2,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-21 18:46:50','2018-05-22 00:03:10','2018-05-22 00:03:10',0,0,'2018-05-21 16:03:17',2,2),('120180522002','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":2,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-22 00:03:33','2018-05-22 00:04:37','2018-05-22 00:04:37',0,0,'2018-05-21 16:04:42',2,3),('120180522003','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"QW00105651~QW00105651\",\"numCarIn\":1,\"numCarNotOut\":2,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\"',1,1,'2018-05-22 00:05:21','2018-05-22 00:40:54','2018-05-22 00:40:54',40,1,'2018-05-21 16:41:09',2,4),('120180522001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-22 01:21:11','2018-05-22 01:36:53','2018-05-22 01:36:53',0,0,'2018-05-21 17:40:28',2,5),('120180522002','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":3,\"numCarNotOut\":3,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-22 01:40:16','2018-05-22 07:59:16','2018-05-22 07:59:16',0,0,'2018-05-21 23:59:21',4,6),('120180522003','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":2,\"numCarNotOut\":5,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-22 07:59:41','2018-05-22 10:21:31','2018-05-22 10:21:31',0,0,'2018-05-22 02:21:50',4,7),('120180522004','{\"accountName\":\"guard_user_2\",\"discount\":60,\"invoiceStartEnd\":\"QW00105850~QW00105852\",\"numCarIn\":6,\"numCarNotOut\":8,\"numCarOut\":3,\"numPayFree\":0,\"numPayModified\":3,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":160,\"payNormal\":0,\"payRent\":0,\"re',1,1,'2018-05-22 10:22:37','2018-05-22 10:54:56','2018-05-22 10:54:56',160,3,'2018-05-22 02:55:24',4,8),('120180524001','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":2,\"numCarNotOut\":9,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":170,\"payRent\":0,\"receivables\":170,\"receiv',1,1,'2018-05-22 10:55:45','2018-05-24 10:47:08','2018-05-24 10:47:08',170,1,'2018-05-24 02:47:50',4,9),('120180524002','{\"accountName\":\"guard_user_2\",\"discount\":310,\"invoiceStartEnd\":\"\",\"numCarIn\":2,\"numCarNotOut\":9,\"numCarOut\":2,\"numPayFree\":0,\"numPayModified\":1,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":200,\"payNormal\":40,\"payRent\":0,\"receivables\":550,\"rec',1,1,'2018-05-24 10:47:51','2018-05-24 10:57:50','2018-05-24 10:57:50',240,2,'2018-05-24 02:58:23',4,10),('120180525001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"QW00106050~QW00106050\",\"numCarIn\":2,\"numCarNotOut\":1,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\"',1,1,'2018-05-25 18:08:58','2018-05-25 18:11:44','2018-05-25 18:11:44',40,1,'2018-05-25 10:11:50',2,11),('120180529001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\":40,\"received\":40,\"re',1,1,'2018-05-28 16:07:56','2018-05-29 16:04:16','2018-05-29 16:04:16',40,1,'2018-05-29 08:05:39',2,12),('120180529001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":2,\"numCarNotOut\":1,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":1,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-29 16:41:15','2018-05-29 17:01:41','2018-05-29 17:01:41',0,1,'2018-05-29 09:01:46',2,13),('120180530001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-30 13:56:08','2018-05-30 13:57:58','2018-05-30 13:57:58',0,0,'2018-05-30 05:58:13',2,14),('120180530001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":1,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-30 14:23:06','2018-05-30 14:25:18','2018-05-30 14:25:18',0,0,'2018-05-30 06:25:19',2,15),('120180530001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-30 15:11:17','2018-05-30 15:11:42','2018-05-30 15:11:42',0,0,'2018-05-30 07:11:47',2,16),('120180530002','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"QW00106450~QW00106453\",\"numCarIn\":7,\"numCarNotOut\":3,\"numCarOut\":4,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":4,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":160,\"payRent\":0,\"rec',1,1,'2018-05-30 15:12:03','2018-05-30 15:57:56','2018-05-30 15:57:56',160,4,'2018-05-30 07:57:57',4,17),('20180531001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\":40,\"received\":40,\"re',1,1,'2018-05-30 18:59:26','2018-05-31 10:25:16','2018-05-31 10:25:16',40,1,'2018-05-31 02:25:23',2,18),('20180531002','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-31 10:26:14','2018-05-31 10:26:19','2018-05-31 10:26:19',0,0,'2018-05-31 02:26:25',4,19),('20180531003','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-31 10:26:54','2018-05-31 10:26:57','2018-05-31 10:26:57',0,0,'2018-05-31 02:27:02',4,20),('20180531001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-31 14:05:08','2018-05-31 14:34:32','2018-05-31 14:34:32',0,0,'2018-05-31 06:34:41',2,21),('20180531002','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\":40,\"received\":40,\"re',1,1,'2018-05-31 14:41:33','2018-05-31 14:48:37','2018-05-31 14:48:37',40,1,'2018-05-31 06:48:45',2,22),('20180531003','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-31 15:07:45','2018-05-31 15:07:47','2018-05-31 15:07:47',0,0,'2018-05-31 07:07:54',4,23),('20180531004','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-05-31 15:08:05','2018-05-31 15:08:08','2018-05-31 15:08:08',0,0,'2018-05-31 07:08:34',4,24),('20180531001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":1,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-05-31 16:00:43','2018-05-31 16:01:59','2018-05-31 16:01:59',0,0,'2018-05-31 08:02:06',2,25),('20180601001','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":400,\"payRent\":0,\"receivables\":400,\"receiv',1,1,'2018-06-01 09:10:51','2018-06-01 09:11:23','2018-06-01 09:11:23',400,1,'2018-06-01 01:11:33',4,26),('20180601002','{\"accountName\":\"guard_user_2\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":0,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\":40,\"received',1,1,'2018-06-01 11:47:47','2018-06-01 11:48:11','2018-06-01 11:48:11',40,1,'2018-06-01 03:48:23',4,27),('20180601001','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-06-01 15:30:09','2018-06-01 15:53:44','2018-06-01 15:53:44',0,0,'2018-06-01 07:53:53',2,28),('20180601002','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-06-01 15:56:05','2018-06-01 15:56:07','2018-06-01 15:56:07',0,0,'2018-06-01 07:56:11',2,29),('20180601003','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":0,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":0,\"refun',1,1,'2018-06-01 15:57:38','2018-06-01 15:58:36','2018-06-01 15:58:36',0,0,'2018-06-01 07:58:41',2,30),('20180601004','{\"accountName\":\"root\",\"discount\":0,\"invoiceStartEnd\":\"QW00107050~QW00107050\",\"numCarIn\":3,\"numCarNotOut\":2,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"receivables\"',1,1,'2018-06-01 15:59:11','2018-06-01 16:05:52','2018-06-01 16:05:52',40,1,'2018-06-01 08:05:59',2,31),('20180601005','{\"accountName\":\"root\",\"discount\":80,\"invoiceStartEnd\":\"\",\"numCarIn\":1,\"numCarNotOut\":1,\"numCarOut\":2,\"numPayFree\":2,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":80,\"received\":0,\"ref',1,1,'2018-06-01 16:07:53','2018-06-01 16:18:05','2018-06-01 16:18:05',0,2,'2018-06-01 08:18:10',2,32),('20180601006','{\"accountName\":\"guard_user_3\",\"discount\":0,\"invoiceStartEnd\":\"\",\"numCarIn\":0,\"numCarNotOut\":1,\"numCarOut\":0,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":0,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":0,\"payRent\":0,\"receivables\":0,\"received\":',1,1,'2018-06-01 16:18:20','2018-06-01 16:18:21','2018-06-01 16:18:21',0,0,'2018-06-01 08:18:25',5,33),('20180601007','{\"accountName\":\"guard_user_3\",\"discount\":0,\"invoiceStartEnd\":\"QW00107051~QW00107051\",\"numCarIn\":1,\"numCarNotOut\":1,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"rece',1,1,'2018-06-01 16:18:59','2018-06-01 16:43:03','2018-06-01 16:43:03',40,1,'2018-06-01 08:43:10',5,34),('20180601008','{\"accountName\":\"guard_user_3\",\"discount\":0,\"invoiceStartEnd\":\"QW00107052~QW00107052\",\"numCarIn\":1,\"numCarNotOut\":1,\"numCarOut\":1,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":1,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":40,\"payRent\":0,\"rece',1,1,'2018-06-01 16:43:51','2018-06-01 16:45:34','2018-06-01 16:45:34',40,1,'2018-06-01 08:45:43',5,35),('20180601009','{\"accountName\":\"guard_user_3\",\"discount\":40,\"invoiceStartEnd\":\"QW00107053~QW00107067\",\"numCarIn\":15,\"numCarNotOut\":0,\"numCarOut\":16,\"numPayFree\":1,\"numPayModified\":0,\"numPayNormal\":15,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":1040,\"payRent\":0',1,1,'2018-06-01 16:52:00','2018-06-01 22:37:50','2018-06-01 22:37:50',1040,16,'2018-06-01 14:37:55',5,36),('20180602001','{\"accountName\":\"guard_user_3\",\"discount\":240,\"invoiceStartEnd\":\"QW00107068~QW00107106\",\"numCarIn\":37,\"numCarNotOut\":0,\"numCarOut\":43,\"numPayFree\":1,\"numPayModified\":16,\"numPayNormal\":26,\"numPayRent\":0,\"payFree\":0,\"payModified\":1760,\"payNormal\":1870,\"payRe',1,1,'2018-06-02 07:54:25','2018-06-02 21:49:50','2018-06-02 21:49:50',3630,43,'2018-06-02 13:52:12',5,37),('20180603001','{\"accountName\":\"guard_user_3\",\"discount\":0,\"invoiceStartEnd\":\"QW00107107~QW00107121\",\"numCarIn\":26,\"numCarNotOut\":10,\"numCarOut\":16,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":16,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":1240,\"payRent\":0',1,1,'2018-06-03 06:44:33','2018-06-03 15:00:58','2018-06-03 15:00:58',1240,16,'2018-06-03 07:01:13',5,38),('20180603002','{\"accountName\":\"guard_user_3\",\"discount\":0,\"invoiceStartEnd\":\"QW00107122~QW00107152\",\"numCarIn\":18,\"numCarNotOut\":0,\"numCarOut\":31,\"numPayFree\":0,\"numPayModified\":0,\"numPayNormal\":31,\"numPayRent\":0,\"payFree\":0,\"payModified\":0,\"payNormal\":3090,\"payRent\":0,',1,1,'2018-06-03 15:01:36','2018-06-03 21:33:16','2018-06-03 21:33:16',3090,31,'2018-06-03 13:33:23',5,39),('20180604001','{\"accountName\":\"guard_user_3\",\"discount\":-230,\"invoiceStartEnd\":\"QW00107153~QW00107175\",\"numCarIn\":24,\"numCarNotOut\":0,\"numCarOut\":25,\"numPayFree\":1,\"numPayModified\":4,\"numPayNormal\":20,\"numPayRent\":0,\"payFree\":0,\"payModified\":690,\"payNormal\":1120,\"payRen',1,1,'2018-06-04 07:01:35','2018-06-04 22:26:10','2018-06-04 22:26:10',1810,25,'2018-06-04 14:26:23',5,40);
/*!40000 ALTER TABLE `shift_checkout` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_config`
--

DROP TABLE IF EXISTS `system_config`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_config` (
  `report_title` varchar(60) NOT NULL COMMENT '報表名稱',
  `is_usb_mode_active` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `usb_version_id` varchar(4) NOT NULL,
  `pv_voice_value` varchar(2) NOT NULL DEFAULT '0' COMMENT 'PV調整音量大小',
  `entry_balance_warning` int(4) NOT NULL DEFAULT '0' COMMENT '進場餘額警示水位',
  `is_commutation_ticket_module_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '定期票功能(1:啟用, 0:停用)',
  `commutation_ticket_sales_type` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1:只有汽車,2:只有機車,3:汽車+機車',
  `is_transfer_module_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '轉乘優惠功能(1:啟用,0:停用)',
  `is_e_invoice_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否使用電子發票',
  `e_invoice_request_minimum` int(4) NOT NULL DEFAULT '0' COMMENT '電子發票發動取號的最低數量',
  `is_java_server_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否為java socket server mode',
  `pv_alert_interval` int(4) NOT NULL DEFAULT '0' COMMENT 'PV警告狀態顯示檢查間隔(單位:秒)',
  `monitor_response_time` int(10) unsigned NOT NULL COMMENT '監控不回應時間警示(單位:分鐘)',
  `is_calculator_parking_data` tinyint(1) NOT NULL DEFAULT '0' COMMENT '更新PMS交易資料清分狀態',
  `is_check_accounting_and_email_notify` tinyint(1) NOT NULL DEFAULT '0' COMMENT '自動對帳與發送通知',
  `is_support_multi_language` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否開啟多國語言選取功能(1:是, 0:否)',
  `is_customize_disability_column_name` tinyint(1) NOT NULL DEFAULT '0' COMMENT '身障計費試算欄位名稱是否客製(0:否, 1:是)',
  `is_invoice_record_number_mode` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否啟用傳統發票號碼記錄',
  `invoice_paperroll_usable_number` int(4) NOT NULL DEFAULT '0' COMMENT '發票紙捲可用張數',
  `invoice_alert_usable_number` int(4) NOT NULL DEFAULT '0' COMMENT '發票紙捲剩餘張數警告通知',
  `is_commuter_ticket_check_entry_balance` tinyint(1) NOT NULL DEFAULT '0' COMMENT '定期票進場是否檢查最低入場餘額',
  `is_fee_caculation_by_config` tinyint(1) NOT NULL DEFAULT '0' COMMENT '計費規則參數化設定(1:啟用, 0:停用)',
  `is_human_pay_and_confirm_fix` tinyint(1) NOT NULL DEFAULT '0' COMMENT '支援[人工結帳已付款]和[已扣款未回confirm狀態]旗標判定',
  `is_auto_add_value_card_check_entry_balance` tinyint(1) NOT NULL DEFAULT '0' COMMENT '自動加值卡片檢查最低入場餘額(0:關,1:開)',
  `e_invoice_service_provider` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1:ChiefPay, 2:台灣聯通, 3:電子發票標準化介面',
  `is_support_gate_control` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否支援遠端開閘',
  `acer_id` varchar(10) DEFAULT NULL,
  `config_name` varchar(60) DEFAULT NULL,
  `csv_file_date` varchar(10) DEFAULT NULL COMMENT '解析csv檔案內容的資料來源日期',
  `modified_account_id` int(11) DEFAULT NULL,
  `modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新時間',
  `system_config_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`system_config_id`),
  UNIQUE KEY `system_config_id` (`system_config_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='系統參數';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_config`
--

LOCK TABLES `system_config` WRITE;
/*!40000 ALTER TABLE `system_config` DISABLE KEYS */;
/*!40000 ALTER TABLE `system_config` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `system_log`
--

DROP TABLE IF EXISTS `system_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `system_log` (
  `system_log_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `event_id` int(11) DEFAULT NULL,
  `create_account_id` int(11) DEFAULT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `event_message` varchar(255) DEFAULT NULL,
  `query_string` varchar(255) DEFAULT NULL,
  `field_1` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`system_log_id`),
  UNIQUE KEY `system_log_id` (`system_log_id`)
) ENGINE=InnoDB AUTO_INCREMENT=38 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `system_log`
--

LOCK TABLES `system_log` WRITE;
/*!40000 ALTER TABLE `system_log` DISABLE KEYS */;
INSERT INTO `system_log` VALUES (1,1,2,'2018-05-21 10:23:35','add_customer: {\"customer_status\": \"1\", \"customer_code\": \"8003\", \"company_name\": \"\\u79be\\u5178\\u5be6\\u696d\\u6709\\u9650\\u516c\\u53f8\", \"contact_username\": \"\\u738b\\u632f\\u6c11\", \"phone_number1\": \"02-27098677\", \"company_address\": \"\\u53f0\\u5317\\u5e02\\u4e2d\\u5c7',NULL,NULL),(2,1,1,'2018-05-21 10:24:58','add_user: {\"is_superuser\": false, \"is_customer_root\": true, \"customer_id\": 1, \"account\": \"guard_user_1\", \"role_id\": 2, \"user_first_name\": \"\\u738b\", \"user_last_name\": \"\\u632f\\u6c11\", \"create_account_id\": 2, \"password\": \"$pbkdf2-sha256$200000$gvBea62VkpJy7p',NULL,NULL),(3,12,3,'2018-05-21 10:26:31','{\"name\": \"\\u7ba1\\u7406\\u54e1\", \"description\": \"\\u7ba1\\u7406\\u54e1\\u6b0a\\u9650\", \"create_account_id\": 3, \"customer_id\": 1}[{\"permission_id\": 131}, {\"permission_id\": 143}, {\"permission_id\": 181}, {\"permission_id\": 182}]',NULL,NULL),(4,1,3,'2018-05-21 10:30:14','{\"caculation_time_base_unit\": 0, \"garage_code\": \"8003101\", \"garage_name\": \"\\u6674\\u7f8e\\u7ad9\\u71df\\u696d\\u8655\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"district\": \"\\u4e2d\\u6b63\\u5340\", \"address1\": \"\\u53f0\\u5317\\u5e02\\u4e2d\\u5c71\\u5340\\u6797\\u68ee\\u5317\\u8de',NULL,NULL),(5,1,1,'2018-05-21 11:54:41','add_user: {\"is_superuser\": false, \"is_customer_root\": true, \"customer_id\": 1, \"account\": \"guard_user_2\", \"role_id\": 3, \"user_first_name\": \"Amy\", \"user_last_name\": \"Fang\", \"create_account_id\": 2, \"password\": \"$pbkdf2-sha256$200000$fU/JWauV8n5P6b1XKkWIcQ$qf',NULL,NULL),(6,2,2,'2018-05-21 12:26:35','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-05-21 12:26:35\", \"create_account_id\": 2, \"modified_account_id\": 3, \"account\": \"guard_user_1\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$gvBea62VkpJy7p2T',NULL,NULL),(7,2,2,'2018-05-21 16:18:48','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-05-21 16:18:48\", \"create_account_id\": 2, \"modified_account_id\": 3, \"account\": \"guard_user_2\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$fU/JWauV8n5P6b1X',NULL,NULL),(8,2,1,'2018-05-22 02:05:10','update_user: {\"account_id\": 1, \"create_date\": \"2018-05-21 07:08:05\", \"modified_date\": \"2018-05-22 02:05:10\", \"create_account_id\": 1, \"modified_account_id\": 2, \"account\": \"system\", \"customer_id\": 0, \"password\": \"$pbkdf2-sha256$200000$8947hzBmLEUopRRC6J2ztg',NULL,NULL),(9,2,1,'2018-05-22 02:05:20','update_user: {\"account_id\": 2, \"create_date\": \"2018-05-21 07:08:05\", \"modified_date\": \"2018-05-22 02:05:20\", \"create_account_id\": 1, \"modified_account_id\": 2, \"account\": \"root\", \"customer_id\": 0, \"password\": \"$pbkdf2-sha256$200000$8947hzBmLEUopRRC6J2ztg$5',NULL,NULL),(10,2,2,'2018-05-22 02:54:29','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-05-22 02:54:29\", \"create_account_id\": 2, \"modified_account_id\": 3, \"account\": \"guard_user_2\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$lPIeQ6jV2juHcM45',NULL,NULL),(11,2,2,'2018-05-22 02:54:47','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-05-22 02:54:47\", \"create_account_id\": 2, \"modified_account_id\": 3, \"account\": \"guard_user_1\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$6B3DmHPOmfMeI8T4',NULL,NULL),(12,2,1,'2018-05-23 04:02:27','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-05-23 04:02:27\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_1\", \"customer_id\": 0, \"password\": \"$pbkdf2-sha256$200000$ipGylpIyZsx5rxXi',NULL,NULL),(13,2,1,'2018-05-23 04:11:28','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-05-23 04:11:28\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_2\", \"customer_id\": 0, \"password\": \"$pbkdf2-sha256$200000$MSZECAHgXOtdK6V0',NULL,NULL),(14,1,3,'2018-05-23 04:18:32','{\"caculation_time_base_unit\": 0, \"garage_code\": \"test\", \"garage_name\": \"123\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"create_account_id\": 3}',NULL,NULL),(15,2,1,'2018-05-25 06:55:14','update_user: {\"account_id\": 1, \"create_date\": \"2018-05-21 07:08:05\", \"modified_date\": \"2018-05-25 06:55:14\", \"create_account_id\": 1, \"modified_account_id\": 2, \"account\": \"system\", \"customer_id\": 0, \"password\": \"$pbkdf2-sha256$200000$8947hzBmLEUopRRC6J2ztg',NULL,NULL),(16,2,2,'2018-05-30 05:33:48','{\"garage_code\": \"1\", \"garage_name\": \"\\u6674\\u7f8e\\u7ad9\\u71df\\u696d\\u8655\", \"customer_id\": 1, \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": \"\\u4e2d\\u6b63\\u5340\", \"district_code\": null, \"address1\": \"\\u53f0\\u5317\\u5e02\\u4e2d\\u5c71\\u5340\\',NULL,NULL),(17,1,2,'2018-06-01 03:14:48','add_user: {\"is_superuser\": false, \"is_customer_root\": false, \"customer_id\": 1, \"account\": \"guard_user_3\", \"role_id\": 3, \"user_first_name\": \"Yen\", \"user_last_name\": \"Kitty\", \"create_account_id\": 3, \"password\": \"$pbkdf2-sha256$200000$WssZ4xxjrLXWmpMSImSMEQ$',NULL,NULL),(18,2,2,'2018-06-01 05:32:51','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-06-01 05:32:51\", \"create_account_id\": 2, \"modified_account_id\": 3, \"account\": \"guard_user_2\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$MSZECAHgXOtdK6V0',NULL,NULL),(19,2,2,'2018-06-01 05:33:08','update_user: {\"account_id\": 5, \"create_date\": \"2018-06-01 03:14:48\", \"modified_date\": \"2018-06-01 05:33:08\", \"create_account_id\": 3, \"modified_account_id\": 3, \"account\": \"guard_user_3\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$WssZ4xxjrLXWmpMS',NULL,NULL),(20,2,2,'2018-06-01 07:19:46','{\"garage_code\": \"test\", \"garage_name\": \"123\", \"customer_id\": null, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": null, \"district_code\": null, \"address1\": null, \"address2\": null, \"total_capacity\": 0, \"sedan_',NULL,NULL),(21,2,2,'2018-06-01 07:20:00','{\"garage_code\": \"test\", \"garage_name\": \"123\", \"customer_id\": null, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": null, \"district_code\": null, \"address1\": null, \"address2\": null, \"total_capacity\": 0, \"sedan_',NULL,NULL),(22,2,2,'2018-06-01 07:25:26','{\"garage_code\": \"test\", \"garage_name\": \"123\", \"customer_id\": null, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": null, \"district_code\": null, \"address1\": null, \"address2\": null, \"total_capacity\": 0, \"sedan_',NULL,NULL),(23,2,2,'2018-06-01 07:26:41','{\"garage_code\": \"test\", \"garage_name\": \"123\", \"customer_id\": null, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": null, \"district_code\": null, \"address1\": null, \"address2\": null, \"total_capacity\": 0, \"sedan_',NULL,NULL),(24,2,2,'2018-06-01 07:26:49','{\"garage_code\": \"test\", \"garage_name\": \"123\", \"customer_id\": null, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": null, \"district_code\": null, \"address1\": null, \"address2\": null, \"total_capacity\": 0, \"sedan_',NULL,NULL),(25,2,2,'2018-06-01 07:29:59','{\"customer_id\": 1, \"customer_code\": \"8003\", \"company_name\": \"\\u79be\\u5178\\u5be6\\u696d\\u6709\\u9650\\u516c\\u53f8\", \"company_english_name\": null, \"company_union_number\": \"72962808\", \"contact_username\": \"\\u738b\\u632f\\u6c11\", \"contact_datetime\": \"3\", \"mobile\": ',NULL,NULL),(26,2,2,'2018-06-01 07:30:35','{\"customer_id\": 1, \"customer_code\": \"8003\", \"company_name\": \"\\u79be\\u5178\\u5be6\\u696d\\u6709\\u9650\\u516c\\u53f8\", \"company_english_name\": null, \"company_union_number\": \"72962808\", \"contact_username\": \"\\u738b\\u632f\\u6c11\", \"contact_datetime\": \"1\", \"mobile\": ',NULL,NULL),(27,2,1,'2018-06-01 07:56:09','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-06-01 07:56:09\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_1\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$ttYa47x3DuE8x9i7',NULL,NULL),(28,2,1,'2018-06-01 07:57:09','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-06-01 07:57:09\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_2\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$0vp/z1lrDeGcc87Z',NULL,NULL),(29,2,1,'2018-06-01 07:57:59','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-06-01 07:57:59\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_1\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$vDfmvBdCCOE8B.Dc',NULL,NULL),(30,2,1,'2018-06-01 07:59:54','update_user: {\"account_id\": 3, \"create_date\": \"2018-05-21 10:24:58\", \"modified_date\": \"2018-06-01 07:59:54\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_1\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$S0kpJYTQGmOMkfIe',NULL,NULL),(31,2,1,'2018-06-01 08:00:02','update_user: {\"account_id\": 4, \"create_date\": \"2018-05-21 11:54:41\", \"modified_date\": \"2018-06-01 08:00:02\", \"create_account_id\": 2, \"modified_account_id\": 2, \"account\": \"guard_user_2\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$YExJqdU653xvDYHQ',NULL,NULL),(32,2,1,'2018-06-01 08:00:04','update_user: {\"account_id\": 5, \"create_date\": \"2018-06-01 03:14:48\", \"modified_date\": \"2018-06-01 08:00:04\", \"create_account_id\": 3, \"modified_account_id\": 2, \"account\": \"guard_user_3\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$xhijNCZEKEXImbN2',NULL,NULL),(33,2,1,'2018-06-01 08:00:09','update_user: {\"account_id\": 5, \"create_date\": \"2018-06-01 03:14:48\", \"modified_date\": \"2018-06-01 08:00:09\", \"create_account_id\": 3, \"modified_account_id\": 2, \"account\": \"guard_user_3\", \"customer_id\": 1, \"password\": \"$pbkdf2-sha256$200000$cE6pdQ4BoBTi/P./',NULL,NULL),(34,1,1,'2018-06-01 08:00:48','add_user: {\"is_superuser\": false, \"is_customer_root\": true, \"customer_id\": 1, \"account\": \"user1\", \"role_id\": 2, \"create_account_id\": 2, \"password\": \"$pbkdf2-sha256$200000$eC8lRAiBcO79/x8jBCAkpA$EZMWqUHjgWhep10M6CdgL4/zlt5L4DvSFhg4.kuKyO8\"}',NULL,NULL),(35,2,2,'2018-06-01 08:18:31','{\"customer_id\": 1, \"customer_code\": \"8003\", \"company_name\": \"\\u79be\\u5178\\u5be6\\u696d\\u6709\\u9650\\u516c\\u53f8\", \"company_english_name\": null, \"company_union_number\": \"72962808\", \"contact_username\": \"\\u738b\\u632f\\u6c11\", \"contact_datetime\": \"1\", \"mobile\": ',NULL,NULL),(36,2,2,'2018-06-02 05:21:07','{\"garage_code\": \"1\", \"garage_name\": \"\\u6674\\u7f8e\\u7ad9\", \"customer_id\": 1, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": \"\\u4e2d\\u6b63\\u5340\", \"district_code\": null, \"address1\": \"\\u53f0\\u5317\\u5e02\\u4e2d\\u',NULL,NULL),(37,2,2,'2018-06-02 05:21:07','{\"garage_code\": \"1\", \"garage_name\": \"\\u6674\\u7f8e\\u7ad9\", \"customer_id\": 1, \"customer_garage_id\": \"R17\", \"city_name\": \"\\u53f0\\u5317\\u5e02\", \"city_code\": null, \"district\": \"\\u4e2d\\u6b63\\u5340\", \"district_code\": null, \"address1\": \"\\u53f0\\u5317\\u5e02\\u4e2d\\u',NULL,NULL);
/*!40000 ALTER TABLE `system_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ticket_provider`
--

DROP TABLE IF EXISTS `ticket_provider`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ticket_provider` (
  `ticket_provider_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `company_name` varchar(32) NOT NULL,
  `type_id` varchar(32) NOT NULL,
  `ticket_provider_code` varchar(32) NOT NULL COMMENT 'Acer ITS 定義票證業者代碼',
  `provider_garage_code` varchar(10) DEFAULT NULL COMMENT '場站編號(悠遊卡,一卡通)',
  `provider_transaction_code` varchar(10) DEFAULT NULL COMMENT '交易系統代碼(一卡通)',
  `provider_system_code` varchar(32) DEFAULT NULL COMMENT '交易車種代碼(一卡通)',
  `provider_transfer_code` varchar(32) DEFAULT NULL COMMENT '系統轉乘代碼(一卡通)',
  `modified_account_id` int(11) DEFAULT NULL,
  `modified_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ticket_provider_id`),
  UNIQUE KEY `ticket_provider_id` (`ticket_provider_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ticket_provider`
--

LOCK TABLES `ticket_provider` WRITE;
/*!40000 ALTER TABLE `ticket_provider` DISABLE KEYS */;
/*!40000 ALTER TABLE `ticket_provider` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `trx_data`
--

DROP TABLE IF EXISTS `trx_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `trx_data` (
  `import_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `file_name` varchar(54) NOT NULL DEFAULT ' ',
  `trx_date` varchar(8) NOT NULL DEFAULT ' ',
  `trx_time` varchar(6) NOT NULL DEFAULT ' ',
  `card_no` varchar(50) NOT NULL DEFAULT ' ',
  `txn_no` varchar(6) NOT NULL DEFAULT '',
  `trx_amt` int(11) DEFAULT '0',
  `device_id` varchar(10) DEFAULT ' ',
  `trx_type` varchar(2) DEFAULT NULL,
  `trx_sub_type` varchar(2) DEFAULT NULL,
  `el_value` int(11) DEFAULT '0',
  `cal_date` varchar(8) DEFAULT ' ',
  `cal_status` varchar(2) DEFAULT ' ',
  `dept_id` varchar(10) NOT NULL DEFAULT '00',
  `unit_id` varchar(2) NOT NULL DEFAULT '02',
  `cal_err_code` varchar(10) NOT NULL DEFAULT '',
  `source_filename` varchar(100) DEFAULT NULL,
  `garage_code` varchar(20) DEFAULT NULL,
  `csv_file_date` varchar(20) DEFAULT NULL,
  `trx_data_id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `create_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`trx_data_id`),
  UNIQUE KEY `trx_data_id` (`trx_data_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `trx_data`
--

LOCK TABLES `trx_data` WRITE;
/*!40000 ALTER TABLE `trx_data` DISABLE KEYS */;
/*!40000 ALTER TABLE `trx_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `parking_view`
--

/*!50001 DROP TABLE IF EXISTS `parking_view`*/;
/*!50001 DROP VIEW IF EXISTS `parking_view`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8 */;
/*!50001 SET character_set_results     = utf8 */;
/*!50001 SET collation_connection      = utf8_general_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `parking_view` AS select `b`.`garage_code` AS `garage_code`,`b`.`id` AS `id`,`a`.`pv` AS `pv`,`b`.`pv_out` AS `pv_out`,`a`.`type` AS `type`,`a`.`pricing_scheme` AS `pricing_scheme`,`a`.`pricing_scheme_disability` AS `pricing_scheme_disability`,`b`.`card_id` AS `card_id`,`b`.`card_id16` AS `card_id16`,`b`.`enter_time` AS `enter_time`,`b`.`exit_time` AS `exit_time`,`b`.`paid_time` AS `paid_time`,`b`.`fee` AS `fee`,`b`.`real_fee` AS `real_fee`,`b`.`note` AS `note`,`b`.`paid_type` AS `paid_type`,`b`.`entry_balance` AS `entry_balance`,`b`.`exit_balance` AS `exit_balance`,`b`.`settlement_type` AS `settlement_type`,`b`.`disability_mode` AS `disability_mode`,`c`.`customer_id` AS `customer_id` from ((`parking` `b` left join `lane` `a` on(((`a`.`pv` = `b`.`pv`) and (`a`.`garage_code` = `b`.`garage_code`)))) left join `garage` `c` on((`a`.`garage_code` = `c`.`garage_code`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-05  3:22:01
