# Generator för nya stäng och städ

## Sätt upp utvecklingsmiljö

Installera [Pipenv](https://github.com/pypa/pipenv)

Clona detta Git-repo.

Ställa dig med en terminal i repo-rooten.

Sätt upp en pipenv enligt följande:

1. `pipenv --python 3.8`
1. `pipenv install -d` för att installera beroenden
1. `pipenv run test` för att köra testerna. Dessa ska alltid gå grönt i ett repo utan ocommitade ändringar

## Genererar nya stäng-och-städ

Säkerställ att alla stängda datum är inlaggda i kalendern som heter "Stängda dagar". Du gör det här https://medlem.forskolannatet.se/adm_program/modules/dates/dates.php

Säkerställ att de som ska sluta inom de kommande 3 månaderna har sina slutdatum inlagda.
Detta görs på en medlem under rubriken "Role memberships". Klicka på pennan på raden med texten "General - Member" och lägg in ett slutdatum.

Se till så det inte finns några gamla kalenderfiler kvar genom att köra kommandor `rm *.ics`

Anslut till Kardos VPN (för att nå databasen).

Se till att `database.py` har korrekt IP, username och password till databasen.

Kör kommandot `pipenv run python generate_sos.py`

VALBART: Man kan lägga på flaggorna `--extraTo a b c` samt `--lessTo x y z` där `a, b, c, x, y, z` är ID:n på medlemmar i medelemsregistret. Detta används om någon medlem ska tilldelas ett extra eller slippa ett SOS. Exemple: `pipenv run python generate_sos.py --extraTo 1 2 --lessTo 3 4`

När genereringen är färdig får du svara på frågan om det ska sparas i databasen eller ej:

- Ja? `y + enter` gör att schemat sparas i databasen och du kan maila ut det.
- Nej? `n + enter` gör att schemat inte sparas (dock genereras kalenderfilerna så de måste du ta bort manuellt)

Tryck `y + enter` så att det sparas.

Du har fått schema per dag och per familj i konsolen. Klipp och klistra detta till det mail som skickas till medelmmarna.

Släng kalenderfilerna med `rm *.ics`

Skicka mail.
