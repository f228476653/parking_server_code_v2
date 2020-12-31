import asyncio
import sqlalchemy as sa
import sqlalchemy.orm as orm
import datetime
from sqlalchemy.types import Enum
from aiomysql.sa import create_engine
from keystore.keystore_status_enum import KeystoreStatusEnum
from keystore.keystore_validation_enum import KeystoreValidationEnum

"""
create tables and models
"""
metadata = sa.MetaData()

SpecialDay = sa.Table(
    'special_day', metadata,
    sa.Column('special_day_id', sa.Integer),
    sa.Column('date', sa.String(20)),
    sa.Column('year', sa.Integer),
    sa.Column('day_type', sa.Integer),
    sa.Column('description', sa.String(50))
)

DayRevenueSumTypeView = sa.Table(
    'day_revenue_sum_type', metadata,
    sa.Column('parking_date', sa.Date),
    sa.Column('total_cnt', sa.Integer),
    sa.Column('total', sa.Integer),
    sa.Column('type', sa.String(2))
)

DayRevenueSumView = sa.Table(
    'day_revenue_sum', metadata,
    sa.Column('parking_date', sa.Date),
    sa.Column('paid_type', sa.String(2)),
    sa.Column('pv_out', sa.String(100)),
    sa.Column('total_cnt', sa.Integer),
    sa.Column('total', sa.Integer)
)

DayRevenueView = sa.Table(
    'day_revenue', metadata,
    sa.Column('parking_date', sa.Date),
    sa.Column('fee', sa.Integer),
    sa.Column('paid_type', sa.String(2)),
    sa.Column('pv_out', sa.String(100)),
    sa.Column('cnt', sa.Integer),
    sa.Column('subtotal', sa.Integer)
)

FeeRule = sa.Table(
    'fee_rule', metadata,
    sa.Column('fee_rule_id', sa.Integer),
    sa.Column('fee_args_name', sa.String(20)),
    sa.Column('car_type', sa.String(20)),
    sa.Column('new_car_hour', sa.Integer),
    sa.Column('period', sa.Integer),
    sa.Column('normal_day', sa.String(200)),
    sa.Column('holiday', sa.String(200)),
    sa.Column('free_time', sa.Integer),
    sa.Column('fee_mode', sa.Integer),
    sa.Column('update_time', sa.DateTime),
    sa.Column('update_user', sa.String(200)),
    sa.Column('garage_id', sa.Integer)
)

FeePara = sa.Table(
    'fee_para', metadata,
    sa.Column('fee_para_id', sa.Integer),
    sa.Column('fee_para_mode', sa.String(20)),
    sa.Column('hour_period_fee1', sa.Integer),
    sa.Column('hour_period_fee1_start', sa.Integer),
    sa.Column('hour_period_fee1_end', sa.Integer),
    sa.Column('hour_period_fee2', sa.Integer),
    sa.Column('hour_period_fee2_start', sa.Integer),
    sa.Column('hour_period_fee2_end', sa.Integer),
    sa.Column('max_fee', sa.Integer),
    sa.Column('max_hour', sa.Integer),
    sa.Column('special_rule', sa.Integer),
    sa.Column('special_fee_start', sa.Integer),
    sa.Column('special_fee_end', sa.Integer),
    sa.Column('special_fee_max', sa.Integer),
    sa.Column('special_fee_hour', sa.Integer),
    sa.Column('monthly_pass', sa.Integer),
    sa.Column('update_time', sa.DateTime),
    sa.Column('update_user', sa.String(200)),
    sa.Column('fee_rule_id', sa.Integer)
)

CustomerMapCardCase = sa.Table(
    'customer_map_card_case', metadata,
    sa.Column('customer_map_card_case_id', sa.Integer),
    sa.Column('device_type', sa.String(20)),
    sa.Column('enable_card_case', sa.Integer),
    sa.Column('customer_id', sa.Integer)
)

CustomerIboxArgs = sa.Table(
    'customer_ibox_args', metadata,
    sa.Column('customer_ibox_args_id', sa.Integer),
    sa.Column('market_code', sa.String(3)),
    sa.Column('cashier_no', sa.String(4)),
    sa.Column('system_id', sa.String(2)),
    sa.Column('comp_id', sa.String(2)),
    sa.Column('machine', sa.String(8)),
    sa.Column('ipass_water_lv_host', sa.String(50)),
    sa.Column('ipass_water_lv_port', sa.Integer),
    sa.Column('socket_ip', sa.String(50)),
    sa.Column('transaction_system_id', sa.String(2)),
    sa.Column('loc_id', sa.String(2)),
    sa.Column('transaction_terminal_no', sa.String(8)),
    sa.Column('tid', sa.String(8)),
    sa.Column('mid', sa.String(16)),
    sa.Column('YHDP_water_lv', sa.String(10)),
    sa.Column('YHDP_water_lv_host', sa.String(50)),
    sa.Column('YHDP_water_lv_port', sa.Integer),
    sa.Column('nii', sa.String(5)),
    sa.Column('host_ip', sa.String(20)),
    sa.Column('host_port', sa.String(20)),
    sa.Column('host_user', sa.String(20)),
    sa.Column('host_pwd', sa.String(20)),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('customer_id', sa.Integer)
)

CustomerPv3Args = sa.Table(
    'customer_pv3_args', metadata,
    sa.Column('customer_pv3_args_id', sa.Integer),
    sa.Column('market_code', sa.String(3)),
    sa.Column('cashier_no', sa.String(4)),
    sa.Column('system_id', sa.String(2)),
    sa.Column('comp_id', sa.String(2)),
    sa.Column('machine', sa.String(8)),
    sa.Column('ipass_water_lv_host', sa.String(50)),
    sa.Column('ipass_water_lv_port', sa.Integer),
    sa.Column('socket_ip', sa.String(50)),
    sa.Column('transaction_system_id', sa.String(2)),
    sa.Column('loc_id', sa.String(2)),
    sa.Column('transaction_terminal_no', sa.String(8)),
    sa.Column('tid', sa.String(8)),
    sa.Column('mid', sa.String(16)),
    sa.Column('YHDP_water_lv', sa.String(10)),
    sa.Column('YHDP_water_lv_host', sa.String(50)),
    sa.Column('YHDP_water_lv_port', sa.Integer),
    sa.Column('nii', sa.Integer),
    sa.Column('client_pv', sa.String(50)),
    sa.Column('time_sync_period', sa.Integer),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('customer_id', sa.Integer)
)

GarageIboxArgs = sa.Table(
    'garage_ibox_args', metadata,
    sa.Column('garage_ibox_args_id', sa.Integer),
    sa.Column('garage_code', sa.String(10)),
    sa.Column('store_no', sa.String(20)),
    sa.Column('eid_store_no', sa.String(20)),
    sa.Column('plid', sa.String(4)),
    sa.Column('printer', sa.Integer),
    sa.Column('tax_id_num', sa.String(20)),
    sa.Column('ntp_server', sa.String(20)),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('garage_id', sa.Integer)
)

GaragePv3Args = sa.Table(
    'garage_pv3_args', metadata,
    sa.Column('garage_pv3_args_id', sa.Integer),
    sa.Column('garage_code', sa.String(10)),
    sa.Column('store_no', sa.String(20)),
    sa.Column('pos_no', sa.String(10)),
    sa.Column('eid_store_no', sa.String(20)),
    sa.Column('plid', sa.String(4)),
    sa.Column('printer', sa.Integer),
    sa.Column('tax_id_num', sa.String(20)),
    sa.Column('ntp_server', sa.String(20)),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('garage_id', sa.Integer)
)

