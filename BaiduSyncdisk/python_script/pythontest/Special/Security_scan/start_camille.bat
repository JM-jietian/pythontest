@echo off
set current_dir=%cd%
cd tool\camille-master && python camille.py com.heytap.music -t 2 -f %current_dir%\results\camille_music.xls