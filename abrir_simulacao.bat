@echo off
title Abrir Simulador Webots - Seguidor de Linha
echo ============================================================
echo INICIANDO O WEBOTS COM O SEGUIDOR DE LINHA CALIBRADO...
echo ============================================================

cd /d "C:\Users\Natan\AppData\Local\Programs\Webots"
start "" "C:\Users\Natan\AppData\Local\Programs\Webots\msys64\mingw64\bin\webotsw.exe" "f:\IDE Antigravity\worlds\pista_seguidor.wbt"
exit
