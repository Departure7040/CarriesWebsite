(function(){
  var parents=document.querySelectorAll('.has-drop>a');
  for(var i=0;i<parents.length;i++){
    parents[i].setAttribute('aria-haspopup','true');
    parents[i].setAttribute('aria-expanded','false');
  }
  function setOpen(item, open){
    var link=item.querySelector(':scope>a');
    if(open){
      item.classList.add('open');
    } else {
      item.classList.remove('open');
    }
    if(link) link.setAttribute('aria-expanded', open ? 'true' : 'false');
  }
  function closeAll(except){
    var open=document.querySelectorAll('.has-drop.open');
    for(var j=0;j<open.length;j++){
      if(open[j]!==except) setOpen(open[j], false);
    }
  }
  for(var i=0;i<parents.length;i++){
    parents[i].addEventListener('click',function(e){
      var isCoarse=window.matchMedia&&window.matchMedia('(pointer: coarse)').matches;
      var narrow=window.innerWidth<=720;
      if(!(isCoarse||narrow))return; // desktop mouse: hover handles it, click navigates
      var item=this.parentNode;
      if(!item.classList.contains('open')){
        e.preventDefault();
        closeAll(item);
        setOpen(item, true);
      } // second tap follows the link
    });
  }
  document.addEventListener('click', function(e){
    if(!e.target.closest||!e.target.closest('.has-drop')){
      closeAll(null);
    }
  });
  document.addEventListener('keydown', function(e){
    if(e.key!=='Escape' && e.key!=='Esc') return;
    var open=document.querySelectorAll('.has-drop.open');
    if(!open.length) return;
    for(var j=0;j<open.length;j++){
      var link=open[j].querySelector(':scope>a');
      setOpen(open[j], false);
      if(link) link.focus();
    }
  });
})();
