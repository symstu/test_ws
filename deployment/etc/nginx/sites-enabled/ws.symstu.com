server {
    listen 80;
    client_max_body_size 4G;

    gzip on;
    gzip_min_length 1000;
    gzip_types      text/plain text/css text/html image/svg+xml application/json;

    server_name ws.symstu.com;

    location / {
          proxy_set_header Host $http_host;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
          proxy_redirect off;
          proxy_buffering off;
          proxy_pass http://localhost:6868;
    }

    location /timer {
            proxy_pass http://localhost:6868;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "Upgrade";
            proxy_set_header Host $host;
    }

}
