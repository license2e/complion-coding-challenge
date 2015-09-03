import random
import math
from flask.ext.script import Manager
from app import app, db
from models import DocumentType, MetadataProperty, Document

FixturesCommand = Manager(usage='Perform database fixture insertion')

@FixturesCommand.command
def init():
    print '\nExecuting the fixture init command...\n'
    all_document_types = add_document_types()
    all_metadata_properties = add_metadata_properties()
    link_document_types_to_properties(all_document_types, all_metadata_properties)
    all_documents = add_documents(all_document_types, all_metadata_properties)
    print '\n'

def add_document_types():
    print '\tAdding the DocumentTypes:'
    all_document_types = DocumentType.query.all()
    if len(all_document_types) is 0:
        # add document types
        doc_type1 = DocumentType('protocol', 'Protocol')
        doc_type2 = DocumentType('consent', 'Consent')
        doc_type3 = DocumentType('contract', 'Contract')
        db.session.add(doc_type1)
        db.session.add(doc_type2)
        db.session.add(doc_type3)
        db.session.commit()
        all_document_types = DocumentType.query.all()
        print '\t\tDocumentType fixture executed successfully, {0} added'.format(len(all_document_types))
    else:
        print '\t\tDocumentType fixture was already executed, {0} document types exists'.format(len(all_document_types))
    return all_document_types

def add_metadata_properties():
    print '\tAdding the Properties:'
    all_metadata_properties = MetadataProperty.query.all()
    if len(all_metadata_properties) is 0:
        # add properties
        property1 = MetadataProperty('irb_number', 'irb_number_123')
        property2 = MetadataProperty('contract_number', 'contract_number_123')
        db.session.add(property1)
        db.session.add(property2)
        db.session.commit()
        all_metadata_properties = MetadataProperty.query.all()
        print '\t\tMetadata fixture executed successfully, {0} added'.format(len(all_metadata_properties))
    else:
        print '\t\tMetadata fixture was already executed, {0} properties exists'.format(len(all_metadata_properties))
    return all_metadata_properties

def link_document_types_to_properties(all_document_types = [], all_metadata_properties = []):
    if len(all_document_types) > 0 and len(all_metadata_properties) > 0:
        print '\tLinking the DocumentTypes and Properties:'
        metadata_property_hashmap = {}
        for metadata_property in all_metadata_properties:
            metadata_property_hashmap[metadata_property.property_name] = metadata_property
        for doc_type in all_document_types:
            if doc_type.document_type in ['protocol','consent'] and metadata_property_hashmap['irb_number'] not in doc_type.metadata_properties:
                doc_type.metadata_properties.append(metadata_property_hashmap['irb_number'])
            elif doc_type.document_type in ['contract'] and metadata_property_hashmap['contract_number'] not in doc_type.metadata_properties:
                doc_type.metadata_properties.append(metadata_property_hashmap['contract_number'])
        db.session.commit()
        print '\t\tLinking fixture executed successfully'

def add_documents(all_document_types = [], all_metadata_properties = []):
    print '\tAdding the Documents:'
    all_documents = Document.query.all()
    if len(all_documents) is 0:
        document_types_hashmap = {}
        for document_type in all_document_types:
            document_types_hashmap[document_type.document_type] = document_type
        metadata_property_hashmap = {}
        for metadata_property in all_metadata_properties:
            metadata_property_hashmap[metadata_property.property_name] = metadata_property

        # add documents
        for x in range(0,20):
            document_type = document_types_hashmap['protocol']
            if x % 3 == 0:
                document_type = document_types_hashmap['consent']
            elif x % 4 == 0:
                document_type = document_types_hashmap['contract']
            doc = Document(document_type, '/path/to/document/', 'document{0}.pdf'.format(x))
            db.session.add(doc)
            db.session.commit()
            # add the metadata_property_value
            table_name = metadata_property_hashmap['contract_number'].dynamic_table_name
            if document_type.document_type in ['protocol','consent']:
                table_name = metadata_property_hashmap['irb_number'].dynamic_table_name
            sql = '''
                INSERT INTO {0} (document_id,metadata_property_value)
                VALUES ({1}, '{2}')
            '''.format(table_name, doc.id, int(math.floor(random.random()*100000000)))
            results = db.engine.execute(sql)
            print results.lastrowid

        all_documents = Document.query.all()
        print '\t\tDocuments fixture executed successfully, {0} added'.format(len(all_documents))
    else:
        print '\t\tDocuments fixture was already executed, {0} documents exists'.format(len(all_documents))
    return all_documents
