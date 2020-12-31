# PMS PLUS WEB API

# API URL

http://ec2-54-245-162-118.us-west-2.compute.amazonaws.com:81/api/v1

# 新增交易資料API
新增停車交易資料
### 新增API路徑(PUT)
/real-time-transaction/add_transaction
### 新增參數
| 參數名稱                      | 格式    | 進場必填 |出場必填| 描述                                                                  |
|-------------------------------|---------|----------|--------|-----------------------------------------------------------------------|
| in_or_out                     | string | Y    | Y    | 進離場類別(0:進場、1:離場)                                            |
| parking_type          		| string | Y    | Y   | 臨時車或月租車(0:臨停車、1:月租車)                                    |
| card_id_16                       | string  | Y    | Y    | 票卡卡號(如:票證卡片卡號、停車卡卡號、token ID)(卡內碼mifire)         |
| in_or_out_datetime            | string  | Y    | Y    | 進/出場日期時間 (ex. 2018-01-08 23:59:00)                             |
| pay_datetime                  | string  |      | Y   | 付費時間(ex. ex. 2018-01-08 23:59:00)                                 |
| card_type                     | string |      |    | 卡別(01:ECC,02:愛金,03:KRTC, /遠鑫:05 /99:人工結帳….).                |
| receivable                    | string | Y    | Y    | 應收費用                                                              |
| real_fees                     | string | Y    | Y   | 實際費用                                                              |
| before_pay_balance            | string |      |    | 卡片餘額(扣款前)                                                      |
| is_disability                 | string | Y     | Y    | 是否為身障計費(>0:身障計費規則id,0:否)                                |
| vehicle_identification_number | string  | Y    | Y   | 車牌號碼                                                              |
| device_ip                         | string  | Y    | Y   | device的ip                                                                |
| garage_id                 | string  | Y     | Y   | 場站代碼                                                              |
| customer_id                   | string  | Y     | Y   | 業者代碼                                                              |
| discount_type                 | string |      |    | 0: 無優惠，1: 身障優惠，2: 折扣優惠                                   |
| discount_amount               | string |      |    | 優惠金額                                                              |
| status_number                 | string | Y    | Y    | 狀態碼(交易正常:0 異常:1)                                                                |
| vehicle_type                  | string | Y    | Y   | 車種(汽車:01/機車:02/大客車:03)                                       |
| card_id_appearance            | string | Y    | Y   | 卡片卡號(卡片外碼)                                                                |
| is_autoload                   | string | Y    | Y   | 是否開啟自動加值功能(1:開啟,0:無)                                       |
| autoload_amout                | string  |      |    | 自動加值金額 (default:0)                                                            |
| parking_id                    | string  | Y     | Y   | 進場=""/出場="此車進場資料id"                                                            |
| create_account_id             | string  | Y     | Y   | 新增帳號ＩＤ                                         |
| exit_type_config_detail_id             | string  |      | Y   | 出場設定                                         |
| exit_type_config_detail_remarks        | string  |      |    | 出場設定備註                                         |
### 新增範例

進場參數:
{
  "transaction": {
    "in_or_out": "0",
    "parking_type": "0",
    "card_id_16": "888888",
    "in_or_out_datetime": "2018-04-21 19:10:00",
    "receivable": "100",
    "real_fees": "50",
    "vehicle_identification_number": "KFC-100",
    "pv_ip": "192.168.0.1",
    "garage_id": "1",
    "customer_id": "120",
    "discount_type": "0",
    "discount_amount": "10",
    "status_number": "0",
    "vehicle_type": "01",
    "parking_id" : "",
    "is_disability":"0",
    "is_autoload":"0",
    "create_account_id" : "123",
    "card_id_appearance" : "00000",
    "customer_id" :"22"
  }
}
出場參數:
{
  "transaction": {
    "in_or_out": "1",
    "parking_type": "0",
    "card_id_16": "888888",
    "in_or_out_datetime": "2018-04-22 19:10:00",
    "receivable": "1500",
    "real_fees": "500",
    "vehicle_identification_number": "KFC-100",
    "pv_ip": "192.168.0.1",
    "garage_id": "1",
    "customer_id": "120",
    "discount_type": "0",
    "discount_amount": "10",
    "status_number": "0",
    "vehicle_type": "01",
    "parking_id" : "1",
    "is_disability":"0",
    "is_autoload":"0",
    "create_account_id" : "123",
    "card_id_appearance" : "00000",
    "customer_id" :"22",
    "pay_datetime":"2018-04-22 19:10:00",
    "exit_type_config_detail_id":"1"
  }
}
return:
{
    "data": 7,
    "has_error": false,
    "message": "success"
}

