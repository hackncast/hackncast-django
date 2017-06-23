//=include src/js/user/base.js


$(document).ready(function() {
  $('.resend-button').api({
    action: 'add email',
    method: 'POST',
    data: {
      action_send: '',
      csrfmiddlewaretoken: csrftoken
    },
    beforeSend: function(settings) {
      settings.data.email = $(this).data('email');
      return settings;
    },
    onResponse: function(response) {
      window.location.href = response.location;
      return response;
    },
  });

  $('.remove-button').api({
    action: 'add email',
    method: 'POST',
    data: {
      action_remove: '',
      csrfmiddlewaretoken: csrftoken
    },
    beforeSend: function(settings) {
      settings.data.email = $(this).data('email');
      return settings;
    },
    onResponse: function(response) {
      window.location.href = response.location;
      return response;
    }
  });

  $('.primary-email-checkbox').checkbox().api({
    action: 'add email',
    method: 'POST',
    data: {
      action_primary: '',
      csrfmiddlewaretoken: csrftoken
    },
    beforeSend: function(settings) {
      settings.data.email = $(this).find('input').val();
      return settings;
    },
    onResponse: function(response) {
      window.location.href = response.location;
      return response;
    },
  });
});
