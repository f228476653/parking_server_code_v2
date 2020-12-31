
""" utes module."""
from app.controllers.device_pv_controller import DevicePvController
from app.controllers.exit_config_controller import ExitConfigController
from app.controllers.user_controller import UserController
from app.controllers.login_controller import LoginController
from app.controllers.customer_controller import CustomerController
from app.controllers.keystore_controller import KeystoreController
from app.controllers.garage_controller import GarageController
from app.controllers.garage_group_controller import GarageGroupController
from app.controllers.systemlog_controller import SystemlogController
from app.controllers.cli_controller import CliController
from app.controllers.entry_gate_controller import EntryGateController
from app.controllers.system_helper_controller import SystemHelperController
from app.controllers.real_time_transaction_controller import RealTimeTransactionController
from app.controllers.original_real_time_transaction_controller import OriginalRealTimeTransactionController
from app.controllers.einvoice_number_controller import EinvoiceController
from app.controllers.einvoice_config_controller import EinvoiceConfigController
from app.controllers.clock_in_and_out_controller import ClockInAndOutController
from app.controllers.shift_checkout_controller import ShiftCheckoutController
from app.controllers.commutation_ticket_controller import CommutationTicketController
from app.controllers.file_controller import FileController
from app.controllers.device_controller import DeviceController

from app.controllers.device_pad_controller import DevicePadController
from app.controllers.regularly_report_controller import RegularlyReportController
from app.controllers.system_configuration_controller import SystemConfigurationController
from app.controllers.pms_data_upload_controller import PmsDataUploadController
from app.controllers.ticket_transaction_controller import TicketTransactionController
from app.controllers.fee_controller import FeeController
from app.controllers.kafka_controller import KafkaController
import aiohttp_cors

prefix_v1 = "/api/v1"

