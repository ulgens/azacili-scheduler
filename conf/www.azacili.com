server {
    server_name www.azacili.com;
    charset utf-8;

    client_max_body_size 75M;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/developer/scheduler/azacili.sock;
    }

    listen 443 ssl; # managed by Certbot
    ssl_certificate /etc/letsencrypt/live/www.azacili.com/fullchain.pem; # managed by Certbot
    ssl_certificate_key /etc/letsencrypt/live/www.azacili.com/privkey.pem; # managed by Certbot
    include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
    if ($host = www.azacili.com) {
        return 301 https://$host$request_uri;
    }

    listen 80;
    server_name www.azacili.com;
    return 404;
}
