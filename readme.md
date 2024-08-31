# Совместимый с OpenAI API endpoint

Этот проект настраивает совместимую с OpenAI API конечную точку, используя Docker, Flask и SOCKS5 прокси. Сервер аутентифицирует запросы, используя список авторизованных токенов, и пересылает их в OpenAI API через SOCKS5 прокси.

## Обоснование

Доступ к OpenAI API иногда может быть заблокирован из-за сетевых ограничений или настроек провайдера. Этот проект предоставляет альтернативную конечную точку API, которую клиенты могут использовать для обхода таких ограничений и продолжения доступа к OpenAI API. Путем маршрутизации запросов через SOCKS5 прокси, эта конечная точка обеспечивает возможность клиентам поддерживать подключение к сервисам OpenAI даже в условиях ограниченной сети.

## Предварительные требования

- Docker
- Docker Compose

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/yourusername/openai-api-proxy.git
    cd openai-api-proxy
    ```

2. Создайте файл `.env` в корневом каталоге проекта и добавьте следующие переменные окружения:

    ```env
    SOCKS_PROXY=socks5://user:pass@1.2.3.4:1234
    TARGET_WEBSITE=api.openai.com
    ```

3. Создайте файл `authorized-tokens.json` в корневом каталоге проекта со следующим содержимым:

    ```json
    {
        "tokens": [
            "sk-1234",
            "sk-abcd"
        ]
    }
    ```

4. Постройте и запустите контейнеры Docker:

    ```bash
    docker-compose up --build
    ```

    Это создаст образ Docker и запустит сервер на порту 3000.

## Конфигурация

### Переменные окружения

- `SOCKS_PROXY`: URL SOCKS5 прокси-сервера с данными для аутентификации.
- `TARGET_WEBSITE`: Целевой веб-сайт, в данном случае это OpenAI API.

### Авторизованные токены

Файл `authorized-tokens.json` содержит список токенов, которые авторизованы для доступа к серверу. Обновите этот файл своими токенами.

## Использование

Документация по API доступна на [OpenAI API Reference](https://platform.openai.com/docs/api-reference/). Чтобы использовать этот прокси, просто измените конечную точку в ваших API-запросах, чтобы они указывали на этот сервер.

### Пример запроса

```bash
curl -X POST http://localhost:3000/v1/engines/davinci-codex/completions \
    -H "Authorization: Bearer sk-1234" \
    -H "Content-Type: application/json" \
    -d '{
        "prompt": "Переведите следующий английский текст на французский: \"Hello, world!\"",
        "max_tokens": 60
    }'
```

Сервер пересылает этот запрос в OpenAI API через SOCKS5 прокси.
