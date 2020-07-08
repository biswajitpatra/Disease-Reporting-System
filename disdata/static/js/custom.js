(function($) {

  // Add smooth scrolling to all links in navbar
  $(".navbar a,a.btn-appoint, .quick-info li a, .overlay-detail a").on('click', function(event) {

    var hash = this.hash;
    if (hash) {
      event.preventDefault();
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 900, function() {
        window.location.hash = hash;
      });
    }

  });

  $(".navbar-collapse a").on('click', function() {
    $(".navbar-collapse.collapse").removeClass('in');
  });

  //jQuery to collapse the navbar on scroll
  $(window).scroll(function() {
    if ($(".navbar").offset().top > 500) {
      $(".navbar-fixed-top").addClass("top-nav-collapse");
      $('.navbar').css('background-color','rgba(28,74,90, .96)');
    } else {
      $(".navbar-fixed-top").removeClass("top-nav-collapse");
      $('.navbar').css('background-color','transparent');
    }
  });

})(jQuery);
