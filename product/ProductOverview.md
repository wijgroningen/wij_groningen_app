Hierin komt het “wat en waarom” van de applicatie:

doel

doelgroep

context

high-level functionaliteit

systeemgrenzen

****

# Sociaal domein applicatie
Tbv WMO, Jeugdwet, Basis jeugdhulp, Omgevings gerichte aanpak en wellicht meerdere toepassingen

## Doelstelling
- inwoner centraal
- minimale administratielast. 
- hoge datakwaliteit
- persoonlijk dashboard (inclusief visuals)
- inwoner dashboard met tijdlijn en relaties
- operationele stuurinformatie in de applicatie (wachtlijst, doorlooptijden, etc)
- open source, dus beschikbaar via github
- generieke opzet, geen customizations
- API's voor in en uit
- OGA in de applicatie (als module)
- koppeling met HR systeem voor personele wijzigingen. Je moet dus ook geen handmatige HR wijzigingen kunnen doorvoeren in het casussysteem, alleen wanneer het externe personen betreft.
- duidelijk onderscheid tussen casusregie en werkelijke ondersteuning (zonder tijdschrijven)
- berichtenverkeer naar afhankelijke applicaties
- data kwaliteit controles in de applicatie
- machine learning op alle casussen. Kunnen we voorspellen hoe een casus kan/zal verlopen?
- machine learning: waar mogelijk moeten velden vooraf zijn ingevuld (dit kan dmv een machine learning model)
- toegang voor externe partijen (GON)
- inwoner portaal (digid)
- inzicht in activiteit en doorlooptijd

## Structuur
In de basis gaat het om de wat en de wie. Dus wat is het probleem (triage) en wie gaat het oplossen (werkdeling). <br>
Vervolgens gaat het om de 'hoe', dus om de uitvoering waarbij per 'inzet' vastgelegd moet worden wie deze inzet pleegt en hoe lang dat duurt (doorlooptijd)<br>
In sommige gevallen wordt ook vastgelegd hoeveel uren er per een bepaalde periode worden ingezet (geldt alleen voor basis jeugdhulp)

Mensen moeten met verschillende rollen (casusregiseur, tweede casusregiseur, ondersteuner) kunnen samenwerken aan 1 of meerdere casussen. Binnen een casus kunnen ook meerdere personen werken.

## aantekeningen
- welke rol speelt een inwoner in een casus? Is het direct op de inwoner gericht (kind) of ben je bijvoorbeeld ondersteunend (moeder). 
- Hoe ga je om met gezinssituaties waarbij meerdere gezinsleden een casus hebben
- breaking the glass toevoegen
- casusregisseur moet melding krijgen wanneer en nog een traject wordt aangemaakt voor dezelfde inwoner maar door een andere generalist.
- traject moet ook kunnen worden gekoppeld aan een organisatie (school, huisarts, etc.)
