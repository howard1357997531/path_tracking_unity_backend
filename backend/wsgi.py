"""
WSGI config for backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_wsgi_application()

# pip install gunicorn
# 可以在 render: Start Command 輸入 gunicorn backend.wsgi 來做連接

# 因為 render 在讀取 requirements.txt 時的預設路徑適合 .git同目錄的地方，
# 所以 requirements.txt 要放在同一目錄
# 目前 render Django==3.2.19 不能大於 3.2.20 要去 requirements.txt 改
# 可以使用 render.yaml 來自訂指令（Custom Command）
# 在 Environment Variables 設定的 DATABASE_URL  interal
'''
ALLOWED_HOSTS  threed-object.onrender.com localhost
DATABASE_URL   postgres://django_render_sql_user:UlqCcY0HqCzRK6NCS58hVRxinWFHVxZM@dpg-cj3llamnqql8v0de9t20-a/django_render_sql
DEBUG          False
SECRET_KEY     
'''