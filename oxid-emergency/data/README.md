# Les dades

**Inventades.** Cap persona d'aquests fitxers existeix: els noms surten de dues llistes a l'atzar
i els números d'un generador amb llavor fixa. Tracta-les, però, com si fossin reals: és l'exercici.

Mig any (5 de gener – 28 de juny de 2026, 25 setmanes) d'un hospital comarcal inventat, l'Hospital
de Vallnova, exportat per **tres sistemes** diferents. Cada sistema té els seus costums.

| fitxer | sistema | separador | files | què és una fila |
|---|---|---|---:|---|
| `patients.csv` | admissions | `;` | 800 | un pacient |
| `visits.csv` | urgències i plantes | `,` | 2 089 | una visita (ingrés) |
| `labs.csv` | laboratori | `,` | 2 956 | un resultat d'una prova |
| `wards.csv` | l'hospital | `,` | 6 | una unitat |

## `patients.csv` (admissions, en català)

| columna | significat |
|---|---|
| `nhc` | número d'història clínica, 8 xifres. **Un codi**, no un número |
| `nom`, `cognoms` | identificadors directes |
| `data_naixement` | dd/mm/aaaa |
| `sexe` | `D` dona, `H` home, tal com el va teclejar el taulell |
| `codi_postal` | 5 xifres, tots comencen per `08` |
| `alcada_cm` | centímetres… normalment |
| `pes_kg` | quilos, amb coma decimal; `n/a` si no consta |

## `visits.csv`

| columna | significat |
|---|---|
| `visit_id` | identificador de la visita |
| `nhc` | el pacient |
| `ward` | codi de la unitat (`wards.csv`) |
| `admitted_at`, `discharged_at` | `aaaa-mm-dd hh:mm`; sense alta: encara hi és |
| `triage` | Manchester, només a `URG`: `blue` < `green` < `yellow` < `orange` < `red` |

## `labs.csv`

| columna | significat |
|---|---|
| `visit_id` | la visita on es va fer la prova (com a molt un resultat per prova i visita) |
| `test` | `glucose`, `hba1c`, `creatinine` |
| `value` | el valor; buit o `NA` si el laboratori no en va donar |
| `unit` | `mmol/L` (glucosa), `%` (HbA1c), `mg/dL` (creatinina)… i l'analitzador de cardiologia |
| `taken_at` | quan es va prendre la mostra |

## `wards.csv`

`code`, `name`, `floor`. La llista de l'hospital, tal com la mantenen.
