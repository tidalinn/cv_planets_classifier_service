# final_project [service]

> [Финальный проект (GitLab)](https://gitlab.deepschool.ru/dl-deploy2/lectures/-/tree/main/big-hw)

Свойство | Значение
-|-
Задача сервиса | Классификация спутниковых снимков
Инструменты | Python, FastAPI, DVC, CI/CD, Linters

<br>

## Файлы

Расположение | Предназначение
-|-
`.env` | Настройка перемнных в `docker-compose.yml`
`src/constants.py` | Настройка путей к файлам
`src/app.py` | Запуск FastAPI-приложения

## Запуск

### DEV

Запуск обучения:
```
make run.dev
```
Последовательность выполнения:
1. Сборка образа
2. Запуск контейнера скачивания модели
3. Контейнер выполняет команду `make dvc.get.files` и скачивает модель из dvc
4. Запуск базового контейнера
5. Контейнер копирует модель и выполняет команду `make run.inference` (`docker-compose.yml` -> `command`) и запускает FastAPI

Запуск тестов:
```
make run.tests
```
Запуск составления отчёта покрытия тестами:
```
make run.tests.coverage_report
```

### PROD

Запуск обучения:
```
make run.dev
```

### Сервисы

Сервис | Логин | Пароль | Ссылка
-|-|-|-
Swagger | | | [http://localhost:8080/docs](http://localhost:8080/docs)
Grafana | admin | admin | [http://localhost:3000](http://localhost:3000)
Grafana Dashboard JSON | | | [dashboard](deploy\grafana\provisioning\dashboards\docker_host.json)
Jaeger | | | [http://localhost:16686](http://localhost:16686)
Node Exporter | | | [http://localhost:9100](http://localhost:9100)
Prometheus | | | [http://localhost:9090](http://localhost:9090)

### CICD

Пайплайн CI/CD отрабатывает при коммите в ветку `dev`.

## Структура проекта

```
├── configs/                                   # конфигурационные файл
│    └── project.yaml                          # весь проект
├── deploy/                                    # Grafana и Prometheus
├── logs/                                      # логи
├── models/                                    # модели в ONNX
├── requirements/                              # зависимости
├── src/                                       # исходный код
│    ├── configs/                              # модуль конфигураций
│    │    └── project_config.py                # конфигурация
│    ├── containers/                           # модуль DI-контейнеров
│    │    ├── classificator.py                 # классификатор изображений
│    │    └── containers.py                    # DI-контейнеры
│    ├── routes/                               # модуль маршрутизации
│    │    ├── classificator.py                 # классификатор изображений
│    │    └── metrics.py                       # мониторинг метрик
│    ├── utils/                                # модуль полезных функций
│    │    ├── logger.py                        # кастомный логгер
│    │    ├── metrics.py                       # настройка Prometheus
│    │    └── tracing.py                       # настройка Jaeger
│    ├── constants.py                          # константы
│    ├── main_pipeine.py                       # запуск пайплайна ClearML
│    └── main.py                               # запуск обучения
├── tests/                                     # тесты
├── .gitlab-ci.yml                             # настройка CICD
├── Makefile                                   # управляющие команды
└── ...
```
