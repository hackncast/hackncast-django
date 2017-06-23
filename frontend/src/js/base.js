//=include vendor/jquery/jquery-3.1.1.js
//=include vendor/semantic-ui/components/api.js
//=include vendor/semantic-ui/components/form.js
//=include vendor/semantic-ui/components/transition.js
//=include vendor/jquery/jquery.jgrowl.js
//=include src/js/jquery-custom-functions.js

$.fn.api.settings.successTest = function(response) {
  if(response && response.success) {
    return response.success;
  }
  return false;
};

$.fn.api.settings.className = {
  loading : 'disabled loading',
  error   : 'error'
};
