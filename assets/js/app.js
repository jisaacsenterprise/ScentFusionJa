(function(){
'use strict';
var C = window.SFJ || {};
var BASE = (document.body && document.body.getAttribute('data-base')) || '';

/* ---------- safe storage ---------- */
var mem = {};
var store = {
  get:function(k){ try{ var v=localStorage.getItem(k); return v==null?mem[k]:v; }catch(e){ return mem[k]; } },
  set:function(k,v){ mem[k]=v; try{ localStorage.setItem(k,v); }catch(e){} }
};

/* ---------- header ---------- */
var hdr = document.querySelector('.hdr');
function onScroll(){ if(hdr) hdr.classList.toggle('stuck', window.scrollY > 24); }
window.addEventListener('scroll', onScroll, {passive:true}); onScroll();

var burger = document.querySelector('.burger'), nav = document.querySelector('.nav');
if(burger && nav){
  burger.addEventListener('click', function(){
    var open = nav.classList.toggle('open');
    burger.setAttribute('aria-expanded', open);
    document.body.style.overflow = open ? 'hidden' : '';
  });
  nav.addEventListener('click', function(e){
    if(e.target.tagName==='A'){ nav.classList.remove('open'); document.body.style.overflow=''; burger.setAttribute('aria-expanded',false); }
  });
}

/* ---------- reveal ---------- */
var rvs = document.querySelectorAll('.rv');
if('IntersectionObserver' in window && rvs.length){
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); } });
  },{rootMargin:'0px 0px -8% 0px',threshold:.06});
  rvs.forEach(function(el){ io.observe(el); });
} else { rvs.forEach(function(el){ el.classList.add('in'); }); }

/* ---------- money ---------- */
function money(n){ return '$' + Number(n).toLocaleString('en-JM'); }
window.sfjMoney = money;

/* ---------- cart ---------- */
var cart = [];
try{ cart = JSON.parse(store.get('sfj_cart') || '[]') || []; }catch(e){ cart = []; }

function save(){ store.set('sfj_cart', JSON.stringify(cart)); paint(); }
function count(){ return cart.reduce(function(a,i){ return a + i.qty; },0); }
function total(){ return cart.reduce(function(a,i){ return a + i.price*i.qty; },0); }

window.sfjAdd = function(item){
  var k = cart.filter(function(i){ return i.id===item.id && i.variant===item.variant; })[0];
  if(k) k.qty += item.qty; else cart.push(item);
  save(); toast(item.name + ' added'); open();
};
function remove(i){ cart.splice(i,1); save(); }

var scrim = document.querySelector('.scrim'), drawer = document.querySelector('.drawer');
function open(){ if(!drawer) return; drawer.classList.add('on'); scrim.classList.add('on'); document.body.style.overflow='hidden'; }
function close(){ if(!drawer) return; drawer.classList.remove('on'); scrim.classList.remove('on'); document.body.style.overflow=''; }
document.querySelectorAll('[data-cart-open]').forEach(function(b){ b.addEventListener('click', open); });
document.querySelectorAll('[data-cart-close]').forEach(function(b){ b.addEventListener('click', close); });
if(scrim) scrim.addEventListener('click', close);
document.addEventListener('keydown', function(e){ if(e.key==='Escape') close(); });

var BOTTLE = '<svg viewBox="0 0 60 90" aria-hidden="true"><rect x="24" y="4" width="12" height="9" rx="1.5" fill="none" stroke="#efbf00" stroke-width="1.6"/><path d="M27 13h6v6h-6z" fill="none" stroke="#efbf00" stroke-width="1.4"/><rect x="12" y="19" width="36" height="66" rx="4" fill="none" stroke="#efbf00" stroke-width="1.6"/></svg>';

function paint(){
  document.querySelectorAll('.cart-count').forEach(function(el){
    var n = count(); el.textContent = n; el.classList.toggle('on', n>0);
  });
  var body = document.querySelector('.drawer-body'), ft = document.querySelector('.drawer-ft');
  if(!body) return;
  if(!cart.length){
    body.innerHTML = '<div class="empty"><p>Your selection is empty.</p><a class="ul" href="'+BASE+'collection/index.html">Browse the collection</a></div>';
    if(ft) ft.style.display='none';
    return;
  }
  if(ft) ft.style.display='grid';
  body.innerHTML = cart.map(function(i,ix){
    return '<div class="line-item"><div class="li-art">'+BOTTLE+'</div><div><p class="li-name">'+esc(i.name)+'</p>'+
      '<span class="li-meta">'+esc(i.variant)+' · Qty '+i.qty+'</span><br><a class="li-rm" href="#" data-rm="'+ix+'">Remove</a></div>'+
      '<div class="li-price">'+money(i.price*i.qty)+'</div></div>';
  }).join('');
  body.querySelectorAll('[data-rm]').forEach(function(a){
    a.addEventListener('click', function(e){ e.preventDefault(); remove(+a.dataset.rm); });
  });
  var t = document.querySelector('[data-cart-total]'); if(t) t.textContent = money(total());
}
function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); }

