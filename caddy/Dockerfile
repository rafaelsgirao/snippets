FROM caddy:builder-alpine AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/cloudflare
    --with github.com/sillygod/cdp-cache \
    --with github.com/porech/caddy-maxmind-geolocation
#    --with github.com/caddyserver/nginx-adapter \
#    --with github.com/hairyhenderson/caddy-teapot-module@v0.0.3-0

FROM caddy:alpine

COPY --from=builder /usr/bin/caddy /usr/bin/caddy

#Run with docker build . -t your-custom-image-name/caddy-custom
