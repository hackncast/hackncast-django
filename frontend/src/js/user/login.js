//=include src/js/base.js

$(document).ready(function() {
  $('.ui.form').form({
    fields: {
      email: {
        identifier  : 'login',
        rules: [
        {
          type   : 'email',
          prompt : 'Por favor, informe um email válido'
        }
        ]
      },
      password: {
        identifier  : 'password',
        rules: [
        {
          type   : 'length[6]',
          prompt : 'Sua senha deve possuir pelo menos 6 caracteres'
        }
        ]
      }
    }
  });
  $('.ui.checkbox').checkbox();
});
