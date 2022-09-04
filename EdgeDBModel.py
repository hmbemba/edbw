from dataclasses import dataclass, field
from typing import Any, List
from .Properties import Type, Property, LinkProperty, MultiLinkProperty
from .Functions import GetAll, GetByProperty, Insert, Update, Delete
from typing import TypeVar

EdgeDBSet = TypeVar('EdgeDBSet')

@dataclass
class EdgeDBModel:
    modelName: str
    client: Any
    _props: List = field(default_factory=lambda: [])
    lb = "{"
    rb = "}"
    
    '''
    ###################################################
    MODEL BUILDER FUNCTIONS
    ###################################################
    '''
    
    def addProperty(self, _propertyName: str, _propertyType: Type, _req: bool) -> None:
        self._props.append(Property(propertyName=_propertyName,
                          type=_propertyType, required=_req))
    
    def printModel(self):
        propertyStrings = ''
        for prop in self._props:
            propertyStrings += prop.renderStr()

        model = f"""
\ttype {self.modelName} {self.lb}
{propertyStrings}
\t{self.rb}
"""
        print(model)

    '''
    ###################################################
    CRUD FUNCTIONS
    ###################################################
    '''
    def insertEntry(self,printStr = False,**valuesToInsert) -> None:
        Insert(printStr=printStr, 
               propsList=self._props,
               modelName=self.modelName,
               client=self.client,
               valuesToInsert = valuesToInsert
               ).execute()
        
    def getAll(self,printStr = False) -> EdgeDBSet:
        data = GetAll(printStr=printStr, 
               propsList=self._props,
               modelName=self.modelName,
               client=self.client,
               ).execute()
        return data
            

    def getByProperty(self,printStr, propName:str, propType: Type, **valueToFilterBy ) -> EdgeDBSet:
        data = GetByProperty(
                      client = self.client, 
                      propsList=self._props,
                      modelName = self.modelName,
                      propName = propName,
                      propType = propType,
                      printStr=printStr, 
                      valueToFilterBy=valueToFilterBy
    ).execute()
        return data
    

    
    def getByFilterString(self, filterString) -> EdgeDBSet:
        ...
    
    def updateEntry(self,uuid,printStr = False, **argsToUpdate) -> EdgeDBSet:
        """
        Finds an entry by its uuid then updates it with **args
        
        entry = fakeModel.get(...)
        fakeModel.update(entry.id, printStr=True, name="blade runner")
        """
        Update(printStr=printStr, 
               propsList=self._props,
               modelName=self.modelName,
               client=self.client,
               uuid = uuid,
               argsToUpdate = argsToUpdate
               ).execute()
    
    def delEntry(self, uuid,printStr = False) -> None:
        """
        Finds an entry by its uuid then deletes it
        """
        Delete(printStr=printStr, 
               propsList=self._props,
               modelName=self.modelName,
               client=self.client,
               uuid = uuid,
               ).execute()
    
    def delAll(self,) -> None:
        """
        Deletes all entries in this model
        
        """
        ...
    

