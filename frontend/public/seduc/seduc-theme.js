(function(){
var V='10';
var P=location.pathname;
var MINHAS=/\/(inscricao-realizada|pagamento-pix)(\.html)?\/?$/.test(P);
var BASE=':host{all:initial;display:block;font-family:"Open Sans",Helvetica,Arial,sans-serif;font-size:14px;line-height:1.42857;color:#333;text-align:left}'+
'.vn-wrap{font-size:14px}'+
'.vn-minhas{display:inline-flex;align-items:center;gap:7px;background:#1172db;color:#fff!important;text-decoration:none!important;font:700 12px "Open Sans",Arial,sans-serif;text-transform:uppercase;padding:10px 14px;border-radius:2px;white-space:nowrap}'+
'.vn-minhas:hover{background:#0b4f9c}'+
'.vn-minhas-box{position:absolute;right:15px;top:50%;transform:translateY(-50%);z-index:5}'+
'@media(min-width:992px){.vn-minhas-box{right:auto;left:calc(50% + 370px)}}';
function fontsLink(){
 if(document.getElementById('vn-fonts'))return;
 var l=document.createElement('link');l.id='vn-fonts';l.rel='stylesheet';l.href='/vunesp/fonts.css?v='+V;document.head.appendChild(l);
}
function host(id,html,atTop,extra){
 var h=document.createElement('div');h.id=id;
 h.style.cssText='display:block;width:100%;position:relative;z-index:'+(atTop?'9999':'100')+';visibility:hidden;';
 if(atTop)document.body.insertBefore(h,document.body.firstChild);else document.body.appendChild(h);
 var r=h.attachShadow({mode:'open'});
 r.innerHTML='<link rel="stylesheet" href="/vunesp/chrome.css?v='+V+'"><style>'+BASE+(extra||'')+'</style><div class="vn-wrap">'+html+'</div>';
 var ln=r.querySelector('link');ln.addEventListener('load',function(){h.style.visibility='visible';});
 setTimeout(function(){h.style.visibility='visible';},2500);
 r.addEventListener('click',function(e){var a=e.target.closest&&e.target.closest('a');if(!a)return;var hr=a.getAttribute('href');if(!hr||hr==='#'){e.preventDefault();}});
 return r;
}
function build(parts){
 if(document.getElementById('seduc-header-host'))return;
 fontsLink();
 var hh=parts.h;
 if(MINHAS){hh=hh.replace('</header>','<div class="vn-minhas-box"><a class="vn-minhas" href="/minhas-inscricoes.html" data-testid="header-minhas-inscricoes-btn">Minhas inscrições</a></div></header>');}
 var r=host('seduc-header-host',hh,true,'header{position:relative}');
 document.querySelectorAll('#aocp-footer,.seduc-footer').forEach(function(el){el.remove();});
 host('vunesp-footer-host',parts.f,false,'#rodape{margin-top:40px}');
}
function go(){
 fetch('/vunesp/parts.json?v='+V).then(function(r){return r.json();}).then(build).catch(function(){});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',go);else go();
})();
