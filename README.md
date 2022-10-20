# ASR-Telegram-Bot
* Для запуска контейнеров надо скачать dev зависимости и выкачать с S3 бакета QuartzNet: 
  ```bash
  poetry install --only dev
  make aws-model-pull
  make docker-build
  ```
* У бота, @my_asr_bot, есть только одна комманда `help`, которая выводит инструкцию по пользованию. На рандомные сообщения бот отвечает, что так делать не надо. На аудиозапись выдает транскрипцию.
* В дополнение к заданию реализовал:
  * Терраформ код для поднятия S3 бакета, в который загружается заскриптованная модель через `dvc add` и `dvc push`. 
  * Pre-commit хуки, которые проверяют и форматируют все закомиченные файлы на правильность (к примеру, проверка Python кода по конфигам flake8, форматирование через black; проверка того, что код не содержит секретных значений etc.)
  * Вместо баш скриптов использовалась система сборки GNU Make. Посмотреть все реализованные команды можно через `make help`.
