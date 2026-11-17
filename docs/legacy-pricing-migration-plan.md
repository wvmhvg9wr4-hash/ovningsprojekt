# Reversibel databasmigrationsplan – äldre prisberäkning

## 1. Syfte

Den här planen beskriver hur en framtida databasändring för prisberäkningen kan genomföras säkert och hur ändringen kan ångras vid problem.

**Ingen databasmigration genomförs i denna uppgift.** Dokumentet är en plan.

## 2. Nuläge

Prisberäkningen finns i `src/legacy/price_calc.py` och använder PostgreSQL.

Funktionen läser information från tre tabeller:

- `orders` – beställningar och rabattkoder.
- `order_lines` – antal och styckpriser.
- `discounts` – rabattsatser.

Resultatet består av nettopris, moms och totalpris. Beräkningen använder befintliga avrundningsregler som måste bevaras.

## 3. Föreslagen framtida förändring

En möjlig framtida förbättring är att lagra beräknade prisuppgifter direkt på beställningen.

Föreslagna nya kolumner i tabellen `orders`:

- `calculated_net`
- `calculated_vat`
- `calculated_total`

Kolumnerna ska använda datatypen `NUMERIC` för att undvika avrundningsfel från flyttal.

## 4. Framåtmigration (UP)

1. Ta en säkerhetskopia av databasen.
2. Lägg till de tre nya kolumnerna som tillåter `NULL`.
3. Behåll den gamla prisberäkningen oförändrad.
4. Fyll kolumnerna stegvis med resultat från den befintliga beräkningen.
5. Jämför lagrade värden med resultat från karakteriseringstesterna.
6. Aktivera läsning av de nya kolumnerna först när värdena har verifierats.

Exempel på planerad SQL:

```sql
ALTER TABLE orders
    ADD COLUMN calculated_net NUMERIC,
    ADD COLUMN calculated_vat NUMERIC,
    ADD COLUMN calculated_total NUMERIC;
```

## 5. Återställning (DOWN)

Om ändringen orsakar problem ska systemet först återgå till att läsa priser från den gamla Python-beräkningen.

När de nya kolumnerna inte längre används kan de tas bort:

```sql
ALTER TABLE orders
    DROP COLUMN calculated_net,
    DROP COLUMN calculated_vat,
    DROP COLUMN calculated_total;
```

**Viktigt:** Att ta bort kolumner raderar deras innehåll. Säkerhetskopian måste därför behållas tills ändringen är godkänd.

## 6. Tester och verifiering

Före och efter en framtida migration ska följande kontrolleras:

- Alla fem karakteriseringstester ska vara godkända.
- Nettopris, moms och totalpris ska vara oförändrade.
- Beställningar med och utan rabatt ska ge samma resultat som tidigare.
- Avrundning av moms och totalpris ska kontrolleras.
- Befintliga API-tester ska fortsätta fungera.
- Återställningen ska testas i en separat testdatabas.

## 7. Risker och säkerhetsåtgärder

- Säkerhetskopiera databasen före migrationen.
- Kontrollera att gamla och nya prisvärden stämmer överens.
- Behåll den gamla beräkningen tills den nya lösningen är verifierad.
- Testa återställningen innan ändringen används i produktion.