# 查詢交易資料API
查詢停車交易資料

### 查詢API路徑(POST)
/real-time-transaction/get_transaction

### 查詢參數


| 參數名稱                      | 格式   | 必填 | 描述                                               |
|-------------------------------|--------|------|----------------------------------------------------|
| enter_time_to                 | string | N    | 入場時間起始範圍(無入場時間 '0000-00-00 00:00:00') |
| enter_time_from               | string | N    | 入場時間結束範圍(無入場時間 '0000-00-00 00:00:00') |
| exit_time_to                  | string | N    | 出場時間起始範圍(無入場時間 '0000-00-00 00:00:00') |
| exit_time_from                | string | N    | 出場時間結束範圍(無入場時間 '0000-00-00 00:00:00') |
| in_or_out                     | string | Y    | 入場 :0 / 出場 :1                                  |
| garage_id                     | string | Y    | 場站代碼                                 |
| card_id_16                       | string | N    | 票卡內碼(如:票證卡片卡號、停車卡卡號、token ID)    |
| card_id_appearance              | string | N    | 票卡外碼(如:票證卡片卡號、停車卡卡號、token ID)    |
| disability_mode               | string | N    | 身障計費(0: 無優惠，1: 身障優惠，2: 折扣優惠)      |
| exit_type_config_detail_id             | string  | N   | 出場設定                                         |
| vehicle_identification_number | string | N    | 車牌號碼                                           |                                     |

### 查詢範例

入場查詢:
{
    "enter_time_from":"2018-03-10 19:20:00",
    "enter_time_to":"2019-05-30 19:20:00",
    "in_or_out":"0",
    "disability_mode":"0",
    "card_id_16":"888888",
    "vehicle_identification_number":"KFC-100",
    "garage_id":"111111"
}

出場查詢:
{
    "enter_time_from":"2018-03-10 19:20:00",
    "enter_time_to":"2019-05-30 19:20:00",
    "in_or_out":"1",
    "disability_mode":"1",
    "card_id_16":"888888",
    "vehicle_identification_number":"KFC-100",
    "exit_type_config_detail_id":"1",
    "garage_id":"111111"
}

# 刪除交易資料API
刪除停車交易資料

# 刪除API路徑(DELETE)
/real-time-transaction/delete_transaction_by_id/{parking_id}/{garage_id}

### 刪除API路徑return
{
    "data": true,
    "has_error": false,
    "message": "success"
}


# 查詢場站出場管理資訊(GET)
顯示出場管理頁面所需資訊
/exit_settings
取得指定群組下, 所有的尚未設定場站
/exit_settings/garages/{group_name}
取得指定場站資訊
/exit_settings/garage/{garage_id}

# 查詢參數

 exit_config 主表

| 參數名稱                       | 格式     |必填  | 描述                                               |
|-------------------------------|----------|------|----------------------------------------------------|
| exit_config_id                | int      | N    | 流水號 PrimaryKey                                   |
| garage_id                     | int      | Y    | 場站流水號                                          |
| description                   | string   | Y    | 場站設定描述 DEFAULT ''                             |
| is_configured                 | int      | Y    | 場站是否設定過 (0:尚未設定 1:已設定) DEFAULT 0       |
| disabled                      | int      | Y    | 是否在頁面上顯示 (0:顯示 1:隱藏) DEFAULT 0           |
| update_account_id             | int      | N    | 更新帳號                                            |
| update_date                   | Timestmp | N    | 更新時間                                            |

 exit_type_config_detail 子表