/* WhatsApp order */
function waLink(){
  var lines = cart.map(function(i){ return '• '+i.name+' ('+i.variant+') ×'+i.qty+' — '+money(i.price*i.qty); });
  var msg = 'Hello Scent Fusion Jamaica — I would like to place an order:\n\n' + lines.join('\n') +
            '\n\nTotal: ' + money(total()) + '\n\nName:\nDelivery address:';
  return 'https://wa.me/' + C.whatsapp + '?text=' + encodeURIComponent(msg);
}
var waBtn = document.querySelector('[data-wa-order]');
if(waBtn) waBtn.addEventListener('click', function(e){ e.preventDefault(); if(!cart.length) return; window.open(waLink(),'_blank','noopener'); });

var payBtn = document.querySelector('[data-card-pay]');
if(payBtn){
  if(C.checkoutUrl){ payBtn.href = C.checkoutUrl; payBtn.target='_blank'; payBtn.rel='noopener'; }
  else { payBtn.style.display='none'; }
}

/* toast */
var tEl;
function toast(msg){
  if(!tEl){ tEl = document.createElement('div'); tEl.className='toast'; document.body.appendChild(tEl); }
  tEl.textContent = msg; tEl.classList.add('on');
  clearTimeout(tEl._t); tEl._t = setTimeout(function(){ tEl.classList.remove('on'); }, 2400);
}
paint();

/* ---------- collection filters ---------- */
var gridEl = document.querySelector('[data-collection]');
if(gridEl){
  var cards = Array.prototype.slice.call(gridEl.querySelectorAll('[data-card]'));
  var state = { wear:'all', family:'all', q:'' };
  var params = new URLSearchParams(location.search);
  if(params.get('family')) state.family = params.get('family');
  if(params.get('wear')) state.wear = params.get('wear');

  function apply(){
    var shown = 0;
    cards.forEach(function(c){
      var okW = state.wear==='all' || c.dataset.wear===state.wear || (state.wear!=='unisex' && c.dataset.wear==='unisex');
      var okF = state.family==='all' || c.dataset.family===state.family;
      var okQ = !state.q || c.dataset.search.indexOf(state.q) > -1;
      var ok = okW && okF && okQ;
      c.style.display = ok ? '' : 'none';
      if(ok) shown++;
    });
    var cEl = document.querySelector('[data-count]');
    if(cEl) cEl.textContent = shown + (shown===1?' fragrance':' fragrances');
    var none = document.querySelector('[data-none]');
    if(none) none.style.display = shown ? 'none' : 'block';
  }
  document.querySelectorAll('[data-filter]').forEach(function(b){
    var g = b.dataset.filter, v = b.dataset.value;
    if(state[g]===v) b.setAttribute('aria-pressed','true');
    b.addEventListener('click', function(){
      state[g] = v;
      document.querySelectorAll('[data-filter="'+g+'"]').forEach(function(x){ x.setAttribute('aria-pressed', x===b); });
      apply();
    });
  });
  var s = document.querySelector('[data-search]');
  if(s) s.addEventListener('input', function(){ state.q = s.value.toLowerCase().trim(); apply(); });
  apply();
}

/* ---------- PDP ---------- */
var pdp = document.querySelector('[data-pdp]');
if(pdp){
  var qty = 1;
  var qEl = pdp.querySelector('[data-qty]');
  pdp.querySelectorAll('[data-qty-btn]').forEach(function(b){
    b.addEventListener('click', function(){
      qty = Math.max(1, Math.min(99, qty + (b.dataset.qtyBtn==='+'?1:-1)));
      if(qEl) qEl.textContent = qty;
    });
  });
  var addBtn = pdp.querySelector('[data-add]');
  if(addBtn) addBtn.addEventListener('click', function(){
    var sel = pdp.querySelector('input[name="variant"]:checked');
    window.sfjAdd({
      id: pdp.dataset.pdp, name: pdp.dataset.name,
      variant: sel ? sel.dataset.label : 'Glass 10ml',
      price: sel ? +sel.value : 3600, qty: qty
    });
  });
}

/* ---------- quick add from cards ---------- */
document.querySelectorAll('[data-quick-add]').forEach(function(b){
  b.addEventListener('click', function(e){
    e.preventDefault(); e.stopPropagation();
    window.sfjAdd({ id:b.dataset.id, name:b.dataset.name, variant:'Glass 10ml', price:+b.dataset.price, qty:1 });
  });
});

/* ---------- forms → WhatsApp ---------- */
document.querySelectorAll('form[data-wa-form]').forEach(function(f){
  f.addEventListener('submit', function(e){
    e.preventDefault();
    var d = new FormData(f), out = [];
    d.forEach(function(v,k){ if(String(v).trim()) out.push(k + ': ' + v); });
    var msg = f.dataset.waForm + '\n\n' + out.join('\n');
    window.open('https://wa.me/'+C.whatsapp+'?text='+encodeURIComponent(msg), '_blank', 'noopener');
    var ok = f.querySelector('[data-sent]');
    if(ok) ok.style.display='block';
  });
});

/* ---------- year ---------- */
document.querySelectorAll('[data-year]').forEach(function(el){ el.textContent = new Date().getFullYear(); });
})();
