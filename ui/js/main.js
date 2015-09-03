(function($, Handlebars, window, document, undefined){
  var $document_types = $('#document_types'),
    $search_form = $('#search_form'),
    $view = $('#view'),
    document_tpl = Handlebars.compile($('#document-tpl').html());

  function formatDocumentTypes(document_type){
    return {
      id: document_type.document_type,
      text: document_type.document_name
    };
  }

  function process_documents(results){
    var $document_list = $('<div class="document_list"></div>');

    results.forEach(function(doc){
      $document_list.append(document_tpl(doc));
    }.bind(this));

    if(results.length === 0){
      $document_list.append('<em>Sorry, no documents found...</em>');
    }

    $view.html('').append($document_list);
  }

  $search_form.on('submit', function(e){
    e.preventDefault();
    var form_values = $search_form.serializeArray(),
      search_data = {
        document_types: [],
        query: []
      },
      query_obj = {};
    form_values.forEach(function(item){
      if(item.value !== ''){
        if(item.name === 'document_types'){
          search_data.document_types.push(item.value);
        } else {
          if(query_obj.hasOwnProperty(item.name) === false){
            query_obj[item.name] = [];
          }
          query_obj[item.name].push(item.value);
        }
      }
    }.bind(this));

    Object.keys(query_obj).forEach(function(query_key){
      if(query_obj[query_key].length > 0){
        search_data.query.push(query_key + ':' + query_obj[query_key].join(','));
      }
    });

    search_data.document_types = search_data.document_types.join(',');
    if(search_data.document_types === ''){
      search_data.document_types = 'all';
    }
    search_data.query = search_data.query.join(';');

    $.ajax({
      url: '/api/search',
      data: search_data,
      dataType: 'json',
      success: function(res){
        process_documents(res.data.results);
      }.bind(this)
    });

    return false;
  }.bind(this));

  $.get('/api/config', function(res){
    var data = res.data.results.map(formatDocumentTypes);
    // data.unshift({
    //   id:'all',
    //   text:'... ',
    //   disabled: true
    // });
    $document_types.select2({
      data: data,
      placeholder: 'Select document type or empty for all...'
    });
  }.bind(this));

  window.setTimeout(function(){
    $.get('/api/documents', function(res){
      process_documents(res.data.results);
    }.bind(this));
  }.bind(this), 250);

})(jQuery, Handlebars, window, window.document);
