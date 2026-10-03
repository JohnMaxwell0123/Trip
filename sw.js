// Silk Road PWA Service Worker (Cache-First Shell + Network-Fallback / SWR)
const CACHE_NAME = 'silkroad-shell-v4.2.0';

const PRECACHE_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/images/dunhuang_feitian_bg.jpg',
  './assets/images/dunhuang_hero_banner.jpg',
  './assets/images/dunhuang_seal_badge.jpg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      await Promise.allSettled(
        PRECACHE_ASSETS.map((asset) => cache.add(asset).catch((err) => {
          console.warn(`[SW] Precache failed for ${asset}:`, err);
        }))
      );
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Only handle same-origin shell resources
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(event.request).then((cachedResponse) => {
        // Stale-While-Revalidate / Cache-First with Network fallback
        const fetchPromise = fetch(event.request)
          .then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
              const responseToCache = networkResponse.clone();
              caches.open(CACHE_NAME).then((cache) => {
                cache.put(event.request, responseToCache);
              });
            }
            return networkResponse;
          })
          .catch(() => {
            // When offline: if navigating to a page, fallback to cached index.html
            if (event.request.mode === 'navigate') {
              return caches.match('./index.html').then((res) => res || caches.match('./'));
            }
          });

        // If cached resource exists, return it immediately for instant response
        if (cachedResponse) {
          return cachedResponse;
        }

        // Otherwise await network, with navigation fallback on error
        return fetchPromise.then((networkRes) => {
          if (!networkRes && event.request.mode === 'navigate') {
            return caches.match('./index.html').then((r) => r || caches.match('./'));
          }
          return networkRes;
        });
      })
    );
  }
});
