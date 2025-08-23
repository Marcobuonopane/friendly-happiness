// Service Worker per AUTENTICO v2.2 PWA
const CACHE_NAME = 'autentico-v2.2-cache';
const urlsToCache = [
  '/',
  '/src/index.html',
  '/INSTANT_APP_DEPLOY.html',
  '/assets/icon-192x192.png',
  '/assets/icon-512x512.png'
];

// Installazione Service Worker
self.addEventListener('install', (event) => {
  console.log('🔧 Service Worker: Installazione in corso...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('📦 Cache aperta');
        return cache.addAll(urlsToCache);
      })
  );
});

// Attivazione Service Worker
self.addEventListener('activate', (event) => {
  console.log('✅ Service Worker: Attivato');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('🗑️ Cache vecchia rimossa:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Intercettazione richieste
self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        // Restituisce la versione cached se disponibile
        if (response) {
          console.log('📁 Servito dalla cache:', event.request.url);
          return response;
        }
        
        // Altrimenti scarica dalla rete
        console.log('🌐 Scaricato dalla rete:', event.request.url);
        return fetch(event.request);
      })
  );
});

// Notifiche push (opzionale)
self.addEventListener('push', (event) => {
  const options = {
    body: 'AUTENTICO v2.2 ha una nuova funzionalità!',
    icon: '/assets/icon-192x192.png',
    badge: '/assets/icon-192x192.png'
  };

  event.waitUntil(
    self.registration.showNotification('AUTENTICO v2.2', options)
  );
});