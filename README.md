DETECTAREA INFLUENȚEI ÎN ȘTIRILE SPORTIVE

1. DESCRIERE ȘI MODEL MATEMATIC
Acest proiect utilizează tehnici de procesare a limbajului natural (NLP) pentru 
a clasifica știrile sportive.

Modelul utilizat este NAIVE BAYES (MultinomialNB), bazat pe:
A. Teorema lui Bayes: P(c|x) = (P(x|c) * P(c)) / P(x)
   Unde calculăm probabilitatea ca un document 'x' să aparțină clasei 'c'.

B. Asumpția "Naive": 
   Presupunem că apariția unui cuvânt este independentă de apariția altora.

C. Modelul Multinomial:
   Ia în calcul frecvența cuvintelor (de câte ori apare un termen), nu doar 
   prezența lor.

2. STRUCTURA CODULUI (Fișiere Principale)
Proiectul este împărțit în trei module:

1. colectare_date.py
   - Funcție: Web Scraping.
   - Extrage titlul și conținutul de pe site-uri de sport (DigiSport, GSP, ProSport).

2. procesare_date.py
   - Funcție: Procesare și Etichetare.
   - Curăță textul (elimină stopwords, punctuație).
   - Etichetează automat în "Despre_Becali" sau "Altele".

3. model_bayes.py
   - Funcție: Antrenare AI.
   - Vectorizează textul (Bag of Words).
   - Antrenează modelul MultinomialNB și calculează acuratețea.

3. INSTRUCȚIUNI DE UTILIZARE

PASUL 1: PREGĂTIREA MEDIULUI
Instalează bibliotecile necesare:
   pip install pandas scikit-learn nltk beautifulsoup4 requests unidecode

PASUL 2: DESCĂRCAREA DATELOR NLTK
Rulează în Python:
   import nltk
   nltk.download('stopwords')
   nltk.download('punkt')

PASUL 3: RULAREA SECVENȚIALĂ
1. Colectare:   python colectare_date.py
2. Procesare:   python procesare_date.py
3. Model:       python model_bayes.py

4. EXEMPLE DE UTILIZARE 
După rularea modelului, poți testa interactiv:

Exemplu 1 (Becali):
   Input: "mm stoica a plecat"
   Text procesat: "patronul fcsb tunat fulgerat palat stoica plecat"
   Predicție: Despre_Becali (Probabilitate: 98.45%)

Exemplu 2 (Altele):
   Input: "simona halep a castigat meciul de tenis la madrid"
   Text procesat: "simona halep castigat meciul tenis madrid..."
   Predicție: Altele (Probabilitate: 99.12%)

5. REFERINȚE BIBLIOGRAFICE
1. Manning, C. D., Raghavan, P., & Schütze, H. (2008). Introduction to 
   Information Retrieval. Cambridge University Press.
2. Jurafsky, D., & Martin, J. H. (2023). Speech and Language Processing.
3. Scikit-learn Developers (2023) - Documentație oficială MultinomialNB.
4. Bird, S., Klein, E. (2009). Natural Language Processing with Python.
