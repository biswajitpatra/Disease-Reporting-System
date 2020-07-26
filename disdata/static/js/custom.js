(function($) {

  //* Add smooth scrolling to all links in navbar
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
  

  //*jQuery to collapse the navbar on scroll
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

$('document').ready(function () {


  // RESTYLE THE DROPDOWN MENU
  $('#google_translate_element').on("click", function () {
  
      // Change font family and color
      $("iframe").contents().find(".goog-te-menu2-item div, .goog-te-menu2-item:link div, .goog-te-menu2-item:visited div, .goog-te-menu2-item:active div, .goog-te-menu2 *")
          .css({
              'color': '#544F4B',
              'font-family': 'Roboto',
              'width':'100%'
          });
      // Change menu's padding
      $("iframe").contents().find('.goog-te-menu2-item-selected').css ('display', 'none');
    
      // Change menu's padding
      $("iframe").contents().find('.goog-te-menu2').css ('padding', '0px');
    
      // Change the padding of the languages
      $("iframe").contents().find('.goog-te-menu2-item div').css('padding', '20px');
    
      // Change the width of the languages
      $("iframe").contents().find('.goog-te-menu2-item').css('width', '100%');
      $("iframe").contents().find('td').css('width', '100%');
    
      // Change hover effects
      $("iframe").contents().find(".goog-te-menu2-item div").hover(function () {
          $(this).css('background-color', '#4385F5').find('span.text').css('color', 'white');
      }, function () {
          $(this).css('background-color', 'white').find('span.text').css('color', '#544F4B');
      });
  
      // Change Google's default blue border
      $("iframe").contents().find('.goog-te-menu2').css('border', 'none');
  
      // Change the iframe's box shadow
      $(".goog-te-menu-frame").css('box-shadow', '0 16px 24px 2px rgba(0, 0, 0, 0.14), 0 6px 30px 5px rgba(0, 0, 0, 0.12), 0 8px 10px -5px rgba(0, 0, 0, 0.3)');
      
    
    
      // Change the iframe's size and position?
      $(".goog-te-menu-frame").css({
          'height': '100%',
          'width': '100%',
          'top': '0px'
      });
      // Change iframes's size
      $("iframe").contents().find('.goog-te-menu2').css({
          'height': '100%',
          'width': '100%'
      });
  });
  });

   // array describing the news' categories
   const categories = ['all', 'news', 'updates', 'maintenance', 'events', 'important'];
   // array describing the colors matching the categories
   const colors = ['#66d7ee', '#66a1ee', '#7166ee', '#a866ee', '#ee66aa', '#ee6d66'];
   
   // array describing the navigation's items through the category and color
   const navItems = categories.map((category, index) => ({
     category,
     color: colors[index],
   }));
   
   
   // date used to establish the age of the news items
   const latestDate = new Date();
   // filler text used fo the news
   const fillerTitle = 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Error, saepe';
   
   // number of items for each news' category, sans the first one
   const limit = 5;
   // array describing every piece of news
   // the idea is to have _limit_ number of news for each category, sans the first one
   const data = [];
   
   // for every navigation item sans the first one include _limit_ number of news in the data array
   navItems.slice(1).forEach(({ category, color }) => {
     for (let i = 0; i < limit; i += 1) {
       // specify the category, color according to the navigation item
       // use the latest date to find an earlier date instance
       // use the filler text for the title
       const date = new Date(latestDate - (1000 * 60 * 60 * 24) * (Math.ceil(Math.random() * 100)));
       data.push({
         category,
         color,
         date,
         title: fillerTitle,
       });
     }
   });
   // console.log(data);
   // function called when clicking the button elements, with the selected category
   function showNews(selectedCategory) {
     // if matching the first cateogry, display the latest news
     if (selectedCategory === 'all') {
       addNews(latestNews);
     } else {
       // else retrieve the news items matching the selected category
       const specificNews = data.filter(({ category }) => category === selectedCategory);
       // add the news through the appropriate function
       addNews(specificNews);
     }
   }
   // ADD NAVIGATION ITEMS
   const boardNav = document.querySelector('.board__nav');
   // specify a showNews() function passing as argument the specific cateogry
   // specify the background with a slightly transparent version of the chosen color
   boardNav.innerHTML = navItems.map(({ category, color }) => `
     <button onclick="showNews('${category}')" class="nav--item ${category === 'all' && 'active'}" style="background: ${color}44">
       ${category}
     </button>
   `).join('');
   
   // function _adding_ the news in the .board__news element
   // accepting as argument an array of news items
   function addNews(news) {
     const boardNews = document.querySelector('.board__news');
   
     // include the first five items of the input array
     //  include the theme color as a solid border
     boardNews.innerHTML = news.slice(0, 5).map(({ color, date, title }) => `
     <a class="news--item" href="#" style="border-left: 4px solid ${color}">
         <p class="date">
             ${date.toDateString()}
         </p>
         <p class="title">
             ${title}
         </p>
     </a>
     `).join('');
   }
   // sort the data
   //  this ultimately _mutates_ the data array, sorting the elements in place
   // this is actually useful to always include the latest news no matter the category
   const latestNews = data.sort(({ date: dateA }, { date: dateB }) => (dateA > dateB ? -1 : 1));
   // immediately call the function with the most recent news items
   addNews(latestNews);
   
