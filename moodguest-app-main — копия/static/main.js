function showXpPopup(text){
  const el=document.getElementById('xp-popup');
  if(!el)return;
  document.getElementById('xp-popup-text').textContent=text;
  el.classList.remove('hidden');
  el.style.animation='none';
  requestAnimationFrame(()=>{el.style.animation='xpPop 0.9s forwards';});
  setTimeout(()=>el.classList.add('hidden'),1000);
}

function showToast(message,type='default'){
  const c=document.getElementById('toast-container');
  if(!c)return;
  const t=document.createElement('div');
  t.className='toast '+type;
  t.textContent=message;
  c.appendChild(t);
  setTimeout(()=>{t.style.animation='toastOut .3s forwards';setTimeout(()=>t.remove(),350);},3000);
}

function updateXpBar(newXp, newLevel){
  const xpText=document.querySelector('.xp-text');
  if(xpText)xpText.textContent=newXp+' XP';
  const lvlBadge=document.querySelector('.level-badge');
  if(lvlBadge)lvlBadge.textContent='LVL '+newLevel;
}
