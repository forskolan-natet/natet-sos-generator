# Generator för nya stäng och städ

## Sätt upp utvecklingsmiljö

Installera [Pipenv](https://github.com/pypa/pipenv)

Clona detta Git-repo.

Ställa dig med en terminal i repo-rooten.

Sätt upp en pipenv enligt följande:

1. `pipenv --python 3.13`
1. `pipenv install -d` för att installera beroenden
1. `pipenv run test` för att köra testerna. Dessa ska alltid gå grönt i ett repo utan ocommitade ändringar

## Genererar nya stäng-och-städ

1. Säkerställ att alla stängda datum är inlaggda i closed_days.txt

1. Säkerställ att medlemsregistret är uppdaterat. Kontrollera med sekreteraren.

1. Fyll i properties.conf.

1. Kör kommandot `pipenv run python generate_sos.py`

1. När genereringen är färdig, kontrollera att det genererade schemat är korrekt.

1. Du har fått tre genererade filer.

   1. Schemat per dag skriver du ut och sätter upp på torkskåpen på avdelnignarna.

   1. Schemat per familj klistrar du in i det mail som skickas till medelmmarna.

   1. Schemat per dag med datum och ID istället för namn sparar du till nästa generering.

1. Skicka mailet! Klart!