| 參數名稱                       | 格式     |必填  | 描述                                                |
|-------------------------------|----------|------|----------------------------------------------------|
| exit_type_config_detail_id    | int      | N    | 流水號 PrimaryKey                                   |
| exit_type                     | string   | Y    | 出場設定類型                                        |
| exit_config_id                | string   | Y    | 對應主表(exit_config)流水號                          |
| exit_type_disabled            | int      | Y    | 是否在頁面上顯示 (0:顯示 1:隱藏) DEFAULT 0           |


### 查詢範例
顯示出場管理頁面所需資訊:
/exit_settings
"groupname": [
            "North",
            "South",
            "East"
],
"garage": [
            {
              "description": "description_something~",
              "exit_config_id": 1,
              "garage_id": 1,
              "garage_name": "s_name1",
              "garage_code": "01",
              "exit_type": [
                    {
                        "exit_type_config_detail_id": 1,
                        "exit_type": "Free",
                        "exit_config_id": 1,
                        "exit_type_disabled": 0
                    },
                    {
                        "exit_type_config_detail_id": 2,
                        "exit_type": "Half Price",
                        "exit_config_id": 1,
                        "exit_type_disabled": 0
                    }
              ]
            },
            {
                "description": "description_something~",
                "exit_config_id": 2,
                "garage_id": 2,
                "garage_name": "s_name2",
                "garage_code": "02",
                "exit_type": [
                    {
                        "exit_type_config_detail_id": 3,
                        "exit_type": "Double Price",
                        "exit_config_id": 2,
                        "exit_type_disabled": 0
                    }
                ]
            } 
]
取得指定群組下, 所有的尚未設定場站
/exit_settings/garages/North
[
  {
      "garage_id": 1,
      "garage_name": "s_name1",
      "garage_code": "01"
  }
]
取得指定場站資訊
/exit_settings/garage/1
{
        "garage": [
            {
                "description": "description_something~",
                "garage_name": "s_name1",
                "garage_code": "01"
            }
        ],
        "exit_type": [
            {
                "exit_type_config_detail_id": 1,
                "exit_type": "Free",
                "exit_config_id": 1,
                "exit_type_disabled": 0
            },
            {
                "exit_type_config_detail_id": 2,
                "exit_type": "Half Price",
                "exit_config_id": 1,
                "exit_type_disabled": 0
            }
        ]
}

# 新增/修改場站出場管理設定(POST)

### 新增範例
儲存單一場站資訊
/exit_settings/garage

{ "exit_type_config_detail" : { 
                               "exit_type_config_detail_id" : [1,2], 
                               "exit_type" : ["free", "aa", "bb"] 
                               },
  "exit_config" : {"description" : "aaaa", "exit_config_id" : 1}
 }
return boolean

# 儲存場站管理設定(PUT)

### 修改範例
初始化場站管理設定
/exit_settings/garage
停用該場站管理資訊
/exit_settings/garage/disable_toggle

/exit_settings/garage
{"exit_config_id": 1}
return bollean

/exit_settings/garage/disable_toggle
{"exit_config_id": 1, "disabled" : 1}
return 修改筆數

#新增發票
新增發票API
新增訂單時，不新增發票欄位，需另外呼叫新增發票API

### 新增發票API路徑(PUT)
/einvoice-number/add_einvoice

### 新增發票參數

