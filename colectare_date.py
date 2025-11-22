import requests
from bs4 import BeautifulSoup
import time
import csv 
from urllib.parse import urlparse

SITE_RULES = {
    "www.prosport.ro": {
        "titlu":    {"tag": "div", "clasa": "single__title", "cauta_in_interior": "h1"},
        "continut": {"tag": "div", "clasa": "single__text"}
    },
    "www.gsp.ro": {
        "titlu":    {"tag": "div", "clasa": "article-container", "cauta_in_interior": "h1"},
        "continut": {"tag": "div", "clasa": "article-body-container"}
    },
    "www.digisport.ro": {
        "container": {"tag": "div", "clasa": "container article-page article-content"}
    }
}

ARTICOLE_DE_SCRAPAT = [
    # --- PROSPORT.RO ---
    "https://www.prosport.ro/fotbal-intern/superliga/planul-din-spatele-numirii-lui-toni-petrea-la-universitatea-craiova-de-ce-a-fost-preferat-ca-secund-al-portughezului-filipe-coelho-exclusiv-20323193",
    "https://www.prosport.ro/fotbal-intern/nationala/s-a-schimbat-totul-duminica-seara-pentru-romania-in-barajul-de-mondial-cum-arata-scenariul-de-cosmar-si-cel-ideal-dupa-ce-ucraina-a-prins-urna-1-20323038",
    "https://www.prosport.ro/alte-sporturi/tenis/momente-de-groaza-la-meciul-jannik-sinner-carlos-alcaraz-dupa-ce-doi-spectatori-au-decedat-inca-unei-persoane-i-s-a-facut-rau-la-turneul-campionilor-chiar-in-timpul-finalei-video-20323249",
    "https://www.prosport.ro/fotbal-intern/superliga/gigi-becali-il-vrea-pe-denis-dragus-la-fcsb-patronul-campioanei-vrea-sa-i-dea-un-salariu-ametitor-lui-asa-o-sa-ii-fac-20322876",
    "https://www.prosport.ro/fotbal-intern/nationala/anuntul-momentului-ce-a-hotarat-mircea-lucescu-dupa-bosnia-romania-3-1-20322867",
    "https://www.prosport.ro/fotbal-intern/nationala/gata-bosniacilor-le-a-ajuns-si-l-au-jignit-pe-lucescu-desi-acesta-are-80-de-ani-20323169",
    "https://www.prosport.ro/fotbal-intern/nationala/gigi-becali-a-vazut-bosnia-romania-si-s-a-dezlantuit-in-direct-esti-vagabond-nu-am-vazut-asa-ceva-20322982",
    "https://www.prosport.ro/fotbal-intern/superliga/gigi-becali-a-negociat-din-nou-in-secret-transferul-lui-louis-munteanu-la-fcsb-si-a-facut-o-oferta-imbunatatita-20322844",
    "https://www.prosport.ro/fotbal-intern/de-ce-vrea-gigi-becali-sa-i-puna-sofer-si-supraveghetor-lui-louis-munteanu-fotbalistul-filmat-in-clubul-de-noapte-20321997",
    "https://www.prosport.ro/alte-sporturi/tenis/simona-halep-si-sorana-cirstea-decizii-controversate-dupa-ce-si-au-luat-apartamente-in-dubai-ce-au-facut-chiar-in-timpul-meciului-nationalei-romaniei-20323069",
    "https://www.prosport.ro/alte-sporturi/tenis/simona-halep-intrebata-daca-uraste-tenisul-dupa-ce-a-fost-ingropata-de-itia-raspunsul-sincer-al-romancei-totul-a-fost-demonstrat-20322428",
    "https://www.prosport.ro/fotbal-intern/superliga/fcsb-intra-in-infernul-de-o-luna-ce-program-de-cosmar-are-echipa-lui-charalambous-si-pintilii-20319737",
    "https://www.prosport.ro/cupa-romaniei/fcsb-la-un-pas-sa-piarda-meciul-la-masa-verde-si-sa-fie-depunctata-in-superliga-m-a-intrebat-gigi-becali-ce-se-intampla-20312385",
    "https://www.prosport.ro/alte-sporturi/tenis/polonia-romania-in-play-off-ul-billie-jean-king-cup-live-text-online-ruxandra-bertea-si-linda-klimovicova-deschid-intalnirea-decisiva-pentru-calificare-cine-o-va-infrunta-pe-iga-swiatek-20322927",
    "https://www.prosport.ro/fotbal-intern/nationala/adrian-mutu-i-a-pus-la-zid-pe-ianis-hagi-si-pe-dennis-man-dupa-bosnia-romania-20322989",
    "https://www.prosport.ro/fotbal-intern/superliga/filipe-coelho-are-motive-de-ingrijorare-anzor-mekvabishvili-a-iesit-accidentat-in-meciul-cu-spania-jucatorul-universitatii-craiova-evidentiat-alaturi-de-kvaratskhelia-de-presa-spaniola-20322990",
    "https://www.prosport.ro/campionatul-mondial-2026/spania-are-golaveraj-19-0-dar-exista-un-scenariu-apocaliptic-cu-000001-la-suta-sanse-prin-care-rateaza-calificarea-directa-la-campionatul-mondial-din-2026-20322858",
    "https://www.prosport.ro/fotbal-intern/nationala/ce-fundasi-centrali-vom-avea-in-bosnia-hertegovina-romania-el-e-primul-ales-si-nu-mai-vreau-sa-aud-asta-versus-a-gresit-la-ambele-goluri-din-doar-al-doilea-lui-meci-ca-20320159",
    "https://www.prosport.ro/fotbal-intern/nationala/patronul-din-superliga-cere-schimbarea-selectionerului-romaniei-lucescu-va-iesi-sifonat-boloni-e-scaparea-noastra-la-baraj-exclusiv-20322744",
    "https://www.prosport.ro/campionatul-mondial-2026/imaginile-care-ne-dor-s-a-dezlantuit-nebunia-in-vestiar-dupa-bosnia-romania-20322707",
    "https://www.prosport.ro/alte-sporturi/handbal/anuntul-selectionerului-nationalei-de-handbal-feminin-a-romaniei-despre-campionatul-mondial-din-germania-si-olanda-nu-vreau-sa-transmit-asta-20323062",
    "https://www.prosport.ro/alte-sporturi/handbal/alexandru-dedu-parere-transanta-despre-situatia-handbalului-romanesc-puteti-sa-i-aduceti-si-pe-putin-si-trump-20320989",
    "https://www.prosport.ro/alte-sporturi/handbal/nu-se-intampla-doar-la-fotbal-antrenor-paravan-pentru-bogdan-burcea-in-ehf-european-league-20319948",
    "https://www.prosport.ro/alte-sporturi/handbal/gestul-de-suflet-al-fanilor-lui-dinamo-din-superliga-cainii-se-impart-in-europa-pentru-doua-meciuri-tari-care-se-joaca-in-acelasi-timp-exclusiv-20319174",
    "https://www.prosport.ro/alte-sporturi/handbal/csm-bucuresti-victorie-mare-in-liga-campionilor-cum-s-a-descurcat-campioana-romaniei-in-primul-meci-fara-adi-vasile-20317784",
    "https://www.prosport.ro/fotbal-intern/superliga/cine-e-pe-primul-loc-alex-dobre-a-inceput-sa-cante-la-flash-interviu-dupa-rapid-fc-arges-2-0-20317901",
    "https://www.prosport.ro/fotbal-intern/bogdan-andone-cere-intariri-dupa-rapid-fc-arges-2-0-vom-avea-nevoie-de-solutii-20317885",
    "https://www.prosport.ro/fotbal-intern/superliga/vinde-echipa-anuntul-lui-giovanni-becali-despre-decizia-lui-gigi-becali-dupa-ce-s-a-vorbit-de-o-oferta-de-100-000-000-de-euro-pentru-fcsb-20317870",
    "https://www.prosport.ro/fotbal-intern/superliga/mihai-stoica-a-anuntat-noua-achizitie-de-la-fcsb-vine-il-cunosc-cel-mai-bine-20317653",
    "https://www.prosport.ro/fotbal-intern/lovitura-bomba-intre-rivalele-din-cluj-emil-boc-si-u-l-au-ofertat-pe-omul-cheie-care-a-plecat-de-la-cfr-exclusiv-20317819",
    "https://www.prosport.ro/fotbal-intern/superliga/reactia-fcsb-dupa-moartea-lui-emerich-ienei-nu-a-folosit-cuvantul-steaua-20315081",
    "https://www.prosport.ro/fotbal-intern/superliga/gigi-becali-reactie-tulburatoare-dupa-moartea-marelui-emerich-ienei-maine-poimaine-sunt-si-eu-in-cosciug-20315055",
    "https://www.prosport.ro/fotbal-intern/superliga/marea-suparare-a-lui-emerich-ienei-statul-roman-ii-taiase-renta-viagera-20314998",
    # --- GSP ---
    "https://www.gsp.ro/fotbal/nationala/gigi-becali-reactie-bosnia-romania-preliminarii-cm-2026-868107.html",
    "https://www.gsp.ro/fotbal/nationala/10-idei-de-la-leo-grozavu-romania-mircea-lucescu-868163.html",
    "https://www.gsp.ro/fotbal/nationala/soc-ungaria-eliminata-mondial-lista-adversari-romania-baraj-868222.html",
    "https://www.gsp.ro/fotbal/nationala/gabi-balint-rabufnit-romania-bosnia-868235.html",
    "https://www.gsp.ro/fotbal/liga-1/gigi-becali-fcsb-denis-dragus-marius-sumudica-868112.html",
    "https://www.gsp.ro/fotbal/nationala/raul-rusescu-gsp-live-scandari-rasiste-bosnia-romania-868145.html",
    "https://www.gsp.ro/sporturi/tenis/carlos-alcaraz-record-novak-djokovic-finala-turneul-campionilor-torino-868122.html",
    "https://www.gsp.ro/sporturi/tenis/live-carlos-alcaraz-jannik-sinner-finala-turneul-campionilor-868049.html",
    "https://www.gsp.ro/sporturi/baschet/haos-total-in-nba-dupa-scandalul-pariurilor-868187.html",
    "https://www.gsp.ro/sporturi/baschet/stephen-curry-golden-state-nba-michael-jordan-867651.html",
    "https://www.gsp.ro/sporturi/baschet/matt-ryan-poveste-incredibila-cimitir-nba-dubai-867070.html",
    "https://www.gsp.ro/sporturi/baschet/u-bt-cluj-napoca-baxi-manresa-eurocup-live-866562.html",
    "https://www.gsp.ro/fotbal/nationala/cine-e-italia-un-nume-legendar-al-romaniei-mircea-lucescu-868108.html",
    "https://www.gsp.ro/fotbal/liga-1/gigi-becali-fcsb-denis-dragus-marius-sumudica-868112.html",
    "https://www.gsp.ro/fotbal/nationala/kosovo-calificare-mondial-2026-baraj-868016.html",
    "https://www.gsp.ro/fotbal/nationala/daniel-birligea-dupa-esecul-cu-bosnia-867974.html",
    "https://www.gsp.ro/fotbal/nationala/dorin-goian-bosnia-romania-preliminarii-cm-2026-edin-dzeko-868094.html",
    "https://www.gsp.ro/fotbal/nationala/bosnia-ne-a-aratat-marea-fragilitate-mircea-lucescu-868106.html",
    "https://www.gsp.ro/fotbal/liga-1/dinamo-metaloglobus-amical-saftica-868105.html",
    "https://www.gsp.ro/fotbal/nationala/frf-andrei-vochin-bosnia-romania-reclamtie-uefa-derapaj-rasist-868086.html",
    "https://www.gsp.ro/international/campionate/presedintele-lui-lazio-preot-echipa-ghinion-868130.html",
    "https://www.gsp.ro/fotbal/nationala/vestiare-zenica-mircea-lucescu-bosnia-romania-868060.html",
    "https://www.gsp.ro/fotbal/nationala/mircea-lucescu-declaratii-conferinta-bosnia-romania-3-1-867981.html",
    "https://www.gsp.ro/fotbal/nationala/adrian-porumboiu-reactie-bosnia-romania-gsp-live-special-867956.html",
    "https://www.gsp.ro/fotbal/liga-1/daniel-birligea-pedeapsa-lpf-eliminare-hermannstadt-fcsb-866623.html",
    "https://www.gsp.ro/fotbal/liga-1/noi-vrem-sa-plecam-mihai-pintilii-are-planul-facut-cand-o-rupe-cu-fcsb-866126.html",
    "https://www.gsp.ro/fotbal/liga-1/gigi-becali-sanctiuni-dure-fcsb-amenzi-daniel-birligea-866392.html",
    "https://www.gsp.ro/fotbal/liga-1/charalambous-si-pintilii-si-au-dat-demisia-gigi-becali-fcsb-865639.html",
    "https://www.gsp.ro/international/campionate/lorenzo-insigne-aproape-de-o-revenire-in-serie-a-867808.html",
    "https://www.gsp.ro/fotbal/nationala/emil-gradinescu-bosnia-romania-preliminarii-cm-2026-867941.html",
    "https://www.gsp.ro/fotbal/nationala/mihai-stoica-darius-olaru-bosnia-romania-mircea-lucescu-867842.html",
    "https://www.gsp.ro/fotbal/nationala/romanul-care-a-ajuns-o-legenda-in-sarajevo-dupa-ce-dormea-in-vestiarul-teatrului-din-cluj-aici-platesc-doar-30-de-euro-chirie-867691.html",
    "https://www.gsp.ro/international/europa-league/novak-martinovic-fcsb-steaua-rosie-belgrad-867414.html",
    # --- DIGISPORT ---
    "https://www.digisport.ro/fotbal/cm-2026/barajul-pentru-cm-2026-in-care-unele-echipe-vor-disputa-cate-un-meci-iar-altele-cate-doua-fifa-a-luat-decizia-3927759",
    "https://www.digisport.ro/fotbal/liga-1/gigi-becali-i-a-lasat-masca-vrea-la-fcsb-unul-dintre-eroii-bosniei-ii-da-1-000-000-e-3927793",
    "https://www.digisport.ro/fotbal/suspendat-ronaldo-a-scris-doar-sapte-cuvinte-pe-internet-cu-majuscule-dupa-ce-a-vazut-ce-a-facut-portugalia-3928277",
    "https://www.digisport.ro/fotbal/echipa-nationala/a-fost-antrenat-de-lucescu-dar-n-a-tinut-cont-de-nimic-lasa-nea-mircea-pe-altul-mai-tanar-3928221",
    "https://www.digisport.ro/fotbal/neymar-a-inceput-sa-planga-pe-teren-la-ultimul-meci-jucat-de-santos-motivul-brazilianului-3928305",
    "https://www.digisport.ro/tenis/polonia-romania-acum-pe-digi-sport-3-gabriela-lee-o-infrunta-pe-iga-swiatek-la-billie-jean-king-cup-3927391",
    "https://www.digisport.ro/fotbal/echipa-nationala/presa-din-ungaria-dupa-ce-romania-a-luat-bataie-de-la-bosnia-cei-mai-slabi-3928135",
    "https://www.digisport.ro/fotbal/echipa-nationala/marius-avram-a-dat-trei-verdicte-clare-si-a-avut-un-client-dupa-scandalul-din-bosnia-romania-3928231",
    "https://www.digisport.ro/fotbal/cm-2026/lovitura-pentru-universitatea-craiova-s-a-rupt-la-nationala-3927857",
    "https://www.digisport.ro/fotbal/serie-a/romanul-cu-peste-250-de-meciuri-in-italia-a-vazut-ce-face-dan-sucu-la-genoa-si-i-a-dat-un-singur-sfat-3928009",
    "https://www.digisport.ro/fotbal/liga-1/n-a-mers-cu-60-000-e-pe-luna-gigi-becali-a-facut-o-noua-oferta-pentru-louis-munteanu-3926633",
    "https://www.digisport.ro/fotbal/echipa-nationala/gigi-becali-nu-s-a-ferit-dupa-bosnia-romania-n-am-vazut-niciodata-asa-ceva-3927623",
    "https://www.digisport.ro/fotbal/echipa-nationala/gigi-becali-a-surprins-pe-toata-lumea-dupa-bosnia-romania-e-cel-mai-bun-fotbalist-roman-3927665",
    "https://www.digisport.ro/fotbal/europa-league/lille-ajutor-pentru-fcsb-in-europa-league-ce-se-poate-intampla-la-belgrad-3918059",
    "https://www.digisport.ro/uncategorized/mm-stoica-l-a-vazut-in-meciul-de-la-basel-si-nu-s-a-ferit-de-cuvinte-nu-e-stralucit-dar-e-puternic-3911713",
    "https://www.digisport.ro/fotbal/europa-league/de-trei-ori-mai-putin-gigi-becali-a-ratat-tunul-financiar-din-partea-uefa-3911237",
    "https://www.digisport.ro/fotbal/europa-league/uefa-i-a-dat-vestea-lui-darius-olaru-a-doua-zi-dupa-basel-fcsb-3-1-3910461",
    "https://www.digisport.ro/fotbal/europa-league/out-din-iarna-gigi-becali-i-a-semnat-sentinta-dupa-basel-fcsb-3-1-nu-poti-la-nivelul-asta-3909069",
    "https://www.digisport.ro/fotbal/selectionerul-irlandei-rupe-tacerea-ce-cuvinte-i-a-spus-cristiano-ronaldo-dupa-ce-a-fost-eliminat-direct-3923087",
    "https://www.digisport.ro/fotbal/liga-1/bijuterie-fotbalistul-fcsb-ului-este-asteptat-sa-debuteze-la-echipa-nationala-3923061",
    "https://www.digisport.ro/fotbal/liga-1/mihai-rotaru-l-a-rugat-dar-mirel-radoi-nu-a-tinut-cont-a-inceput-sa-rada-si-mi-a-facut-surpriza-3922499",
    "https://www.digisport.ro/fotbal/liga-1/daniel-pancu-intrebat-direct-de-louis-munteanu-la-fcsb-antrenorul-cfr-ului-nu-a-stat-pe-ganduri-3922239",
    "https://www.digisport.ro/fotbal/liga-1/mirel-radoi-la-fcsb-mihai-rotaru-a-intrat-in-direct-si-a-asigurat-pe-toata-lumea-3922181",
    "https://www.digisport.ro/tenis/taylor-fritz-alex-de-minaur-acum-pe-dgs-2-carlos-alcaraz-lorenzo-musetti-2130-dgs-2-meciuri-tari-la-turneul-campionilor-3921839",
    "https://www.digisport.ro/fotbal/polonezii-au-reactionat-dupa-ce-edi-iordanescu-si-a-gasit-o-noua-echipa-3922503",
    "https://www.digisport.ro/fotbal/cat-de-dramatic-var-ul-i-a-refuzat-victoria-lui-olaroiu-in-minutul-906-la-barajul-pentru-mondial-3922289",
    "https://www.digisport.ro/fotbal/liga-1/daniel-pancu-va-debuta-in-gruia-chiar-impotriva-rapidului-si-e-convins-nu-ai-cum-3922323",
    "https://www.digisport.ro/fotbal/echipa-nationala/adrian-mutu-a-propus-un-jucator-de-la-fcsb-titular-la-echipa-nationala-n-a-avut-niciodata-o-sansa-reala-3920773",
    "https://www.digisport.ro/fotbal/cristiano-ronaldo-i-a-rugat-sa-il-huiduie-cand-il-vad-s-o-terminam-inca-de-pe-acum-3920719",
    "https://www.digisport.ro/fotbal/echipa-nationala/a-jucat-un-an-in-superliga-si-a-numit-cel-mai-periculos-jucator-al-romaniei-inaintea-meciului-din-bosnia-3920737",
    "https://www.digisport.ro/fotbal/la-liga/toni-kroos-i-a-spus-ca-nu-e-inlocuitorul-lui-de-la-real-madrid-nici-vorba-3920651",
    "https://www.digisport.ro/fotbal/echipa-nationala/a-anuntat-in-direct-cand-va-reveni-radu-dragusin-la-nationala-joaca-sigur-3920645",
    "https://www.digisport.ro/fotbal/liga-1/transferul-dat-ca-sigur-la-fcsb-in-aer-gigi-becali-daca-nu-il-lasa-cum-sa-vina-3920379"
]

