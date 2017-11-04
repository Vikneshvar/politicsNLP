from politicsApp.models import Articles, Ngram
import os

def run():
	articles = Articles.objects.all()
	gramList = []
	for article in articles:
		processedText = article.ProcessedText
		sentenceList = processedText.split('.')

		for sentence in sentenceList:
			wordList = sentence.split(' ')			
			
			# 1 gram
			for word in wordList:
				gramList.append(word)
			
			# 2 gram
			if(len(wordList)==2):
				gramList.append(wordList[0]+' '+wordList[1])
			
			# 2 gram - club by 2 words
			if(len(wordList)>2):
				i=0
				j=0
				while(j<len(wordList)-1):
					j = i+1
					gramList.append(wordList[i]+" "+wordList[j])
					i+=1
			
			# 3 gram
			if(len(wordList)>3):
				i=0
				j=0
				while(j<len(wordList)-1):
					j = i+2
					combo = ''
					m=i
					while(m<=j):
						combo = combo + wordList[m]
						if m!=j:
							combo = combo + ' '
						m+=1
					gramList.append(combo)
					i+=1

			# 4 gram
			if(len(wordList)>4):
				i=0
				j=0
				while(j<len(wordList)-1):
					j = i+3
					combo = ''
					m=i
					while(m<=j):
						combo = combo + wordList[m]
						if m!=j:
							combo = combo + ' '
						m+=1
					gramList.append(combo)
					i+=1

			# 5 gram
			if(len(wordList)>5):
				i=0
				j=0
				while(j<len(wordList)-1):
					j = i+4
					combo = ''
					m=i
					while(m<=j):
						combo = combo + wordList[m]
						if m!=j:
							combo = combo + ' '
						m+=1
					gramList.append(combo)
					i+=1

			# 6 gram
			if(len(wordList)>6):
				i=0
				j=0
				while(j<len(wordList)-1):
					j = i+5
					combo = ''
					m=i
					while(m<=j):
						combo = combo + wordList[m]
						if m!=j:
							combo = combo + ' '
						m+=1
					gramList.append(combo)
					i+=1

	# Remove duplicates from ngram
	ngramList = list(set(gramList))

	print("gramList ", len(gramList))
	print("ngramList ", len(ngramList))

	# Store ngram in database
	for item in ngramList:
		ngram = Ngram(Ngram=item)
		ngram.save()