| 參數名稱                      | 格式   | 必填 | 描述                                               |
|-----------------------------|--------|------|----------------------------------------------------|
| in_or_out          | String | Y    | 0:進場開立發票/1:出場開立發票                                                      |
| tax_id             | String | Y    | 公司統編                                                                               |
| tax_id_number_buyer       | String |     | 買受人統編                                                                               |
| random_code        | String | Y    | 隨機碼  |
| use_year_month     | String | Y    | 格式:YYYYMM，發票期數(發票兩個月一期，ex:2018年1月、2月開立之發票統一填入"201802") |
| invoice_number     | String | Y    | 發票號碼                                                                           |
| einvoice_print_status| String | Y    | 電子發票使用狀態(1:不印, 0:印,2=存入載具,3=列印發票並打買受人統編)               |
| donate_status      | String | Y    | 捐贈狀態(0:不捐, 1:捐)                                                             |
| sale_print_status  | String | Y    | 銷貨清單列印狀態(0:不印, 1:印)                                                 |
| preserve_code      | String |     | 愛心碼                                                                             |
| einvoice_device_no | String |     | 載具編號                                                                           |
| txn_total_amt     | String | Y    | 交易金額                                                                           |
| invoice_amt         | String | Y    | 發票金額                                                                           |
| txn_date       | String |     | YYYYMMDD                                                                           |
| txn_time      | String |     | HHMMSS                                                                           |
| merchant_id        | String | Y    | 商家代號                                                                           |
| counter_id         | String | Y    | 門市(停車場)代號                                                                   |
| pos_id             | String | Y    | 收銀機號                                                                           |
| batch_number    | String |     | 批號(車道編號)                                   |
| transaction_number    | String |     | 收銀機交易序號                                   |
| business_date    | String |     | 營業日                                   |
| process_status    | String | Y    | 0:匯入, 1:銷售, 2:退貨(作廢), 3:折讓, 4:折讓取消, 5:註銷                                   |
| process_time    | String | Y    | 0000-00-00 00:00:00                                   |
| upload_status    | String | Y    | 0:未上傳, 1:待上傳, 2:已上傳                                  |
| upload_time    | String | Y    | 0000-00-00 00:00:00                                   |
| use_status    | String | Y    | 0:未使用, 1:已送出給PV                                  |
| use_time    | String | Y    | 0000-00-00 00:00:00                                   |
| sales_type    | String | Y    | 0:parking_id, 1:訂單  |
| sales_id    | String | Y    | parking＿id 或訂單id                                  |
| garage_code    | String | Y    | 場站ID |

### 新增發票範例
{
    "in_or_out" :"0",
    "einvoice": {
        "tax_id":"  ZR2334123",
        "random_code":"29d228j",
        "use_year_month":"201804",  
        "invoice_number":"23123",
        "einvoice_print_status":"0",
        "donate_status":"0",
        "sale_print_status":"0", 
        "txn_total_amt":"150", 
        "invoice_amt":"150", 
        "merchant_id":"c32",   
        "counter_id":"system",    
        "pos_id":"c32",     
        "process_status":"1",   
        "process_time":"2018-03-23 03:32:12", 
        "upload_status":"0",    
        "upload_time":"0000-00-00 00:00:00", 
        "use_status":"1",   
        "use_time":"0000-00-00 00:00:00",   
        "sales_type":"0",  
        "sales_id":"12",  
        "garage_code":"10"
    }
}

#更新發票
更新發票狀態API

### 更新發票API路徑(PUT)
/einvoice-number/update_einvoice

### 更新發票參數

| 參數名稱                      | 格式   | 必填 | 描述                                               |
|-----------------------------|--------|------|----------------------------------------------------|
| invoice_number     | String | Y    | 發票號碼      |
| process_status    | String | Y    | 0:匯入, 1:銷售, 2:退貨(作廢), 3:折讓, 4:折讓取消, 5:註銷  |
| process_time    | String | Y    | 0000-00-00 00:00:00                                   |
| use_year_month     | String | Y    | 格式:YYYYMM，發票期數(發票兩個月一期，ex:2018年1月、2月開立之發票統一填入"201802") |
| upload_status    | String | Y    | 0:未上傳, 1:待上傳, 2:已上傳     |
| upload_time    | String | Y    | 0000-00-00 00:00:00                                   |
| use_status    | String | Y    | 0:未使用, 1:已送出給PV                                  |
| use_time    | String | Y    | 0000-00-00 00:00:00                                   |
| sales_id    | String | Y    | parking＿id 或訂單id                                  |
| update_time    | String | Y    | 0000-00-00 00:00:00 |
| garage_code    | String | Y    | 場站ID |
### 更新發票範例
{
    "invoice_number":"23123",
    "process_status":"2",
    "use_year_month":"201804",   
    "process_time":"2018-03-23 03:32:12", 
    "upload_status":"0",    
    "upload_time":"2018-03-23 03:32:12", 
    "use_status":"1",   
    "use_time":"2018-03-23 03:32:12",   
    "sales_type":"0",  
    "sales_id":"12",  
    "update_time":"2018-02-30 10:30:22",  
    "garage_code":"10"
}

