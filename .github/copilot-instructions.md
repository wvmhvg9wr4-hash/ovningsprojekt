# Instruktioner för GitHub Copilot

## Projektet
Detta är ett REST-API för kunder och beställningar, byggt med TypeScript, Express och PostgreSQL. Prisberäkningen använder en äldre Python-modul.

## Arbetsregler
- Läs relevant kod och befintliga tester innan du föreslår ändringar.
- Gör små och tydliga ändringar.
- Skriv tester före implementation när det är lämpligt.
- Ta aldrig bort, hoppa över eller inaktivera tester för att få dem godkända.
- Kör relevanta tester och redovisa resultatet.
- Följ projektets kodstandard.
- Ändra inte databasschemat utan en dokumenterad migreringsplan.
- Lägg aldrig in lösenord, hemligheter eller verklig kunddata i kod eller loggar.
- Be om godkännande innan riskfyllda eller destruktiva ändringar.
- Förklara vad som ändrats, varför och hur det har testats.

## Viktigt
Dessa instruktioner ersätter inte automatiska kontroller. Reglerna ska också stödjas av tester, kodkontroller och hooks.