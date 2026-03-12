const CACHE_NAME = 'pvp-advisor-v4';
const HTML_URL = './pokemon-go-advisor.html';
const STATIC_ASSETS = [
  './logo.svg',
  './manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache =>
      cache.addAll([HTML_URL, ...STATIC_ASSETS])
    )
  );
  // Do NOT call skipWaiting() here – wait for the page to trigger the update
  // so the user is notified and can choose when to activate the new SW.
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Listen for SKIP_WAITING message sent by the update-banner in the page.
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Network-first for the main HTML document so updates are always delivered.
  if (url.pathname.endsWith('pokemon-go-advisor.html') || url.pathname === '/' || url.pathname.endsWith('index.html')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          // Cache the fresh response for offline use.
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Cache-first for all other static assets (logos, sprites, fonts, etc.).
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        // Only cache non-opaque successful responses to avoid storing errors.
        if (response && response.status === 200 && response.type !== 'opaque') {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        }
        return response;
      });
    })
  );
});