FISIER_CSV = "articole_brute.csv"

def extrage_domeniu(url):
    return urlparse(url).netloc

def colecteaza_articol(url, domeniu, reguli):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    pagina = requests.get(url, headers=headers, timeout=10)
            
    soup = BeautifulSoup(pagina.content, 'html.parser')
        
    titlu = ""
    continut = ""

    if domeniu == "www.gsp.ro" or domeniu == "www.prosport.ro":
        regula_titlu = reguli["titlu"]
        regula_continut = reguli["continut"]

        container_titlu = soup.find(regula_titlu["tag"], class_=regula_titlu["clasa"])
        if container_titlu:
            element_titlu = container_titlu.find(regula_titlu["cauta_in_interior"])
            if element_titlu:
                titlu = element_titlu.get_text(strip=True)
            
        container_continut = soup.find(regula_continut["tag"], class_=regula_continut["clasa"])
        if container_continut:
            continut = container_continut.get_text(strip=True)

    else:
        regula_container = reguli["container"]
        container_principal = soup.find(regula_container["tag"], class_=regula_container["clasa"])
            
        if container_principal:
            element_titlu = container_principal.find("h1")
            if element_titlu:
                titlu = element_titlu.get_text(strip=True)
                
            continut = container_principal.get_text(strip=True)

            
    return titlu, continut

if __name__ == "__main__":
    
    articole_salvate = 0
    
    with open(FISIER_CSV, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        writer.writerow(["url", "domeniu", "titlu", "continut"])
        
        for i, url in enumerate(ARTICOLE_DE_SCRAPAT):
            print(f"\nProcesez articolul {i+1}/{len(ARTICOLE_DE_SCRAPAT)}: {url}")
            
            domeniu = extrage_domeniu(url)
                
            reguli = SITE_RULES[domeniu]
            
            titlu, continut = colecteaza_articol(url, domeniu, reguli)
            
            if titlu and continut:
                writer.writerow([url, domeniu, titlu, continut])
                articole_salvate += 1
                print(f"  [SUCCES] Am salvat: '{titlu[:60]}...'")
            
            time.sleep(1)
            
    print(f"\n--- AM TERMINAT BAA ---")
    print(f"Salvat {articole_salvate} din {len(ARTICOLE_DE_SCRAPAT)} articole.")