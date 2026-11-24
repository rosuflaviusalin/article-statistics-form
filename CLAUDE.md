# CLAUDE.md

Ghid pentru Claude (și pentru oricine lucrează pe proiect). Răspunsurile către utilizator se dau în **română**.

## Ce este proiectul

O pagină web de tip landing + formular pentru **A2 Statistical Analysis** (Dr. Alexandru Găitoane și Dr. Andrei Dăescu),
medici psihiatri specializați în cercetare clinică și statistică medicală. Clienții (alți medici,
doctoranzi) descriu proiectul lor de cercetare, iar răspunsurile ajung automat pe e-mail.

- Repo: https://github.com/rosuflaviusalin/article-statistics-form (privat)

## Tehnologii

- **Un singur fișier HTML** livrabil: [index.html](index.html), cu HTML + CSS + JavaScript vanilla.
  Fără framework-uri, fără npm, fără bundler.
- **Imaginile sunt incluse în HTML ca base64** (data URI), ca pagina să nu depindă de stocare externă.
- **Google Apps Script** (gratuit, max. 100 e-mailuri/zi) trimite formularul pe e-mail: pagina face `fetch()`
  POST cu JSON ca `text/plain` (fără preflight CORS) la URL-ul `/exec` din `ENDPOINT`. Scriptul
  ([apps-script/Code.gs](apps-script/Code.gs)) e instalat în contul a2statisticalanalysis@gmail.com și trimite cu `MailApp`.
  FormSubmit a fost abandonat (e-mailul de activare pentru domeniu nu a sosit niciodată).
- **Fonturi locale**: Spectral (serif, titluri) și Instrument Sans (text), fișiere `.woff2` în
  `src/fonts/`, incluse în pagină ca base64 de `build.py`. **Nu folosi Google Fonts** (link-uri la
  fonts.googleapis.com / fonts.gstatic.com): ar trimite adresa IP a vizitatorilor la Google, problemă
  GDPR (LG München I, 2022). `build.py` oprește build-ul dacă apare o astfel de referință.
- **Python 3** doar pentru build (biblioteca standard, fără dependențe). Fără React: decizie luată,
  găzduirea rămâne statică și gratuită.

## Structura

```
index.html          # FIȘIER GENERAT – nu se editează manual
src/template.html   # SURSA paginii (HTML/CSS/JS), cu placeholder-e /*__FONTS__*/, __LOGO__ și __IMG1__…__IMG5__
apps-script/        # scriptul Google pentru formular (Code.gs) + pașii de instalare (README.md); nu e public
src/img/logo.png    # logo decupat din docs/logo.jpeg, fundal transparent (nu folosi mix-blend-mode/filter: Safari iOS)
src/fonts/          # fonturile .woff2 (latin + latin-ext pentru diacritice) + fonts.css
build.py            # include fonturile și imaginile ca base64 → index.html
docs/               # imaginile articolelor (nume descriptive, ex. clustere-pca.jpeg) + logo.jpeg (sursa logo-ului)
.claude/settings.json        # hook Stop → urcare automată pe GitHub
.claude/hooks/auto-push.sh   # scriptul hook-ului
```

## Fluxul de lucru

1. Modifici **doar** `src/template.html` (sau `build.py` / imaginile din `docs/`).
2. Rulezi `python3 build.py` → regenerează `index.html`.
3. Testezi local prin server HTTP:
   `python3 -m http.server 8000` → http://localhost:8000/index.html
4. Commit + push pe `develop` (vezi secțiunea Git).

`index.html` are ~1,2 MB din cauza imaginilor și fonturilor base64: nu-l citi integral, lucrează pe template.

## Git și urcarea automată

- Branch de lucru: **`develop`**. Tot codul nou se urcă pe `origin/develop`.
- **`develop` este producția** (Cloudflare Pages îl publică automat). `main` nu e folosit pentru publicare;
  merge-ul `develop → main` se face doar la cererea utilizatorului.
