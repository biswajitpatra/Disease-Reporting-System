const TickerScrolling = function ({ id = '#newsticker', time = 3000, typeChild = 'li' } = {}) {
    let i = 0;
    let active;
    let interval;
  
    const el = () => document.querySelectorAll(id)[0];
    const firstElement = el().querySelectorAll(typeChild)[0];
    const addClass = (el, _class) => {
      if (el.classList) {
        el.classList.add(_class);
      } else {
        el.className += ' ' + _class;
      }
    };
    const removeClass = (el, _class) => {
      if (el.classList) {
        el.classList.remove(_class);
      } else {
        el.className = el.className.replace(new RegExp('(^|\\b)' + _class.split(' ').join('|') + '(\\b|$)', 'gi'), ' ');
      }
    };
    const removeAdd = (el, _remove, _add) => {
      removeClass(el, _remove);
      addClass(el, _add);
    };
  
    const init = () => {
      active = firstElement;
      removeAdd(firstElement, 'closed', 'opened');
  
      initTimeout();
    };
  
    const _next = () => {
      const sibling = active.nextElementSibling;
      if (sibling) {
        removeAdd(active, 'opened', 'closed');
        removeAdd(sibling, 'closed', 'opened');
  
        active = sibling;
      } else {
        removeAdd(active, 'opened', 'closed');
        removeAdd(firstElement, 'closed', 'opened');
  
        active = firstElement;
      }
    };
  
    const initTimeout = () => {
      interval = setInterval(_next, time);
    };
  
    init();
  
    return {
      numberElement: function () {
        return el().querySelectorAll(typeChild).length;
      },
      stop: function () {
        clearInterval(interval);
      } };
  
  
  };
  
  const scroll = new TickerScrolling({
    id: '#newsticker',
    typeChild: 'li' });


   // Add, remove, modify your articles here
   document.addEventListener("DOMContentLoaded", function() {
    var articles = [
      {
        onClickLink: 'https://www.devex.com/news/opinion-tobacco-is-a-huge-health-threat-so-why-aren-t-we-doing-more-about-it-93468',
        imgageSource: 'https://res.cloudinary.com/devex/image/fetch/c_scale,f_auto,q_auto,w_720/https://lh4.googleusercontent.com/o0FzC9DUDq79XtqcmQElvPANasuL8vcBjIW1doqmanM-CuU1FEuzirwJvxmrlr9Vmi5BP4CeeA5HG7PgUYW_fEO7Te9b2b0Ys4k4BmCi-FyTiPR2hjSri9v-ncCilhU_o9WE__yi',
        title: 'Opinion: Tobacco is a huge health threat. So why aren’t we doing more about it?'
      },
      {
        onClickLink: 'https://www.devex.com/news/opinion-early-detection-and-diagnosis-a-critical-link-for-effective-ncd-management-92060',
        imgageSource: 'https://res.cloudinary.com/devex/image/fetch/c_scale,f_auto,q_auto,w_720/https://lh5.googleusercontent.com/Dij42vNfp4N7KssfL1Ne64VfFm2oQtsRlbRS7zI2M4iNOT20jnNQf04UrNZ_DcpeWEky1RptDKGnzoJ65V5hW5r3w9S9c4oYyv40m1oPuCbkfzIWZjeiVbjLoWB5g6xU7fA3IVyQ',
        title: 'Opinion: Early detection and diagnosis a critical link for effective NCD management'
      },
      {
        onClickLink: 'https://www.devex.com/news/un-meeting-on-ncds-falls-short-on-hard-commitments-civil-society-say-93547',
        imgageSource: 'https://res.cloudinary.com/devex/image/fetch/c_scale,f_auto,q_auto,w_720/https://lh4.googleusercontent.com/gm_hqLcLPViTWnN7FNPnMRGfeMZhUTB88CGVSVpl-6DXKEOILXOCfpwRmlR81ES2UzC-7faa18GjbizLjtpDKdTTyHilTXgiM5VC9rizSh0ljKuWylxOLPP6Sp40LHYo6fIyXjzb',
        title: 'UN meeting on NCDs falls short on hard commitments, civil society say'
      },
      {
        onClickLink: 'https://www.devex.com/news/how-colombia-battled-big-tobacco-and-won-93451',
        imgageSource: 'https://res.cloudinary.com/devex/image/fetch/c_scale,f_auto,q_auto,w_720/https://lh4.googleusercontent.com/p6vNHWwclj-G91CxkAprWl9f2-6qVVNYah9rLrTLbQLMUysxBh34w4VVEVJWL_oWjVeuLfWAJmIpGzpAQ1RYxbDtX9OSVj67DLtl7vQFjWnzGuVHZXwVOmzAcXHWObKj24IUxcY5',
        title: 'How Colombia battled big tobacco and won'
      },
      {
        onClickLink: 'https://www.devex.com/news/opinion-investing-in-ncd-prevention-to-finance-sustainable-development-92776',
        imgageSource: 'https://lh6.googleusercontent.com/B1qQtuj1Lw1bejRKljOl-Ig4KAprpyVEkSlVUyoatJk7Mm0F8lv7ROiINq1eJbNeWXLkcROhIz97eiOoHQg3FVG1gwt8pR9pDD7E1OFdEPnvVajVnMPh48N7W6RvIlzBr0QKycOT',
        title: 'Opinion: Investing in NCD prevention to finance sustainable development'
      },
      {
        onClickLink: 'https://www.devex.com/news/communicating-noncommunicable-diseases-93049',
        imgageSource: 'https://res.cloudinary.com/devex/image/fetch/c_scale,f_auto,q_auto,w_720/https://lh4.googleusercontent.com/jBjpaTtHhy9V0Q-luk4NdrwZDCz_ZxsVsqoqGwzsATGhDWcqIAgMQdG-ixkV5qpc7cIpcu_2VgLP_PzLnx_1DJPnm0ACjqih5ogjF840VjHYc60wGzj99xLd0BMoE7Wmx-74pfgF',
        title: 'Communicating noncommunicable diseases'
      }
    ]

    var rootElement = document.getElementById("imageGalleryWithTitle");

    for (let i=0; i < articles.length; i++) {
      //Create the container
      var itemContainer = document.createElement("a");
      itemContainer.classList.add("article-container","text-decoration-none");
      var href = document.createAttribute("href");
      href.value = articles[i].onClickLink;
      itemContainer.setAttributeNode(href);
      var target = document.createAttribute("target");
      target.value = '_blank';
      itemContainer.setAttributeNode(target);

      //Create Image
      var image = document.createElement("img");
      image.classList.add("article-image");
      var src = document.createAttribute("src");
      src.value = articles[i].imgageSource;
      image.setAttributeNode(src);
      var alt = document.createAttribute("alt");
      alt.value = articles[i].title;
      image.setAttributeNode(alt);

      //Create title
      var h3 = document.createElement("h3");
      h3.classList.add("article-title");
      var h3Text = document.createTextNode(articles[i].title);
      h3.appendChild(h3Text);

      //Atach image and title to container
      itemContainer.appendChild(image);
      itemContainer.appendChild(h3);

      //Attach element to root div
      rootElement.appendChild(itemContainer);
    }
  });

  var ticker = document.querySelector('.ticker')
  , list = document.querySelector('.ticker__list')
  , clone = list.cloneNode(true)

ticker.append(clone)