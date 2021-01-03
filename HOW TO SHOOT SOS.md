# Genererar nya stäng-och-städ

Säkerställ att alla stängda datum är inlaggda i kalendern som heter "Stängda dagar". Du gör det här https://medlem.forskolannatet.se/adm_program/modules/dates/dates.php

Säkerställ att de som ska sluta inom de kommande 3 månaderna har sina slutdatum inlagda.
Detta görs på en medlem under rubriken "Role memberships". Klicka på pennan på raden med texten "General - Member" och lägg in ett slutdatum.

Se till så det inte finns några gamla kalenderfiler kvar genom att köra kommandor `rm *.ics`

Kör kommandot `pipenv run python generate_sos.py`

När genereringen är färdig får du svara på frågan om det ska sparas i databasen eller ej:

- Ja? `y + enter` gör att schemat sparas i databasen och du kan maila ut det.
- Nej? `n + enter` gör att schemat inte sparas (dock genereras kalenderfilerna så de måste du ta bort manuellt)

Tryck `y + enter` så att det sparas.

Du har fått schema per dag och per familj i konsolen. Klipp och klistra detta till det mail som skickas till medelmmarna.

Släng kalenderfilerna.

Skicka mailet!!
