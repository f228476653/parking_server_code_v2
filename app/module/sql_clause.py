import re
from enum import Enum

class ParkingSQL():
    __sql = f"""select distinctrow p.* , g.garage_name from parking p
    left join garage g on p.garage_id = g.garage_id  
    left join real_time_transaction_data r on r.parking_id = p.parking_id
    where  1=1"""
    class _WhereClause(Enum):
        #paid_time_begin = "and paid_time > :paid_time_begin "
        #paid_time_end = "and paid_time < :paid_time_end "
        enter_time_begin = " and enter_time > :enter_time_begin "
        enter_time_end = " and enter_time < :enter_time_end "
        exit_time_begin = " and exit_time > :exit_time_begin "
        exit_time_end = " and exit_time < :exit_time_end "
        vehicle_type = " and p.vehicle_type = :vehicle_type "
        paid_type = " and paid_type = :paid_type "
        real_fee = " and real_fee = :real_fee "
        vehicle_identification_number = "and vehicle_identification_number = :vehicle_identification_number "
        #card_id16 = "and card_id16 like :card_id16 "
        device_type =" and r.device_type=:device_type "
        card_id = " and card_id like :card_id "
        invoice_number = " and p.einvoice like :invoice_number "
        invoice_check = " and einvoice_print_status = :invoice_check "
        garage_code = " and p.garage_code = :garage_code "
        garage_id = " and p.garage_id = :garage_id "

    def query_argu_by_str(self, data: dict,user):
        argu = data.copy()
        print('--------------')
        print(argu)
        for key in data:
            if not data[key]:
                del argu[key]
                continue
            if key == "einvoice_number" or key == "vehicle_identification_number" or key == "card_id":
                argu[key] = self.process_like_case(argu[key])
            if key == "garage_group_id" :
                del argu['garage_group_id']
                argu[key] = self.get_garage_group(argu[key],user,self.__sql)
            self.__sql += self._WhereClause[key].value
        print(f'---sql---------{self.__sql}')
        query ={"sql":self.__sql,"arg":argu }
        return query

    def process_like_case(self, data: str):
        data = "%" + str(data) + "%"
        return data
    
    def get_garage_group(self, data: str,user ,sql):
        if user.is_superuser:
            if data!='all':
                sql = sql + """ and p.garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                        garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+ data + ')'
            else:
                sql = sql + """ and 1=1 """
        if user.is_superuser:
            if data!='all':
                sql = sql + """ and  p.garage_id in (select gg.garage_id from map_garage_to_garage_group gg join 
                garage g on gg.garage_id = g.garage_id where gg.garage_group_id="""+ data + ' and g.customer_id='+str(user.customer_id)+')'
            else:
                sql =  sql +""" and  p.garage_id in (select gg.garage_id from map_garage_to_garage_group gg 
                    left join map_garage_group_to_account ma on ma.garage_group_id = gg.garage_group_id
                     where ma.account_id= """ + str(user.account_id)+ ')'
        return sql

class PageSQL():

    def page_clause(self, page_info: dict, sql: str):
        sql = re.sub("SELECT", "SELECT SQL_CALC_FOUND_ROWS", sql, flags=re.IGNORECASE)
        page_index = (page_info['page_index']) * page_info['page_size']
        return sql + " LIMIT " + str(page_index) + "," + str(page_info['page_size'])
     
    def get_count_sql(self):
        return "SELECT FOUND_ROWS()"
         
class Device():
    pass
    
# Test 
def main():
    # parking = ParkingSQL()
    # front_end_argu = {"garage_code": "346", "paid_time_begin": '2018:01:02 11:11:11', "paid_type": 1, "einvoice_use_status": None}
    # result = parking.query_argu_by_str(front_end_argu)
    # print(result)
    a ="select aa"
    b = re.sub("SELECT","SELECT SQL_CALC_FOUND_ROWS",a,flags=re.IGNORECASE)
    print(b)
    

    page = PageSQL()
    page_info = {"page_index": 2,"page_size": 10}
    result['query_sql'] = page.page_clause(page_info, result["query_sql"])
    print(result['query_sql'])

if __name__ == '__main__':
    main()
