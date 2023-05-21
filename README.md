# Build system

## Описание
 - Билд-система, которая автоматизирует и ускоряет рутинные процессы.
 - Тестовое задание [text](https://github.com/ZOMini/Build_system/blob/71d37b7e91447d21ab10d36a7fdacc62f03d2661/task.txt)

## Стек
  Python 3.11, FastAPI, Pytest, nginx, aiohttp, networkx

## Запуск
 - docker-compose up --build
 - Функциональные тесты в docker-compose - build_system_test
 - Заполняем .env (см. .env.template) - если нужно изменить базовые значения.
 - Проверка на циклические зависимости в тасках и билдах, происходит при старте сервиса. Если присутствуют, то сервис не стартанет.
 - Дуближи тасков удаляются(в задании что с ними делать не сказано), остается самый ранний. Можно откорректировать - [code](https://github.com/ZOMini/Build_system/blob/master/build_system/services/data_service.py#L87)

## URL(по умолчанию)
 - http://localhost:8081/build/api/openapi
 - {POST}http://localhost:8081/build/api/v1/get_tasks