const IS_LOCAL = self.location.hostname === 'localhost' || self.location.hostname === '127.0.0.1';

if (IS_LOCAL) {
    // Development: atreģistrē sevi un neko nekešo
    self.addEventListener('install', () => self.skipWaiting());
    self.addEventListener('activate', e => {
        e.waitUntil(
            caches.keys()
                .then(keys => Promise.all(keys.map(k => caches.delete(k))))
                .then(() => self.registration.unregister())
                .then(() => self.clients.claim())
        );
    });
} else {
    // Production
    const CACHE = 'eizsole-v4';
    const OFFLINE_URL = '/offline/';

    const PRECACHE = [
        '/',
        '/izsoles/',
        '/offline/',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
        'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
        'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    ];

    self.addEventListener('install', e => {
        e.waitUntil(
            caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting())
        );
    });

    self.addEventListener('activate', e => {
        e.waitUntil(
            caches.keys().then(keys =>
                Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
            ).then(() => self.clients.claim())
        );
    });

    self.addEventListener('fetch', e => {
        if (e.request.method !== 'GET') return;
        const url = new URL(e.request.url);

        if (url.pathname.startsWith('/static/') || url.hostname.includes('jsdelivr') || url.hostname.includes('googleapis')) {
            e.respondWith(
                caches.match(e.request).then(cached => cached || fetch(e.request).then(res => {
                    const clone = res.clone();
                    caches.open(CACHE).then(c => c.put(e.request, clone));
                    return res;
                }))
            );
            return;
        }

        e.respondWith(
            fetch(e.request).catch(() =>
                caches.match(e.request).then(cached => cached || caches.match(OFFLINE_URL))
            )
        );
    });
}
