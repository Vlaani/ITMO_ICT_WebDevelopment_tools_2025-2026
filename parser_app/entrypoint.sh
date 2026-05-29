#!/bin/bash

# Запуск виртуального дисплея
export DISPLAY=:99
Xvfb :99 -screen 0 1280x720x24 &
sleep 2

# Запуск оконного менеджера
fluxbox &
sleep 1

# Запуск VNC сервера
x11vnc -display :99 -forever -nopw -shared &
sleep 2

# Запуск noVNC (веб-интерфейс для VNC на порту 6080)
websockify --web /usr/share/novnc 6080 0.0.0.0:5900 &
sleep 2

# Важно: указываем Playwright использовать установленный браузер
export PLAYWRIGHT_BROWSERS_PATH=/root/.cache/ms-playwright

uvicorn main:app --host 0.0.0.0 --port 8000