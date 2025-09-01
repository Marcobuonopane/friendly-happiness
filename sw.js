/**
 * AUTENTICO v2.2 - Service Worker
 * Sistema di Certificazione Digitale
 * © 2024 Marco Buonopane
 */

const CACHE_NAME = 'autentico-v2.2';
const urlsToCache = [
  '/',
  '/index.html',
  '/src/index.html',
  '/manifest.json',
  '/assets/autentico_logo_official.png',
  '/assets/app_icon.png'
];

// Installazione Service Worker
self.addEventListener('install', function(event) {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        console.log('[Service Worker] Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .catch(function(error) {
        console.log('[Service Worker] Cache failed:', error);
      })
  );
});

// Attivazione Service Worker
self.addEventListener('activate', function(event) {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

// Intercettazione richieste
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Restituisci la risorsa dalla cache se disponibile
        if (response) {
          return response;
        }
        
        // Altrimenti, prova a recuperarla dalla rete
        return fetch(event.request).then(function(response) {
          // Controlla se la risposta è valida
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clona la risposta per salvarla nella cache
          const responseToCache = response.clone();

          caches.open(CACHE_NAME)
            .then(function(cache) {
              cache.put(event.request, responseToCache);
            });

          return response;
        });
      })
      .catch(function() {
        // Se sia cache che rete falliscono, mostra pagina offline
        if (event.request.destination === 'document') {
          return caches.match('/index.html');
        }
      })
  );
});

// Gestione messaggi dal client
self.addEventListener('message', function(event) {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

// Gestione notifiche push (per future implementazioni)
self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push received');
  
  const options = {
    body: event.data ? event.data.text() : 'Nuova notifica da AUTENTICO',
    icon: '/assets/app_icon.png',
    badge: '/assets/app_icon.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };

  event.waitUntil(
    self.registration.showNotification('AUTENTICO', options)
  );
});

// Gestione click sulle notifiche
self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification clicked');
  event.notification.close();

  event.waitUntil(
    clients.openWindow('/')
  );
});