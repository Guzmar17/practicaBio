# C044 A1 · ecb-emergency

**ECB · A1-P1.** Mig any d'urgències d'un hospital inventat: carregar-lo, netejar-lo, validar-lo,
ajuntar-lo, resumir-lo, pseudonimitzar-lo i publicar-ne només el que es pot publicar, en una
pàgina Oxid servida per oxid-server en una màquina virtual gratuïta d'Azure.

Aquest repositori conté la bastida i l'enunciat executable: l'estructura, les signatures, les dades,
les proves i el camí de desplegament ja hi són. Tu escrius el cos de cada funció que diu
`raise NotImplementedError("Rn")` i cada `TODO Rn`.

## Enunciat de l'examen C044 A1

### Objectiu

Construeix una aplicació de dades completa sobre mig any d'urgències de l'Hospital de Vallnova.
La solució ha de carregar quatre exportacions heterogènies, netejar-les sense amagar decisions,
validar i separar les files errònies, combinar-les, produir resums i estadístiques, preparar una
publicació que protegeixi les persones i mostrar-la en una aplicació web Oxid.

**L'alumne construeix la solució.** Implementa R1–R9, documenta els resultats i les decisions a
`INFORME.md` i desplega el resultat a R10. No canviïs les dades, les signatures ni les proves per
fer-les passar. Els docstrings dels fitxers indicats i les proves són part del contracte.

### R1 · Càrrega

Implementa `emergency/load.py`. Llegeix cada CSV una sola vegada, conserva totes les files i
assigna els noms i tipus demanats. Els codis com l'NHC i el codi postal són text i han de conservar
els zeros inicials; les dates, hores, enums i nombres han de quedar tipats. En aquesta fase no
corregeixis dades: carrega exactament el que diu cada sistema.

### R2 · Neteja i variables derivades

Implementa `emergency/clean.py` amb expressions de Polars i comenta cada decisió. Normalitza el
sexe i el triatge, converteix dates i decimals, interpreta les alçades en metres, tracta el pes zero
com a desconegut i unifica la glucosa en mmol/L. Calcula també la durada de l'estada, l'edat en
anys complets en el moment de l'ingrés i l'IMC. No intentis corregir aquí els valors implausibles:
corresponen a R3.

### R3 · Validació

Implementa `emergency/model.py`. Expressa les regles de qualitat amb Polars, separa cada conjunt
en files acceptades i rebutjades i conserva en aquestes últimes tots els motius infringits. Una
regla nul·la no rebutja una fila. Defineix també models Patito equivalents que rebutgin les dades
brutes incorrectes i validin les files conservades. Cap fila pot desaparèixer en silenci.

### R4 · Combinació

Implementa `emergency/combine.py`. Resol la unitat duplicada conservant la primera definició,
compta amb anti-joins què perd un inner join entre visites i pacients i crea una fila per visita
amb les dades del pacient i de la unitat. Declara els joins de consulta com a `m:1` perquè una clau
duplicada provoqui un error en lloc de multiplicar files. Incorpora els resultats de laboratori en
columnes `glucose`, `hba1c` i `creatinine`.

### R5 · Agregacions

Implementa `emergency/summary.py`: resum per unitat amb nombre de visites i pacients, estada
mitjana i mediana i proporció de triatges greus; recompte setmanal per a les cinc unitats i les 25
setmanes, incloent zeros; evolució entre la primera i l'última glucosa dels pacients repetidors; i
diferència de cada glucosa respecte de la mitjana de la seva pròpia unitat.

### R6 · Estadística

Implementa `emergency/statistic.py`. Descriu la glucosa amb `n`, absents, mitjana, mediana,
desviació estàndard mostral, quartils lineals, IQR, tanques d'1,5 IQR i nombre d'atípics. Retorna
els episodis per sobre de la tanca alta i calcula la correlació de Pearson entre HbA1c i glucosa,
sempre indicant quantes observacions sustenten el resultat.

### R7 · Privacitat

Implementa `emergency/privacy.py`. Llegeix una clau hexadecimal exclusivament de
`ECB_EMERGENCY_KEY`, crea pseudònims HMAC-SHA256 estables i generalitza edat, codi postal i temps.
La publicació no pot contenir identificadors directes ni dates o hores exactes. Calcula
k-anonimat sobre persones distintes, no sobre files, i suprimeix els grups de quasi-identificadors
amb menys de cinc persones. El model Patito de publicació ha de refusar qualsevol columna extra.

### R8 · Servidor

Completa `server.py`. L'anàlisi s'executa una vegada en arrencar i les rutes només retornen
agregats o punts anonimitzats: resum d'unitats, 25 setmanes de la unitat demanada, estadístiques,
parelles HbA1c–glucosa i l'histograma SVG generat al servidor. Una unitat inexistent respon 404.
Cap ruta pot filtrar noms, NHC ni pseudònims.

