# CLAUDE.md

Ghid pentru Claude (și pentru oricine lucrează pe proiect). Răspunsurile către utilizator se dau în **română**.

## Ce este proiectul

O pagină web de tip landing + formular pentru **A2 Statistical Analysis** (Dr. Alexandru Găitoane și Dr. Andrei Dăescu),
medici psihiatri specializați în cercetare clinică și statistică medicală. Clienții (alți medici,
doctoranzi) descriu proiectul lor de cercetare, iar răspunsurile ajung automat pe e-mail.

- Repo: https://github.com/rosuflaviusalin/article-statistics-form (privat)
- Sursa conținutului: [docs/idee.docx](docs/idee.docx) (prezentarea medicilor + întrebările formularului)

## Tehnologii

- **Un singur fișier HTML** livrabil: [index.html](index.html), cu HTML + CSS + JavaScript vanilla.
  Fără framework-uri, fără npm, fără bundler.
- **Imaginile sunt incluse în HTML ca base64** (data URI), ca pagina să nu depindă de stocare externă.
- **FormSubmit.co** (gratuit) trimite formularul pe e-mail prin `fetch()` POST JSON la
  `https://formsubmit.co/ajax/<email>`. Nu există backend propriu.
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
src/img/logo.png    # logo decupat din docs/logo.jpeg, fundal transparent (nu folosi mix-blend-mode/filter: Safari iOS)
src/fonts/          # fonturile .woff2 (latin + latin-ext pentru diacritice) + fonts.css
build.py            # include fonturile și imaginile ca base64 → index.html
docs/               # imaginile articolelor (nume descriptive, ex. clustere-pca.jpeg) + idee.docx
.claude/settings.json        # hook Stop → urcare automată pe GitHub
.claude/hooks/auto-push.sh   # scriptul hook-ului
```

## Fluxul de lucru

1. Modifici **doar** `src/template.html` (sau `build.py` / imaginile din `docs/`).
2. Rulezi `python3 build.py` → regenerează `index.html`.
3. Testezi local prin server HTTP (FormSubmit **nu** funcționează din `file://`):
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
   „De la întrebarea de cercetare la articolul publicat.”, butoane. În dreapta, panoul
   **„Aportul fiecărei părți”**: acordeon compact cu 8 etape (un rând = număr, nume, bară împărțită
   client chihlimbar `#E0A23A` / statisticieni bleumarin `--deep`); la click se deschide `.r-who` cu
   textele „Dumneavoastră / Noi” (un singur rând deschis odată). Panoul trebuie să încapă lângă titlu, fără scroll. Proporția clientului e în `style="--y:NN%"` pe fiecare `<li>`.
   Proporțiile și textele sunt estimări, de validat cu medicii.
3. **Despre noi** („Perspectiva clinicianului, rigoarea statisticianului”): text în stânga, în dreapta
   **explorator de metode** `.mx`: 4 file (Analize statistice, Diagnostic și predicție, Sinteza dovezilor,
   Inteligență artificială) cu derulare automată la 6 s (bară roșie), oprită la hover și după primul click;
   fiecare filă are o mini-ilustrație SVG animată (bare + regresie, curbă ROC, selecția studiilor printr-o pâlnie → diamant, rețea neuronală),
   o frază și lista de metode. Intrarea secțiunii: IntersectionObserver adaugă `.anim` apoi `.in` pe `.about`.
4. **Exemple din publicațiile noastre**: galerie „stacked card carousel” (foi suprapuse `.stage/.sheet`,
   index lateral `.index`, lightbox `<dialog id="lb">`, săgeți tastatură + swipe).
   Datele imaginilor sunt în array-ul JS `ARTICLES`.
5. **Formular**: cele 5 întrebări din idee.docx + câmp opțional „detalii”, honeypot `_honey`,
   avertisment să nu se trimită date despre pacienți.
6. **Footer** + **nota de informare GDPR** (`<dialog id="privacy">`, deschisă de orice `[data-privacy]`).

## Formularul și e-mailul

- Configurare în JS: `RECIPIENT` (`a2statisticalanalysis@gmail.com`) și `ENDPOINT`.
- După trimitere: „Mulțumim, <prenume>.” (funcția `prenume()`: tot ce urmează după primul cuvânt din „Nume și prenume”).
- Validare client: nume, contact (e-mail sau telefon), temă, tip proiect (radio), cel puțin o etapă.
  „Întregul proiect” și „Aș dori să stabilim împreună” sunt exclusive (`data-exclusive`).
- Payload: chei în română + `_subject`, `_template: "table"`, `_captcha: "false"`, `_replyto`.
- Fallback la eroare: link `mailto:` cu toate răspunsurile precompletate.
- FormSubmit cere **activare** la prima trimitere de pe fiecare domeniu (e-mail de confirmare).
- Recomandare deschisă: înlocuirea adresei din `ENDPOINT` cu codul aleator oferit de FormSubmit.

## GDPR (implementat)

Explicațiile complete, deciziile deschise și lista pentru lansare sunt în [gdpr.md](gdpr.md).

- Notă de informare art. 13: operatori = cei doi medici, contact = adresa din `RECIPIENT`,
  temei art. 6(1)(b), destinatari FormSubmit + Google, păstrare max. 12 luni, drepturi, ANSPDCP.
- Avertisment vizibil: fără date despre pacienți.
- Adresa de contact din notă = `RECIPIENT` = a2statisticalanalysis@gmail.com (de păstrat sincronizate).
- Puncte rămase (neimplementate, la decizia utilizatorului): FormSubmit fără DPA
  (alternativă: Google Apps Script). Fără bifă în formular: decizie luată (temei art. 6(1)(b), doar informare).

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
- FormSubmit cere `https://` (nu merge din `file://`) și activare de pe domeniul final.
