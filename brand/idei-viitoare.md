# Idei pentru mai tarziu

Idei mai ample pentru site-ul Andreea Sandu, care nu sunt facute inca. Cele 12 idei rapide (butoane aurii, roz, banda crem, hover, aparitie la scroll, coperta pentru mostre, pagina de multumire, buton fix pe telefon, previzualizare pentru linkuri, FAQ, selectie aurie, poza pe telefon) sunt deja pe site.

Pentru fiecare idee: ce este, ce impact are si ce trebuie ca sa o facem.

## 1. Mostrele ca postare de Instagram cu swipe
Un cadru de telefon in care omul da pe lateral prin carusel, cu imagini incarcate de tine.
- **Impact:** e momentul "WOW" care lipseste acum. Arata exact ce vinzi, nu doar il descrie.
- **Ce trebuie:** imaginile fiecarui carusel (le incarci tu din admin) si un camp nou pentru mai multe imagini pe mostra.
- **Recomandare:** prima idee de facut dintre cele mari.

## 2. Quiz de 3 intrebari: "Ce pachet mi se potriveste?"
Raspunsurile duc la un pachet si completeaza formularul.
- **Impact:** il ajuta pe cel care nu stie ce sa aleaga si iti aduce cereri mai clare.
- **Ce trebuie:** alegi tu cele 3 intrebari si ce pachet iese la fiecare combinatie.

## 3. Inainte si dupa pe o mostra
Textul simplu al unui business fictiv langa varianta ta, cu un glisor.
- **Impact:** arata diferenta in cateva secunde, fara recenzii de care nu ai inca.
- **Ce trebuie:** una sau doua mostre scrise in doua variante (simplu si rescris), marcate clar ca business fictiv.

## 4. Pagina privata pentru fiecare client
Un link unde clientul vede starea (mostra trimisa, platit, scriu, revizie, livrat) si descarca documentul.
- **Impact:** seamana a serviciu complet si te scuteste de mesaje de tipul "cum stam?".
- **Ce trebuie:** se construieste pe statusurile din admin. Cere si un link secret pentru fiecare client si o pagina de descarcare.

## 5. Email automat
Tu primesti un email la fiecare cerere, iar clientul primeste "am primit, reclama vine in 2 zile lucratoare".
- **Impact:** raspuns imediat, aer de serviciu serios, nu mai intri in admin ca sa vezi daca a venit ceva.
- **Ce trebuie:** pe contul gratuit PythonAnywhere trimiterea de emailuri e limitata, deci probabil un plan platit sau alt serviciu de email. De verificat inainte.

## 6. Video scurt de prezentare
20-30 de secunde, mut, in bucla, in locul pozei din Home.
- **Impact:** singurul lucru care aduce miscare reala si personalitate.
- **Ce trebuie:** il filmezi tu. Pe site il adaug eu, usor, cu poza actuala ca varianta de rezerva.

## 7. Mici analize de reclame
Un articol scurt pe luna: cum ai rescrie o reclama dintr-un business fictiv.
- **Impact:** te arata ca expert si te aduce pe Google, cu continut doar de la tine.
- **Ce trebuie:** o sectiune "Blog" in site si cate un text pe luna scris de tine. Fara clienti sau povesti inventate.

## 8. Versiune in romana a site-ului
Daca vrei afaceri din Bucuresti, le vorbesti in limba lor.
- **Impact:** ajungi la clienti locali.
- **Ce trebuie:** doar daca hotarasti ca vrei clienti locali, pentru ca dubleaza textul de intretinut. Textele in romana le scriem impreuna.

## 9. Domeniu propriu si email pe domeniu
De exemplu `nume.ro` si `contact@nume.ro`.
- **Impact:** aduce incredere si face linkul usor de tinut minte. Adresa `pythonanywhere.com` si emailul gmail pot parea "proiect de test" pentru unii vizitatori.
- **Ce trebuie:** plan platit pe PythonAnywhere (domeniu propriu nu merge pe cel gratuit) si cumpararea domeniului.

---

## Alte lucruri notate pe parcurs (nu sunt idei de atractivitate)
- **Fonturi gazduite pe site** in loc de Google Fonts: browserul vizitatorului nu mai contacteaza Google si pagina se incarca mai constant. Pagina Privacy spune acum ca fonturile vin de la Google.
- **Protectie suplimentara impotriva spamului din formular** (limita pe adresa IP sau un test simplu), daca incep sa apara cereri false.
- **Protectie la ghicirea parolei de admin** (de exemplu django-axes). Pana atunci: adresa de admin secreta si parola lunga.
- **HSTS** (obliga browserul sa foloseasca doar HTTPS): de pornit dupa ce site-ul merge stabil.
- **Pagini de eroare cu brandul tau** (404, 500).
- **Paginare in Portfolio**, daca ajungi la multe zeci de mostre.

---

## Din auditul de experienta (ce nu s-a facut)

Cele 3 puncte urgente si 3 din cele 4 optionale sunt facute (mesaje de eroare clare cu rezumat, linkuri mai mari pe telefon, nota despre email si spam, campuri obligatorii marcate, pachetul ales afisat sus, campuri pliate). Raman:

- **Validare imediata in formular:** mesajul apare cand iesi dintr-un camp, nu abia dupa trimitere. Efort mediu (cod in browser pe langa verificarea de pe server). Aduce putin acum, pentru ca rezumatul de erori merge bine.
- **Formular in doi pasi pe telefon** (mai intai ce vinzi si cui, apoi datele de contact): ar scurta si mai mult ecranul, dar e o schimbare mai mare si ar ascunde o parte din formular. De gandit doar daca vezi ca oamenii il parasesc.

## De verificat dupa ce actualizezi site-ul pe PythonAnywhere

Acestea nu s-au putut verifica de aici si cer ochii tai:
- **Parcursul complet pe site-ul real:** de la Home la formular, o trimitere de test, pagina de multumire, apoi mesajul apare in admin. Pe site-ul de acum ruleaza inca versiunea veche.
- **Filtrele din Portfolio pe telefon:** au primit mai mult spatiu, dar nu s-au putut masura, pentru ca portofoliul e gol. Dupa ce incarci mostra, verifica ca se apasa usor.
- **PDF-ul deschis in pagina:** browserul meu de test nu are cititor de PDF. Verifica in Chrome si Safari cu mostra ta reala. Daca nu se deschide in pagina, ramane linkul "Open it in a new tab".
- **Emailul din Gmail:** site-ul nu trimite emailuri, deci omul primeste reclama cand ii scrii tu. Trimite-ti un email de test de la adresa din Gmail catre o alta adresa si verifica ca nu ajunge in spam, pentru ca pagina de multumire promite "I will write to you from ...".
- **Previzualizarea linkului** (poza si titlul cand distribui site-ul): dupa actualizare, testeaza-o la distribuire pe WhatsApp si pe LinkedIn. Platformele tin imaginea in memorie, deci poate dura pana apare cea noua.
