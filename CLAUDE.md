# GENERATION_EXE – SoMe-bot (prosjektminne for Claude Code)

Sist oppdatert: 19.10.2026 kl. 18:40 (Europe/Oslo). Overført fra Claude-chatten «SoMe bot».
Skriv alltid på norsk til eieren (Per / «Perra»). Ingen emojier. Foretaksnavnet (AS-et) skal aldri stå i noe materiell. PC-en hans har engelske menynavn; bruk dem i veiledning.

## 1. Mål
Automatisk produksjon av engelske AI-kortfilmer (ca. 35 s, 7 scener x 5 s, stemme og undertekster) for kanalene
The_generationxz: YouTube (@benZern / The_generationxz), Facebook-siden Thegenerationxz og Instagram @the_generationxz.
Temaer: nostalgi, generasjonshumor, hverdagsteknologi. Mål: flere følgere og bedre seertid, ekte engasjement.

## 2. Gjeldende regler (nyeste instruks gjelder)
- Eieren er borte og PC-en er av fra 19.10 kl. 17:00 til og med 09.11.2026. Alt må gå i skyen. Ingenting skal kreve PC-en.
- 1 ny film per døgn (eierens beslutning 16.10). Publisering 1 film per døgn kl. 19:00 på YouTube, Facebook og Instagram.
- Eieren godkjenner HVER film selv ved å skrive APPROVED i kolonne H. Claude skal aldri sette APPROVED på egen hånd (unntak: normalisere «Approved»/«approved» som eieren selv har skrevet).
- Ingen nye kostnader, kredittkjøp, automatisk påfyll, oppgraderinger eller abonnementer uten eierens uttrykkelige godkjenning. Teknologibudsjett maks 100 kr/mnd.
- Ikke aktiver publisering på nye kanaler uten godkjenning. Ikke aktiver gamle scenarioer (V2, V9, V10, V11 osv.).
- Ikke endre eller nullstill radene 3 og 4 i Ideas.
- Ta sikkerhetskopi (hent blueprint) før større endringer. Dokumenter hva som faktisk er endret og testet.
- Ingen permanent sletting. Flytte til papirkurv er lov. Eieren tømmer papirkurven selv.
- Aldri skriv API-nøkler eller passord i chat, filer eller rapporter.
- E-post til perrat89@gmail.com bare når noe feiler eller krever hans handling.
- Ikke rør andre boters ting: Produktbot (PRODUKTBOT_*), Gabriella (GABRIELLA_*), Team Eideng (TEAM_EIDENG_*). Make-kontoen og kredittene er felles.
- Ikke påstå at andre boter er kontaktet eller at noe virker uten å ha kontrollert det.
- TikTok: ikke satt opp. Eieren vurderer selv (se punkt 8).