### 刪除發票API路徑(DELETE)
/einvoice-number/delete_einvoice/{parking_id}/{in_or_out}


# 新增打卡
打卡紀錄API。

### 新增打卡API路徑(PUT)
/clock-in-and-out/add_clock_record

### 新增打卡參數
  
| 參數名稱           | 格式   | 必填 | 描述                                            |
|-------------------|-------|------|----------------------------------------------------|
| account_id         | String | Y    | 帳號ID                                          |
| garage_id            | String | Y    | 場站ID                                        |
| customer_id        | String | Y    | 業者ID                                          |
| clock_in_time         | String | Y    | 上班打卡時間                                        |
| clock_out_time        | String | Y    | 下班打卡時間                                        |


### 新增打卡範例
{
"account_id":"123",
"garage_id":"123",
"customer_id":"222",
"clock_in_time":"2018-01-09 12:44:33",
"clock_out_time":"2018-01-09 16:44:33"
}


# 結班報表查詢API
用結班序號，查詢班別期間應收、實收、進場車輛總數、出場車輛總數
### 結班報表查詢API(GET)
/real-time-transaction/get_transaction_by_checkout_no/{checkout_no:\d*}/{garage_id:\d*}

### 結班報表查詢API return
{
    "data": [
        {
            "out_count": 2,
            "real_fees_total": 300,
            "receivable_total": 300,
            "in_count": 3
            "data_in_json":""
        }
    ],
    "has_error": false,
    "message": "success"
} 


# 新增結班資料API
新增結班資料，業者使用結班序號在PMS+上查詢
### 新增結班資料API(PUT)
/shift-checkout-controller/add_shift_checkout

### 新增結班資料API參數
| 參數名稱           | 格式   | 必填 | 描述                                            |
|-------------------|-------|------|----------------------------------------------------|
| checkout_no        | String | Y    | 結班序號                                          |
| garage_id            | String | Y    | 場站ID                                        |
| customer_id        | String | Y    | 業者ID                                   |
| clock_in_time        | String | Y    | 班別開始時間                                          |
| clock_out_time            | String | Y    | 班別結束時間                                       |
| checkout_time        | String | Y    | 結班時間                                   |
| checkout_amount        | String | Y    | 結班金額                                          |
| number_of_vehicles            | String | Y    | 出場車輛總數                                       |
| data_in_json        | String | Y    | json                                   |

### 新增結班資料API範例
{
    "checkout_no":"123",
    "garage_id":"1200",
    "customer_id":"1500",
    "clock_in_time":"2018-04-19 13:00:00",
    "clock_out_time":"2018-04-19 16:00:00",
    "checkout_time":"2018-04-19 16:00:00",
    "checkout_amount":"1000",
    "number_of_vehicles":"5",
    "data_in_json":{
        "garage_id":"1200",
        "customer_id":"1500",
        "clock_in_time":"2018-04-19 13:00:00",
        "clock_out_time":"2018-04-19 16:00:00","checkout_time":"2018-04-19 16:00:00",
        "checkout_amount":"1000"
    }
}

### 新增結班資料API return
return 結班條序號
{
    "data": "123",
    "has_error": false,
    "message": "success"
}

# 計費設定檔案和月租清單檔案下載
取得設定檔最後一次更新日期
### 計費設定檔案和月租清單檔案下載API(Get)
/file/update_date/{garage_id}

# 取得使用者帳號密碼
取得特定場站之使用者帳號密碼
### 取得使用者帳號密碼API(Get)
/accounts/{garage_id}