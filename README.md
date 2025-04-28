# log-reporting
[![codecov](https://codecov.io/gh/emptybutton/test-workmate/graph/badge.svg?token=YNVP1PHVGS)](https://codecov.io/gh/emptybutton/test-workmate)

Приложение анализа и формирования отчётов логов.

## Варианты установки
test.pypi:
```bash
pip install -i https://test.pypi.org/simple/ log-reporting
```

github и uv:
```bash
git clone https://github.com/emptybutton/test-workmate.git
uv sync
```

github и docker:
```bash
git clone https://github.com/emptybutton/test-workmate.git
docker compose -f test-workmate/deployments/dev/docker-compose.yaml up
```

## Использование
![<demo>](https://github.com/emptybutton/test-workmate/blob/main/assets/demo.png)

## Не функциональные требования
- [X] Дополнительные зависимости только для тестирования и линтинга
- [X] Файлы и их сегменты обрабатываются мультипроцессно. На слабом ПК с 4 ядрами обработка одного 1ГБ мусорного файла занимает 1.5 минуты 
- [X] Код покрыт тестами написанных на `pytest`
- [X] Код содержит аннотации типов и проходит `mypy` в `strict` режиме
- [X] Код соответствует `PEP8` и большому количеству правилам `ruff`-а
- [X] В архитектура проекта заложена унифицированная обработка репортов на всех уровнях, из-за чего добавление нового репорта или добавление представления существуещего репорта занимает < 100 строк

Примеры расширения (с картинками):
- [PR](https://github.com/emptybutton/test-workmate/pull/1) расширения представления существующего репорта
- [PR](https://github.com/emptybutton/test-workmate/pull/2) добавления нового репорта
