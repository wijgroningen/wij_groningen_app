# Functioneel Ontwerp — WIJ Groningen App

## 1. Inleiding
Korte, praktisch toepasbare samenvatting van de productdocumentatie in /product. Doel: duidelijk specificeren wat gebouwd moet worden zodat ontwikkeling en testen starten.

## 2. Doelstellingen
- Ondersteunen van burgerinteractie met lokale voorzieningen.
- Faciliteren van meldingen, agenda en informatievoorziening.
- Eenvoudige beheerinterface voor administrators.

## 3. Gebruikersrollen
- Burger: bekijkt informatie, meldt problemen, schrijft zich in voor activiteiten.
- Community-beheerder: beheert content, plant activiteiten, beantwoordt meldingen.
- Beheerder (admin): volledige configuratie en gebruikersbeheer.

## 4. Kernfunctionaliteiten (hoog niveau)
- Home / Nieuwsfeed
- Activiteiten & agenda (inschrijven, overzicht)
- Meldingen & status tracking (aanmaken, opvolgen)
- Profielbeheer (gegevens, voorkeuren)
- Admin UI (content- & gebruikersbeheer)
- Notificaties (e-mail/push)

## 5. Belangrijke gebruikersverhalen (kort)
- Als burger wil ik een activiteit kunnen zoeken en mij inschrijven zodat ik kan deelnemen.
- Als burger wil ik een probleem kunnen melden met foto zodat de gemeente kan reageren.
- Als beheerder wil ik activiteiten aanmaken en bewerken zodat de agenda actueel blijft.

## 6. Functionele eisen (selectie)
- FE-001: Gebruikers kunnen registreren en inloggen (e-mail + wachtwoord).
- FE-002: Activiteiten CRUD voor beheerders; burgers kunnen inschrijven.
- FE-003: Meldingen met optionele foto en locatie, statustracking.
- FE-004: Nieuws/Feeds filterbaar op categorie en datum.
- FE-005: API beveiligd met token-based auth (JWT).

## 7. Non-functionele eisen (kort)
- NFE-001: Reactietijd API < 300ms (piekbelasting afhankelijk).
- NFE-002: Beschikbaarheid 99% (kernfuncties).
- NFE-003: GDPR-conform opslag van persoonsgegevens.

## 8. Data model (hoog niveau)
- User { id, naam, email, rol, voorkeuren, aangemaakt_op }
- Activity { id, titel, omschrijving, locatie, start, einde, capaciteit, organisator_id }
- Enrollment { id, user_id, activity_id, status, aangemaakt_op }
- Report { id, user_id, titel, omschrijving, foto_url, locatie, status, aangemaakt_op }
- News { id, titel, inhoud, categorie, gepubliceerd_op, auteur_id }

(Relaties: User—Enrollment—Activity; User—Report; User—News(auteur))

## 9. API endpoints (voorstel, REST)
- POST /api/auth/register
- POST /api/auth/login
- GET /api/activities
- POST /api/activities (admin)
- POST /api/activities/:id/enroll
- GET /api/reports
- POST /api/reports
- GET /api/news
- POST /api/news (admin)

(Beveiliging en validatie per endpoint verplicht)

## 10. UI-structuur (hoofdschermen)
- Startpagina (nieuws + snelle acties)
- Activiteitenlijst / detail / inschrijving
- Meldingen: lijst, detail, nieuw melden (foto + locatie)
- Mijn profiel / instellingen
- Admin dashboard: content en gebruikerbeheer

## 11. Acceptatiecriteria (voorbeeld)
- AC-001: Een geregistreerde gebruiker kan succesvol inschrijven voor een activiteit en ontvangt bevestiging.
- AC-002: Een melding kan met foto worden aangemaakt en verschijnt in admin-overzicht met status 'Nieuw'.
- AC-003: Admin kan een activiteit aanmaken en zichtbaar maken voor burgers.

## 12. Implementatie- en testvoorstel
- Sprint 1: Authenticatie, userprofiel, basisactiviteiten (lijst + detail).
- Sprint 2: Inschrijving, meldingen, foto-upload.
- Sprint 3: Admin UI, nieuwsfeed, notificaties.
- Testen: unit tests voor services, integratietests voor API, E2E voor kritische user flows.

## 13. Volgende stappen
1. Itereer over documenten in /product en vul ontbrekende details aan (velden, validatieregels, mockups).  
2. Prioriteer backlog items op basis van waarde en inspanning.  
3. Maak API-contracten (OpenAPI) en eenvoudige UI-wireframes.

<!-- Einde -->
