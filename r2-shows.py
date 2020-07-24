import requests, bs4
link = input("Show rss feed: ")
name = input("Show name: ")
res = requests.get(link)
res.raise_for_status()

soup = bs4.BeautifulSoup(res.text, "xml")
musicURL = soup.find_all("enclosure")
title = soup.find_all("title") #3
date = soup.find_all("pubDate")

length = soup.find_all("itunes:duration")

print("Nothing for current folder.")
place = input("Folder: ")

f = open(place + name + ".PLS", "w")
f.write("[playlist] \nNumberOfEntries=" + str(len(musicURL)) + "\n \n")

i = 1
while i < len(musicURL):

		timestr = length[i].text.strip()
		ftr = [3600,60,1]
		a = str(sum([a*b for a,b in zip(ftr, map(int,timestr.split(':')))]))

		print(title[i].text.strip())
		print(musicURL[i].get("url"))
		print(date[i].text.strip())
		print(a)
		print(" ")

		f.write("Title" + str(i) + "=" + title[i].text.strip() + "\n")
		f.write("Date" + str(i) + "=" + date[i].text.strip() + "\n")
		f.write("Length" + str(i) + "=" + a + "\n")

		f.write("File" + str(i) + "=" + musicURL[i].get("url") + "\n \n")
		i += 1
f.close()