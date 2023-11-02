# nbkurs
Henter ned valutakurser fra Norges bank. 

Bruk:

python nbkurs.py [options] [valuta]

| Parameter | Definition                           |
|-----------|:-------------------------------------|
| valuta    | navn på valuta, f.eks. NOK, EUR, JPY |
| options   | option \| option options             |
| option    | start <dato> \| slutt <dato> \| plot |
| <dato>    | dato på formatet YYYY-MM-DD          |


Hvis en option eller valuta defineres flere ganger så er det siste definisjon som gjelder.
