# Kodkarta – äldre prisberäkning

## 1. Syfte

Den här kodkartan beskriver hur projektets äldre prisberäkning fungerar, vilka filer som berörs och vilka beroenden som finns. Den används som stöd vid moderniseringen.

## 2. Berörda filer

| Fil | Ansvar |
|---|---|
| `src/legacy/price_calc.py` | Beräknar nettopris, moms och totalpris för en beställning. |
| `src/pricing/legacyPrice.ts` | Anropar Python-programmet från TypeScript och tar emot resultatet. |
| `tests/test_price_calc.py` | Innehåller fem karakteriseringstester som kontrollerar befintligt beteende. |
| `db/schema.sql` | Definierar databasens tabeller. |
| `db/seed.sql` | Innehåller testdata för beställningar och rabatter. |

## 3. Flöde

1. TypeScript-funktionen `calcPrice(orderId)` anropar Python-programmet.
2. Python-funktionen `calc_price(order_id)` ansluter till PostgreSQL.
3. Rabattkod och orderrader hämtas från databasen.
4. Nettopris, moms och totalpris beräknas.
5. Resultatet skrivs som JSON.
6. TypeScript läser JSON-resultatet.

## 4. Viktiga beroenden

- Python och biblioteket `psycopg`.
- PostgreSQL-databasen.
- Tabellerna `orders`, `order_lines` och `discounts`.
- TypeScript och Node.js för anropet till Python.

## 5. Risker

- Avrundningsreglerna får inte förändras.
- Rabattberäkningen måste fortsätta ge samma resultat.
- Databasfel behöver hanteras säkert.
- TypeScript är beroende av att Python-programmet returnerar rätt JSON-format.

## 6. Genomförd modernisering

Tre separata refaktoreringar har genomförts:

1. SQL-frågorna har ändrats till parametriserade frågor.
2. Databasanslutningen öppnas vid beräkningen och stängs vid normala returvägar.
3. Loggfilen hanteras med `with`, så att den stängs automatiskt.

Fem karakteriseringstester har körts och godkänts efter ändringarna.

## 7. Avgränsning

Prisberäkningens affärsregler och avrundning har inte ändrats. Ingen databasmigration har genomförts.