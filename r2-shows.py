import requests, bs4

i = 0
while i == 0:
	try: 
		link = input("rss feed: ")
		res = requests.get(link)
		res.raise_for_status()
		soup = bs4.BeautifulSoup(res.text, "xml")
		i = 1
	except:
		print("\nInvalid link")

place = input("Nothing for current folder.\nchoose folder: ")

musicURL = soup.find_all("enclosure")
title = soup.find_all("title")
date = soup.find_all("pubDate")
length = soup.find_all("itunes:duration")
author = soup.find_all("author")

def timeConvert(xd):
	timestr = xd.text.strip()
	ftr = [3600,60,1]
	return str(sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]))

while i != 0:
	format = input("PLS or M3U\nChoose format: ")
	if format == "PLS":
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
		i = 0
	elif format == "M3U":
		f = open(place + title[0].text.strip() + ".M3U", "w")
		f.write("#EXTM3U \n")

		while i < len(musicURL):
			timestr = length[i].text.strip()
			ftr = [3600,60,1]
			a = str(sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]))

			f.write("#EXTINF:" + str(i) + ", " + author[0].text.strip()+ " - " + title[i].text.strip() + "\n")
			f.write(musicURL[i].get("url") + "\n \n")
			i += 1
		i = 0
	else:
		print("\nInvalid option!")
f.close()
print("Done!")