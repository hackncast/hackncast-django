//=include src/js/user/base.js

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
