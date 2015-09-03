import json
from app import db
from models import DocumentType, Document, MetadataProperty
from flask import Blueprint, jsonify, request
api_blueprint = Blueprint('api', __name__, url_prefix='/api')

@api_blueprint.route('/documents')
def documents():
    '''
    Fetch all the documents
    '''
    # TODO: get each documents' metadata properties

    documents = Document.query.all()
    document_list = map(Document.to_json, documents)
    # retrieve the metadata properties
    document_list = retrieve_metadata_properties(document_list)
    return jsonify({
        'data': {
            'count': len(document_list),
            'results': document_list
        },
        'success': True,
    })

@api_blueprint.route('/search')
def search():
    '''
    Search for the documents
    '''
    # TODO: provide a default set of request arguments
    # TODO: limit the search results

    # get the request params
    debug = False
    operator = request.args.get('op') or 'OR'
    document_types = request.args.get('document_types') or 'all'
    query = request.args.get('query') or ''

    # fetch the documents
    document_list = []

    # lets build a select query
    documents_query = Document.query

    # filter by document type
    if document_types != 'all':
        print json.dumps(document_types)
        document_types_list = document_types.split(',')
        if len(document_types_list) > 0:
            documents_query = documents_query.join(Document.document_type)
            for document_type in document_types_list:
                documents_query = documents_query.filter(DocumentType.document_type == document_type)

    # filter by search query
    # TODO: this is a hack, fix to use join methods from dynamic classes
    if query != '':
        query_list = query.split(';')
        if len(query_list) > 0:
            # query_list = map(lambda q: q.split(':'), query_list)
            query_list = map(process_search_query, query_list)
            document_id_list = []
            for query_item in query_list:
                metadata_property = MetadataProperty.query.filter(MetadataProperty.property_name == query_item['property']).first()
                initial_sql = '''
                    SELECT
                        {0}.document_id
                    FROM
                        {0}
                        LEFT JOIN documents ON documents.id = {0}.document_id
                '''.format(metadata_property.dynamic_table_name)
                if document_types != 'all':
                    sql = '''
                        {0}
                            LEFT JOIN document_types ON document_types.id = documents.document_type_id
                        WHERE
                            document_types.document_type IN ('{1}')
                            AND {2}.metadata_property_value IN ('{3}')
                    '''.format(initial_sql,
                                '\',\''.join(document_types.split(',')),
                                metadata_property.dynamic_table_name,
                                '\',\''.join(query_item['value']))
                else:
                    sql = '''
                        {0}
                        WHERE
                            {1}.metadata_property_value IN ('{2}')
                    '''.format(initial_sql,
                                metadata_property.dynamic_table_name,
                                '\',\''.join(query_item['value']))
                result = db.engine.execute(sql)
                for row in result.fetchall():
                    document_id_list.append(row[0])

            # search for all these document.id's
            # TODO: Fix this warning by not filtering if no document.id's matched
            # WARNING: SAWarning: The IN-predicate on "documents.id" was invoked
            #   with an empty sequence. This results in a contradiction,
            #   which nonetheless can be expensive to evaluate.
            #   Consider alternative strategies for improved performance.
            documents_query = documents_query.filter(Document.id.in_(document_id_list))

    # fetch all the documents based on search
    documents = documents_query.all()
    # DEBUG:
    # print documents_query.label('')
    document_list = map(Document.to_json, documents)
    # retrieve the metadata properties
    document_list = retrieve_metadata_properties(document_list)

    return jsonify({
        'debug': debug,
        'data': {
            'count': len(document_list),
            'results': document_list
        },
        'request': {
            'document_types': document_types,
            'query': query,
            'op': operator
        },
        'success': True,
    })

@api_blueprint.route('/config')
def config():
    '''
    Get all the config settings
    '''
    document_types = DocumentType.query.all()
    document_type_list = map(DocumentType.to_json, document_types)
    return jsonify({
        'data': {
            'count': len(document_type_list),
            'results': document_type_list
        },
        'success': True,
    })

def process_search_query(q):
    return_hashmap = {}
    split_list = q.split(':')
    return_hashmap['property'] = split_list[0]
    return_hashmap['value'] = split_list[1].split(',')
    return return_hashmap

def retrieve_metadata_properties(document_list):
    document_id_list = map(lambda d: str(d['id']), document_list)
    document_id_sql_list = ','.join(document_id_list)
    all_metadata_properties = MetadataProperty.query.all()
    sql_list = []
    for metadata_property in all_metadata_properties:
        sql = '''
            SELECT
                {0}.document_id,
                {0}.metadata_property_value,
                '{1}' as property_name
            FROM
                {0}
            WHERE
                {0}.document_id IN ({2})
        '''.format(metadata_property.dynamic_table_name, metadata_property.property_name, document_id_sql_list)
        sql_list.append(sql)
    document_metadata_properties = {}
    if len(sql_list) > 0:
        union_sql = ' UNION '.join(sql_list)
        result = db.engine.execute(union_sql)
        for row in result.fetchall():
            if row[0] not in document_metadata_properties:
                document_metadata_properties[row[0]] = []
            document_metadata_properties[row[0]].append({
                'property_name': row[2],
                'metadata_property_value': row[1],
            })
    new_document_list = []
    for document in document_list:
        new_document = document
        new_document['metadata_properties'] = []
        if document_metadata_properties[new_document['id']]:
            new_document['metadata_properties'] = document_metadata_properties[new_document['id']]
        new_document_list.append(new_document)
    return new_document_list
