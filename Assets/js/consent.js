(function(){
  const banner = document.getElementById('cookie-banner');
  const accept = document.getElementById('cookie-accept');
  const reject = document.getElementById('cookie-reject');

  function getConsent(){
    try { return localStorage.getItem('cookieConsent'); } catch(e) { return null; }
  }

  function saveConsent(value){
    const record = { value, date: new Date().toISOString(), userAgent: navigator.userAgent };
    try { localStorage.setItem('cookieConsent', value); localStorage.setItem('cookieConsentRecord', JSON.stringify(record)); } catch(e){}
  }

  function loadAnalyticsIfAllowed(){
    if(getConsent() === 'accepted'){
      // Aquí cargarías Google Analytics, Pixel, etc. por ejemplo:
      // (function(){ /* código de Analytics */ })();
      console.log('Analytics enabled (placeholder)');
    }
  }

  function showBannerIfNeeded(){
    if(!getConsent()){
      banner.style.display = 'flex';
    }
  }

  accept.addEventListener('click', function(){
    saveConsent('accepted');
    banner.style.display = 'none';
    loadAnalyticsIfAllowed();
  });
  reject.addEventListener('click', function(){
    saveConsent('rejected');
    banner.style.display = 'none';
  });

  // Expose function to record consent when user submits a form with explicit consent
  window.recordFormConsent = function(){
    const consentRecord = { type: 'form-consent', date: new Date().toISOString(), userAgent: navigator.userAgent };
    try { localStorage.setItem('lastFormConsent', JSON.stringify(consentRecord)); } catch(e){}
  }

  // Init
  document.addEventListener('DOMContentLoaded', function(){ showBannerIfNeeded(); loadAnalyticsIfAllowed(); });
})();
