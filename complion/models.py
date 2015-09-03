from app import db

# TODO: make a factory class that returns a model for a dynamic table
# def dynamic_table(tablename):
#     class DT(db.Model):
#         __tablename__ = tablename
#
#         id = db.Column(db.Integer, primary_key=True)
#         document_id = db.Column(db.Integer, db.ForeignKey('documents.id'))
#         document = db.relationship('Document')
#         metadata_value = db.Column(db.String())
#
#         def __init__(self, table_name, document, metadata_value):
#             self.__tablename__ = table_name
#             self.document_id = document.id
#             self.document = document
#             self.metadata_value = metadata_value
#
#         def __repr__(self):
#             return '<id {0} - {1}:{2}>'.format(self.id, self.document, self.metadata_value)
#     return DT

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'))
    document_type = db.relationship('DocumentType')
    file_dir = db.Column(db.String())
    file_name = db.Column(db.String())

    def to_json(self):
        # TODO: return lambda with document_type based on a flag
        return {
            'id': self.id,
            'document_type': self.document_type.to_json(),
            'file_dir': self.file_dir,
            'file_name': self.file_name,
        }

    def __init__(self, document_type, file_dir, file_name):
        self.document_type = document_type
        self.document_type_id = document_type.id
        self.file_dir = file_dir
        self.file_name = file_name

    def __repr__(self):
        return '<id {0} - {1}:{2}>'.format(self.id, self.document_type, self.file_name)


# create a metadata_properties helper table for many-to-many relationships
document_types_x_metadata_properties = db.Table('document_types_x_metadata_properties',
    db.Column('document_type_id', db.Integer, db.ForeignKey('document_types.id')),
    db.Column('metadata_property_id', db.Integer, db.ForeignKey('metadata_properties.id'))
)
# class DocumentTypeProperty(db.Model):
#     __tablename__ = 'document_types_x_metadata_properties'
#
#     document_type_id = db.Column(db.Integer, db.ForeignKey('document_types.id'), primary_key=True)
#     metadata_property_id = db.Column(db.Integer, db.ForeignKey('metadata_properties.id'), primary_key=True)
#     metadata_property = db.relationship('MetadataProperty', backref=db.backref('metadata_property'))


class DocumentType(db.Model):
    __tablename__ = 'document_types'

    id = db.Column(db.Integer, primary_key=True)
    document_type = db.Column(db.String())
    document_name = db.Column(db.String())
    metadata_properties = db.relationship('MetadataProperty', secondary=document_types_x_metadata_properties)
    # metadata_properties = db.relationship('DocumentTypeProperty', backref=db.backref('document_type'))

    def to_json(self):
        # TODO: return lambda with metadata_properties based on a flag
        return {
            'id': self.id,
            'document_type': self.document_type,
            'document_name': self.document_name
        }

    def __init__(self, document_type, document_name):
        self.document_type = document_type
        self.document_name = document_name

    def __repr__(self):
        return '<id {0} - {1}:{2}>'.format(self.id, self.document_type, self.document_name)

class MetadataProperty(db.Model):
    __tablename__ = 'metadata_properties'

    id = db.Column(db.Integer, primary_key=True)
    property_name = db.Column(db.String())
    dynamic_table_name = db.Column(db.String())
    document_types = db.relationship('DocumentType', secondary=document_types_x_metadata_properties)

    def __init__(self, property_name, dynamic_table_name):
        self.property_name = property_name
        self.dynamic_table_name = dynamic_table_name
        # bit o'magic to create dynamic tables on the fly
        db.Table(dynamic_table_name, db.metadata,
            db.Column('id', db.Integer(), primary_key=True),
            db.Column('document_id', db.Integer(), db.ForeignKey('documents.id')),
            db.Column('metadata_property_value', db.String())
        )
        db.metadata.create_all(db.engine)

    def __repr__(self):
        return '<id {0} - {1}:{2}>'.format(self.id, self.property_name, self.dynamic_table_name)
