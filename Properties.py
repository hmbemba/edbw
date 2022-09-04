'''
		- Type
		- BaseProperty
		- Property
		- LinkedProperty
		- MultiLinkProperty
'''
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, List
import abc
from .Constraints import Exclusive
# import pprint
# import edgedb

# client = edgedb.create_client()
# pp = pprint.PrettyPrinter(indent=4)


#Implement some sort of property validator callback
#So that if for example you're updating a phone number it must follow a certain pattern


class Type(Enum):
    str = auto()
    bool = auto()
    int32 = auto()
    int64 = auto()
    float32 = auto()
    float64 = auto()
    uuid = auto()

@dataclass
class BaseProperty(abc.ABC):
    propertyName: str
    type: Type
    required: bool = True
    constraints: List = field(default_factory=lambda: [])
    lb = "{"
    rb = "}"
    

@dataclass
class Property:
    propertyName: str
    type: Type
    required: bool = True
    constraints: List = field(default_factory=lambda: [])
    lb = "{"
    rb = "}"

    def renderStr(self):
        constraintString = ''
        for c in self.constraints:
            constraintString += c.renderStr()
        if self.constraints:
            return f"""
            \t{'required ' if self.required else ''}property {self.propertyName} -> {self.type.name}{self.lb}
            {constraintString}
            {self.rb};\n"""
        else:
            return f"\t{'required ' if self.required else ''}property {self.propertyName} -> {self.type.name};\n"

    def insertStr(self):
        return f"\t{self.propertyName} := <{self.type.name}>$_{self.propertyName},\n"
    
    def printInsertStrValue(self):
        return self.propertyName


@dataclass
class LinkProperty:
    propertyName: str
    otherModel: str
    type = Type.uuid

    def renderStr(self):
        return f"\tlink {self.propertyName} -> {self.otherModel};\n"

    def insertStr(self):
        return f"\t{self.propertyName} := ( select {self.otherModel} filter .id = <uuid>$_linkedModelId )\n"
    
    def printInsertStrValue(self):
        return "linkedModelId"


@dataclass
class MultiLinkProperty:
    propertyName: str
    otherModel: str
    type = Type.uuid

    def renderStr(self):
        return f"\tmulti link {self.propertyName} -> {self.otherModel};\n"

    def insertStr(self):
        return f"\t{self.propertyName} := ( select {self.otherModel} filter .id = <uuid>$_linkedModelId )\n"
    
    def printInsertStrValue(self):
        return "linkedModelId"