### R9 · Pàgina Oxid

Completa `app/app.py`. La pàgina consumeix exclusivament `/api`: gràfic de barres per unitat,
línia de 25 setmanes amb selector d'unitat accessible, histograma servit com a imatge, dispersió
HbA1c–glucosa amb selecció rectangular i una síntesi textual de les estadístiques i la privacitat.
El codi del navegador no importa `emergency` ni `server.py`.

### R10 · Desplegament Azure i lliurament

Desplega l'últim commit en una màquina virtual gratuïta d'Azure amb els scripts de `deploy/`.
La URL pública ha de servir l'aplicació completa per **HTTPS**, amb un certificat TLS vàlid. La
clau de pseudonimització es crea i roman a la màquina. Lliura el repositori, `INFORME.md` complet
i la URL pública; elimina el grup de recursos quan acabi la correcció per evitar costos.

### Criteri d'acceptació

El lliurament està complet quan `mk check` passa des d'un entorn net, `INFORME.md` conté els
resultats i les justificacions demanades, i l'aplicació funciona de cap a cap a la seva URL
pública d'Azure amb HTTPS i un certificat TLS vàlid. La puntuació i qualsevol aclariment publicat
al Moodle prevalen si difereixen d'aquest resum.

## Engegar

```sh
mk sync                                       # Python 3.14, oxid, polars, patito, pytest
mk test                                       # les proves d'acceptació, una per requisit
mk test -- tests/test_r1_load.py               # només les d'un requisit
mk check                                      # format, pàgina, totes les proves i build final
uv run python -m emergency.pipeline           # els números que demana INFORME.md
```

La pàgina es pot obrir abans d'acabar el servidor:

```sh
mk dev                                        # http://127.0.0.1:8600, pàgina de bastida sense l'API
```

Quan R1–R8 ja funcionen, engega també l'API (cal una clau, mira R7):

```sh
export ECB_EMERGENCY_KEY=$(uv run python -c "import secrets; print(secrets.token_hex(32))")
mk dev --full
```

El servidor executa tota l'anàlisi en arrencar: fins que R1–R7 no
funcionin, no arrenca, i l'error que veus és el primer `NotImplementedError` que troba.

## On és cada requisit

| | fitxer | prova |
|---|---|---|
| R1 càrrega | `emergency/load.py` | `tests/test_r1_load.py` |
| R2 neteja | `emergency/clean.py` | `tests/test_r2_clean.py` |
| R3 validació | `emergency/model.py` | `tests/test_r3_model.py` |
| R4 joins | `emergency/combine.py` | `tests/test_r4_combine.py` |
| R5 agregacions | `emergency/summary.py` | `tests/test_r5_summary.py` |
| R6 estadística | `emergency/statistic.py` | `tests/test_r6_statistic.py` |
| R7 privacitat | `emergency/privacy.py` | `tests/test_r7_privacy.py` |
| R8 servidor | `server.py` | `tests/test_r8_server.py` |
| R9 pàgina | `app/app.py` | `tests/test_r9_page.py` |
| R10 desplegament | `deploy/` | la URL pública |

`emergency/pipeline.py` els encadena en ordre i ja està fet: llegeix-lo primer. Les dades i què
vol dir cada columna: `data/README.md`. No canviïs els fitxers de `data/` ni les proves.

## Desplegar a Azure (R10)

Cal [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) i una subscripció
**Azure for Students** (`az login`). Des de la carpeta del repositori, en un terminal bash
(macOS, Linux, WSL o Git Bash):

```sh
deploy/azure.sh ecb-<nom>-<cognom>            # la màquina: B1s, disc P6 de 64 GiB, ports 80 i 443
ssh azureuser@ecb-<nom>-<cognom>.francecentral.cloudapp.azure.com cloud-init status --wait
deploy/push.sh ecb-<nom>-<cognom>.francecentral.cloudapp.azure.com
```

`push.sh` envia l'últim commit (no el que no has confirmat), i a la màquina `install.sh` crea
l'entorn amb `uv sync --frozen`, construeix la pàgina, reinicia el servei i posa Caddy davant amb
HTTPS. Cada canvi posterior: commit i `deploy/push.sh <host>` una altra vegada.

La clau de pseudonimització es crea **a la màquina** en el primer arrencada
(`/etc/ecb-emergency.env`) i no surt mai d'allà ni entra al repositori.

Què costa: la màquina i el disc entren en les 750 hores gratuïtes del primer any si són
**exactament** aquests; l'adreça IP pública es paga des de la primera hora (uns 3 € al mes).
Quan la pràctica estigui corregida:

```sh
az group delete -n rg-ecb --yes
```

## Ús de la IA

L'enunciat ho explica: primer tu, després que revisi. Has de poder explicar i reescriure sense
ajuda tot el que lliuris.
