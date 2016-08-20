//=include src/vendor/jquery/jquery-3.1.0.min.js
//=include dist/semantic/components/form.min.js
//=include dist/semantic/components/transition.min.js

$(document).ready(function() {
  $('.ui.form').form({
    fields: {
      password1: {
        identifier  : 'password1',
        rules: [
        {
          type   : 'length[6]',
          prompt : 'Sua senha deve possuir pelo menos 6 caracteres'
        }
        ]
      },
      password2: {
        identifier  : 'password2',
        rules: [
        {
          type   : 'match[password1]',
          prompt : 'As duas senhas devem ser iguais'
        }
        ]
      }
    }
  });
});