## 3. Arkitektur (alt i skyen)
Styringsark: Google Sheet GENERATION_EXE_CONTROL, id 1bSrNOV6AHPMPvOL8ZMV5Lw4TXLWilKls-VmSWRTAeOo, fane Ideas. Lås: GENEXE_AUTO_V3!B11.
Drive-mappe for filer: 1ODGJVUG3lvhnO8zPLGbg5Gci2J__ny9K (Per's Google Drive).
GitHub-repo for gratis filmsammensetting: edigitalsoulutions-cloud/genexe-render (GitHub Actions). Ferdig film: https://github.com/edigitalsoulutions-cloud/genexe-render/releases/download/<id>/<id>.mp4

Make (eu1, org 9222844, team 3094364, tidssone Europe/Oslo). Aktive GENERATION_EXE-scenarioer:
| ID | Navn | Tidsplan (Oslo) |
|---|---|---|
| 7852891 | V3 – produksjon (manus, sceneplan, stemme, Runway-klipp, APPROVED -> READY_TO_PUBLISH) | hvert 15. min 00:00–06:00 og 18:00–18:45 |
| 7988375 | Vakt: maks 1 ny film per dag (setter film nr. 2+ til PAUSED før Runway-bestilling) | hvert 10. min 00:00–03:00 |
| 7940336 | Filmsammensetting via GitHub + autoopprydding (klipp og stemme til papirkurv) -> REVIEW_READY | hvert 15. min 03:00–09:00 |
| 7881657 | E-postvarsel: film klar for godkjenning | hver time 06:00–12:00 |
| 8054134 | Normaliser godkjenning («Approved» -> APPROVED) | hver 30. min 06:00–18:40 |
| 7882176 | Publisering YouTube/Facebook/Instagram (maks én per time, lås i B11) | hvert 15. min 19:00–20:00 |
| 7895577 | E-postvarsel ved produksjonsfeil | annenhver time 00–21 |
| 7900436 | Arkiver publiserte filmer (flytter rader, radnumre kan forskyve seg) | daglig |

Statusflyt i Ideas!H: SCRIPT_READY -> PLAN_SUBMITTING -> VOICE_READY -> VOICE_SUBMITTING -> VOICE_SAVED -> SCENE_READY -> SCENE_SUBMITTING/SCENE_WAIT (x7) -> ASSEMBLE -> ASSETS_READY -> GHA_RENDERING -> REVIEW_READY -> (eier) APPROVED -> READY_TO_PUBLISH -> PUBLISHING -> PUBLISHED / PUBLISH_ATTENTION. Andre: NEEDS_ATTENTION, PAUSED, SCRIPT_DRAFT, SCRIPT_EXPIRED.
Kolonner (0-basert): A id, C tittel, F manus, G caption, H status, J gha:<id>, K review-URL, L sceneplan, M Runway-oppgave, N scenenr, O–U klipp, V stemme, W feil/info, X ferdig film-ID, AB/AC/AD resultat YT/FB/IG, AE varsel sendt.

Make-verktøy (MCP, last med ToolSearch): s7864941 sheets_api, s7864943 drive_api, s7969189 genexe_runway_info (path «organization» gir creditBalance), s7987443 genexe_elevenlabs_abonnement, s7940258 genexe_github_api, s7912205/7912215/7912268 IG list/get/publish, s7988352 genexe_uploadpost_info (API-nøkkel i Make er ugyldig).
Make-tips: «Too Many Requests» -> vent 60–90 s. Filteroperatoren text:startsWith/startswith finnes ikke (gir aldri treff) – bruk text:contain. scenarios_update erstatter hele blueprinten. V3-blueprinten er ca. 72 kB; unngå å skrive den om – bruk små tilleggsscenarioer.

## 4. Kostnader og kapasitet (målt)
- Runway (gen4.5 text_to_video 720:1280, 5 s): 60 kreditter per klipp, ca. 420 per film. Saldo 3 140 per 19.10 18:25 = ca. 7 filmer til (rekker til ca. 26.10). Ikke kjøp mer uten godkjenning.
- Make: 30 000 kreditter/mnd, 19 395 igjen 18.10 kl. 01, fornyes ca. 09.11. GENERATION_EXE bruker ca. 450–500/døgn (V3 ca. 320). Automatisk kjøp av ekstra kreditter: AV (kontrollert 18.10).
- ElevenLabs Starter: ca. 3 200 av 40 000 tegn brukt, fornyes 08.11 ($7.50, eksisterende abonnement).
- OpenAI (manus/sceneplan): små beløp via eksisterende nøkkel.

## 5. Ferdig og testet
- GitHub-rendering i stedet for Creatomate (testet 13.10).
- Automatisk publisering på alle tre kanaler (testet 15.–17.10; 16.10 og 17.10 OK på YT/FB/IG).
- Instagram via GitHub-URL (rettet operatorfeil 14.10).
- Mer varierte scener og karakterer i sceneplan-prompten (14.10).
- Autoopprydding i Drive (testet 16.10: klipp og stemme i papirkurv, ferdig film urørt).
- 1 film per dag via vakt 7988375 (testet 16.10, fungerer hver natt siden).
- Reduserte kjøretider for å spare Make-kreditter (15.–16.10).
- Normalisering av «Approved» (8054134, testet 19.10 kl. 18:26).

## 6. Ikke gjort / gjenstår
- Sluttrapporten (frist 19.10 kl. 17:00) ble IKKE levert. Lag den.
- Daglig skykontroll: opprettet 19.10 som planlagt oppgave «GENERATION_EXE – daglig kontroll» (trig_0119QCrxrLtWt1cbt4dshPmU, kl. 09:22 Oslo, sky, push + e-post). Første kjøring 20.10 – ikke testet ennå. Ikke lag en ny; kontroller at den kjørte.
- Runway-plan: eieren har ikke valgt mellom A (1/dag til kreditter er tomme, ca. 26.10, så pause) og B (1 annenhver dag til 09.11). Inntil han svarer: fortsett 1/dag, og sett produksjonen på pause før saldoen går under 420 (ikke la en film stoppe halvveis).
- Analyse av resultater (YT/FB/IG) og justering av manus/åpninger: ikke startet.
- Felles oppgavekø med andre boter: ikke bygget. Produktbot har en fane «Koordinering» i sitt regneark 1wuHTO1qCwky3uZFT67I5oEHtZhvspzOdaTYs4NQZYH4 som kan brukes.
- Billigere Runway-oppsett (bilde -> gen4_turbo) er bare et forslag, ikke testet.
- Rad med YouTube FEILET 14.10 (gammel film) står som PUBLISH_ATTENTION; ikke publiser på nytt uten å sjekke kanalen først.

## 7. Daglig kontroll (forventet hver morgen)
Les Ideas!A:AE: nattens film (REVIEW_READY?), publisering i går kl. 19 (AB–AD = OK?), rader med NEEDS_ATTENTION/PUBLISH_ATTENTION, antall APPROVED/READY_TO_PUBLISH i kø, Runway-saldo. Hvis køen er tom: minn eieren på å godkjenne (APPROVED i kolonne H, Sheets-appen på mobil). E-post bare ved feil eller handling som trengs.

## 8. TikTok (ikke startet)
Make har ingen modul for å poste video til TikTok. Alternativer: (a) Upload-Post (eieren hadde abonnement; API-nøkkelen i Make er avvist – han må sjekke abonnement, koble TikTok-kontoen til profilen «default» og lage ny nøkkel); (b) egen TikTok-utviklerapp (gratis, men private innlegg til TikTok har godkjent appen). Eieren sa 16.10: «Det får bare være da» – ikke gjør noe før han tar det opp.
