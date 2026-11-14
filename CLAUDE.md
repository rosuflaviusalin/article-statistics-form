# CLAUDE.md

Ghid pentru Claude (și pentru oricine lucrează pe proiect). Răspunsurile către utilizator se dau în **română**.

## Ce este proiectul

O pagină web de tip landing + formular pentru **Dr. Alexandru Găitoane și Dr. Andrei Dăescu**,
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
- **Google Fonts**: Spectral (serif, titluri) și Instrument Sans (text).
- **Python 3** doar pentru build (biblioteca standard, fără dependențe).

## Structura

```
index.html          # FIȘIER GENERAT – nu se editează manual
src/template.html   # SURSA paginii (HTML/CSS/JS), cu placeholder-e __IMG1__…__IMG5__
build.py            # înlocuiește placeholder-ele cu imaginile din docs/ → index.html
docs/               # imaginile articolelor (WhatsApp Image …jpeg) + idee.docx
.claude/settings.json        # hook Stop → urcare automată pe GitHub
.claude/hooks/auto-push.sh   # scriptul hook-ului
```

## Fluxul de lucru

1. Modifici **doar** `src/template.html` (sau `build.py` / imaginile din `docs/`).
2. Rulezi `python3 build.py` → regenerează `index.html`.
3. Testezi local prin server HTTP (FormSubmit **nu** funcționează din `file://`):
   `python3 -m http.server 8000` → http://localhost:8000/index.html
4. Commit + push pe `develop` (vezi secțiunea Git).

`index.html` are ~900 KB din cauza imaginilor base64: nu-l citi integral, lucrează pe template.

## Git și urcarea automată

- Branch de lucru: **`develop`**. Tot codul nou se urcă pe `origin/develop`.
- `main` rămâne branch-ul stabil; merge-ul `develop → main` se face doar la cererea utilizatorului.
- **Hook automat** (Stop, în `.claude/settings.json`): la finalul fiecărui răspuns, dacă există
  modificări și branch-ul curent e `develop`, scriptul `.claude/hooks/auto-push.sh`:
  regenerează `index.html` dacă s-a schimbat sursa, face `git add -A`, commit și `git push origin develop`.
  Pe alt branch nu comite nimic, doar afișează un avertisment.
- Când implementezi ceva, e preferabil să faci tu commit-ul cu un mesaj descriptiv (în română);
  hook-ul e plasa de siguranță pentru ce a rămas necomis.

## Secțiunile paginii (în ordine)

1. **Header**: brand + meniu (Despre noi, Aportul fiecărei părți, Articole, Formular).
2. **Hero**: titlul „Fiecare studiu are o poveste. O spunem cu cifre.”, sloganul
   „De la întrebarea de cercetare la articolul publicat.”, butoane. În dreapta, panoul
   **„Aportul fiecărei părți”**: 8 etape, fiecare cu bară împărțită client (chihlimbar `#E0A23A`) /
   statisticieni (bleumarin `--deep`). Proporția clientului e în `style="--y:NN%"` pe fiecare `<li>`.
   Proporțiile și textele sunt estimări, de validat cu medicii.
3. **Despre noi**: textul din idee.docx + lista de metode (pastile).
4. **Din articolele noastre**: galerie „stacked card carousel” (foi suprapuse `.stage/.sheet`,
   index lateral `.index`, lightbox `<dialog id="lb">`, săgeți tastatură + swipe).
   Datele imaginilor sunt în array-ul JS `ARTICLES`.
5. **Formular**: cele 5 întrebări din idee.docx + câmp opțional „detalii”, honeypot `_honey`,
   avertisment să nu se trimită date despre pacienți.
6. **Footer** + **nota de informare GDPR** (`<dialog id="privacy">`, deschisă de orice `[data-privacy]`).

## Formularul și e-mailul

- Configurare în JS: `RECIPIENT` (acum `flaviusalinrosu@gmail.com`) și `ENDPOINT`.
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
- **La lansare**: schimbă adresa de e-mail în `RECIPIENT` **și** în nota de informare, plus textul
  „Răspunsurile ajung direct pe e-mail la Alexandru și Andrei”.
- Puncte rămase (neimplementate, la decizia utilizatorului): Google Fonts (IP trimis la Google),
  FormSubmit fără DPA (alternativă: Google Apps Script).

## Comportamente de reținut

- La încărcare pagina pornește mereu de sus: `history.scrollRestoration = "manual"`, se elimină
  `#ancora` din URL, iar linkurile interne derulează fără să modifice adresa.
- `prefers-reduced-motion` este respectat (scroll și tranziții).
- Responsive: breakpoint-uri la 920px, 760px, 560px, 420px.

## Design (direcția aleasă)

- Paletă rece „hârtie de laborator”: `--paper #EAEFF3`, `--ink #1A2533`, `--deep #16334F`,
  accent `--signal #C8322B` (roșul liniei de regresie din figurile lor).
- Utilizatorul a respins: forest plot static rigid, grafice animate pe canvas, colaj de imagini în hero
  și grafice abstracte greu de înțeles. Preferă lucruri **clare, statice, ușor de citit**.

## Publicare

Pagina trebuie servită prin `https://` pentru ca FormSubmit să meargă: Netlify Drop sau GitHub Pages
(e suficient `index.html`, imaginile sunt incluse în el).
