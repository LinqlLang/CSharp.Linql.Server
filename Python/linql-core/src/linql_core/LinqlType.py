from typing_extensions import Self
from .LinqlExpression import LinqlExpression
from .ITypeNameProvider import ITypeNameProvider
from typing import Any

class LinqlType():
    
    ListType: str = "List"
    TypeName: str | None
    GenericParameters: list[Self]  | None

    def IsList(self) -> bool:
        return self.TypeName == LinqlType.ListType
    
    def GetLinqlType(Value: Any, TypeNameProvider: ITypeNameProvider) -> Self:
        type = LinqlType()

        switchDict = { 
            str: "String", 
            int: LinqlType.GetNumberType, 
            float: LinqlType.GetNumberType, 
            complex: LinqlType.InvalidType, 
            list: LinqlType.GetListType,
            bool: "Boolean",
            None: "undefined"
            }

        return type

    def InvalidType(Value: Any, Type: Self, TypeNameProvider: ITypeNameProvider):
        raise Exception(f'Value {Value} is not supported at this time.')
    
    def GetNumberType(Value: int | float | complex, Type: Self, TypeNameProvider: ITypeNameProvider) -> Self:
        if Value > 2^32:
            Type.TypeName = "Long"
        else:
            Type.TypeName = "Int32"
        return Type

    def GetListType(Value: list[Any], Type: Self, TypeNameProvider: ITypeNameProvider) -> Self:
        Type.TypeName = LinqlType.ListType
        if len(Value) > 0:
            firstVal = Value[0]
            Type.GenericParameters = []
            Type.GenericParameters.append(LinqlType.GetLinqlType(firstVal, TypeNameProvider))
        else:
            objectType = LinqlType()
            objectType.TypeName = "object"
            Type.GenericParameters = []
            Type.GenericParameters.append(objectType)
        return Type