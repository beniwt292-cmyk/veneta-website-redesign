document.querySelectorAll('#yr').forEach(function(e){e.textContent=new Date().getFullYear();});
function openNav(){document.getElementById('mnav').classList.add('on');document.body.style.overflow='hidden';}
function closeNav(){document.getElementById('mnav').classList.remove('on');document.body.style.overflow='';}
document.querySelectorAll('.mnav a').forEach(function(a){a.addEventListener('click',closeNav);});
addEventListener('keydown',function(e){if(e.key==='Escape')closeNav();});
var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target);}})},{threshold:.12});
document.querySelectorAll('.rev').forEach(function(el,i){el.style.transitionDelay=(i%4*60)+'ms';io.observe(el);});
var bar=document.getElementById('sticky');
if(bar){addEventListener('scroll',function(){var p=scrollY/(document.body.scrollHeight-innerHeight);bar.classList.toggle('on',p>0.12&&p<0.94);},{passive:true});}
document.querySelectorAll('.chip').forEach(function(c){c.addEventListener('click',function(){c.setAttribute('aria-pressed',c.getAttribute('aria-pressed')==='true'?'false':'true');});});
document.querySelectorAll('form[data-mock]').forEach(function(f){f.addEventListener('submit',function(e){e.preventDefault();var n=f.querySelector('.mockmsg');if(n){n.hidden=false;}});});
document.querySelectorAll('.gal-thumbs button').forEach(function(b){b.addEventListener('click',function(){var m=document.getElementById('gal-main');if(m){m.src=b.dataset.src;m.alt=b.dataset.alt||m.alt;}});});
