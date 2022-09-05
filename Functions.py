'''
		- BaseCRUDFunction
		- GetAll
		- GetByProperty
		- InsertEntry
		- DeleteEntry
		- UpdateEntry
'''
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, List
import abc
from .Properties import Type
from typing import TypeVar

EdgeDBUUID = TypeVar('EdgeDBUUID')

@dataclass
class BaseCRUDFunction(abc.ABC):
    '''
    Allows Model functions to implement 
    returnStr or printStr functionality

    example ---

    miner.addProperty(propName='xxyyzz', printStr=True)

    instead of executing the INSERT this will print the string
    to be examined

    ------------------------------------------------
    
    printStr: bool = False
    
    client:Any = None
    
    lb = "{"
    
    rb = "}"
    
    propsList: List = field(default_factory=lambda: [])
    '''
    printStr: bool = False
    client:Any = None
    lb = "{"
    rb = "}"
    propsList: List = field(default_factory=lambda: [])

    def __post_init__(self):
        if self.printStr:
            print(self.buildBody())
            return

    @abc.abstractmethod
    def buildBody(self) -> str:
        pass
    
    @abc.abstractmethod
    def execute(self):
        pass

@dataclass
class Insert(BaseCRUDFunction):
    modelName:str = ''
    valuesToInsert: dict = None
    
    
    def buildBody(self) -> str:
        insertStrings=''
        for prop in self.propsList:
            insertStrings += f"\t{prop.propertyName} := <{prop.type.name}>$_{prop.propertyName},\n"
        
        body = f"""
select (
    INSERT {self.modelName} {self.lb}
    {insertStrings}
    {self.rb}
) {{
  id
}};
"""
        return body
    
    def execute(self):
        if self.printStr:
            pass
        else:
            entry = self.client.query(self.buildBody(), **self.valuesToInsert)
            self.client.close()
            return entry

@dataclass
class GetAll(BaseCRUDFunction):
    modelName:str = ''

    def buildBody(self) -> str:
        insertStrings=''
        for prop in self.propsList:
            insertStrings += prop.propertyName + ",\n"
        
        body = f"""
        select {self.modelName} {self.lb}
        id,
        {insertStrings}
        {self.rb}
        """
        return body
    
    def execute(self):
        if self.printStr:
            pass
        else:
            entry = self.client.query(self.buildBody())
            self.client.close()
            return entry

@dataclass
class GetByProperty(BaseCRUDFunction):
    '''
    miners.getByProperty(propName='total_mined', propType=Type.float32,_total_mined=10.0)

    '''
    propName:str = ''
    propType: Type = None
    modelName:str = ''
    valueToFilterBy: dict = None
    
    def buildBody(self) -> str:
        insertStrings = ''
        for prop in self.propsList:
            insertStrings += prop.propertyName + ",\n"

        body = f"""
select {self.modelName} {self.lb}
id,
{insertStrings}
{self.rb}
filter .{self.propName} = <{self.propType.name}>$_{self.propName}
"""
        return body
    
    def execute(self):
        if self.printStr:
            pass
        else:
            #print('executing from getby property')
            entry = self.client.query(self.buildBody(), **self.valueToFilterBy)
            self.client.close()
            return entry

@dataclass
class Update(BaseCRUDFunction):
    modelName:str = ''
    uuid: EdgeDBUUID = ''
    argsToUpdate: dict = None
    
    def buildBody(self) -> str:
        insertStrings=''
        for key, val in self.argsToUpdate.items():
            insertStrings += f'\t{key} := "{val}",\n'
        body = f"""
UPDATE {self.modelName} 
filter .id = <uuid>$_id
set {self.lb}
{insertStrings}
{self.rb};
        """
        return body
 
    def execute(self):
        if self.printStr:
            pass
        else:
            entry = self.client.query(self.buildBody(), _id=self.uuid)
            self.client.close()
            return entry

@dataclass
class Delete(BaseCRUDFunction):
    modelName:str = ''
    uuid: EdgeDBUUID = ''
    
    def buildBody(self) -> str:
        body = f"""
delete {self.modelName} 
filter .id = <uuid>$_id;
"""
        return body
    
    def execute(self):
        if self.printStr:
            pass
        else:
            entry = self.client.query(self.buildBody(), _id=self.uuid)
            self.client.close()
            return entry

@dataclass
class DeleteAll(BaseCRUDFunction):
    modelName:str = ''
    
    def buildBody(self) -> str:
        body = f"""
delete {self.modelName};
"""
        return body
    
    def execute(self):
        if self.printStr:
            pass
        else:
            entry = self.client.query(self.buildBody())
            self.client.close()
            return entry
