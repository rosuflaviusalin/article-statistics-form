# GDPR – formularul de contact pentru proiecte de cercetare

Acest document explică ce prevede GDPR (Regulamentul UE 2016/679) pentru pagina noastră, ce este
deja implementat, ce mai trebuie făcut și ce rămâne de decis. Nu este o consultanță juridică;
pentru siguranță deplină se recomandă o verificare scurtă cu un jurist.

## Pe scurt

- GDPR se aplică: formularul colectează nume, e-mail și/sau telefon și detalii despre proiect.
- **Operatorii** datelor (cei care răspund de ele) sunt Dr. Alexandru Găitoane și Dr. Andrei Dăescu.
- Minimul obligatoriu **este implementat**: nota de informare și avertismentul despre datele pacienților.
- **Nu este nevoie** de bifă „Sunt de acord cu prelucrarea datelor” și nici de „Termeni și condiții”.
- Înainte de lansare trebuie schimbată adresa de e-mail (vezi lista de la final).

## Temeiul legal: de ce nu cerem consimțământ

GDPR permite prelucrarea datelor doar pe baza unui **temei legal**. Consimțământul este doar unul
din cele șase temeiuri posibile.

În cazul nostru, clientul ne scrie din proprie inițiativă ca să-i răspundem la o cerere. Temeiul
potrivit este **„demersuri efectuate la cererea persoanei înainte de încheierea unui contract”**
(art. 6 alin. 1 lit. b). Pentru acest temei, legea cere doar ca persoana să fie **informată**,
nu să-și dea acordul.

### De ce o bifă de consimțământ ar fi chiar dăunătoare

- Consimțământul trebuie să fie **liber**: clientul ar trebui să poată trimite formularul și fără
  să bifeze. O bifă obligatorie „sunt de acord” nu este, juridic, un consimțământ valid.
- Consimțământul poate fi **retras oricând**, iar atunci datele trebuie șterse imediat.
- Nota noastră de informare spune deja că temeiul este art. 6(1)(b). O bifă „sunt de acord”
  ar contrazice-o.

### Ce bifă se poate pune totuși (opțional)

O bifă obligatorie de **confirmare că persoana a citit nota**, nu de consimțământ:

> ☐ Am citit Nota de informare privind datele personale.

Este o practică frecventă pe site-urile din România, nu contrazice temeiul legal și dovedește că
persoana a avut nota la dispoziție. **Status: nu este implementată, se poate adăuga la cerere.**

### Termeni și condiții / „licence agreement”

Nu sunt necesari pentru un formular de contact. Devin necesari doar dacă pe site se vând servicii
sau se încheie contracte online.

## Ce este implementat pe pagină

1. **Nota de informare (art. 13 GDPR)**, deschisă dintr-un link de lângă butonul de trimitere și
   din subsolul paginii. Conține:
   - cine sunt operatorii și adresa de contact;
   - ce date se colectează și de ce;
   - temeiul legal (art. 6 alin. 1 lit. b);
   - cine mai primește datele: FormSubmit (transmite formularul) și Google (Gmail), cu mențiunea
     că pot fi prelucrate și în afara Spațiului Economic European;
   - durata de păstrare: maximum 12 luni dacă nu se ajunge la o colaborare;
   - drepturile persoanei și dreptul de a face plângere la ANSPDCP (dataprotection.ro).
2. **Avertisment despre datele pacienților**: o casetă deasupra formularului cere să nu se includă
   nume, CNP, diagnostice sau alte informații care pot identifica un pacient. Datele de sănătate
   au un regim mult mai strict, iar câmpurile de text liber sunt riscul principal.
3. **Fără cookies și fără analiză de trafic**, deci nu este nevoie de banner de cookies.

## Obligații practice (nu țin de cod)

- **Ștergerea e-mailurilor**: mesajele de la persoanele care nu devin clienți se șterg în cel mult
  12 luni de la primire, așa cum promite nota.
- **Cererile persoanelor** (acces, ștergere etc.) primite la adresa din notă trebuie rezolvate în
  maximum o lună.
- **Înregistrare la ANSPDCP**: nu mai este necesară.

## Ce rămâne de decis (opțional)

### 1. Fonturile Google: adresa IP a vizitatorului ajunge la Google

**Ce se întâmplă:** pagina încarcă fonturile (Spectral și Instrument Sans) de pe serverele Google
Fonts. La fiecare vizită, browserul vizitatorului se conectează la Google, care primește astfel
**adresa IP** a vizitatorului. Adresa IP este dată cu caracter personal, iar vizitatorul nu a fost
întrebat și nici informat despre asta.

**De ce contează:** în 2022, un tribunal din München (LG München I, 3 O 17493/20) a decis că
folosirea Google Fonts încărcate de la Google, fără acordul vizitatorului, încalcă GDPR, și a
acordat despăgubiri. Riscul practic pentru un site mic este redus, dar problema e ușor de evitat.

**Variante:**

| Variantă | Ce înseamnă | Efect |
|---|---|---|
| **A. Fonturile incluse în pagină** (recomandat) | Fișierele de font se pun direct în `index.html`, ca și imaginile | Niciun contact cu Google, designul rămâne identic, pagina crește cu ~100–200 KB |
| B. Fonturile sistemului | Se renunță la Spectral / Instrument Sans | Zero contact cu Google, dar aspectul se schimbă |
| C. Lăsăm așa | Se menționează Google Fonts în nota de informare | Cel mai simplu, dar rămâne transferul de IP fără acord |

**Recomandare:** varianta A. Se potrivește cu ideea de „un singur fișier” a proiectului și elimină
problema complet. **Status: de decis.**

### 2. FormSubmit fără contract de prelucrare (DPA)

**Ce se întâmplă:** FormSubmit este un serviciu gratuit care primește datele din formular și le
trimite pe e-mail. Nu oferă un contract de prelucrare a datelor (DPA, art. 28 GDPR), iar datele
pot trece prin servere din afara UE.

**Variantă mai curată:** un **Google Apps Script** legat de contul de Gmail al medicilor. Rămâne
gratuit, datele ajung doar la Google, fără un intermediar în plus. Pagina se modifică foarte puțin.

**Recomandare:** acceptabil pentru început, dat fiind volumul mic; de reluat dacă volumul crește.
**Status: de decis.**

### 3. Gmail gratuit vs. Google Workspace

Pentru uz profesional, Google Workspace (cu plată) include un contract de prelucrare a datelor
semnat de Google. Gmail gratuit nu. Pentru volumul actual este acceptabil, dar e bine de știut.

## Lista de verificat înainte de lansare

- [ ] Adresa de e-mail din cod (variabila `RECIPIENT` din `src/template.html`) schimbată cu cea a medicilor
- [ ] Aceeași adresă pusă și ca adresă de contact în nota de informare
- [ ] Textul „Răspunsurile ajung direct pe e-mail la Alexandru și Andrei” este adevărat
- [ ] Formularul activat în FormSubmit de pe domeniul final (e-mail de confirmare)
- [ ] Decizie luată pentru fonturile Google (varianta A, B sau C)
- [ ] Medicii știu de regula de ștergere în 12 luni și de răspunsul la cereri în maximum o lună
