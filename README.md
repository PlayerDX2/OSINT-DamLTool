ЗАПУСК НА ПК.
Как использовать консольные приложения python на ПК многим ясно но всё же вот инструкция, сначала устанавливаем Python версии 3.13.3 и выше, обязательно при установке добавить в PATH. в cmd пишем эту команду: pip install phonenumbers requests beautifulsoup4 python-whois googlesearch-python lxml или если выдает ошибки устанавливайте по отдельности, и запускаем файл OSINT DamLTool — 0.1.py.

ЗАПУСК НА АНДРОИДЕ.
Есть два известных мне способа запустиь приложение на телефоне, через Pydroid 3 и Termux. Т.к. Пайдроид это полноценная IDE из за чего есть полный доступ к исходному коду, а Termux это типо cmd (Terminal).

ШАГИ ЗАПУСКА НА Pydroid 3:
1. Установка IDE. Установите эти приложения Pydroid 3 - IDE for python 3, Pydroid repository plugin, Pydroid permissions plugin в Google Play
2. Распоковка. Скачаный zip скорее всего будет в папке downloads, распокуйте его.
3. Установка библиотек. В приложении Pydroid 3 нажать на три полоски вверху слева, нажать на раздел Pip и сверху в подразделе INSTALL вписать поочередно эти библиотеки: phonenumbers, requests, beautifulsoup4, python-whois, googlesearch-python, lxml
4. Запуск. На главном экране нажать на иконку папки сверху выбрать Open далее Internal storage и идти по пути который скорее всего будет таким: Download\OSINT-DamLTool-main и выбрать файл OSINT DamLTool — 0.1.py.

ШАГИ ЗАПУСКА НА Termux:
1. Распоковка zip
2. Установка\обновление python в termux. Для установки вставьте эту команду: pkg install python или для обновления эту: pkg upgrade python -y
3. Установка библиотек. Можно вставить одну команду: pip install phonenumbers requests beautifulsoup4 python-whois googlesearch-python lxml но если выдает ошибки устанавливайте по отдельности.
4. Запуск. тут придется уже вручную всё делать, пишем эти команды cd storage, cd downloads, cd OSINT-DamLTool-main далее dir должен отобразиться файл OSINT\DamLTool\—\0.1.py если так то спокойно пишем команду python OSINT\ DamLTool\ —\ 0.1.py (название файла лучше скопируйте которое выдаст dir) хз как облегчить запуск.

РЕЗУЛЬТАТЫ:

ПК:
![Снимок экрана (9)](https://github.com/user-attachments/assets/b5e8e64d-7e28-417f-8a9b-39a564813045)
Pydroid:
![photo_2025-05-10_16-06-01](https://github.com/user-attachments/assets/fac013c0-42ee-466d-9494-9ef6ff634540)
Termux:
![photo_2025-05-10_16-05-12](https://github.com/user-attachments/assets/c7247777-6a9f-497f-a029-7398c6bde9a8)

txt:
1. +79255652435

Результат:
{
  "basic_info": {
    "страна": "Россия",
    "оператор": "МегаФон",
    "валидность": true,
    "формат": "+7 925 565-24-35"
  },
  "add_info": {
    "база NumVerify": {
      "valid": true,
      "country_name": "Russian Federation",
      "region": "",
      "line_type": "mobile",
      "carrier": ""
    },
    "база Truecaller": {
      "name": null,
      "spam_score": null
    }
  },
  "spam_info": {
    "spamcalls": "Чистый"
  }
}

2. юзернейм: SmirnovIvan

Результат:
{
  "Telegram": {
    "имя": "Ivan Smirnov",
    "био": "Нет описания",
    "url": "https://t.me/SmirnovIvan",
    "существует?": true
  },
  "VK": {
    "имя": "Ivan Smirnov",
    "био": "Нет информации",
    "фото": "https://sun77-1.userapi.com/s/v1/ig1/...",
    "друзья": 0,
    "url": "https://vk.com/id9774161",
    "существует?": true
  },
  "YouTube": {
    "заголовок": "SmirnovIvan",
    "описании": "",
    "url": "https://www.youtube.com/channel/UCvPVvuTmWwm5FyTpFDvIP-w",
    "существует?": true
  },
  "GitHub": {
    "имя": "Ivan",
    "био": null,
    "подписчики": 3,
    "репосты": 0,
    "url": "https://github.com/smirnovivan",
    "существует?": true
  },
  "Steam": {
    "имя": "Пушок",
    "url": "https://steamcommunity.com/id/SmirnovIvan",
    "существует?": true
  },
  "Reddit": {
    "существует?": false
  }
}

3. smirnovivan@gmail.com

Результат:
{
  "success": true,
  "found": 2,
  "sources": [
    {
      "name": "Mycube.ru",
      "date": "2016-11"
    },
    {
      "name": "Deezer.com",
      "date": "2019-09"
    }
  ]
}

4. домен: russtop.top

Результат:
{
  "регистратор": "TUCOWS, INC.",
  "дата_создания": "2024-12-06 13:30:16",
  "дата_окончания": "2025-12-06 13:30:16",
  "org": "REDACTED FOR PRIVACY",
  "статус": [
    "clientTransferProhibited https://icann.org/epp#clientTransferProhibited",
    "clientUpdateProhibited https://icann.org/epp#clientUpdateProhibited"
  ],
  "dns": [
    "1-you.njalla.no",
    "3-get.njalla.fo",
    "2-can.njalla.in"
  ],
  "контакты": {
    "admin": "domainabuse@tucows.com",
    "registrant": "REDACTED FOR PRIVACY"
  }
}

5. IP-адрес: 185.127.16.116

Результат:
{
  "геолокация": {
    "страна": "United Kingdom",
    "регион": "England",
    "город": "London",
    "почтовый_код": "E14 95D",
    "координаты": [
      51.5073,
      -0.1277
    ],
    "часовой_пояс": "Europe/London"
  },
  "сеть": {
    "провайдер": "Kamatera Inc",
    "организация": "Cloudwebmanage EU LO",
    "ASN": "AS210329 Kamatera Inc",
    "IP-диапазон": "185.127.16.116/AS210329"
  },
  "безопасность": {
    "угроза": "нет данных",
    "тип_прокси": null
  },
  "репутация": {
    "оценка_доверия": 100,
    "всего_жалоб": 39,
    "последнее_нарушение": "2025-05-10T19:49:52+00:00"
  }
}

6. Google Dork запрос: hucking on python

Результат:
{
  "results": [
    {
      "source": "https://academy.tcm-sec.com/p/python-101-for-hackers",
      "content": "Python 101 For Hackers | TCM Security, Inc. Certifications Consulting Gift a Subscription Login Sign Up Python 101 for Hackers Learn Python with a foc..."
    },
    {
      "source": "https://www.udemy.com/course/ethical-hacking-with-phyton/?srsltid=AfmBOoobpHdZ0Z-Ue2Uw0KLN0kggrXja23d0pbDnLfv72SFJhLR0hord",
      "error": "Ошибка парсинга: HTTPSConnectionPool(host='www.udemy.com', port=443): Read timed out. (read timeout=10)"
    },
    {
      "source": "https://www.reddit.com/r/learnpython/comments/y6u0dn/getting_started_with_ethical_hacking/",
      "content": "Reddit - The heart of the internet Skip to main content Open menu Open navigation Go to Reddit Home r/learnpython A chip A close button Get App Get th..."
    }
  ]
}
