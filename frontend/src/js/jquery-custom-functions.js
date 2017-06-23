(function($) {

  $.fn.slideTo = function(to, reverse=false, delay=310) {
    var direction;
    if (reverse) {
      direction = 'slide left';
    } else {
      direction = 'slide right';
    }
    $(this).transition(direction);

    setTimeout(function() {
      if (reverse) {
        direction = 'slide right';
      } else {
        direction = 'slide left';
      }
      $(to).transition({
        animation: direction,
        onComplete: function() {
          $(to).find('input').filter(':visible:first').focus();
        }
      });
    }, delay);
    return this;
  };

  $.fn.toggleLoading = function(inverted=false, text='Por favor, aguarde...') {
    var dimmer = $(this).find('.ui.dimmer');
    if (dimmer.length == 0) {
      var loader_wrapper = $('<div/>');
      if (inverted) {
        loader_wrapper.addClass('ui active inverted dimmer');
      } else {
        loader_wrapper.addClass('ui active dimmer');
      }
      var text_wrapper = $('<div/>').addClass('ui text loader').html(text);
      $(this).prepend(loader_wrapper.html(text_wrapper));
    } else {
      dimmer.remove();
    }
  };

}(jQuery));
