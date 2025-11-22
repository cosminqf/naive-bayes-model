import pandas as pd 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from unidecode import unidecode

ETICHETE_BECALI = [
    'becali', 'gigi', 'jiji',
    'patronul', 'latifundiarul',
    'fcsb', 'steaua',
    'mm', 'stoica', 'pintilii', 'charalambous', 'olaru',
    'palat', 'palatul'
]

ETICHETE_ALTELE = [
    'dinamo', 'cfr', 'rapid', 'craiova', 'cluj',
    'romania', 'nationala', 'bosnia', 'ungaria', 'spania', 'italia', 'kosovo',
    'portugalia', 'mondial', 'cm', 'baraj',
    'lucescu', 'hagi', 'mutu', 'chivu', 'rotaru', 'varga', 'sucu', 
    'radoi', 'pancu', 'iordanescu', 'boloni', 'sumudica', 'petrea', 
    'balint', 'rusescu', 'goian', 'porumboiu', 'gradinescu', 'avram',
    'ronaldo', 'neymar', 'kroos', 'dragusin', 'birligea', 'man', 
    'dragus', 'munteanu', 'insigne', 'dzeko',
    'tenis', 'halep', 'cirstea', 'swiatek', 'alcaraz', 'sinner', 
    'djokovic', 'fritz', 'wta', 'turneul-campionilor',
    'handbal', 'baschet', 'nba', 'csm', 'volei'
]

NUME_FISIER_BRUT = "articole_brute.csv"
NUME_FISIER_PROCESAT = "articole_procesate.csv"

stop_words_ro_raw = set(stopwords.words('romanian'))
stop_words_ro = {unidecode(w) for w in stop_words_ro_raw}
stop_words_ro.update(['citeste', 'spus', 'declarat', 'citi', 'ani', 'intr', 'foto'])

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

if __name__ == "__main__":
    
    df = pd.read_csv(NUME_FISIER_BRUT)
    
    date_procesate = [] 
    
    articole_becali = 0
    articole_altele = 0
    articole_ignorate = 0

    for index, rand in df.iterrows():
        titlu = str(rand['titlu']).lower()
        continut = str(rand['continut'])
        
        eticheta = None
        
        #print(titlu)
        if any(keyword in titlu for keyword in ETICHETE_BECALI):
            eticheta = "Despre_Becali"
            articole_becali += 1
        elif any(keyword in titlu for keyword in ETICHETE_ALTELE):
            eticheta = "Altele"
            articole_altele += 1
        else:
            articole_ignorate += 1
            
        lista_cuvinte = proceseaza_text(continut)
        
        if eticheta != None:
            date_procesate.append({
                    "eticheta": eticheta,
                    "text_procesat": lista_cuvinte 
            })
    
    df_procesat = pd.DataFrame(date_procesate)
        
    df_procesat.to_csv(NUME_FISIER_PROCESAT, index=False, encoding='utf-8')
        
    print(f"\n--- TERMINAT ---")
    print(f"Am salvat {len(df_procesat)} articole in '{NUME_FISIER_PROCESAT}'.")
    print(f"  Articole 'Becali': {articole_becali}")
    print(f"  Articole 'Altele': {articole_altele}")
    print(f"  Articole ignorate (nu au eticheta relevanta pt noi deci pot fi date murdare): {articole_ignorate}")