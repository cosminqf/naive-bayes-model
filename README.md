# 📘 Clasificator Articole Sportive (Știri despre Becali vs Altele)

Acest proiect realizează automat:

1.  **Colectarea articolelor** (web scraping)\
2.  **Procesarea și etichetarea conținutului**\
3.  **Antrenarea unui model Naive Bayes** care clasifică articolele în:
    -   `Despre_Becali`\
    -   `Altele`

## Structura proiectului

    /proiect
    │── colectare_date.py
    │── procesare_date.py
    │── model_bayes.py
    │── articole_brute.csv        (generat automat)
    │── articole_procesate.csv    (generat automat)


## 1. Colectarea datelor

**Script:** `colectare_date.py`\
**Output:** `articole_brute.csv`

Scraperul extrage articole de pe:

-   prosport.ro\
-   gsp.ro\
-   digisport.ro

Pentru fiecare articol se salvează:

-   URL\
-   domeniu\
-   titlu\
-   conținut

### Rulare:

``` bash
python3 colectare_date.py
```

## 2. Procesarea și etichetarea datelor

**Script:** `procesare_date.py`\
**Input:** `articole_brute.csv`\
**Output:** `articole_procesate.csv`

Operațiile efectuate:

-   convertire la lowercase\
-   tokenizare\
-   eliminare stop-words românești\
-   filtrare cuvinte scurte / non-alfabetice\
-   detecție automată a etichetei din titlu pe baza listelor:
    -   `ETICHETE_BECALI`
    -   `ETICHETE_ALTELE`

Articolele fără cuvinte-cheie relevante sunt ignorate.

### Rulare:

``` bash
python3 procesare_date.py
```


## 3. Model Naive Bayes

**Script:** `model_bayes.py`\
**Input:** `articole_procesate.csv`

Ce face scriptul:

-   reconstruiește textul procesat\
-   vectorizează cu CountVectorizer\
-   împarte setul în train/test\
-   antrenează modelul `MultinomialNB`\
-   afișează acuratețea\
-   oferă un prompt pentru testare manuală

### Rulare:

``` bash
python3 model_bayes.py
```

Exemplu testare:

    Scrie text pt test sau exit pt a inchide:
    > Becali a anunțat...


## Dependențe

Instalează pachetele necesare:

``` bash
pip install requests beautifulsoup4 pandas scikit-learn nltk unidecode
```

### Setup NLTK:

``` python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```
