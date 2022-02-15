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

1. Säkerställ att alla stängda datum är inlaggda i kalendern som heter "Stängda dagar". Du gör det här https://medlem.forskolannatet.se/adm_program/modules/dates/dates.php

1. Säkerställ att de som ska sluta inom de kommande 3 månaderna har sina slutdatum inlagda.
   Detta görs på en medlem under rubriken "Role memberships". Klicka på pennan på raden med texten "General - Member" och lägg in ett slutdatum.

1. Se till så det inte finns några gamla kalenderfiler kvar genom att köra kommandor `rm *.ics`

1. Anslut till Kardos VPN (för att nå databasen).

1. Se till att `database.py` har korrekt IP, username och password till databasen.

1. Kör kommandot `pipenv run python generate_sos.py`

   - VALBART: Man kan specificera minsta antal dagar som man som familj måste ha mellan två stäng och städ. Lägg på flaggan `--minNrOfDaysBetweenSos x` där `x` är antalet dagar. Om inget anges kommer `10` dagar användas. Exemple: `pipenv run python generate_sos.py --minNrOfDaysBetweenSos 12`. Detta kan vara bra att använda om scriptet inte klarar av att generera ett giltigt schema med så mycket som 10 dagar mellan SOS.

   - VALBART: Man kan lägga på flaggorna `--extraTo a b c` samt `--lessTo x y z` där `a, b, c, x, y, z` är ID:n på medlemmar i medelemsregistret (man ser det i URL:en för en medlem). Detta används om någon medlem ska tilldelas ett extra eller slippa ett SOS. Exemple: `pipenv run python generate_sos.py --extraTo 1 2 --lessTo 3 4`

1. När genereringen är färdig får du svara på frågan om det ska sparas i databasen eller ej. Om schemat ser bra ut och du vill använda det så är det viktigt att det blir sparat i databasen. Nästa generering som görs kommer nämligen utgå från de stäng och städ som redan ligger i databasen.

   - Ja? `y + enter` gör att schemat sparas i databasen och du kan maila ut det.
   - Nej? `n + enter` gör att schemat inte sparas (dock genereras kalenderfilerna så de måste du ta bort manuellt)

   Tryck `y + enter` så att det sparas.

1. Du har fått schema per dag och ett per familj i konsolen.

   1. Schemat per dag klistrar du in i ett kalkylark för att skriva ut och upp på torkskåpen på avdelnignarna.

   1. Schemat per familj klistrar jag in i det mail som skickas till medelmmarna.

1. Bifoga de skapade kalender-filerna i mailet.

1. Släng kalenderfilerna med `rm *.ics`

1. Skicka mailet! Klart!
