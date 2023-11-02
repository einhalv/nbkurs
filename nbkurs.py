# (C) Einar  Halvorsen 2023
import urllib.request
import json
import matplotlib.pyplot as plt
import datetime
import sys 

argv =  sys.argv
today = datetime.date.today()
currencies = ['USD', 'EUR', 'GBP', 'JPY', 'SEK', 'DKK']

def xtrcurr(s):
    assert(len(s['dataSets']) == 1)
    d = s['dataSets'][0]
    ser = d['series']
    info = s['structure']['dimensions']['series']
    obs = s['structure']['dimensions']['observation'][0]['values']
    ends = [o['end'] for o in obs]
    for d in info:
        if d['id'] == 'QUOTE_CUR':
            quote_currency = d['values']
            break
    qc = (quote_currency[0]['id'], quote_currency[0]['name'])
    for d in info:
        if d['id'] == 'BASE_CUR':
            base_currency = d['values']
            break
    bcs = [(b['id'],b['name'])   for b in base_currency]
    val = len(ser)*[None]
    for ii in  range(len(val)):
        k = list(ser.keys())[ii]
        val[ii] = [float(c[0]) for c in list(ser[k]['observations'].values())]
    return {'motvaluta': qc, 'valutaer': bcs, 'dato': ends, 'verdier': val}

def extract(vc, id):
    ii = list(zip(*vc['valutaer']))[0].index(id)
    return [datetime.datetime.fromisoformat(d) for d in  vc['dato']], vc['verdier'][ii]

start = ''
slutt = ''
plot = False
id = ''
prog = argv.pop(0)
while argv:
    a = argv.pop(0)
    if a == 'start':
        start = argv.pop(0)
    elif a == 'slutt':
        slutt = argv.pop(0)
    elif a == 'plot':
        plot = True
    elif a.upper() in currencies:
        id = a.upper()
    else:
        print('error: argument \"{}\" invalid'.format(a))
        exit(1)

if not slutt:
    slutt = str(today)
if not start:
    start = (datetime.datetime.strptime(slutt, "%Y-%m-%d")
             -datetime.timedelta(365)).strftime("%Y-%m-%d")
link = 'https://data.norges-bank.no/api/data/EXR/B.{}.NOK.SP?'.format('+'.join(currencies))\
    + 'startPeriod={}'.format(start)\
    + '&endPeriod={}'.format(slutt)\
    + '&format=sdmx-json&locale=no'

h = urllib.request.urlopen(link)
s = str(h.read().decode())
sj = json.loads(s)
vc = xtrcurr(sj['data'])
curr0 = vc['motvaluta'][0]

if not id:
    print('Valutaer:')
    for t in vc['valutaer']:
        print('   ', t[0], ' ', t[1])
    exit(0)

t,v = extract(vc, id)
print(t[-1], '{}{}'.format(v[-1], curr0))
if plot:
    plt.plot(t, v)
    plt.ylabel(curr0)
    plt.xlabel('date')
    plt.title('Kurs, ' + id)
    plt.show()
