//=include src/js/base.js
//=include dist/semantic/components/visibility.min.js
//=include dist/semantic/components/api.min.js
//=include dist/semantic/components/dropdown.min.js

$(document).ready(function() {
  $('.remove-social-account').api({
    action: 'social connections',
    method: 'POST',
    data: {
      //account: '3',
      csrfmiddlewaretoken: csrftoken
    },
    beforeSend: function(settings) {
      settings.data.account = $(this).data('record-id');
      return settings;
    },
    onResponse: function(response) {
      window.location.href = response.location;
      return response;
    },
  });
});