DeviceIboxArgs = sa.Table(
    'device_ibox_args', metadata,
    sa.Column('device_ibox_args_id', sa.Integer),
    sa.Column('device_name', sa.String(20)),
    sa.Column('type', sa.String(20)),
    sa.Column('external_ip', sa.String(20)),
    sa.Column('station_inout', sa.Integer),
    sa.Column('pos_no', sa.Integer),
    sa.Column('slot1', sa.Integer),
    sa.Column('slot2', sa.Integer),
    sa.Column('slot3', sa.Integer),
    sa.Column('slot4', sa.Integer),
    sa.Column('ip', sa.String(200)),
    sa.Column('gateway', sa.String(20)),
    sa.Column('eid_pos_no', sa.String(20)),
    sa.Column('client_pv', sa.String(50)),
    sa.Column('time_sync_period', sa.Integer),
    sa.Column('card_order', sa.String(20)),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('garage_id', sa.Integer)
)

DevicePv3Args = sa.Table(
    'device_pv3_args', metadata,
    sa.Column('device_pv3_args_id', sa.Integer),
    sa.Column('device_name', sa.String(20)),
    sa.Column('external_ip', sa.String(20)),
    sa.Column('station_inout', sa.Integer),
    sa.Column('ECC', sa.Integer),
    sa.Column('iPass', sa.Integer),
    sa.Column('iCash', sa.Integer),
    sa.Column('YHDP', sa.Integer),
    sa.Column('ip', sa.String(200)),
    sa.Column('mac_ip', sa.String(20)),
    sa.Column('eid_pos_no', sa.String(20)),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(200)),
    sa.Column('garage_id', sa.Integer)
)

SystemConfiguration = sa.Table(
    'system_configuration', metadata,
    sa.Column('key', sa.String(50), nullable = False),
    sa.Column('value', sa.String(50), nullable = False),
    sa.Column('description', sa.String(100), nullable = False),
    sa.Column('config_group_name', sa.String(50), nullable = False)
)

DevicePV = sa.Table(
    'device_pv', metadata,
    sa.Column('device_pv_id', sa.Integer, primary_key = True),
    sa.Column('garage_id', sa.Integer, nullable = False),
    sa.Column('pv', sa.String(128), nullable = False),
    sa.Column('type', sa.String(1), nullable = False),
    sa.Column('pricing_scheme', sa.Integer, nullable = False),
    sa.Column('pv_ip', sa.String(64), nullable = False),
    sa.Column('pv_netmask', sa.String(64), nullable = False),
    sa.Column('pv_gateway', sa.String(64), nullable = False),
    sa.Column('pms_ip', sa.String(64), nullable = False),
    sa.Column('pms_port', sa.Integer, nullable = False),
    sa.Column('ecc_ip', sa.String(64), nullable = False),
    sa.Column('ecc_port', sa.Integer, nullable = False),
    sa.Column('in_out', sa.Integer, nullable = False),
    sa.Column('aisle', sa.String(10), nullable = False),
    sa.Column('auto_print_invoice', sa.Integer, nullable = False),
    sa.Column('pv_cutoff', sa.String(4), nullable = False),
    sa.Column('MEntryB', sa.String(10), nullable = False),
    sa.Column('MExitD', sa.Integer, nullable = False),
    sa.Column('pv_version', sa.String(20), nullable = False),
    sa.Column('last_response_time', sa.DateTime, nullable = False, default = '0000-00-00 00:00:00'),
    sa.Column('response_type', sa.String(4), nullable = False, default = '00'),
    sa.Column('invoice_printer_status', sa.String(2), nullable = False, default = '00'),
    sa.Column('pricing_scheme_disability', sa.Integer, nullable = False, default = '0'),
    sa.Column('pv_response_confirm', sa.Integer, nullable = False, default = '0'),
    sa.Column('etag_flag', sa.Integer, nullable = False, default = '0'),
    sa.Column('costrule_using_para', sa.Integer, nullable = False, default = '0'),
    sa.Column('lane_costrule_mode', sa.Integer, nullable = False, default = '0'),
    sa.Column('gate_control_mode', sa.Integer, nullable = False, default = '0'),
    sa.Column('lpr_lane', sa.String(4), nullable = False, default = '99'),
    sa.Column('update_date', sa.DateTime, nullable = False, default = datetime.datetime.utcnow),
    sa.Column('update_account_id', sa.Integer, nullable = False, default = '99')
)

ExitConfig = sa.Table(
    'exit_config', metadata,
    sa.Column('exit_config_id', sa.Integer, primary_key = True),
    sa.Column('garage_id', sa.Integer, unique = False,nullable = False),
    sa.Column('description', sa.String(100), unique = False, nullable = True),
    sa.Column('is_configured', sa.Integer, unique = False, nullable = True),
    sa.Column('disabled', sa.Integer, unique = False, nullable = True),
    sa.Column('update_account_id', sa.Integer, unique=True, nullable = True),
    sa.Column('update_date', sa.DateTime, default = datetime.datetime.utcnow)
)

ExitTypeConfigDetail = sa.Table(
    'exit_type_config_detail', metadata,
    sa.Column('exit_type_config_detail_id', sa.Integer, primary_key = True),
    sa.Column('exit_type', sa.String(50), unique = False, nullable = True),
    sa.Column('exit_config_id', sa.Integer, nullable=False),
    sa.Column('exit_type_disabled', sa.Integer, nullable=False),
    sa.Column('create_time', sa.DateTime, default = datetime.datetime.utcnow),
    sa.Column('update_time', sa.DateTime, default = datetime.datetime.utcnow)
)

