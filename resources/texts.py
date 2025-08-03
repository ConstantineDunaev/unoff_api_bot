class Texts:
    menu = "Меню:"
    no_access = "У Вас нет доступа к функционалу бота."

    markets = "Управление магазинами:"
    input_name_market = "Введите имя магазина:"
    input_curl_market = "Введите cURL скопированный из браузера:"
    market_view = ("<b>ID</b>: <code>{market_id}</code>\n"
                   "<b>Наименование</b>: <code>{name}</code>\n"
                   "<b>Дата обновления</b>: <code>{updated_at}</code>\n\n")
    added_market = "Магазин <code>{name}</code> добавлен!"
    updated_market = "Cookies магазина <code>{name}</code> успешно обновлены!"

    scripts = "Запуск скриптов:"

    market_result = ("Магазин: <code>{market_name}</code>\n"
                     "JOB ID: <code>{job_id}</code>\n"
                     "Результат: <code>{result}</code>")
    script_result = "Скрипт <code>{caption}</code> завершил работу:\n\n{markets_result}"
    script_runned = "Скрипт <code>{caption}</code> запущен"
    error_401 = "Ошибка! Необходимо обновить cookies"



