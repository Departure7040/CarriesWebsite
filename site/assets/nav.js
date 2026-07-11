(function(){
  var drops=document.querySelectorAll('.has-drop>a');
  for(var i=0;i<drops.length;i++){
    drops[i].addEventListener('click',function(e){
      var isCoarse=window.matchMedia&&window.matchMedia('(pointer: coarse)').matches;
      var narrow=window.innerWidth<=720;
      if(!(isCoarse||narrow))return; // desktop mouse: hover handles it, click navigates
      var item=this.parentNode;
      if(!item.classList.contains('open')){
        e.preventDefault();
        var open=document.querySelectorAll('.has-drop.open');
        for(var j=0;j<open.length;j++)open[j].classList.remove('open');
        item.classList.add('open');
      } // second tap follows the link
    });
  }
  document.addEventListener('click',function(e){
    if(!e.target.closest||!e.target.closest('.has-drop')){
      var open=document.querySelectorAll('.has-drop.open');
      for(var j=0;j<open.length;j++)open[j].classList.remove('open');
    }
  });
})();
