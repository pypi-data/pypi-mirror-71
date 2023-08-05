@ECHO OFF
:: This batch file is started rendering.
TITLE Rendering window
celery -A render.celery worker -Q rendering --loglevel info --hostname=z@%d --without-gossip --without-mingle --heartbeat-interval=30