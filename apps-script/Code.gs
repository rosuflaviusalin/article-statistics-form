/**
 * Google Apps Script pentru formularul de pe a2statisticalanalysis.ro
 * Se instalează în contul a2statisticalanalysis@gmail.com (vezi apps-script/README.md).
 * Primește răspunsurile din pagină și le trimite pe e-mail din contul Google,
 * fără intermediari (înlocuiește FormSubmit).
 */
const RECIPIENT = "a2statisticalanalysis@gmail.com";

// Câmpurile afișate în e-mail, în ordine: [cheia trimisă de pagină, eticheta din e-mail].
// Cheile nu se schimbă (ca o versiune veche a scriptului să funcționeze în continuare).
const FIELDS = [
  ["Nume și prenume", "Nume și prenume"],
  ["Contact", "Contact"],
  ["Specialitate și temă", "Specialitate și temă"],
  ["Tip de proiect", "Tip de proiect"],
  ["Etape pentru care se cere asistență", "Cu ce vă putem ajuta"],
  ["Detalii suplimentare", "Etapa proiectului"]
];

function doPost(e) {
  try {
    const d = JSON.parse(e.postData.contents);
    if (d._honey) return reply({ success: true }); // robot: ignorăm în tăcere

    const val = k => String(d[k] == null || d[k] === "" ? "-" : d[k]).slice(0, 5000);
    if (val("Nume și prenume") === "-") throw new Error("Lipsește numele.");

    const rows = FIELDS.map(([k, label]) =>
      '<tr><th style="text-align:left;vertical-align:top;padding:8px 12px;background:#EAEFF3;border:1px solid #d5dde5;width:34%">' +
      esc(label) + '</th><td style="padding:8px 12px;border:1px solid #d5dde5">' +
      esc(val(k)).replace(/\n/g, "<br>") + "</td></tr>"
    ).join("");
    const html =
      '<div style="font-family:Arial,sans-serif;color:#1A2533">' +
      '<p>Proiect nou trimis din formularul de pe a2statisticalanalysis.ro:</p>' +
      '<table style="border-collapse:collapse;font-size:14px;max-width:720px">' + rows + "</table></div>";
    const text = FIELDS.map(([k, label]) => label + ": " + val(k)).join("\n\n");

    const opts = { htmlBody: html, name: "Formular A2 Statistical Analysis" };
    const re = String(d._replyto || "");
    if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(re)) opts.replyTo = re;

    const subject = String(d._subject || "Proiect nou").slice(0, 200);
    MailApp.sendEmail(RECIPIENT, subject, text, opts);
    return reply({ success: true });
  } catch (err) {
    return reply({ success: false, message: String(err.message || err) });
  }
}

// Test rapid din editor: selectează „testEmail” și apasă Run.
function testEmail() {
  doPost({ postData: { contents: JSON.stringify({
    "Nume și prenume": "Test Instalare",
    "Contact": "test@example.com",
    "Specialitate și temă": "Verificare script",
    "_subject": "TEST: scriptul formularului funcționează"
  }) } });
}

function esc(s) {
  return String(s).replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}
