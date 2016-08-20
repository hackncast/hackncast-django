//=include src/vendor/jquery/jquery-3.1.0.min.js
//=include dist/semantic/components/form.min.js
//=include dist/semantic/components/transition.min.js

$(document).ready(function() {
  $('.ui.form').form({
    fields: {
      email: {
        identifier  : 'email',
        rules: [
        {
          type   : 'email',
          prompt : 'Por favor, informe um email válido'
        }
        ]
      }
    }
  });
});

