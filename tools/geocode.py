import json, time, urllib.request, urllib.parse, re
Q = json.load(open('tools/spots.json'))
FR = r', (Bruxelles|Cracovie|Édimbourg|Hô Chi Minh-Ville|Lisbonne|Londres|Pékin|Séoul|Séville|Varsovie|Vienne|Barcelone|Bologne|Le Cap|Singapour|Dubaï|Valence)$'
out = []
for c, i, q, la, lo in Q:
    vb = ','.join(map(str, [lo - .35, la + .35, lo + .35, la - .35]))
    u = 'https://nominatim.openstreetmap.org/search?' + urllib.parse.urlencode({'format': 'jsonv2', 'limit': 1, 'accept-language': 'en', 'viewbox': vb, 'bounded': 1, 'q': re.sub(FR, '', q)})
    r = None
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Escale-study-abroad/1.0 (sal635479@gmail.com)'})
        j = json.load(urllib.request.urlopen(req, timeout=20))
        if j: r = [round(float(j[0]['lat']), 5), round(float(j[0]['lon']), 5), j[0].get('type'), j[0].get('category'), j[0]['display_name'][:60]]
    except Exception as e:
        r = ['err', str(e)[:80]]
    out.append([c, i, r]); time.sleep(1.2)
json.dump(out, open('tools/spots_geo.json', 'w'), ensure_ascii=False, indent=0)