- **Hook automat** (Stop, în `.claude/settings.json`): la finalul fiecărui răspuns, dacă există
  modificări și branch-ul curent e `develop`, scriptul `.claude/hooks/auto-push.sh`:
  regenerează `index.html` dacă s-a schimbat sursa, face `git add -A`, commit și `git push origin develop`.
  Pe alt branch nu comite nimic, doar afișează un avertisment.
- Când implementezi ceva, e preferabil să faci tu commit-ul cu un mesaj descriptiv (în română);
  hook-ul e plasa de siguranță pentru ce a rămas necomis.

## Secțiunile paginii (în ordine)

1. **Header**: logo A2 Statistical Analysis + meniu (Despre noi, Aportul fiecărei părți, Exemple, Formular).
   Numele de brand afișat peste tot este „A2 Statistical Analysis” (nu „Găitoane & Dăescu”).
2. **Hero**: titlul „Fiecare studiu are o poveste. O spunem cu cifre.”, sloganul
   „Analiză statistică pentru cercetare medicală și sprijin editorial pentru articole științifice.”, un paragraf
   (analiza statistică poate fi cerută și separat), butoane. În dreapta, panoul
   **„Aportul fiecărei părți”**: acordeon compact cu 5 etape (un rând = număr, nume, bară împărțită
   client chihlimbar `#E0A23A` / statisticieni bleumarin `--deep`); la click se deschide `.r-who` cu
   textele „Dumneavoastră / Echipa A²” (un singur rând deschis odată). Panoul trebuie să încapă lângă titlu, fără scroll. Proporția clientului e în `style="--y:NN%"` pe fiecare `<li>`.
   Proporțiile și textele sunt estimări, de validat cu medicii.
3. **Despre noi** („Perspectiva clinicianului, rigoarea statisticianului”): text în stânga, în dreapta
   **explorator de metode** `.mx`: 4 file (Analize statistice, Diagnostic și predicție, Sinteza dovezilor,
   Inteligență artificială) cu derulare automată la 6 s (bară roșie), oprită la hover și după primul click;
   fiecare filă are o mini-ilustrație SVG animată (bare + regresie, curbă ROC, selecția studiilor printr-o pâlnie → diamant, rețea neuronală),
   o frază și lista de metode. Intrarea secțiunii: IntersectionObserver adaugă `.anim` apoi `.in` pe `.about`.
4. **Exemple din publicații** („Selecție de articole științifice la care au contribuit membri ai echipei A²”): galerie „stacked card carousel” (foi suprapuse `.stage/.sheet`,
   index lateral `.index`, lightbox `<dialog id="lb">`, săgeți tastatură + swipe).
   Datele imaginilor sunt în array-ul JS `ARTICLES`.
5. **Formular**: nume, contact, temă, tip proiect (un articol / mai multe / alt tip), „Cu ce vă putem ajuta?”
   (servicii, bife), câmp opțional „În ce etapă se află proiectul?”, honeypot `_honey`,
   avertisment să nu se trimită date despre pacienți.
6. **Footer** + **nota de informare GDPR** (`<dialog id="privacy">`, deschisă de orice `[data-privacy]`).

## Formularul și e-mailul

- Configurare în JS: `RECIPIENT` (`a2statisticalanalysis@gmail.com`, folosit la `mailto:`) și `ENDPOINT`
  (URL-ul Web app al scriptului). Destinatarul real e constanta `RECIPIENT` din `Code.gs`.
- După trimitere: „Mulțumim, <prenume>.” (funcția `prenume()`: tot ce urmează după primul cuvânt din „Nume și prenume”).
- Validare client: nume, contact (e-mail sau telefon), temă, tip proiect (radio), cel puțin un serviciu.
  „Aș dori să stabilim împreună serviciile potrivite” e exclusivă (`data-exclusive`).
- Poziționare (2026-11-24): echipa face analiza statistică și **sprijin editorial** (revizuire, pregătirea trimiterii),
  nu redactează articolul în locul autorilor. Nu promite „de la întrebare la articolul publicat”.
- Cheile din payload rămân vechi (`Etape pentru care se cere asistență`, `Detalii suplimentare`); etichetele
  afișate în e-mail se schimbă în `FIELDS` din `apps-script/Code.gs`.
