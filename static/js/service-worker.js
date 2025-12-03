const CACHE_NAME = 'monitoramento-v1';
const urlsToCache = [
  '/',
  '/dashboard/',
  '/static/css/mobile.css',
  '/static/js/dashboard.js'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => response || fetch(event.request))
  );
});