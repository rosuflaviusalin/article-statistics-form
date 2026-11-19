# Instalarea scriptului pentru formular (o singură dată, ~5 minute)

Se face din contul **a2statisticalanalysis@gmail.com**, pe calculator.

1. Deschide https://script.google.com și apasă **New project** (Proiect nou).
2. Sus, dă click pe „Untitled project” și redenumește-l **Formular A2**.
3. Șterge tot textul din editor și lipește conținutul fișierului `Code.gs`. Apasă iconița de salvare (sau Cmd+S).
4. Test: în bara de sus alege funcția **testEmail** și apasă **Run**.
   - Google cere permisiuni: **Review permissions** → alege contul → **Advanced** →
     **Go to Formular A2 (unsafe)** → **Allow**. Avertismentul apare pentru orice script personal.
   - În Inbox trebuie să sosească „TEST: scriptul formularului funcționează”.
5. Publicare: **Deploy** → **New deployment** → rotița de lângă „Select type” → **Web app**.
   - Description: `formular`
   - Execute as: **Me (a2statisticalanalysis@gmail.com)**
   - Who has access: **Anyone**
   - **Deploy**, apoi copiază **Web app URL** (începe cu `https://script.google.com/macros/s/…/exec`).
6. Trimite URL-ul acesta (el se pune în `APPS_SCRIPT` din `src/template.html`).

Dacă mai târziu se modifică scriptul: **Deploy** → **Manage deployments** → creion → Version: **New version**
→ **Deploy**. Așa URL-ul rămâne același.
