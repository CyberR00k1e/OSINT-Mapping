import requests
import json

url1="https://demo.vectra.io/api/v2.2/detections?category=command"


#paste vectra token below
r=requests.get(url1,headers={'Authorization': 'Token <enter vectra token here>>'})
detections=r.json()


u=detections["results"]
id=[]
for i in u:

    id.append(i["id"])

#print(id)
notes=[]
for l in id:
    try:
        s=requests.get(f"https://demo.vectra.io/api/v2.2/detections/{l}",headers={'Authorization': 'Token <token>'})
        capture = s.json()

        #x = capture["results"]
        dst_ips = capture["grouped_details"][0]["dst_ips"]
        #print(dst_ips)
        try:
            lookup=f"http://ip-api.com/json/{dst_ips[0]}"
        except:
            pass
        #notes.append(dst_ips)
        geo_name=requests.request("GET",lookup,verify=False).json()

        country=geo_name["country"]
        region=geo_name["regionName"]
        city=geo_name["city"]
        print(country,region,city)

        updates= requests.request('POST', f"https://demo.vectra.io/api/v2.2/detections/{l}/notes",headers={'Authorization': 'Token <paste vectra token here>',"Content-Type": "application/json"},data=json.dumps({'note':f"Public IP {dst_ips} is from {city} in the region {region} in {country}"}))
        #print(updates)
    except:
        pass
