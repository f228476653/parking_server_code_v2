import enum
 
# creating enumerations using class
class SystemEventType(enum.Enum):
    Add = 1
    UPDATE_INFO = 2
    DELETE_INFO = 3
    otherException = 4
    KEY_ERROR = 5
    KEYSTORE_EXPIRED_ERROR = 6
    KEYSTORE_INVALID_ERROR = 7
    TOKEN_INVALID = 8
    ADD_GARAGE_GROUP = 9
    UPDATE_GARAGE_GROUP = 10
    DELETE_GARAGE_GROUP = 11

    ADD_ROLE = 12
    UPDATE_ROLE = 13
    DELETE_ROLE = 14
    SELECT_GARAGE_BY_CODE = 15


    ADD_DEVICE_EVENT=16
    UPDATE_DEVICE_EVENT=17
    DELETE_DEVICE_EVENT=18

    REAL_TIME_TRANSACTION_PARSER_ERROR = 778

    REAL_TIME_TRANSACTION_PARSER_log = 707
