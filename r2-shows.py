import requests, bs4, lxml

def timeConvert(xd):
	timestr = xd.text.strip()
	ftr = [3600,60,1]
	return str(sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]))
def choose(): 
	while True:
		ttt = input("PLS or M3U\nChoose format: ")
		if ttt == "PLS" or ttt == "M3U":
			return ttt
		else: 
			continue

service_link = "https://services.err.ee/podcast/channel/"
shows = [
["5", "Hallo, Kosmos!"],
["6", "Erik Morna"],
["7", "Olukorrast Riigis"],
["8", "Programm"],
["9", "Hommik!"],
["10", "Tallinn Express"],
["11", "Tjuun In"],
["12", "Linnadzungel"],
["13", "Elu Edetabelid"],
["14", "Nestor ja Morna"],
["15", "Tramm Ja Buss"],
["16", "Rahva Oma Kaitse"],
["17", "Draiv"],
["19", "Urbanism"],
["20", "Vibratsioon"],
["21", "Metallion"],
["22", "Eesti Pops"],
["23", "Etnokonservid"],
["25", "Haigla saade"],
["26", "Klubi R2"],
["27", "Rocki Ministeerium"],
["30", "Muusikanõukogu"],
["33", "Reede Hommik"],
["37", "Progressioon"],
["38", "Grindtape"],
["39", "Jazzitup"],
["40", "Bashment FM"],
["41", "Sinu Saade"],
["44", "Öötöö"],
["45", "Koit Raudsepp"],
["46", "Deeper Shades Of House"],
["59", "Suvehommik"],
["63", "Margus Kamlat"],
["64", "Laupäeva Hommik"],
["65", "Maarja Merivoo-Parro"],
["66", "Meloturniir"],
["67", "Ilus koht suudlemiseks"],
["72", "Tudengi 45"],
["76", "Machine Nation"],
["77", "Tähetund"]
]
for show in shows:
    print(show[1] + " [No. " + show[0] + "]")
print("")
while True:
    vastus = input("Palun vali saade/Please choose show: ")
    for show in shows:
        if vastus == show[0] or vastus == show[1]:
            vastus = [show[0], show[1]]
            break
    else:
        continue
    break
    
res = requests.get(service_link + vastus[0] + ".xml")
res.raise_for_status()
soup = bs4.BeautifulSoup(res.text, "lxml")


place = input("Nothing for current folder.\nchoose folder: ")

musicURL = soup.find_all("enclosure")
title = soup.find_all("title")
date = soup.find_all("pubDate")
length = soup.find_all("itunes:duration")
author = soup.find_all("author")

format = choose()

i = 0
if format == "M3U":
		f = open(place + title[0].text.strip() + ".M3U", "w")
		f.write("#EXTM3U \n")

		while i < len(musicURL):
			timestr = length[i].text.strip()
			ftr = [3600,60,1]
			a = str(sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]))

			f.write("#EXTINF:" + str(i) + ", " + author[0].text.strip()+ " - " + title[i].text.strip() + "\n")
			f.write(musicURL[i].get("url") + "\n \n")
			i += 1
elif format == "PLS":
		f = open(place + title[0].text.strip() + ".PLS", "w")
		f.write("[playlist] \nNumberOfEntries=" + str(len(musicURL)) + "\n \n")
		while i < len(musicURL):	
			# converts normal lenght to seconds which the PLS format uses
			fileLength = timeConvert(length[i])

			#writes all of the info to the file
			f.write("Title" + str(i) + "=" + title[i].text.strip() + "\n")
			f.write("Date" + str(i) + "=" + date[i].text.strip() + "\n")
			f.write("Length" + str(i) + "=" + fileLength + "\n")
			f.write("File" + str(i) + "=" + musicURL[i].get("url") + "\n \n")
			i += 1
f.close()
print("Done!")
