# [SMS-AREA](https://sms-area.org)
Официальная [документация](http://sms-area.org/api/ru/documentation.html)


## Установка и использование:
```sh 
pip install sms-area-api
```

```python 
import sms_area_api
sms = sms_area_api.SmsArea(sms_ara_api_key)

print("Доступные сервисы: {}".format(sms.aviable_services()))

aviable_numbers = sms.aviable_numbers("tg", country="ru")
if 0 < aviable_numbers:
	print("Есть {} доступных номеров".format(aviable_numbers))

	balance = sms.balance()
	tg_price = sms.service_price("tg", country="ru")

	if balance >= tg_price:
		print("Денег хватает")
		activate = sms.get_number("tg", country="ru")
		print(activate)
		input("Нажмите inter, когда отправите смс")
		sms.set_activation_status(activate["id_activation"], 1)
		
	else:
		text = "У вас на балансе {} руб, а активация стоит {} руб"
		text = text.format(balance, price)
		print(text)
else:
	print("Нет доступных номеров")
```


# Таблица сервисов:
Название | Код
------------ | -------------
ВКонтакте | vk
Mamba | mb
Одноклассники | ok
4Game | 4g
facebook | fb
SEOsprint | ss
Instagram | ig
WebTransfer | wt
Telegram | tg
Viber | vr
WhatsApp | wa
WebMoney | wm
QIWI | qm
Yandex | ym
Google | gm
ЦЕНОБОЙ | cb
Avito | at
Любой другой сервис | or


# Таблица стран и операторов:
Страна | оператор
------------ | -------------
ru_beeline | Россия/Beeline
ru_mts | Россия/MTS
ru_megafon | Россия/Megafon
ru_tele2 | Россия/Tele2
ru | Россия/Любой
ua_beeline | Украина/Beeline
ua_kyivstar | Украина/Киевстар
ua_djuice | Украина/djuice
ua_mts | Украина/MTS
ua_jeans | Украина/Jeans
ua_life | Украина/Life
ua | Украина/Любой
by | Белоруссия/Любой
pl | Польша/Любой
uk | Великобритания/Любой
or | Любой


# To do





