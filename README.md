# Anonymous polls
Aplikace pro přidávání anonymních dotazníků pro předměty KI/NSQL a KI/LTP. Aplikace je vyvíjená v jazyce [Python](https://www.python.org) a frameworku [Flask](https://flask.palletsprojects.com/en/3.0.x/). K ukládání dotazníků je použitá databáze [Mongo](https://www.mongodb.com) a [redis](https://redis.io) jako cache při hlasování.
## Návod
Uživatel začíná na úvodní obrazovce. Po uživateli je požadována registrace pro přidávání dotazníků a pro hlasování.

![image](https://github.com/Helmanzs/NSQL/assets/86473760/7127751c-997f-42ad-975b-7feda8a37e03)

Při vstupu na stránku `/populate` se do aplikace vloží základní dummy data.

![image](https://github.com/Helmanzs/NSQL/assets/86473760/ca9ed7b3-0195-4c42-a4b3-f4a06452e467)

Přidají se 3 dotazníky a 3 účty.
Uživatelské jméno | Heslo
--- | ---
kaja | kaja
pepa | pepa
franta | franta

Uživatel nemůže hlasovat ve vlastních dotaznících a nebo na dotazníky u kterých již hlasoval.

![image](https://github.com/Helmanzs/NSQL/assets/86473760/d7c50e8c-0d3b-41e8-b2a0-d2b8604a7841)


