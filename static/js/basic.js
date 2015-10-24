jQuery(document).ready(function($) {

  $('#air_lines :checkbox').prop('checked', true);

  FilterJS(results, "#service_list", {
    template: '#template',
    criterias:[
      {field: 'CARRIER', ele: '#air_lines :checkbox'}
              ],
      search: { ele: '#search_box' }
  });

});
