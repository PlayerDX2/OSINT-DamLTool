import phonenumbers
from phonenumbers import carrier, geocoder
import requests
from bs4 import BeautifulSoup
import whois
from datetime import datetime
from googlesearch import search
import json
#import random
#import time

#вспомогательный класс для анализа номера телефона
class PhoneAnalyzer:
    @staticmethod
    def _check_numverify(phone, api_key):
        """Проверка через NumVerify"""
        try:
            response = requests.get(
                f"http://apilayer.net/api/validate?number={phone}&access_key={api_key}",
                timeout=5
            )
            data = response.json()
            return {
                "valid": data.get("valid"),
                "country_name": data.get("country_name"),
                "region": data.get("location"),
                "line_type": data.get("line_type"),
                "carrier": data.get("carrier")
            }
        except:
            return "API Error"
        
    @staticmethod
    def _check_truecaller(phone, headers):
        """Проверка через веб-версию Truecaller"""
        try:
            # Используем облегченную версию сайта
            response = requests.get(
                f"https://www.truecaller.com/search/ru/{phone}",
                headers=headers,
                timeout=10
            )
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Парсим основные данные
            name = soup.find("h1", class_="profile-name")
            spam_score = soup.find("div", class_="spam-score")
            
            return {
                "name": name.text.strip() if name else None,
                "spam_score": spam_score.text.strip() if spam_score else None
            }
        except Exception as e:
            return {"error": str(e)}

