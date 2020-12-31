import re
from enum import Enum
from enum import IntEnum

class BillNoGenerator():
    __sql = f"""select distinctrow p.* , g.garage_name from parking p
    left join garage g on p.garage_id = g.garage_id  
    left join real_time_transaction_data r on r.parking_id = p.parking_id
    where  1=1"""
    class _letter_reference(IntEnum):
        A =10
        B =11
        C =12
        D =13
        E =14
        F =15
        G =16
        H =17
        I =18
        J =19
        K =20
        L =21
        M =22
        N =23
        O =24
        P =25
        Q =26
        R =27
        S =28
        T =29
        U =30
        V =31
        W =32
        X =33
        Y =34
        Z =35
    
    class _time_reference(Enum):
        year = 35942400
        month = 2764800
        day = 86400
        hour = 3600
        minute =60

    def generator(self, road_code:str ,viechel_number:str, bill_create_year:int, bill_create_month:int, bill_create_day:int, bill_create_hour:int, bill_create_min:int, bill_create_sec:int):
        # road_code 路段代碼
        # viechel_number 車牌號碼 ex:AB-3342
        # bill_create 開單時間 (年：2016,月：8, 日：10, 時：23, 分：34, 秒：8)
        time_column = self.time(bill_create_year, bill_create_month, bill_create_day, bill_create_hour, bill_create_min, bill_create_sec)
        ase = self.viechel_number(viechel_number)
        bill_no = road_code + time_column + ase
        verification_code = self.verification_code(bill_no)
        bill_no_return = bill_no + verification_code
        return bill_no_return


    def time(self ,bill_create_year:int, bill_create_month:int, bill_create_day:int, bill_create_hour:int, bill_create_min:int, bill_create_sec:int):
        letter_reference_list = []
        letter_reference = list(self._letter_reference)
        for enum in letter_reference :
            letter_reference_list.append(enum.value)
        # (開單年-2012)*35942400+月＊2764800+日＊86400+時＊3600+分＊60+秒
        bill_create_time_number = (bill_create_year-2012) * self._time_reference['year'].value+ bill_create_month * self._time_reference['month'].value+ bill_create_day * self._time_reference['day'].value+ bill_create_hour * self._time_reference['hour'].value+ bill_create_min * self._time_reference['minute'].value+ bill_create_sec
        loop = 0
        left = 0
        time_column = ''
        #總數/36取得第一個商數及第一個餘數
        #第一個商數/36取得第2個商數及第2個餘數
        #第2個商數/36取得第3個商數及第3個餘數
        #第3個商數/36取得第4個商數及第4個餘數
        #第4個商數/36取得第5個商數及第5個餘數
        #第5個商數/36取得第6個商數及第6個餘數
        while loop < 6:
            left = bill_create_time_number%36
            bill_create_time_number = bill_create_time_number//36
            if left in letter_reference_list:
                time_column = time_column + self._letter_reference(left).name
            else:
                time_column = time_column + str(left)
            loop = loop +1
        return time_column

    def viechel_number(self ,viechel_number:str):
        # 不夠要補0
        viechel_number_return = viechel_number.replace('-','')
        viechel_number_return = viechel_number_return.ljust(6, '0')
        return viechel_number_return

    def verification_code(self , bill_no ):
        verification_code_factor = [3,5,9,11,13,17,19,3,5,9,11,13,17,19]
        #letter_reference_number = list(map(int, self._letter_reference))
        letter_reference_names = self._letter_reference._member_names_
        print(letter_reference_names)
        j = 0
        total = 0
        for letter in bill_no:
            print(letter)
            if letter in letter_reference_names:
                i = self._letter_reference[letter].value
            else:
                i = int(letter)
            print(f'---total---{total}')
            print(f'---verification_code_factor---{verification_code_factor[j]}')
            print(f'--- i**verification_code_factor---{i * verification_code_factor[j]}')
            total = total + i * verification_code_factor[j]
            j=j+1
        verification_code = total%7
        print(verification_code)
        return verification_code

    
# Test 
def main():
    # parking = ParkingSQL()
    # front_end_argu = {"garage_code": "346", "paid_time_begin": '2018:01:02 11:11:11', "paid_type": 1, "einvoice_use_status": None}
    # result = parking.query_argu_by_str(front_end_argu)
    # print(result)
    page = BillNoGenerator()
    result = page.generator('01', 'AB-5684' ,2013,1,1,0,1,1)

if __name__ == '__main__':
    main()
