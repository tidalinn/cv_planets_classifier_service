# CV planets classifier [service]

> [CV planets classifier [modelling]](https://github.com/tidalinn/cv_planets_classifier_modelling)

Свойство | Значение
-|-
Задача сервиса | Multilabel-классификация спутниковых снимков
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

Загрузка модели из dvc:
```
make -f Makefile_dvc dvc.get_files
```
Запуск сервиса:
```
make run.dev
```
Запуск тестов:
```
make run.tests
```
Запуск составления отчёта покрытия тестами:
```
make run.tests.coverage_report
```

### PROD

Запуск сервиса:
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