Customer = sa.Table(
    'customer', metadata,
    sa.Column('customer_id', sa.Integer, primary_key=True),
    sa.Column('customer_code', sa.String(150), unique=True,nullable=False),
    sa.Column('company_name', sa.String(255), unique=False,nullable=False),
    sa.Column('company_english_name', sa.String(255), unique=False,nullable=False),
    sa.Column('company_union_number', sa.String(15), unique=False,nullable=False),
    sa.Column('contact_username', sa.String(150), unique=False,nullable=False),
    sa.Column('contact_datetime', sa.String(10), unique=False,nullable=False),
    sa.Column('mobile', sa.String(30), unique=True, nullable=True),
    sa.Column('fax', sa.String(30), unique=True, nullable=True),
    sa.Column('phone_number1', sa.String(30), unique=True, nullable=True),
    sa.Column('phone_number2', sa.String(30), unique=True, nullable=True),
    sa.Column('email',sa.String(255), unique=True,nullable=True),
    sa.Column('customer_status',sa.Integer, unique=False,nullable=True),
    sa.Column('note',sa.String(255), unique=False,nullable=True),
    sa.Column('contact_availible_datetime',sa.String(255), unique=False,nullable=True),
    sa.Column('company_address',sa.String(255), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)


Keystore = sa.Table(
    'keystore', metadata,
    sa.Column('keystore_id', sa.Integer, primary_key=True),
    sa.Column('customer_id', sa.String(150), unique=True,nullable=False),
    sa.Column('key_version', sa.String(255), unique=False,nullable=False),
    sa.Column('key_type', sa.String(150), unique=False,nullable=False),
    sa.Column('fixed_account_total', sa.Integer, unique=True, nullable=False,default=1),
    sa.Column('dynamic_account_total', sa.String(30), unique=True, nullable=False,default=1),
    sa.Column('key_manager_email', sa.String(255), unique=True, nullable=False),
    sa.Column('service_type', sa.String(30), unique=True, nullable=False),
    sa.Column('start_date', sa.DateTime, nullable=False,default=datetime.datetime.utcnow),
    sa.Column('end_date', sa.DateTime, nullable=False,default=datetime.datetime.utcnow),
    sa.Column('note',sa.String(255), unique=False,nullable=True),
    sa.Column('key_status',Enum(KeystoreStatusEnum), unique=False,nullable=True),
    sa.Column('key_validation_status',Enum(KeystoreValidationEnum), unique=False,nullable=True),
    sa.Column('key_value',sa.String(4000), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

LicenseInfo = sa.Table(
    'licenseinfo', metadata,
    sa.Column('license_info_id', sa.Integer, primary_key=True),
    sa.Column('requested_keystore', sa.String(150), unique=False,nullable=True),
    sa.Column('applied_keystore', sa.String(150), unique=False,nullable=True),
    sa.Column('customer_id', sa.String(150), unique=True,nullable=False),
    sa.Column('key_version', sa.String(255), unique=False,nullable=False),
    sa.Column('key_type', sa.String(150), unique=False,nullable=False),
    sa.Column('fixed_account_total', sa.Integer, unique=True, nullable=False,default=1),
    sa.Column('dyanmic_account_total', sa.String(30), unique=True, nullable=False,default=1),
    sa.Column('key_manager_email', sa.String(255), unique=True, nullable=False),
    sa.Column('service_type', sa.String(30), unique=True, nullable=False),
    sa.Column('start_date', sa.DateTime, nullable=False,default=datetime.datetime.utcnow),
    sa.Column('end_date', sa.DateTime, nullable=False,default=datetime.datetime.utcnow),
    sa.Column('note',sa.String(255), unique=False,nullable=True),
    sa.Column('key_status',Enum(KeystoreStatusEnum), unique=False,nullable=True),
    sa.Column('key_string',sa.String(2000), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Garage = sa.Table(
    'garage', metadata,
    sa.Column('garage_code', sa.String(10), unique=True,nullable=False),
    sa.Column('garage_name', sa.String(50), unique=False,nullable=True),
    sa.Column('customer_id', sa.Integer, unique=False,nullable=True),
    sa.Column('city_name', sa.String(50), unique=False,nullable=True),
    sa.Column('city_code', sa.String(3), unique=False,nullable=True),
    sa.Column('district', sa.String(10), unique=False,nullable=True),
    sa.Column('district_code', sa.String(3), unique=False,nullable=True),
    sa.Column('address1', sa.String(255), unique=False,nullable=True),
    sa.Column('address2', sa.String(255), unique=False,nullable=True),
    sa.Column('total_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_priority_pragnant_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_priority_pragnant_capacity', sa.Integer,nullable=True),
    sa.Column('sedan_priority_disability_capacity', sa.Integer,nullable=True),
    sa.Column('motocycle_priority_disability_capacity', sa.Integer,nullable=True),
    sa.Column('garage_lat',sa.String(50),nullable=True),
    sa.Column('garage_lng',sa.String(50),nullable=True),
    sa.Column('caculation_time_base_unit', sa.Integer,nullable=True),
    sa.Column('charge_infomation',sa.String(1000),nullable=True),
    sa.Column('supplementary_details',sa.String(1000),nullable=True),
    sa.Column('business_hour_begin',sa.String(5) ,nullable=True),
    sa.Column('business_hour_end',sa.String(5),nullable=True),
    sa.Column('number_of_entrance',sa.Integer,nullable=True),
    sa.Column('number_of_exit',sa.Integer,nullable=True),
    sa.Column('number_of_driveway_in',sa.Integer,nullable=True),
    sa.Column('number_of_driveway_out',sa.Integer,nullable=True),
    sa.Column('management_type',sa.Integer,nullable=True),
    sa.Column('garage_type',sa.Integer,nullable=True),
    sa.Column('lot_type',sa.Integer,nullable=True),
    sa.Column('establish_status',sa.Integer,nullable=True),
    sa.Column('max_clearance',sa.String(5),nullable=True),
    sa.Column('on_site_liaison',sa.String(20),nullable=True),
    sa.Column('on_site_phone',sa.String(20),nullable=True),
    sa.Column('on_site_email',sa.String(20),nullable=True),
    sa.Column('on_site_cell_phone',sa.String(20),nullable=True),
    sa.Column('customer_garage_id',sa.String(20),nullable=True),
    sa.Column('current_capacity_sedan',sa.Integer,nullable=True),
    sa.Column('current_capacity_suv',sa.Integer,nullable=True),
    sa.Column('current_capacity_bicycle',sa.Integer,nullable=True),
    sa.Column('current_capacity_motocycle',sa.Integer,nullable=True),
    sa.Column('current_capacity_truck',sa.Integer,nullable=True),
    sa.Column('current_capacity_bus',sa.Integer,nullable=True),
    sa.Column('current_capacity_total',sa.Integer,nullable=True),
    sa.Column('gov_id',sa.String(30), unique=False,nullable=True),
    sa.Column('current_capacity_update_account_id',sa.Integer,nullable=True),
    sa.Column('current_capacity_updatetime',sa.DateTime,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer),
    sa.Column('garage_id', sa.Integer, primary_key=True)
    ,mysql_charset='utf8'
)

GarageGroup = sa.Table(
    'garage_group', metadata,
    sa.Column('garage_group_id', sa.Integer, primary_key=True),
    sa.Column('garage_group_name', sa.String(255), unique=True,nullable=False),
    sa.Column('customer_id', sa.String(50), unique=True,nullable=False),
    sa.Column('parent_id',sa.Integer, default = 0),
    sa.Column('description', sa.String(150), unique=False,nullable=True),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
    ,mysql_charset='utf8'
)

Map_Garage_To_Garage_Group = sa.Table(
    'map_garage_to_garage_group', metadata,
    sa.Column('garage_id', sa.Integer, unique=True,nullable=False),
    sa.Column('garage_group_id', sa.Integer, unique=True, nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Map_Garage_Group_To_Account = sa.Table(
    'map_garage_group_to_account', metadata,
    sa.Column('garage_group_id', sa.Integer, unique=True,nullable=False),
    sa.Column('account_id', sa.Integer, unique=True, nullable=False)
)

Map_Garage_To_Account = sa.Table(
    'map_garage_to_account', metadata,
    sa.Column('garage_id', sa.Integer, unique=True,nullable=False),
    sa.Column('account_id', sa.Integer, unique=True, nullable=False)
)

Account = sa.Table(
    'account', metadata,
    sa.Column('account_id', sa.Integer, primary_key=True),
    sa.Column('account', sa.String(255), unique=True,nullable=False),
    sa.Column('customer_id',sa.String(50),nullable=True),
    sa.Column('password', sa.String(1000), unique=False,nullable=False),
    sa.Column('user_first_name', sa.String(255), unique=True, nullable=True),
    sa.Column('user_middle_name', sa.String(255), unique=True, nullable=True),
    sa.Column('user_last_name', sa.String(255), unique=True, nullable=True),
    sa.Column('email',sa.String(255), unique=True,nullable=True),
    sa.Column('mobile',sa.String(255), unique=True,nullable=True),
    sa.Column('role_id',sa.Integer, sa.ForeignKey('role.role_id'), unique=False,nullable=False),
    sa.Column('is_superuser', sa.Boolean(), default=False, nullable=False),
    sa.Column('is_customer_root', sa.Boolean(), default=False, nullable=False),
    sa.Column('create_date', sa.TIMESTAMP, default=datetime.datetime.timestamp),
    sa.Column('modified_date', sa.TIMESTAMP, default= datetime.datetime.timestamp),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)


Permission = sa.Table(
    'permission', metadata,
    sa.Column('permission_id', sa.Integer, primary_key=True),
     sa.Column('name', sa.String(255), unique=True,nullable=False),
    sa.Column('description', sa.String(255), unique=False, nullable=False),
    sa.Column('permission_type', sa.String(255), unique=False, nullable=False),
    sa.Column('parent_id',sa.Integer,unique=False,nullable=True),
    sa.Column('enable',sa.Integer,unique=False,nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer),
    sa.Column('modified_account_id',sa.Integer)
)
 
Role = sa.Table(
    'role', metadata,
    sa.Column('role_id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(255), unique=True,nullable=False),
    sa.Column('description', sa.String(255), unique=True, nullable=False),
    sa.Column('role_type', sa.String(255), unique=True, nullable=False),
    sa.Column('is_system_role', sa.Integer, unique=False,nullable=False,default=0),
    sa.Column('customer_id', sa.Integer),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Map_Role_Permission = sa.Table(
    'map_role_permission', metadata,
    sa.Column('role_id', sa.Integer, unique=True,nullable=False),
    sa.Column('permission_id', sa.Integer, unique=True, nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Event = sa.Table(
    'event', metadata,
    sa.Column('event_id', sa.Integer, unique=True,nullable=False),
    sa.Column('SystemEventType', sa.Integer, unique=False,nullable=False),
    sa.Column('event_subtype', sa.Integer, unique=False,nullable=False),
    sa.Column('description', sa.String(255), unique=False, nullable=False)
)

SystemLog = sa.Table(
    'system_log', metadata,
    sa.Column('system_log_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('event_id', sa.Integer, unique=False,nullable=False),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('event_message', sa.String(2000), unique=False, nullable=False),
    sa.Column('query_string', sa.String(255), unique=False, nullable=True),
    sa.Column('field_1', sa.String(255), unique=False, nullable=False)
)

EntryGate = sa.Table(
    'entry_gate', metadata,
    sa.Column('entry_gate_id', sa.Integer, primary_key=True),
    sa.Column('garage_id', sa.Integer),
    sa.Column('customer_id', sa.Integer),
    sa.Column('entry_gate_sn', sa.Integer, unique=False,nullable=False),
    sa.Column('direction', sa.Integer, unique=False, nullable=False),
    sa.Column('has_e_envoicing', sa.Integer, unique=False, nullable=False),
    sa.Column('description', sa.String(1000), unique=False, nullable=False),
    sa.Column('create_date', sa.DateTime, default=datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer, unique=False,nullable=False),
    sa.Column('modified_account_id',sa.Integer)
)

Trx_Data = sa.Table(
    'trx_data', metadata,
    sa.Column('import_date', sa.DateTime,nullable=True),
    sa.Column('file_name', sa.String(54), unique=True,nullable=False),
    sa.Column('trx_date', sa.String(8), unique=True, nullable=False),
    sa.Column('trx_time', sa.String(6), unique=True, nullable=False),
    sa.Column('card_no', sa.String(50), unique=True, nullable=False),
    sa.Column('txn_no', sa.String(6), unique=True, nullable=False),
    sa.Column('trx_amt',sa.Integer),
    sa.Column('device_id', sa.String(20), unique=False, nullable=True),
    sa.Column('trx_type', sa.String(2), unique=False, nullable=True),
    sa.Column('trx_sub_type', sa.String(2), unique=False, nullable=True),
    sa.Column('el_value', sa.Integer, unique=False, nullable=True),
    sa.Column('cal_date', sa.String(8), unique=False, nullable=True),
    sa.Column('cal_status', sa.String(2), unique=False, nullable=True),
    sa.Column('dept_id', sa.String(10), unique=False, nullable=True),
    sa.Column('unit_id', sa.String(2), unique=False, nullable=True),
    sa.Column('cal_err_code', sa.String(10), unique=False, nullable=True),
    sa.Column('update_date', sa.DateTime, unique=False, nullable=True),
    sa.Column('source_filename', sa.String(100), unique=False, nullable=True),
    sa.Column('garage_code', sa.String(20), unique=False, nullable=True),
    sa.Column('csv_file_date', sa.String(20), unique=False, nullable=True),
    sa.Column('trx_data_id', sa.Integer, primary_key=True),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('upload_zip_name', sa.String(50), unique=False, nullable=True),
    sa.Column('feedback_file_name', sa.String(50), unique=False, nullable=True)
)

Parking = sa.Table(
    'parking', metadata,
    sa.Column('id', sa.Integer),
    sa.Column('pv', sa.String(32), unique=True,nullable=False),
    sa.Column('pv_out', sa.String(32), unique=True, nullable=False),
    sa.Column('card_id', sa.String(32), unique=True, nullable=False),
    sa.Column('card_id16', sa.String(32), unique=True, nullable=False),
    sa.Column('enter_time', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('exit_time', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('paid_time', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('duration', sa.Integer, default=0),
    sa.Column('fee', sa.Integer, default=0),
    sa.Column('real_fee', sa.Integer, default=0),
    sa.Column('note', sa.String(5000), nullable=False),
    sa.Column('paid_type', sa.String(2), nullable=True,default='00'),
    sa.Column('entry_balance', sa.Integer, default=0),
    sa.Column('exit_balance', sa.Integer, default=0),
    sa.Column('settlement_type', sa.Integer, default=0),
    sa.Column('txn_datetime', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('txn_amt', sa.Integer, default=0),
    sa.Column('disability_mode', sa.Integer, default=0),
    sa.Column('card_autoload_flag', sa.Integer, default=0),
    sa.Column('entry_mode', sa.Integer, default=1),    
    sa.Column('last_source_filename', sa.String(100), unique=False, nullable=True),
    sa.Column('garage_code', sa.String(20), unique=False, nullable=True),
    sa.Column('last_csv_file_date', sa.String(20), unique=False, nullable=True),
    sa.Column('parking_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('modified_date', sa.DateTime),
    sa.Column('vehicle_identification_number', sa.String(10), default= '000-0000'),
    sa.Column('vehicle_type', sa.Integer),
    sa.Column('enter_account_id', sa.Integer),
    sa.Column('exit_account_id', sa.Integer),
    sa.Column('einvoice', sa.String(20)),
    sa.Column('einvoice_print_status', sa.Integer),
    sa.Column('record_status' ,sa.Integer),
    sa.Column('garage_id' ,sa.Integer)
)

TicketProvider = sa.Table(
    'ticket_provider', metadata,
    sa.Column('ticket_provider_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('company_name', sa.String(32), unique=True,nullable=False),
    sa.Column('type_id', sa.String(32), unique=True, nullable=False),
    sa.Column('ticket_provider_code', sa.String(32), unique=True, nullable=False),
    sa.Column('provider_transaction_code', sa.String(32), unique=True, nullable=False),
    sa.Column('provider_system_code', sa.String(32), unique=True, nullable=False),
    sa.Column('provider_transfer_code', sa.String(32), unique=True, nullable=False),
    sa.Column('modified_account_id', sa.Integer, default=1),
    sa.Column('modified_date', sa.DateTime)
    )

Driveway = sa.Table(
    'driveway', metadata,
    sa.Column('acer_id', sa.String(5), unique=True,nullable=False),
    sa.Column('pv_name', sa.String(128),nullable=False),
    sa.Column('type', sa.String(64),nullable=False),
    sa.Column('charge_rule', sa.String(64),nullable=False),
    sa.Column('pv_ip', sa.String(64),nullable=False),
    sa.Column('pv_netmask', sa.String(64),nullable=False),
    sa.Column('pv_gateway', sa.String(64)),
    sa.Column('pms_plus_ip', sa.String(64),nullable=False),
    sa.Column('pms_plus_port', sa.Integer,nullable=False),
    sa.Column('direction', sa.Integer,nullable=False),
    sa.Column('aisle', sa.String(10),nullable=False),
    sa.Column('is_invoice_printing_enabled', sa.Integer,nullable=False),
    sa.Column('pv_turn_off_time', sa.String(4),nullable=False),
    sa.Column('minimun_entry_balance', sa.String(10),nullable=False),
    sa.Column('maximun_exit_buffer_minutes', sa.Integer,nullable=False),
    sa.Column('pv_version', sa.String(20),nullable=False),
    sa.Column('pv_last_response_time', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('pv_response_type', sa.String(4),default='00',nullable=False),
    sa.Column('pv_response_confirm', sa.Integer,default=0,nullable=False),
    sa.Column('invoice_printer_status', sa.String(2),default='00',nullable=False),
    sa.Column('disability_charge_rule', sa.Integer,default=0,nullable=False),
    sa.Column('is_etag_drvieway', sa.Integer,default=0,nullable=False),
    sa.Column('is_charge_params_enabled',sa.Integer,default=0,nullable=False),
    sa.Column('driveway_charge_mode',sa.Integer,default=0,nullable=False),
    sa.Column('gate_control_mode',sa.Integer,default=0,nullable=False),
    sa.Column('car_recognition_driveway_code', sa.String(4),default='99',nullable=False),
    sa.Column('driveway_id', sa.Integer,primary_key=True)
)

Lane = sa.Table(
    'lane', metadata,
    sa.Column('garage_lane_id', sa.Integer, unique=False,nullable=False),
    sa.Column('pv', sa.String(128),nullable=False),
    sa.Column('type', sa.String(1),nullable=False),
    sa.Column('pricing_scheme', sa.Integer,nullable=False),
    sa.Column('pv_ip', sa.String(64),nullable=False),
    sa.Column('pv_netmask', sa.String(64),nullable=False),
    sa.Column('pv_gateway', sa.String(64)),
    sa.Column('pms_ip', sa.String(64),nullable=False),
    sa.Column('pms_port', sa.Integer,nullable=False),
    sa.Column('ecc_ip', sa.String(64),nullable=False),
    sa.Column('ecc_port', sa.Integer,nullable=False),
    sa.Column('in_out', sa.Integer,nullable=False),
    sa.Column('aisle', sa.String(10),nullable=False),
    sa.Column('invoice', sa.Integer,nullable=False),
    sa.Column('cps_ip', sa.String(64)),
    sa.Column('pv_cutoff', sa.String(4),nullable=False),
    sa.Column('MEntryB', sa.String(10),nullable=False),
    sa.Column('MExitD', sa.Integer,nullable=False),
    sa.Column('pv_version', sa.String(20),nullable=False),
    sa.Column('last_response_time', sa.DateTime, nullable=False,default= '0000-00-00 00:00:00'),
    sa.Column('response_type', sa.String(4),default='00',nullable=False),
    sa.Column('invoice_printer_status', sa.String(2),default='00',nullable=False),
    sa.Column('pricing_scheme_disability', sa.Integer,default=0,nullable=False),
    sa.Column('pv_response_confirm', sa.Integer,default=0,nullable=False),
    sa.Column('etag_flag', sa.Integer,default=0,nullable=False),
    sa.Column('costrule_using_para',sa.Integer,default=0,nullable=False),
    sa.Column('lane_costrule_mode',sa.Integer,default=0,nullable=False),
    sa.Column('gate_control_mode',sa.Integer,default=0,nullable=False),
    sa.Column('lpr_lane', sa.String(4),default='99',nullable=False),
    sa.Column('source_filename', sa.String(100), unique=False, nullable=True),
    sa.Column('garage_code', sa.String(20), unique=False, nullable=True),
    sa.Column('csv_file_date', sa.String(20), unique=False, nullable=True),
    sa.Column('garage_id', sa.Integer),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('lane_id', sa.Integer,primary_key=True)
)

SystemConfig = sa.Table(
    'system_config', metadata,
    sa.Column('report_title', sa.String(60), unique=True,nullable=False),
    sa.Column('is_usb_mode_active', sa.Integer, default=0),
    sa.Column('usb_version_id', sa.String(4), unique=True,nullable=False),
    sa.Column('pv_voice_value', sa.Integer,default=0),
    sa.Column('entry_balance_warning', sa.Integer,default=0),
    sa.Column('is_commutation_ticket_module_active', sa.Integer,default=0),
    sa.Column('commutation_ticket_sales_type', sa.Integer,default=0),
    sa.Column('is_transfer_module_active', sa.Integer,default=0),
    sa.Column('is_e_invoice_mode', sa.Integer,default=0),
    sa.Column('e_invoice_request_minimum', sa.Integer,default=0),
    sa.Column('is_java_server_mode', sa.Integer,default=0),
    sa.Column('pv_alert_interval', sa.Integer,default=0),
    sa.Column('monitor_response_time', sa.Integer,default=0),
    sa.Column('is_calculator_parking_data', sa.Integer,default=0),
    sa.Column('is_check_accounting_and_email_notify', sa.Integer,default=0),
    sa.Column('is_support_multi_language', sa.Integer,default=0),
    sa.Column('is_customize_disability_column_name', sa.Integer,default=0),
    sa.Column('is_invoice_record_number_mode', sa.Integer,default=0),
    sa.Column('invoice_paperroll_usable_number', sa.Integer,default=0),
    sa.Column('invoice_alert_usable_number', sa.Integer,default=0),
    sa.Column('is_commuter_ticket_check_entry_balance', sa.Integer,default=0),
    sa.Column('is_fee_caculation_by_config', sa.Integer,default=0),
    sa.Column('is_human_pay_and_confirm_fix', sa.Integer,default=0),
    sa.Column('is_auto_add_value_card_check_entry_balance', sa.Integer,default=0),
    sa.Column('e_invoice_service_provider', sa.Integer,default=0),
    sa.Column('is_support_gate_control', sa.Integer,default=0),
    sa.Column('acer_id',sa.String(10)),
    sa.Column('config_name', sa.String(60), unique=True,nullable=False),
    sa.Column('csv_file_date',sa.String(10)),
    sa.Column('modified_account_id', sa.Integer),
    sa.Column('modified_date', sa.DateTime),
    sa.Column('system_config_id', sa.Integer, unique=True,nullable=False,primary_key=True)
)

Map_Garage_To_System_Config = sa.Table(
    'map_garage_to_system_config', metadata,
    sa.Column('map_garage_to_system_config_id', sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('garage_id', sa.String(60), unique=True,nullable=False),
    sa.Column('system_config_id', sa.Integer, default=0),
    sa.Column('modified_account_id', sa.Integer),
    sa.Column('modified_date', sa.DateTime)
)

Real_Time_Transaction_Data = sa.Table(
    'real_time_transaction_data', metadata,
    sa.Column('in_or_out' ,sa.Integer, nullable=False),
    sa.Column('parking_type' , sa.Integer ,nullable=False ,default=0),
    sa.Column('card_id_16' , sa.String(30) ,nullable=False),
    sa.Column('in_or_out_datetime' , sa.DateTime ,nullable=False),
    sa.Column('pay_datetime' , sa.DateTime),
    sa.Column('card_type' , sa.Integer),
    sa.Column('receivable', sa.Integer),
    sa.Column('real_fees', sa.Integer),
    sa.Column('before_pay_balance' , sa.Integer),
    sa.Column('is_disability' , sa.Integer, default=0),
    sa.Column('vehicle_identification_number' , sa.String(10), nullable=False),
    sa.Column('device_ip' , sa.String(15) , nullable=False),
    sa.Column('garage_id' , sa.Integer),
    sa.Column('customer_id' , sa.Integer),
    sa.Column('discount_type' , sa.Integer , default=0),
    sa.Column('discount_amount', sa.Integer),
    sa.Column('status_number' , sa.Integer , nullable=False),
    sa.Column('vehicle_type' , sa.Integer , nullable=False),
    sa.Column('einvoice' , sa.String(15)),
    sa.Column('einvoice_print_status' , sa.Integer),
    sa.Column('tax_id_number' , sa.String(15)),
    sa.Column('tax_id_number_buyer' , sa.String(15)),
    sa.Column('card_id_appearance' , sa.String(30)),
    sa.Column('is_autoload' , sa.Integer),
    sa.Column('autoload_amout' , sa.Integer),
    sa.Column('error_message' , sa.String(500)),
    sa.Column('create_account_id',sa.Integer),
    sa.Column('create_date',sa.DateTime),
    sa.Column('parking_id', sa.Integer),
    sa.Column('real_time_transaction_data_id' , sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('exit_type_config_detail_id',  sa.Integer, nullable=True),
    sa.Column('exit_type_config_detail_remarks',  sa.String(50), nullable= True),
    sa.Column('record_status' ,sa.Integer),
    sa.Column('ibox_no', sa.Integer, nullable= True),
    sa.Column('device_id', sa.Integer, nullable= True),
    sa.Column('device_type', sa.Integer, nullable= True)
)


Invoice_Number_Data = sa.Table(
    'invoice_number_data', metadata,
    sa.Column('id' , sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('tax_id' ,sa.Integer, nullable=False),
    sa.Column('use_year_month' , sa.String(10) ,nullable=False),
    sa.Column('invoice_number' , sa.String(10) ,nullable=False),
    sa.Column('print_status' , sa.Integer),
    sa.Column('donate_status', sa.Integer),
    sa.Column('preserve_code', sa.String(15)),
    sa.Column('einvoice_device_no' , sa.String(15)),
    sa.Column('total_amt' , sa.Integer),
    sa.Column('invoice_amt' , sa.Integer),
    sa.Column('merchant_id' , sa.String(15)),
    sa.Column('counter_id' , sa.String(15)),
    sa.Column('pos_id' , sa.String(15)),
    sa.Column('invoice_status' , sa.Integer),
    sa.Column('upload_status' , sa.Integer),
    sa.Column('parking_id' , sa.Integer),
    sa.Column('random_code' , sa.String(15)),
    sa.Column('transaction_number' , sa.String(15)),
    sa.Column('transaction_date',sa.DateTime),
    sa.Column('create_account_id',sa.Integer),
    sa.Column('create_date',sa.DateTime)
)


Clock_Time_Card = sa.Table(
    'clock_time_card', metadata,
    sa.Column('id' , sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('account_id', sa.Integer, nullable=False),
    sa.Column('garage_id',sa.Integer, nullable=True),
    sa.Column('customer_id',sa.String(50), nullable=True),
    sa.Column('clock_in_time',sa.DateTime, nullable=True),
    sa.Column('clock_out_time',sa.DateTime, nullable=True),
    sa.Column('create_date', sa.DateTime),
    sa.Column('create_account_id',sa.Integer , nullable=False)
)

Einvoice_Number_Data = sa.Table(
    'e_invoice_number_data', metadata,
    sa.Column('no', sa.Integer , nullable=False),
    sa.Column('tax_id', sa.String(10) ,nullable=False),
    sa.Column('tax_id_buyer', sa.String(10)),
    sa.Column('random_code' ,sa.String(4) ,nullable=False),
    sa.Column('use_year_month' ,sa.String(6) ,nullable=False),
    sa.Column('invoice_number' ,sa.String(20) ,nullable=False),
    sa.Column('einvoice_print_status' ,sa.Integer , nullable=False),
    sa.Column('donate_status' ,sa.Integer , nullable=False),
    sa.Column('sale_print_status' ,sa.Integer , nullable=False),
    sa.Column('preserve_code', sa.String(20)),
    sa.Column('einvoice_device_no', sa.String(20)),
    sa.Column('txn_total_amt' ,sa.Integer , nullable=False),
    sa.Column('invoice_amt' ,sa.Integer , nullable=False),
    sa.Column('txn_date', sa.String(8)),
    sa.Column('txn_time',  sa.String(6)),
    sa.Column('merchant_id', sa.String(20) , nullable=False),
    sa.Column('counter_id', sa.String(20) , nullable=False),
    sa.Column('pos_id', sa.String(20) , nullable=False),
    sa.Column('batch_number', sa.String(6)),
    sa.Column('transaction_number', sa.String(6)),
    sa.Column('business_date', sa.String(8)),
    sa.Column('process_status', sa.Integer , nullable=False),
    sa.Column('process_time', sa.DateTime, nullable=False),
    sa.Column('upload_status', sa.Integer , nullable=False),
    sa.Column('upload_time', sa.DateTime, nullable=False),
    sa.Column('use_status', sa.Integer , nullable=False),
    sa.Column('use_time', sa.DateTime, nullable=False),
    sa.Column('sales_type', sa.Integer , nullable=False),
    sa.Column('sales_id', sa.Integer , nullable=False),
    sa.Column('update_time', sa.DateTime , nullable=False),
    sa.Column('update_user', sa.String(100), nullable=False),
    sa.Column('source_filename', sa.String(100), unique=False, nullable=True),
    sa.Column('garage_code', sa.String(20), unique=False, nullable=True),
    sa.Column('csv_file_date', sa.String(20), unique=False, nullable=True),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('garage_id', sa.Integer , nullable=False),
    sa.Column('no' , sa.Integer, unique=True,nullable=False,primary_key=True)
)

Parking_In_Out_Record= sa.Table(
    'parking_in_out_record', metadata,
    sa.Column('parking_in_out_record_id' , sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('state', sa.String(2), nullable=False),
    sa.Column('trans_type', sa.String(2), nullable=False),
    sa.Column('card_id',sa.String(32), nullable=True),
    sa.Column('entry_time',sa.DateTime, nullable=True),
    sa.Column('exit_time',sa.DateTime, nullable=True),
    sa.Column('car_number', sa.String(16), nullable=True),
    sa.Column('parking_id',  sa.Integer, nullable=True),
    sa.Column('paid_type',sa.String(2), nullable=True),
    sa.Column('update_time',sa.DateTime, nullable=True),
    sa.Column('update_user',sa.String(100) , nullable=False),
    sa.Column('source_filename', sa.String(100), unique=False, nullable=True),
    sa.Column('garage_code', sa.String(20), unique=False, nullable=True),
    sa.Column('csv_file_date', sa.String(20), unique=False, nullable=True),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('no' , sa.Integer, unique=True,nullable=False,primary_key=True)
)

Shift_Checkout= sa.Table(
    'shift_checkout', metadata,
    sa.Column('shift_checkout_id' , sa.Integer, unique=True,nullable=False,primary_key=True),
    sa.Column('checkout_no' , sa.String(20), nullable=False),
    sa.Column('data_in_json', sa.String(1000), nullable=False),
    sa.Column('garage_id', sa.Integer, nullable=False),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('clock_in_time',sa.DateTime, nullable=False),
    sa.Column('clock_out_time',sa.DateTime, nullable=False),
    sa.Column('checkout_time',sa.DateTime, nullable=False),
    sa.Column('checkout_amount', sa.Integer, nullable=False),
    sa.Column('number_of_vehicles',sa.Integer , nullable=False),
    sa.Column('create_date', sa.DateTime, default= datetime.datetime.utcnow),
    sa.Column('create_account_id',sa.Integer)
)

Commutation_Ticket_Order= sa.Table(
    'commutation_ticket_order', metadata,
    sa.Column('commutation_ticket_order_id' , sa.Integer, unique=True, nullable=False,primary_key=True),
    sa.Column('card_id16', sa.String(32) , nullable=False),
    sa.Column('commutation_ticket_config_id',sa.Integer , nullable=False),
    sa.Column('begin_date' , sa.DateTime , nullable=False),
    sa.Column('end_date' , sa.DateTime , nullable=False),
    sa.Column('customer_garage_id', sa.String(15), unique=False,nullable=True),
    sa.Column('sale_amount', sa.Integer , nullable=False),
    sa.Column('buyer_name', sa.String(30), nullable=False),
    sa.Column('telephone', sa.String(30), nullable=True),
    sa.Column('cellphone', sa.String(30), nullable=False),
    sa.Column('email', sa.String(100), nullable=True),
    sa.Column('address', sa.String(100), nullable=True),
    sa.Column('vehicle_plate_number', sa.String(16), nullable=False),
    sa.Column('vehicle_color', sa.String(16), nullable=True),
    sa.Column('notes', sa.String(200), nullable=True),
    sa.Column('order_status' , sa.Integer , nullable=False),
    sa.Column('create_date', sa.DateTime , default= datetime.datetime.utcnow),
    sa.Column('update_date', sa.DateTime, nullable=True),
    sa.Column('update_reason', sa.String(200), nullable=True),
    sa.Column('create_account_id', sa.Integer , nullable=False),
    sa.Column('update_account_id' , sa.Integer , nullable=True),
    sa.Column('garage_id' , sa.Integer , nullable=False),
    sa.Column('customer_id' , sa.Integer , nullable=False),
    sa.Column('unit_amount' , sa.Integer , nullable=False),
    sa.Column('is_active', sa.Integer , nullable=False)
)

Commutation_Ticket_Config= sa.Table(
    'commutation_ticket_config', metadata,
    sa.Column('commutation_ticket_config_id' , sa.Integer, unique=True, nullable=False,primary_key=True),
    sa.Column('commutation_ticket_config_name', sa.String(60) , nullable=False),
    sa.Column('unit_sales', sa.Integer , nullable=False),
    sa.Column('sales_num', sa.Integer , nullable=False),
    sa.Column('pay_amount', sa.Integer , nullable=False),
    sa.Column('vehicle_type', sa.String(1) , nullable=False),
    sa.Column('customer_id' , sa.Integer , nullable=False),
    sa.Column('create_date', sa.DateTime, nullable=False),
    sa.Column('update_date', sa.DateTime, nullable=True),
    sa.Column('create_account_id', sa.Integer , nullable=False),
    sa.Column('update_account_id', sa.Integer , nullable=True),
    sa.Column('is_active', sa.Integer , nullable=False)
)

Commutation_Ticket_Period_Config= sa.Table(
    'commutation_ticket_period_config', metadata,
    sa.Column('commutation_ticket_period_config_id' , sa.Integer, unique=True, nullable=False,primary_key=True),
    sa.Column('days_of_the_week' , sa.Integer , nullable=False),
    sa.Column('time_begin1', sa.String(10) ,nullable=True),
    sa.Column('time_end1', sa.String(10) ,nullable=True),
    sa.Column('time_begin2', sa.String(10) ,nullable=True),
    sa.Column('time_end2', sa.String(10) ,nullable=True),
    sa.Column('create_date', sa.DateTime, nullable=False),
    sa.Column('update_date', sa.DateTime, nullable=True),
    sa.Column('create_account_id', sa.Integer , nullable=False),
    sa.Column('update_account_id', sa.Integer , nullable=True),
    sa.Column('commutation_ticket_config_id', sa.Integer , nullable=True),
    sa.Column('is_active', sa.Integer , nullable=False)
)

Garage_Ftp_Info= sa.Table(
    'garage_ftp_info', metadata,
    sa.Column('garage_code' , sa.String(20), unique=True, nullable=False,primary_key=True),
    sa.Column('garage_name' , sa.String(20) , nullable=False),
    sa.Column('ftp_ip', sa.String(20) ,nullable=True),
    sa.Column('ftp_port', sa.String(10) ,nullable=True),
    sa.Column('ftp_userid', sa.String(10) ,nullable=True),
    sa.Column('ftp_pwd', sa.String(50) ,nullable=True),
    sa.Column('is_active', sa.Integer , nullable=False)
)

DeviceEvent = sa.Table(
    'device_event', metadata,
    sa.Column('device_event_id', sa.Integer, unique=True, nullable=False,primary_key=True),
    sa.Column('event_category' , sa.String(30) , nullable=False),
    sa.Column('event_type' , sa.String(30) , nullable=False),
    sa.Column('message' , sa.String(2000) , nullable=False),
    sa.Column('event_source' , sa.String(200) , nullable=False),
    sa.Column('source_ip_address' , sa.String(20) , nullable=False),
    sa.Column('field_01' , sa.String , nullable=False),
    sa.Column('field_02' , sa.String(200) , nullable=False),
    sa.Column('field_03' , sa.String(200) , nullable=False),
    sa.Column('field_04' , sa.String(200) , nullable=False),
    sa.Column('field_05' , sa.String(200) , nullable=False),
    sa.Column('update_date', sa.DateTime, nullable=False)
)

ActivationCode = sa.Table(
    'activation_code', metadata,
    sa.Column('activation_code_id', sa.Integer, unique=True, nullable=False,primary_key=True),
    sa.Column('garage_id' , sa.Integer , nullable=False),
    sa.Column('activation_code' , sa.String(45) , nullable=False),
    sa.Column('device_key' , sa.String(45) , nullable=False),
    sa.Column('is_used' , sa.Integer , nullable=False),
    sa.Column('create_date', sa.DateTime, nullable=False),
    sa.Column('create_account_id' , sa.Integer, nullable=True)
)


GaragePadArgs = sa.Table(
    'garage_pad_args', metadata,
    sa.Column('garage_pad_args_id', sa.Integer),
    sa.Column('garage_code', sa.String(10)),
    sa.Column('prepayment', sa.Integer),
    sa.Column('e_invoice_config_id', sa.Integer),
    sa.Column('create_time', sa.DateTime , nullable=False),
    sa.Column('create_user_id', sa.Integer),
    sa.Column('update_time', sa.DateTime ),
    sa.Column('update_user_id', sa.Integer),
    sa.Column('garage_id', sa.Integer)
)

DevicePadArgs = sa.Table(
    'device_pad_args', metadata,
    sa.Column('device_pad_args_id' ,sa.Integer),
    sa.Column('device_name',sa.String(20)),
    sa.Column('android_id',sa.String(50)),
    sa.Column('pos_no',sa.String(20)),
    sa.Column('device_ip',sa.String(50)),
    sa.Column('device_key',sa.String(50)),
    sa.Column('create_time', sa.DateTime , nullable=False),
    sa.Column('create_user_id', sa.Integer),
    sa.Column('update_time', sa.DateTime ),
    sa.Column('update_user_id', sa.Integer),
    sa.Column('garage_id', sa.Integer)
) 

E_Invoice_Config = sa.Table(
    'e_invoice_config', metadata,
    sa.Column('e_invoice_config_id', sa.Integer),
    sa.Column('tax_id' ,sa.String(30)),
    sa.Column('qrcode_encrypt_key' ,sa.String(50)),
    sa.Column('txn_file_generate_flag' ,sa.String(10)),
    sa.Column('txn_file_import_folder' ,sa.String(100)),
    sa.Column('txn_file_upload_folder' ,sa.String(100)),
    sa.Column('txn_file_backup_folder' ,sa.String(100)),
    sa.Column('txn_file_upload_interval',sa.Integer),
    sa.Column('api_txn_upload_url' ,sa.String(1000)),
    sa.Column('api_txn_upload_key' ,sa.String(1000)),
    sa.Column('ftp_upload_address' ,sa.String(100)),
    sa.Column('ftp_upload_port' ,sa.String(20)),
    sa.Column('ftp_upload_login_account' ,sa.String(50)),
    sa.Column('ftp_upload_login_pwd' ,sa.String(50)),
    sa.Column('ftp_upload_path' ,sa.String(100)),
    sa.Column('customer_id', sa.Integer),
    sa.Column('is_used', sa.Integer),
    sa.Column('einvoice_company' ,sa.String(20)),
    sa.Column('create_time', sa.DateTime ),
    sa.Column('create_user_id', sa.Integer),
    sa.Column('update_time', sa.DateTime ),
    sa.Column('update_user_id', sa.Integer),
    sa.Column('txn_file_upload_setting', sa.String(10)),
    sa.Column('get_number_setting', sa.String(10)),
    sa.Column('get_number_via', sa.String(10)),
    sa.Column('ftp_get_number_address', sa.String(100)),
    sa.Column('ftp_get_number_port', sa.String(100)),
    sa.Column('ftp_get_number_login_account', sa.String(100)),
    sa.Column('ftp_get_number_login_pwd', sa.String(100)),
    sa.Column('ftp_get_number_down_path', sa.String(100)),
    sa.Column('api_get_number_url' ,sa.String(1000)),
    sa.Column('api_get_number_key' ,sa.String(1000)),
    sa.Column('txn_file_upload_via', sa.String(10)),
    sa.Column('web_url', sa.String(1000)),
    sa.Column('web_api_key', sa.String(1000))
)

ICashConfig = sa.Table(
    'icash_config', metadata,
    sa.Column('id', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('garage_id', sa.Integer, nullable=False),
    sa.Column('icash_garage_code', sa.String(8), nullable=False),
    sa.Column('icash_garage_name', sa.String(30), nullable=False),
    sa.Column('icash_garage_abbreviated_name', sa.String(10), nullable=False),
    sa.Column('icash_garage_effective_begin_date', sa.Date, nullable=True, default = '2014-01-01'),
    sa.Column('icash_garage_effective_end_date', sa.Date, nullable=True, default = '9999-12-31'),
    sa.Column('icash_garage_opening_day', sa.Date, nullable=True, default = '2014-01-01'),
    sa.Column('icash_garage_saleable_day', sa.Date, nullable=True, default = '2014-01-01'),
    sa.Column('icash_garage_closing_day', sa.Date, nullable=True, default = '9999-12-31'),
    sa.Column('icash_garage_postal_code', sa.String(8), nullable=False),
    sa.Column('icash_garage_address', sa.String(60), nullable=False),
    sa.Column('icash_garage_telephone_area_code', sa.String(3), nullable=False),
    sa.Column('icash_garage_telephone', sa.String(12), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('create_user_id', sa.Integer, nullable=True),
    sa.Column('create_time', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('last_update_user_id', sa.Integer, nullable=True),
    sa.Column('last_update_time', sa.DateTime, nullable=True)
)

IPassConfig = sa.Table(
    'ipass_config', metadata,
    sa.Column('id', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('garage_id', sa.Integer, nullable=False),
    sa.Column('ipass_garage_code_decimal', sa.Integer, nullable=False),
    sa.Column('ipass_garage_code_hexadecmial', sa.String(4), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('create_user_id', sa.Integer, nullable=True),
    sa.Column('create_time', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('last_update_user_id', sa.Integer, nullable=True),
    sa.Column('last_update_time', sa.DateTime, nullable=True)
)

HappyCashConfig = sa.Table(
    'happycash_config', metadata,
    sa.Column('id', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('garage_id', sa.Integer, nullable=False),
    sa.Column('happycash_garage_code', sa.String(15), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('create_user_id', sa.Integer, nullable=True),
    sa.Column('create_time', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('last_update_user_id', sa.Integer, nullable=True),
    sa.Column('last_update_time', sa.DateTime, nullable=True)
)

TicketTransactionFtpConfig = sa.Table(
    'ticket_transaction_ftp_config', metadata,
    sa.Column('id', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('customer_id', sa.Integer, nullable=False),
    sa.Column('card_type', sa.String(2), nullable=False),
    sa.Column('ip_address', sa.String(50), nullable=False),
    sa.Column('ip_port', sa.Integer, nullable=False),
    sa.Column('account', sa.String(50), nullable=False),
    sa.Column('password', sa.String(50), nullable=False),
    sa.Column('upload_path', sa.String(100), nullable=False),
    sa.Column('download_path', sa.String(100), nullable=False),
    sa.Column('icash_customer_tax_id', sa.String(8), nullable=False),
    sa.Column('ipass_company_id', sa.String(4), nullable=False),
    sa.Column('ipass_system_id', sa.String(2), nullable=False),
    sa.Column('happycash_source_id', sa.String(2), nullable=False),
    sa.Column('status', sa.Integer, nullable=False),
    sa.Column('create_user_id', sa.Integer, nullable=True),
    sa.Column('create_time', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('last_update_user_id', sa.Integer, nullable=True),
    sa.Column('last_update_time', sa.DateTime, nullable=True)
)

ForgetPassword = sa.Table(
    'forget_password', metadata,
    sa.Column('no', sa.Integer, unique=True, nullable=False, primary_key=True),
    sa.Column('account_id', sa.Integer, nullable=False),
    sa.Column('account', sa.String(50), nullable=False),
    sa.Column('email', sa.Integer, nullable=False),
    sa.Column('token', sa.String(500), nullable=False),
    sa.Column('create_date', sa.DateTime, nullable=True, default = datetime.datetime.utcnow),
    sa.Column('has_change_pwd', sa.Integer, nullable=True),
    sa.Column('expiration_date', sa.DateTime, nullable=True)
)