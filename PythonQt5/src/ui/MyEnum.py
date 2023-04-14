from enum import Enum, unique


# @unique  # 枚举值不可以重复
class MyEnum(Enum):
    Protocol_type = 0
    Xml_type = 1
    File_type = 0
    Dir_type = 1


if __name__ == '__main__':
    print(MyEnum.Dir_type.value)
