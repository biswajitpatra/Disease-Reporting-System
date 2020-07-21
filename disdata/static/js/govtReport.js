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
      removeAdd(firstElement, 'close', 'open');
  
      initTimeout();
    };
  
    const _next = () => {
      const sibling = active.nextElementSibling;
      if (sibling) {
        removeAdd(active, 'open', 'close');
        removeAdd(sibling, 'close', 'open');
  
        active = sibling;
      } else {
        removeAdd(active, 'open', 'close');
        removeAdd(firstElement, 'close', 'open');
  
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
  
  
  $('#stop').on('click', function () {
    scroll.stop();
  });