class OSINTToolkit:
    @staticmethod
    def phone_osint(phone_number):
        """Анализ номера телефона"""
        result = {
            "basic_info": {},
            "add_info": {}, 
            "spam_info": {}
        }
        
        try:
            # --- 1. Базовая информация ---
            parsed = phonenumbers.parse(phone_number)
            country = geocoder.description_for_number(parsed, "ru")
            result["basic_info"] = {
                "страна": country,
                "оператор": carrier.name_for_number(parsed, "ru"),
                "валидность": phonenumbers.is_valid_number(parsed),
                "формат": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            # --- 3. Поиск доп информации ---
            result["add_info"] = {
                "база NumVerify": PhoneAnalyzer._check_numverify(phone_number, "30f89a5c3318f0a38db69f4b1a365ed3"),
                "база Truecaller": PhoneAnalyzer._check_truecaller(phone_number, headers)
            }
            
            # Проверка через SpamCalls (основной источник)
            spam_result = {
                "spamcalls": "Не проверено"
            }
            
            try:
                # SpamCalls проверка
                response = requests.get(
                    f"https://spamcalls.net/en/num/{phone_number}", 
                    headers=headers,
                    timeout=15
                )
                
                # Простая проверка двух ключевых точек
                if "Spam-Risk" in response.text and "User Report" in response.text:
                    spam_result["spamcalls"] = "СПАМ"
                else:
                    spam_result["spamcalls"] = "Чистый"
            
            except Exception as e:
                spam_result["spamcalls"] = f"Ошибка: {str(e)}"
                
            
            result["spam_info"] = spam_result
            return result

        except Exception as e:
            return {"error": f"Analysis failed: {str(e)}"}

    @staticmethod
    def username_osint(username, verbose=False):
        """Поиск по юзернейму с детальной информацией"""
        try:
            results = {}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
    
            # Telegram
            try:
                tg_url = f"https://t.me/{username}"
                response = requests.get(tg_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    title = soup.find('div', class_='tgme_page_title')
                    desc = soup.find('div', class_='tgme_page_description')
                    
                    results['Telegram'] = {
                        'имя': title.text.strip() if title else "Не найдено",
                        'био': desc.text.strip() if desc else "Нет описания",
                        'url': tg_url,
                        'существует?': True
                    }
                else:
                    results['Telegram'] = {'существует?': False, 'url': tg_url}
            except Exception as e:
                results['Telegram'] = {'error': f"Ошибка парсинга: {str(e)}"}
    
            # VK (с вашим API ключом)
            try:
                vk_token = '1c44bd291c44bd291c44bd292c1f7440c511c441c44bd29745856262473fc4dd5e09607'
                vk_response = requests.get(
                    f"https://api.vk.com/method/users.get?user_ids={username}"
                    f"&fields=first_name,last_name,about,counters,photo_200&v=5.131&access_token={vk_token}",
                    timeout=10
                )
                vk_data = vk_response.json()
                
                if 'response' in vk_data and len(vk_data['response']) > 0:
                    user = vk_data['response'][0]
                    results['VK'] = {
                        'имя': f"{user.get('first_name', '')} {user.get('last_name', '')}".strip(),
                        'био': user.get('about', 'Нет информации'),
                        'фото': user.get('photo_200', None),
                        'друзья': user.get('counters', {}).get('friends', 0),
                        'url': f"https://vk.com/id{user['id']}",
                        'существует?': True
                    }
                else:
                    results['VK'] = {'существует?': False, 'error': vk_data.get('error', 'Пользователь не найден')}
            except Exception as e:
                results['VK'] = {'error': f"API ошибка: {str(e)}"}
    
            # YouTube (с вашим API ключом)
            try:
                yt_api_key = 'AIzaSyCi19Q7TIbCJFSRbrBZ65wQIG1vJBy63Yo'
                yt_response = requests.get(
                    f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={username}"
                    f"&type=channel&maxResults=1&key={yt_api_key}",
                    timeout=10
                )
                yt_data = yt_response.json()
                
                if 'items' in yt_data and len(yt_data['items']) > 0:
                    channel = yt_data['items'][0]['snippet']
                    results['YouTube'] = {
                        'заголовок': channel.get('title', ''),
                        'описании': channel.get('description', 'Нет описания'),
                        'url': f"https://www.youtube.com/channel/{yt_data['items'][0]['id']['channelId']}",
                        'существует?': True
                    }
                else:
                    results['YouTube'] = {'существует?': False}
            except Exception as e:
                results['YouTube'] = {'error': f"API ошибка: {str(e)}"}
    
            # GitHub (упрощенный вариант)
            try:
                gh_response = requests.get(f"https://api.github.com/users/{username}", timeout=10)
                if gh_response.status_code == 200:
                    gh_data = gh_response.json()
                    results['GitHub'] = {
                        'имя': gh_data.get('name', username),
                        'био': gh_data.get('bio', 'Нет описания'),
                        'подписчики': gh_data.get('followers', 0),
                        'репосты': gh_data.get('public_repos', 0),
                        'url': gh_data.get('html_url'),
                        'существует?': True
                    }
                else:
                    results['GitHub'] = {'существует?': False}
            except Exception as e:
                results['GitHub'] = {'error': str(e)}
    
            # Steam (улучшенный парсинг)
            try:
                steam_url = f"https://steamcommunity.com/id/{username}"
                response = requests.get(steam_url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    name = soup.find('span', {'class': 'actual_persona_name'})
                    
                    if name:
                        results['Steam'] = {
                            'имя': name.text.strip(),
                            'url': steam_url,
                            'существует?': True
                        }
                    else:
                        results['Steam'] = {'существует?': False, 'url': steam_url}
                else:
                    results['Steam'] = {'существует?': False, 'url': steam_url}
            except Exception as e:
                results['Steam'] = {'error': str(e)}
    
            # Reddit (упрощенный вариант)
            try:
                reddit_response = requests.get(
                    f"https://www.reddit.com/user/{username}/about.json",
                    headers=headers,
                    timeout=10
                )
                if reddit_response.status_code == 200:
                    reddit_data = reddit_response.json()
                    if 'data' in reddit_data and not reddit_data['data'].get('is_suspended', False):
                        results['Reddit'] = {
                            'имя': reddit_data['data'].get('name', username),
                            'карма': reddit_data['data'].get('total_karma', 0),
                            'url': f"https://reddit.com/user/{username}",
                            'существует?': True
                        }
                    else:
                        results['Reddit'] = {'существует?': False}
                else:
                    results['Reddit'] = {'существует?': False}
            except Exception as e:
                results['Reddit'] = {'error': str(e)}
    
            # Удаляем пустые ошибки и добавляем статус
            for platform in list(results.keys()):
                if 'error' in results[platform] and not results[platform]['error']:
                    del results[platform]['error']
                if 'существует?' not in results[platform]:
                    results[platform]['существует?'] = True if any(k in results[platform] for k in ['name', 'url', 'bio']) else False
    
            return results
    
        except Exception as e:
            return {"error": f"Общая ошибка: {str(e)}"} 


    @staticmethod
    def email_osint(email):
        """Проверка email в утечках через leakcheck.io"""
        try:
            response = requests.get(
                "https://leakcheck.io/api/public",
                params={
                    "key": "431ef8d4f4d21a0f5891483ddd4a6b309d6c91d4",
                    "check": email
                },
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10
            )
            
            if response.status_code != 200:
                return {"error": f"HTTP {response.status_code}"}
    
            data = response.json()
            
            # Формируем ограниченный результат
            result = {
                "success": data.get("success", False),
                "found": data.get("found", 0),
                "sources": data.get("sources", [])[:10]  # Берем первые 10 источников
            }
    
            return result
    
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def domain_osint(domain):
        """Улучшенный WHOIS-анализ домена с обработкой datetime"""
        try:
            # Проверка валидности домена
            if not domain or '.' not in domain:
                return {"error": "Неверный формат домена"}
    
            # Получение WHOIS-данных
            domain_info = whois.whois(domain)
    
            # Функция для преобразования объектов datetime
            def convert_dates(obj):
                if isinstance(obj, datetime):
                    return obj.strftime("%Y-%m-%d %H:%M:%S")
                elif isinstance(obj, list):
                    return [convert_dates(item) for item in obj]
                return obj
    
            # Функция безопасного получения атрибутов
            def safe_get(data, key, default="Не указано"):
                value = getattr(data, key, None)
                return convert_dates(value) if value is not None else default
    
            # Формирование результата
            result = {
                "регистратор": safe_get(domain_info, 'registrar'),
                "дата_создания": safe_get(domain_info, 'creation_date'),
                "дата_окончания": safe_get(domain_info, 'expiration_date'),
                "org": safe_get(domain_info, 'org'),
                "статус": safe_get(domain_info, 'status'),
                "dns": list(set(safe_get(domain_info, 'name_servers', []))),
                "контакты": {
                    "admin": safe_get(domain_info, 'emails') or [],
                    "registrant": safe_get(domain_info, 'name')
                }
            }
    
            return result
    
        except whois.parser.PywhoisError as e:
            return {"error": f"WHOIS ошибка: {str(e)}"}
        except Exception as e:
            return {"error": f"Общая ошибка: {str(e)}"}    
        
    @staticmethod
    def geo_osint(ip_address):
        """Расширенный анализ IP-адреса"""
        try:
            # Проверяем валидность IP
            import socket
            try:
                socket.inet_aton(ip_address)
            except socket.error:
                return {"error": "Неверный формат IP-адреса"}
    
            results = {}
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
    
            # 1. Основная геолокация через ip-api.com (бесплатно)
            ipapi_response = requests.get(
                f"http://ip-api.com/json/{ip_address}?fields=66842623",
                headers=headers,
                timeout=10
            ).json()
            
            if ipapi_response.get("status") == "success":
                results.update({
                    "геолокация": {
                        "страна": ipapi_response.get("country"),
                        "регион": ipapi_response.get("regionName"),
                        "город": ipapi_response.get("city"),
                        "почтовый_код": ipapi_response.get("zip"),
                        "координаты": (ipapi_response.get("lat"), ipapi_response.get("lon")),
                        "часовой_пояс": ipapi_response.get("timezone")
                    },
                    "сеть": {
                        "провайдер": ipapi_response.get("isp"),
                        "организация": ipapi_response.get("org"),
                        "ASN": ipapi_response.get("as"),
                        "IP-диапазон": ipapi_response.get("query") + "/" + str(ipapi_response.get("as").split()[0])
                    }
                })
    
            # 2. Проверка на VPN/Tor/прокси через iphub.info
            try:
                iphub_key = "MjgxNTc6Yk9EZHQxbFFDcHFEeFNCY1FTV056VFVlWnBUdVdNV0Q=" 
                iphub_response = requests.get(
                    f"http://v2.api.iphub.info/ip/{ip_address}",
                    headers={"X-Key": iphub_key},
                    timeout=5
                ).json()
                threat_info = {
                    0: "нет данных",
                    1: "чистый IP",
                    2: "прокси/VPN",
                    3: "спам-бот"
                }
                results["безопасность"] = {
                    "угроза": threat_info.get(iphub_response.get("block", 0)),
                    "тип_прокси": iphub_response.get("proxyType")
                }
            except:
                pass
    
            # 3. Дополнительные данные из AbuseIPDB
            try:
                abuseipdb_key = "17d382bfb187f919360e6a87f1ab12c90e14317d053d6c54ae65a2e2fb23d70bf3d862ac0ded19ef" 
                abuse_response = requests.get(
                    f"https://api.abuseipdb.com/api/v2/check",
                    params={"ipAddress": ip_address},
                    headers={"Key": abuseipdb_key, "Accept": "application/json"},
                    timeout=10
                ).json()
                if abuse_response.get("data"):
                    results["репутация"] = {
                        "оценка_доверия": abuse_response["data"].get("abuseConfidenceScore"),
                        "всего_жалоб": abuse_response["data"].get("totalReports"),
                        "последнее_нарушение": abuse_response["data"].get("lastReportedAt")
                    }
            except:
                pass
    
            return results if results else {"error": "Не удалось получить данные"}
    
        except requests.exceptions.RequestException as e:
            return {"error": f"Ошибка сети: {str(e)}"}
        except Exception as e:
            return {"error": f"Неожиданная ошибка: {str(e)}"}

    @staticmethod
    def google_dork(query, num_results=3):
        """Поиск через Google Dorks с парсингом контента"""
        try:
            results = []
            # Получаем результаты поиска
            urls = list(search(query, num=num_results, stop=num_results, pause=2))
            
            for url in urls[:num_results]:
                try:
                    # Заголовки для обхода базовой защиты
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                    }
                    
                    # Получаем контент страницы
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Извлекаем и форматируем текст
                    text = soup.get_text()
                    clean_text = ' '.join(text.split()).strip()[:150]  # Первые 500 символов
    
                    results.append({
                        "source": url,
                        "content": clean_text + "..." if len(clean_text) >= 150 else clean_text
                    })
    
                except Exception as page_error:
                    results.append({
                        "source": url,
                        "error": f"Ошибка парсинга: {str(page_error)}"
                    })
    
            return {"results": results}
    
        except Exception as main_error:
            return {"error": str(main_error)}

    @staticmethod
    def image_search(image_url):
        """Обратный поиск изображений через Яндекс"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Referer": "https://yandex.ru/images/"
            }
    
            # Формируем URL для Яндекс Поиска по картинке
            yandex_url = f"https://yandex.ru/images/search?source=collections&url={image_url}&rpt=imageview"
            
            response = requests.get(yandex_url, headers=headers, timeout=15)
            
            # Проверка на блокировку
            if "checkcaptcha" in response.url:
                return {"error": "Яндекс требует CAPTCHA. Откройте ссылку вручную:", "url": yandex_url}
            
            # Парсим результаты
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            
            # Ищем блоки с результатами
            for item in soup.find_all("div", class_="CbirItem"):
                link = item.find("a", class_="Link")
                if link and link.get("href"):
                    results.append("https://yandex.ru" + link["href"])
            
            # Альтернативный вариант поиска
            if not results:
                for a in soup.find_all("a", class_="serp-item__link"):
                    href = a.get("href")
                    if href and "/images/search" not in href:
                        results.append("https://yandex.ru" + href)
            
            return results[:5] if results else {"error": "Ничего не найдено"}
    
        except Exception as e:
            return {"error": f"Ошибка: {str(e)}"}

def show_menu():
    print("\n=== OSINT DamLTool ===")
    print("ПОИСК ...")
    print("1. по номеру телефона")
    print("2. по юзернейму")
    print("3. email в утечках")
    print("4. домена")
    print("5. геолокации по IP")
    print("6. через Google Dorks")
    print("7. по изображению")
    print("8. помощь")
    print("0. выход")
    return input("Ввод: ")

def main():
    toolkit = OSINTToolkit()
    
    while True:
        choice = show_menu()
        
        if choice == "0":
            print("Выход из программы...")
            break
            
        elif choice == "1":
            phone = input("Введите номер телефона (+79001234567): ")
            result = toolkit.phone_osint(phone)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "2":
            username = input("Введите юзернейм: ")
            result = toolkit.username_osint(username)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "3":
            email = input("Введите email: ")
            result = toolkit.email_osint(email)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "4":
            domain = input("Введите домен (example.com): ")
            result = toolkit.domain_osint(domain)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "5":
            ip = input("Введите IP-адрес: ")
            result = toolkit.geo_osint(ip)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "6":
            query = input("Введите Google Dork запрос: ")
            result = toolkit.google_dork(query)
            print("\nРезультат:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
        elif choice == "7":
            print("\n!ФУНКЦИЯ В РАЗРАБОТКЕ!")
            #image_url = input("Введите URL изображения: ")
            #result = toolkit.image_search(image_url)
            #print("\nРезультат:")
            #print(json.dumps(result, indent=2, ensure_ascii=False))
        elif choice == "8":
            print("\n=== СПРАВКА ===\n1. Поиск данных по номеру телефона. Обязательно вводить номер телефона начиная с + далее без пробелов, скобочек и черточек ПРИМЕР: +79001234567. Проверяет международные номера и выдает базовую информацию для проверки которой не требуется API, дополнительную информацию поиск которой происходит по API NumVerify кол-во результатов ограниченно, и по базе Truecaller (нестабильно) и проверяет номер на спам через сайт spamcalls.\n2. Поиск информациипо user-name. Ищет на 6-ти площадках: Telegram, VK, YouTube, GitHub, Steam, Reddit. вывводит такую инфорамцию как: имя, биография, ссылка на источник, фото и т.д.\n3. Поиск по email. Ищет платформы где и когда был зарегистрирован указаный email.\n4. Поиск данных по домену. Выдаёт такие данные как регистратора этого домена, дата создания и окончания, организация которой принадлежит домен, какие то статусы, email`ы админов и елси указано имя регистратора.\n5. Поиск информации по IP. Мощная функция работающая на двух API, выдает информацию о геолокации, сети и другое.\n6. Поиск по запросу в Google Dorks. парсит первые 150 символов из 3 источников найденных по запросу. Тут можно найти то что не нашли в других функциях.\n7. Поиск по изображению. Находит источники изображения через Яндекс поиск по фото, но функция НЕ РАБОТАЕТ из за того что яндекс блокирует запросы не от человека даже headrs не помог.")

if __name__ == "__main__":
    main()