def map_routes(app):
    """Map routes to app object."""
    cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*"
        )
    })

    # kafka_controller = KafkaController()
    # cors.add(app.router.add_route("POST", prefix_v1+r'/kafka/producer', kafka_controller.kafka_producer))
    # cors.add(app.router.add_route("POST", prefix_v1+r'/kafka/consumer', kafka_controller.kafka_consumer))

    regularly_report = RegularlyReportController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/regularly_report/day_revenue/{garage_code}/{the_day}/{paid_type}', regularly_report.get_day_revenue_report))
    cors.add(app.router.add_route("GET", prefix_v1+r'/regularly_report/monthly_revenue/{garage_code}/{the_month}/{paid_type}', regularly_report.get_monthly_revenue_report))
    cors.add(app.router.add_route("GET", prefix_v1+r'/regularly_report/monthly_usage/{garage_code}/{monthly}', regularly_report.get_monthly_usage_report))
    

    fee_controller = FeeController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/fee/{garage_id}/{car_type}', fee_controller.get_fee_args))
    cors.add(app.router.add_route("POST", prefix_v1+r'/fee', fee_controller.store_fee_args))
    cors.add(app.router.add_route("DELETE", prefix_v1+r'/fee/{fee_rule_id}', fee_controller.delete_fee_args))
    cors.add(app.router.add_route("GET", prefix_v1+r'/special_day/{year}', fee_controller.get_special_day_list))

    system_configuration_controller = SystemConfigurationController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/system/configuration/{key}', system_configuration_controller.get_system_configuration_by_key))
    cors.add(app.router.add_route("GET", prefix_v1+r'/system/configuration', system_configuration_controller.get_all_system_configuration))
    cors.add(app.router.add_route("POST", prefix_v1+r'/system/configuration', system_configuration_controller.create_system_configuration))
    cors.add(app.router.add_route("PUT", prefix_v1+r'/system/configuration/update', system_configuration_controller.update_system_configuration_by_key))
    cors.add(app.router.add_route("PUT", prefix_v1+r'/system/configuration/delete', system_configuration_controller.delete_system_configuration_by_key))

    device_controller = DeviceController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/customer/{customer_id}/{device_type}', device_controller.get_customer_device_by_customer_id))
    cors.add(app.router.add_route("POST", prefix_v1+r'/device/customer/add_or_update', device_controller.add_or_update_customer_device_args))
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/garage/{garage_id}/{device_type}', device_controller.get_garage_device_by_garage_id))
    # cors.add(app.router.add_route("POST", prefix_v1+r'/device/garage/add_or_update', device_controller.add_or_update_garage_device_args))
    cors.add(app.router.add_route("GET", prefix_v1+r'/enable_card_case/{customer_id}/{device_type}', device_controller.is_enable_card_type_by_customer_id))
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/single/{device_type}/{device_id}', device_controller.get_device_by_device_id))
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/all/{garage_id}', device_controller.get_all_device_by_garage_id))
    cors.add(app.router.add_route("POST", prefix_v1+r'/device/add_or_update', device_controller.add_or_update_device))
    cors.add(app.router.add_route("DELETE", prefix_v1+r'/device/delete/{device_type}/{device_id}', device_controller.delete_device_by_device_id))
    cors.add(app.router.add_route("POST", prefix_v1+r'/device/export', device_controller.device_export))
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/exist/{garage_id}/{ip}', device_controller.is_duplicate_ip_from_same_garage))
    # 測試ftp
    cors.add(app.router.add_route("POST", prefix_v1+r'/device/ftp', device_controller.download_device_parameter))
    
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/event', device_controller.get_device_event))
    cors.add(app.router.add_route("PUT", prefix_v1+r'/device/event', device_controller.add_device_event))
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/event/sse', device_controller.get_device_event_sse))

    device_pv_controller = DevicePvController()
    
    cors.add(app.router.add_route("GET",prefix_v1+r'/device/pv/{device_pv_id}', device_pv_controller.show_device_pv_by_device_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/device/pv/all/{garage_id}', device_pv_controller.show_all_device_pv_by_garage_id))
    cors.add(app.router.add_route("POST",prefix_v1+r'/device/pv', device_pv_controller.add_device_pv))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/device/pv/update', device_pv_controller.update_device_pv_by_device_pv_id))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/device/pv/delete', device_pv_controller.delete_device_pv_by_device_pv_id))

    device_pad_controller = DevicePadController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/device/pad/{garage_id}', device_pad_controller.get_device_pad_by_garage_id))
    
    exit_controller = ExitConfigController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/exit_settings/garage_group', exit_controller.get_garage_groupname_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/exit_settings', exit_controller.get_all_exit_config_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/exit_settings/garages/{group_name}', exit_controller.get_garages_by_group_name))
    cors.add(app.router.add_route("GET",prefix_v1+r'/exit_settings/garage/{garage_id}', exit_controller.get_exit_type_info_by_garage_id))
    cors.add(app.router.add_route("POST",prefix_v1+r'/exit_settings/garage', exit_controller.update_exit_type_by_exit_config_id))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/exit_settings/garage/disable_toggle', exit_controller.disable_exit_config_by_exit_config_id))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/exit_settings/garage', exit_controller.reset_exit_config_by_exit_config_id))
 
    login_controller=LoginController()
    cors.add(app.router.add_route("GET", prefix_v1+r'/device/test/{c}/{g}/{d}', login_controller.aaa))
    cors.add(app.router.add_route("POST", prefix_v1+r'/login', login_controller.login))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/login/au/forget_password',login_controller.forget_passward_query_reset))
    cors.add(app.router.add_route("GET", prefix_v1+r'/login/au/get_reset_password_account/{token}', login_controller.get_reset_password_account))

    
    user_controller = UserController()
    cors.add(app.router.add_route("PUT", prefix_v1+r'/account/au/update_password',user_controller.update_password))
    cors.add(app.router.add_route("GET", prefix_v1+r"/permissions",user_controller.get_permissions))
    cors.add(app.router.add_route("GET", prefix_v1+r'/permissions/{id:\d*}',user_controller.get_permission_by_id))
    cors.add(app.router.add_route("GET", prefix_v1+r'/permissions/maximun',user_controller.get_maximun_permission))
    
    cors.add(app.router.add_route("GET",prefix_v1+r'/accounts',user_controller.get_users)) 
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/{id:\d*}',user_controller.get_user_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/one/{id:\d*}',user_controller.get_first_user_by_account_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/accounts/customer_id/{customer_id}',user_controller.get_users_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/{account}',user_controller.get_user_by_account))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/account/{id:\d*}',user_controller.delete_user_by_id))
    cors.add(app.router.add_route("POST",prefix_v1+r'/account',user_controller.add_user))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/account',user_controller.update_user))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/garage/{account_id:\d*}',user_controller.get_map_garage_to_account_by_account_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/garage_group/{account_id:\d*}',user_controller.get_map_garage_group_to_account_by_account_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/garage_list/{account_id:\d*}',user_controller.get_map_garage_to_account_list_by_acocunt_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/accounts/users/{customer_id}',user_controller.get_users_by_customer_id_with_system_account))
    cors.add(app.router.add_route("GET",prefix_v1+r'/accounts/{garage_id}',user_controller.get_users_by_garage_id_xor_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/account/exist/{account}',user_controller.is_account_exist))

    cors.add(app.router.add_route("GET",prefix_v1+r'/permissions',user_controller.get_permissions))
    cors.add(app.router.add_route("GET",prefix_v1+r'/permissions/{id:\d*}',user_controller.get_permission_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/permissions/maximun',user_controller.get_maximun_permission))

    cors.add(app.router.add_route("GET",prefix_v1+r'/roles',user_controller.get_roles))
    cors.add(app.router.add_route("GET",prefix_v1+r'/roles/{id:\d*}',user_controller.get_role_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/role/exist/{role_name}',user_controller.is_role_name_exist_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/roles/customer_id/{customer_id:\d*}',user_controller.get_roles_by_customer_id))
    
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/role/delete/{role_id:\d*}',user_controller.delete_role))
    cors.add(app.router.add_route("POST",prefix_v1+r'/roles',user_controller.add_role))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/roles',user_controller.update_role))
    cors.add(app.router.add_route("GET",prefix_v1+r'/map_role_permission/{id:\d*}',user_controller.get_permission_by_rold_id))


    customer_controller=CustomerController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/customers',customer_controller.get_customers))
    cors.add(app.router.add_route("GET",prefix_v1+r'/customers/{id:\d*}',customer_controller.get_customer_by_id))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/customers/{id:\d*}',customer_controller.delete_customer_by_id))
    cors.add(app.router.add_route("POST",prefix_v1+r'/customers',customer_controller.add_customer))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/customers',customer_controller.update_customer))

    keystore_controller=KeystoreController()
    cors.add(app.router.add_route("POST",prefix_v1+r'/keystores',keystore_controller.new_keystore))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/keystores',keystore_controller.update_keystore))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystores',keystore_controller.get_keystores))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystores/customer_id/{customer_id}',keystore_controller.get_keystores_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystores/{id:\d*}',keystore_controller.get_keystores_by_id))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/keystores/{id:\d*}',keystore_controller.delete_keystore_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystorestatus',keystore_controller.get_keystore_status))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystores/encrypt_key_for_pad_config/{garage_id}/{device_key}', keystore_controller.encrypt_key_for_pad_config))
    cors.add(app.router.add_route("GET",prefix_v1+r'/keystores/au/get_pad_config_by_key/{key}', keystore_controller.get_pad_config_by_key))

    garage_controller=GarageController()
    cors.add(app.router.add_route("POST",prefix_v1+r'/garage',garage_controller.add_garage))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/garage',garage_controller.update_garage))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/garage/{id:\d*}',garage_controller.delete_garage_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages',garage_controller.get_garages))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garage/{garage_id:\d*}',garage_controller.get_garage_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages/total',garage_controller.get_garages_total))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages/customer_id/{customer_id}',garage_controller.get_garages_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages/amount/customer_id/{customer_id:\d*}',garage_controller.get_garage_amount_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages/garage_group_id/{garage_group_id}', garage_controller.get_garages_by_garage_group_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garages/{garage_code}', garage_controller.is_garage_code_exist))
    cors.add(app.router.add_route("GET",prefix_v1+r'/pad-garage-args/{garage_id}',garage_controller.get_pad_garage_args_garage_id))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/garage/update_garage_capacity',garage_controller.update_garage_capacity))
    
    #cors.add(app.router.add_route("GET",prefix_v1+r'/garage/exist/{garage_name}',garage_controller.is_garage_name_exit))
    
    garage_group_controller=GarageGroupController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/garage_groups/customer_id/{customer_id}',garage_group_controller.get_garage_groups_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garage_groups/account_id',garage_group_controller.get_garage_groups_by_account_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garage_group/{id:\d*}',garage_group_controller.get_garage_group_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/garage_groups',garage_group_controller.get_garage_groups))
    cors.add(app.router.add_route("POST",prefix_v1+r'/garage_group',garage_group_controller.add_garage_group))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/garage_group',garage_group_controller.update_garage_group))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/garage_group/{id:\d*}',garage_group_controller.delete_garage_group_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/map_garage_to_garage_group/{id:\d*}',garage_group_controller.get_map_garage_to_garage_group_by_garage_group_id))

    syslog_controller=SystemlogController()
    cors.add(app.router.add_route("POST",prefix_v1+r'/system_log',syslog_controller.add_log))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/system_log',syslog_controller.delall_log))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log',syslog_controller.query_by_message))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/date',syslog_controller.query_by_date))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/event/',syslog_controller.query_by_event))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/system_log/type',syslog_controller.query_SystemEventType))

    cli_controller=CliController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/cli/accounting_parse/{csv}',cli_controller.accounting_parse))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_accounting',cli_controller.query_accounting))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_pms_diff_record',cli_controller.query_pms_diff_record))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_amt_diff_record',cli_controller.query_amt_diff_record))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_cps_diff_record',cli_controller.query_cps_diff_record))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_parking_settlement_record',cli_controller.query_parking_settlement_record))
    cors.add(app.router.add_route("POST",prefix_v1+r'/cli/query_records_after_manual_close',cli_controller.query_records_after_manual_close))
    cors.add(app.router.add_route("POST",prefix_v1+r'/au/accounting_daily',cli_controller.accounting_daily))
    

    entry_gate_controller=EntryGateController()

    cors.add(app.router.add_route("POST",prefix_v1+r'/entry-gate',entry_gate_controller.add_entry_gate))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/entry-gate',entry_gate_controller.update_entry_gate))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/entry-gate/{id:\d*}',entry_gate_controller.delete_entry_gate_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/entry-gates',entry_gate_controller.get_entry_gates))
    cors.add(app.router.add_route("GET",prefix_v1+r'/entry-gate/{id:\d*}',entry_gate_controller.get_entry_gates_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/entry-gate/customer_id{customer_id:\d*}',entry_gate_controller.get_entry_gates_by_customer_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/entry-gate/garage/{id:\d*}',entry_gate_controller.get_entry_gates_by_garage_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/entry-gate/garage/{garage_id:\d*}/exist/{sn:\d*}',entry_gate_controller.get_entry_gates_exist_by_garage_id))
    
    real_time_transaction_controller=RealTimeTransactionController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/real-time-transaction/add_transaction',real_time_transaction_controller.add_transaction))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/real-time-transaction/get_transaction',real_time_transaction_controller.get_transaction))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/real-time-transaction/delete_transaction_by_id/{parking_id:\d*}/{garage_id:\d*}',real_time_transaction_controller.delete_transaction_by_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/real-time-transaction/get_transaction_by_checkout_no/{checkout_no}/{garage_id:\d*}',real_time_transaction_controller.get_transaction_by_checkout_no))
    cors.add(app.router.add_route("POST",prefix_v1+r'/real-time-transaction/get_transaction_by_garage_code', real_time_transaction_controller.get_transaction_by_garage_code))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/real-time-transaction-pad/get_transaction_pad',real_time_transaction_controller.get_transaction_pad))
    #cors.add(app.router.add_route("PUT",prefix_v1+r'/real-time-transaction-pad/get_transaction_pad_row_count',real_time_transaction_controller.get_transaction_pad_row_count))
    cors.add(app.router.add_route("GET",prefix_v1+r'/real-time-transaction/cancel_parking/{parking_id:\d*}',real_time_transaction_controller.cancel_parking))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/real-time-transaction/add_complete_transaction',real_time_transaction_controller.add_complete_transaction))
    
    original_real_time_transaction_controller=OriginalRealTimeTransactionController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/original_real_time_transaction/query_pms_transaction',original_real_time_transaction_controller.query_transaction))

    system_helper_controller=SystemHelperController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_system_config',system_helper_controller.parse_system_config))
    #cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_driveway_data',system_helper_controller.parse_driveway_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_parking_data',system_helper_controller.parse_parking_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_trxdata_data',system_helper_controller.parse_trxdata_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_real_time_transaction_data',system_helper_controller.parse_real_time_transaction_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_lane_data',system_helper_controller.parse_lane_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_einvoice_number_data',system_helper_controller.parse_e_invoice_number_data))
    cors.add(app.router.add_route("GET",prefix_v1+r'/system-config/parse_parking_in_out_record',system_helper_controller.parse_parking_in_out_record))

    einvoice_number_controller=EinvoiceController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/einvoice-number/add_einvoice',einvoice_number_controller.add_einvoice))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/einvoice-number/update_einvoice',einvoice_number_controller.update_einvoice))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/einvoice-number/delete_einvoice/{parking_id:\d*}/{in_or_out:\d*}',einvoice_number_controller.delete_einvoice))
    
    einvoice_config_controller=EinvoiceConfigController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/einvoice-config/get_einvoice_config/{garage_id}',einvoice_config_controller.get_garage_einvoice_config))
    cors.add(app.router.add_route("POST",prefix_v1+r'/einvoice-config/add_einvoice_config',einvoice_config_controller.add_customer_level_einvoice_config))
    cors.add(app.router.add_route("GET",prefix_v1+r'/einvoice-config/get_customer_einvoice_config/{customer_id}',einvoice_config_controller.get_customer_level_einvoice_config))
    cors.add(app.router.add_route("POST",prefix_v1+r'/einvoice-config/update_einvoice_config',einvoice_config_controller.update_customer_level_einvoice_config))
    

    clock_in_and_out_controller=ClockInAndOutController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/clock-in-and-out/add_clock_record',clock_in_and_out_controller.add_clock_record))

    shift_checkout_controller=ShiftCheckoutController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/shift-checkout-controller/add_shift_checkout',shift_checkout_controller.add_shift_checkout))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/shift-checkout-controller/get_shift_checkout_by_condition',shift_checkout_controller.get_shift_checkout_by_condition))


    commutation_ticket_controller=CommutationTicketController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/commutation-ticket/update_commutation_ticket',commutation_ticket_controller.update_commutation_ticket))
    
    file_controller=FileController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/file/get_apk_by_garage_id/{customer_id}/{garage_id}/{file_server_name}',file_controller.get_apk_by_garage_id))
    cors.add(app.router.add_route("GET",prefix_v1+r'/file/update_date/{customer_id}/{garage_id}/{file_server_name}',file_controller.get_updated_date_by_garage_id))
    cors.add(app.router.add_route("POST",prefix_v1+r'/file/file_upload',file_controller.file_upload))

    ticket_transaction_controller=TicketTransactionController()
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/icash_pack',ticket_transaction_controller.icash_pack))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/icash_upload',ticket_transaction_controller.icash_upload))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/icash_download_feedback_files',ticket_transaction_controller.icash_download_feedback_files))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/icash_download_black_list',ticket_transaction_controller.icash_download_black_list))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/icash_feedback_files_import',ticket_transaction_controller.icash_feedback_files_import))

    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_pack',ticket_transaction_controller.ipass_pack))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_upload',ticket_transaction_controller.ipass_upload))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_download_feedback_files',ticket_transaction_controller.ipass_download_feedback_files))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_download_black_list_KBLI',ticket_transaction_controller.ipass_download_black_list_KBLI))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_download_black_list_KBLN',ticket_transaction_controller.ipass_download_black_list_KBLN))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_download_close_autoload_list',ticket_transaction_controller.ipass_download_close_autoload_list))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/ipass_feedback_files_import',ticket_transaction_controller.ipass_feedback_files_import))

    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/happycash_pack',ticket_transaction_controller.happycash_pack))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/happycash_upload',ticket_transaction_controller.happycash_upload))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/happycash_download_feedback_files',ticket_transaction_controller.happycash_download_feedback_files))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/happycash_download_black_list',ticket_transaction_controller.happycash_download_black_list))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/happycash_feedback_files_import',ticket_transaction_controller.happycash_feedback_files_import))

    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/garage/icash/{garage_id}',ticket_transaction_controller.icash_query_garage))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/garage/ipass/{garage_id}',ticket_transaction_controller.ipass_query_garage))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/garage/happycash/{garage_id}',ticket_transaction_controller.happycash_query_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/icash/add',ticket_transaction_controller.icash_insert_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/ipass/add',ticket_transaction_controller.ipass_insert_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/happycash/add',ticket_transaction_controller.happycash_insert_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/icash/update',ticket_transaction_controller.icash_update_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/ipass/update',ticket_transaction_controller.ipass_update_garage))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/garage/happycash/update',ticket_transaction_controller.happycash_update_garage))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/garage/icash/delete/{garage_id}',ticket_transaction_controller.icash_delete_garage))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/garage/ipass/delete/{garage_id}',ticket_transaction_controller.ipass_delete_garage))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/garage/happycash/delete/{garage_id}',ticket_transaction_controller.happycash_delete_garage))

    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/customer/icash/{customer_id}',ticket_transaction_controller.icash_query_customer))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/customer/ipass/{customer_id}',ticket_transaction_controller.ipass_query_customer))
    cors.add(app.router.add_route("GET",prefix_v1+r'/ticket_transaction/customer/happycash/{customer_id}',ticket_transaction_controller.happycash_query_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/icash/add',ticket_transaction_controller.icash_insert_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/ipass/add',ticket_transaction_controller.ipass_insert_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/happycash/add',ticket_transaction_controller.happycash_insert_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/icash/update',ticket_transaction_controller.icash_update_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/ipass/update',ticket_transaction_controller.ipass_update_customer))
    cors.add(app.router.add_route("POST",prefix_v1+r'/ticket_transaction/customer/happycash/update',ticket_transaction_controller.happycash_update_customer))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/customer/icash/delete/{customer_id}',ticket_transaction_controller.icash_delete_customer))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/customer/ipass/delete/{customer_id}',ticket_transaction_controller.ipass_delete_customer))
    cors.add(app.router.add_route("DELETE",prefix_v1+r'/ticket_transaction/customer/happycash/delete/{customer_id}',ticket_transaction_controller.happycash_delete_customer))

    pms_data_upload_controller=PmsDataUploadController()
    cors.add(app.router.add_route("PUT",prefix_v1+r'/pms-data-upload/parking',pms_data_upload_controller.add_pms_parking))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/pms-data-upload/lane',pms_data_upload_controller.add_pms_lane))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/pms-data-upload/einvoice_number',pms_data_upload_controller.add_pms_einvoice_number))
    cors.add(app.router.add_route("PUT",prefix_v1+r'/pms-data-upload/trx_data',pms_data_upload_controller.add_pms_trx_data))
