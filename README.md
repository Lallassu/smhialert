# Home Assistant - SMHI Weather Warnings & Alerts
Alerts on SMHI Warnings & Alerts in Sweden.

## Districts
curl -s https://opendata-download-warnings.smhi.se/api/version/2/districtviews/all.json|jq . |egrep '(id|name)' | perl -p -e 's%^\s*(.*),\n%$1%g' | perl -p -e 's%""id%\n"id%g' |tr  '"' ' ' | perl -p -e 's% : %:%g'

id: 030  name: Uppsala län,Upplandskusten
id: 031  name: Värmlands län
id: 032  name: Västerbottens län inland
id: 033  name: Västerbottens län kustland
id: 034  name: Västernorrlands län
id: 035  name: Västmanlands län
id: 036  name: Västra Götalands län,norra Västergötland
id: 037  name: Kalmar län,Öland
id: 038  name: Örebro län
id: 039  name: Östergötlands län
id: 040  name: Skåne län,Österlen
id: 041  name: Bottenviken
id: 042  name: Norra Kvarken
id: 043  name: Norra Bottenhavet
id: 044  name: Södra Bottenhavet
id: 001  name: Norrbottens län,norra Lapplandsfjällen
id: 045  name: Ålands hav
id: 002  name: Västerbottens län,södra Lapplandsfjällen
id: 046  name: Skärgårdshavet
id: 003  name: Jämtlands län,Jämtlandsfjällen
id: 047  name: Finska viken
id: 004  name: Jämtlands län,Härjedalsfjällen
id: 048  name: Norra Östersjön
id: 005  name: Dalarnas län,Dalafjällen
id: 049  name: Mellersta Östersjön
id: 006  name: Blekinge län
id: 007  name: Västra Götalands län,Bohuslän och Göteborg
id: 008  name: Dalarnas län utom Dalafjällen
id: 009  name: Västra Götalands län,inre Dalsland
id: 050  name: Rigabukten
id: 051  name: Sydöstra Östersjön
id: 052  name: Södra Östersjön
id: 053  name: Sydvästra Östersjön
id: 010  name: Gotlands län
id: 054  name: Bälten
id: 011  name: Gävleborgs län inland
id: 055  name: Öresund
id: 012  name: Hallands län
id: 056  name: Kattegatt
id: 013  name: Jämtlands län utom fjällen
id: 057  name: Skagerack
id: 014  name: Jönköpings län,västra delen utom syd om Vättern
id: 058  name: Vänern
id: 015  name: Jönköpings län,östra delen
id: 016  name: Kalmar län utom Öland
id: 017  name: Kronobergs län,västra delen
id: 018  name: Kronobergs län,östra delen
id: 019  name: Norrbottens län inland
id: 020  name: Norrbottens län kustland
id: 021  name: Stockholms län,Roslagskusten
id: 022  name: Västra Götalands län,Sjuhäradsbygden och Göta älv
id: 023  name: Skåne län utom Österlen
id: 024  name: Gävleborgs län kustland
id: 025  name: Stockholms län utom Roslagskusten
id: 026  name: Jönköpings län,syd om Vättern
id: 027  name: Västra Götalands län,sydväst Vänern
id: 028  name: Södermanlands län
id: 029  name: Uppsala län utom Upplandskusten %

