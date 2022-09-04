import edgedb
from EDBW.EdgeDBModel import EdgeDBModel
from EDBW.Properties import Type
import pprint
pp = pprint.PrettyPrinter(indent=4)

client = edgedb.create_client()

InvoicesModel = EdgeDBModel(modelName='Invoices', client=client)
InvoicesModel.addProperty(_name = 'three_word_name', _type = Type.str, _req = True)

#InvoicesModel.getByProperty(printStr=True, propName='three_word_name', propType=Type.str, _three_word_name='TameHolographcScallop')

#InvoicesModel.insert(printStr=True, _three_word_name="hello world")

#InvoicesModel.updateEntry(uuid="123",printStr=True, title="blade runner")

#InvoicesModel.delEntry(uuid="123", printStr=True)