- Payload: chei în română + `_subject`, `_replyto` (devine Reply-To dacă e un e-mail valid). Răspuns: `{"success":true}`.
- Fallback la eroare: link `mailto:` cu toate răspunsurile precompletate.
- Modificarea scriptului: în script.google.com → Deploy → Manage deployments → creion → New version
  (URL-ul rămâne același; un „New deployment” ar schimba URL-ul și trebuie actualizat `ENDPOINT`).
- Contul A2 a fost creat supravegheat în Family Link, care blochează Apps Script; supravegherea a fost scoasă.

## GDPR (implementat)

Explicațiile complete, deciziile deschise și lista pentru lansare sunt în [gdpr.md](gdpr.md).

- Notă de informare art. 13: operatori = cei doi medici, contact = adresa din `RECIPIENT`,
  temei art. 6(1)(b), destinatari Google (Apps Script + Gmail) și Cloudflare (găzduire), păstrare max. 12 luni, drepturi, ANSPDCP.
- Avertisment vizibil: fără date despre pacienți.
- Adresa de contact din notă = `RECIPIENT` = a2statisticalanalysis@gmail.com (de păstrat sincronizate).
- Fără bifă în formular: decizie luată (temei art. 6(1)(b), doar informare).

## Comportamente de reținut

- La încărcare pagina pornește mereu de sus: `history.scrollRestoration = "manual"`, se elimină
  `#ancora` din URL, iar linkurile interne derulează fără să modifice adresa.
- `prefers-reduced-motion` este respectat (scroll și tranziții).
- Responsive: breakpoint-uri la 920px, 760px, 560px, 420px.

## Design (direcția aleasă)

- Paletă rece „hârtie de laborator”: `--paper #EAEFF3`, `--ink #1A2533`, `--deep #16334F`,
  accent `--signal #C8322B` (roșul liniei de regresie din figurile lor).
- Butonul principal `.btn` este albastru (`--deep`), cel secundar `.btn.ghost` are contur albastru.
- Utilizatorul a respins: diagrama Venn clinician/statistician, galeria fixată la scroll (GSAP, eliminată),
  lista de metode ca pastile pe rânduri sau ca listă simplă în coloane („prea mult pentru puțin”), forest plot static rigid, grafice animate pe canvas, colaj de imagini în hero
  și grafice abstracte greu de înțeles. Preferă lucruri **clare, statice, ușor de citit**.

## Publicare

- Site live: **https://a2statisticalanalysis.ro** (și `www.`, live din 2026-11-19), găzduit pe **Cloudflare Pages**,
  proiect `article-statistics-form` (previzualizare https://article-statistics-form.pages.dev), plan gratuit.
- Domeniul e cumpărat de la **Datahost**, fără administrare DNS; nameserverele sunt cele Cloudflare
  (`dara`/`lou.ns.cloudflare.com`), iar DNS-ul e în același cont Cloudflare ca vitrina_cu_delicii.
- **Production branch = `develop`**: orice push pe `develop` (inclusiv hook-ul automat) ajunge live în ~1 minut.
- Build în Pages: comanda `mkdir -p dist && cp index.html dist/`, output `dist`. Așa se publică
  **doar** `index.html`; `docs/`, `src/`, `gdpr.md`, `CLAUDE.md` nu devin publice. Nu schimba output-ul în rădăcină.
- `dist/` (în git) conține fișierele publicate lângă pagină: `og-image.jpg` (1200×630, previzualizarea
  linkului pe WhatsApp/Facebook), `favicon.png`, `apple-touch-icon.png`. Build-ul Cloudflare doar adaugă
  `index.html` în `dist/`. Rețelele sociale cer URL absolut, deci aici nu merge base64.
- Cloudflare „Email Obfuscation” înlocuiește adresa din nota GDPR cu un script `/cdn-cgi/...`
  (în browser se afișează normal). Verifică modificările și pe site-ul live, nu doar local.
- Formularul merge și local (Apps Script nu verifică domeniul), dar fiecare test trimite un e-mail real.
