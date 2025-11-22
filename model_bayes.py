import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
import ast 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from unidecode import unidecode

FISIER_PROCESAT = "articole_procesate.csv"

stop_words_ro_raw = set(stopwords.words('romanian'))
stop_words_ro = {unidecode(w) for w in stop_words_ro_raw}
stop_words_ro.update(['citeste', 'spus', 'declarat', 'citi', 'ani', 'intr', 'foto'])

df = pd.read_csv(FISIER_PROCESAT)

def proceseaza_text(text):
    text = text.lower()
    tokens = word_tokenize(text)
    cuvinte_curatate = []
    for cuvant in tokens:
        if (cuvant.isalpha() and 
            cuvant not in stop_words_ro and 
            len(cuvant) > 2): 
            cuvinte_curatate.append(cuvant)
            
    return cuvinte_curatate

def uneste_cuvintele(lista_string):
    lista_reala = ast.literal_eval(lista_string)
    return " ".join(lista_reala)

df['text_unit'] = df['text_procesat'].apply(uneste_cuvintele)

X = df['text_unit']
y = df['eticheta']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

print(f"Date impartite: {len(X_train)} articole pentru antrenament si {len(X_test)} pentru test.")

vectorizer = CountVectorizer()
X_train_counts = vectorizer.fit_transform(X_train)
X_test_counts = vectorizer.transform(X_test)

#print("Se antreneaza modelul Naive Bayes...")
model = MultinomialNB()
model.fit(X_train_counts, y_train)
#print("Model antrenat.")

#print("Se evalueaza modelul pe setul de test...")
y_pred = model.predict(X_test_counts)

acuratete = accuracy_score(y_test, y_pred)

print("\n--- REZULTATE EVALUARE MODEL ---")
print(f"Acuratete: {acuratete * 100:.2f}%")

print("\n--- TESTARE PE TEXT NOU ---")
while True:
    text_brut = input("\nScrie text pt test sau exit pt a inchide: ")
    
    if text_brut.lower() == 'exit':
        break
        
    lista_cuvinte = proceseaza_text(text_brut)
    text_procesat = " ".join(lista_cuvinte)
    
    print(text_procesat)
    
    text_counts = vectorizer.transform([text_procesat])
    
    pred = model.predict(text_counts)
    prob = model.predict_proba(text_counts)
    
    print(f"Textul procesat: '{text_procesat}'")
    print(f"Predictie: {pred[0]}")
    

    if pred[0] == 'Despre_Becali':
        prob_becali = prob[0][1]
        print(f"Probabilitate sa fie 'Despre_Becali': {prob_becali * 100:.2f}%")
    else:
        prob_altele = prob[0][0]
        print(f"Probabilitate sa fie 'Altele': {prob_altele * 100:.2f}%")