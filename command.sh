#!/bin/bash



# Systemd xizmatlarini qayta boshlash
sudo systemctl daemon-reload

# Celery xizmatini qayta boshlash
sudo systemctl enable video_downloader_multi_bot
sudo systemctl start video_downloader_multi_bot
sudo systemctl restart video_downloader_multi_bot








# client.service xizmatini qayta boshlash (agar kerak bo'lsa)
#sudo systemctl restart client.service

# Nginx konfiguratsiyasini tekshirish va Nginx ni qayta boshlash
sudo nginx -t && sudo systemctl restart nginx
sudo systemctl status video_downloader_multi_bot
