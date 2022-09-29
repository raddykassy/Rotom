$(window).on('scroll load', function(){
  var scroll = $(this).scrollTop();
  var windowHeight = $(window).height();
  $('.fadeIn').each(function(){
    var cntPos = $(this).offset().top;
    if(scroll > cntPos - windowHeight + windowHeight / 3){
      $(this).addClass('active');
    }
  });
});