```bash
sudo apt update
sudo apt install nginx
```

```bash
sudo nano /etc/nginx/sites-available/default
```

Изменить конфиг файл следующим образом, чтобы проксировать запросы к вашему ZenML серверу:

```
server {
    listen 80;

    server_name 91.224.86.145;

    location / {
        proxy_pass http://127.0.0.1:8237;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/
```

```bash
sudo nginx -t
```

```bash
sudo systemctl restart nginx
```

```bash
export ZENML_CONFIG_PATH=$PWD/services/zenml
```

```bash
zenml down
```

```bash
zenml up
```