# -- coding:utf-8 --
from typing import Any


class TypeDTO(object):
    typeName: str
    typeValue: Any

    def __init__(self, typeName, value):
        """ 合约出入参的数据结构

        :param typeName: 参数类型(uint, string, address, byte32, ...)
        :param value: 参数值
        """
        self.typeName = typeName.lower()
        self.typeValue = value

        self.isInvalid = False
        if self.typeName == '':
            self.isInvalid = True
