# Informe · ECB A1-P1

Nom i cognoms:
URL pública:

Cada resposta porta **el número** (copiat de `uv run python -m emergency.pipeline` o d'un test) i
**una frase** que digui què vol dir o per què has decidit el que has decidit.

## R1 · Càrrega

- Files llegides de cada fitxer:
- Per què `nhc` i `codi_postal` no poden ser enters (un exemple de la teva sortida):

## R2 · Neteja

Per a cada correcció: què has trobat, quantes files, què has decidit.

| problema | files | decisió |
|---|---:|---|
| sexe amb espais o minúscules | | |
| triatge mal escrit | | |
| alçada en metres | | |
| pes 0 | | |
| glucosa en mg/dL | | |

## R3 · Validació

- Files rebutjades per fitxer i per motiu:
- Un exemple de missatge de Patito quan valides sense `split`:

## R4 · Joins

- Visites sense pacient, pacients sense visita:
- Què passa si fas el join amb `wards.csv` tal com és, i per què `validate="m:1"`:

## R5 · Agregacions

- Unitat amb l'estada mediana més llarga, i per què la mitjana és més alta que la mediana a totes:
- La setmana en què una unitat no va tenir cap visita:

## R6 · Estadística

- Glucosa: n, mitjana, mediana, desviació, tanques. Quina citaries i per què:
- Els valors per sobre de la tanca alta són errors? Com ho saps:
- r(HbA1c, glucosa) i la seva n. Què diu, i què no diu:

## R7 · Pseudonimització i anonimització

- Per què un SHA-256 de l'nhc sense clau no protegeix ningú (quant trigaries a desfer-lo):
- On és la clau a la teva màquina virtual, i què passa si es filtra:
- k-anonimitat segons l'amplada de la franja d'edat:

| franja | files publicades | persones suprimides | % |
|---:|---:|---:|---:|
| 10 | | | |
| 20 | | | |
| 30 | | | |

- La franja que has triat, i per què:
- La publicació és anònima o pseudonimitzada? Per què:

## R8–R9 · Servidor i pàgina

- Bytes de `/api/points` i de `/api/glucose.svg` (`curl -s -o /dev/null -w '%{size_download}'`):
- Per què l'histograma es dibuixa al servidor i la dispersió al navegador:

## R10 · Desplegament

- Mida de la màquina, disc i oferta de la subscripció (`az account show`):
- Què has de fer quan s'acabi la correcció perquè no costi res:
