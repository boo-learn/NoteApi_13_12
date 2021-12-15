# Развертывание на локальной машине
1. Создаем виртуальное окружение: python3 -m venv flask_venv
1. Активируем venv: source flask_venv/bin/activate
1. Устанавливаем зависимости: pip install -r requirements.txt
1. Создаем локальную БД: flask db upgrade

# Миграции
1. Активировать миграции: flask db init
1. Создать миграцию: flask db migrate -m "comment"
1. Применить миграции: flask db upgrade