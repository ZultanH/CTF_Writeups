import requests

BASE_URL = 'http://challenge.ctf.games:31879'
def getLinks():
	global BASE_URL
	userAgentCount = 0
	userAgentDict = {}
	r = requests.get(f"{BASE_URL}/robots.txt")
	content = r.text
	firstSplit = content.split("\n")
	betterData = [line for line in firstSplit if len(line) > 1]
	for line in betterData:
		if line == '':
			continue

		if "User-agent" in line:
			userAgentCount = userAgentCount + 1
			if not userAgentDict.get(userAgentCount):
				userAgentDict[userAgentCount] = []
				userAgentDict[userAgentCount].append(line.replace("User-agent: ", ''))

		elif "Disallow" in line:
			line = line.replace("Disallow: ", '')
			userAgentDict[userAgentCount].append(line)
	return userAgentDict

def main():
	flagArray = {}
	while True:
		result = getLinks()
		for key in result:
			_array = result[key]
			userAgent = _array[0]
			for i in range(1, len(_array)):
				r = requests.get(BASE_URL + _array[i], headers={'User-agent': userAgent})
				text = r.text
				if "REJOICE" in text:
					print(text + "\n")
					fileName = _array[i].replace('/', '')
					splitText = text.split(' ')
					flagIndex = [int(splitText[idx + 1]) for idx in range(0, len(splitText)) if splitText[idx] == 'INDEX'][0]
					characterIndex = [int(splitText[idx + 1]) for idx in range(0, len(splitText)) if splitText[idx] == 'INDEX'][1]
					flagArray[flagIndex] = fileName[characterIndex]
					print(flagArray)
					
if __name__ == "__main__":
	main()
