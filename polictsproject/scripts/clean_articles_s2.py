from politicsApp.models import Articles
import os, re
from django.db import connection

# Clean the article
def run():
#	cursor = connection.cursor()
#	cursor.execute("select * from politicsApp_articles;")
#	row = cursor.dictfetchall()
#	articles = Articles.objects.raw("select * from politicsApp_articles;")
	articles = Articles.objects.all()
	for article in articles:
		dict_output = textClean(article.RawText)
		processedText=dict_output.get('string')
		wordCount=dict_output.get('count')
		articleId = article.ArticleId
		Articles.objects.filter(ArticleId=articleId).update(ProcessedText=processedText,WordCount=wordCount)

		
def textClean(rawText):
	dict_output=regExp(rawText)
	return dict_output

def regExp(text):
	newString = ''
	for ch in text:
		if ch.isalpha() == True or ch == ',' or ch == '.' or ch == ' ' or ch == ';':
			newString+= ch
		else:
			pass

	newString = newString.replace('\n','')
	newString = newString.replace(',','.')
	print("newString:",newString)
	print("\n")
	newString = newString.replace('. ','.')
	newString = newString.replace(' .','.')
#	print("newString:",newString)
#	print("\n")
	
#	regex = re.compile(r'\b[A-Z]{1}\b')
#	result = regex.search(newString)
#	print("result: ",result)

	finalString = ''
	wordCount = 0
	for each in newString.split('.'):
#		print("each:",each)		
		if(len(each.split(' '))>1):
			for word in each.split(' '):
				if (len(word)>1 and len(word)<7) and (word.isupper() == True):
					finalString+=word
					wordCount+=1
					if each.split(' ').index(word) == len(each.split(' '))-1:
						finalString+=''
					else:
						finalString+=' '
				else:
					finalString+=word.lower()
					wordCount+=1
#					print("flag",flag)
					if each.split(' ').index(word) == len(each.split(' '))-1:
						finalString+=''
					else:
						finalString+=' '						
#					print("finalString:",finalString)

		else:
			if (len(each)>1 and len(each)<7) and (each.isupper() == True):
					finalString+=each
					wordCount+=1
			else:
				finalString+=each.lower()
				wordCount+=1
		finalString+='.'
	
	finalString = finalString.replace('..','.')
	finalString = finalString.replace('  ',' ')

	print("finalString:",finalString)
	print("\n")
	print('wordCount:',wordCount)
	dict_output={}
	dict_output['string']=finalString
	dict_output['count']=wordCount

	return dict_output

"""	
	nextString = ''
	for each in newString.split('.'):
		# need changes - not working for "RAriz. conceded" - result is RAriz.
		if (len(each)>1 and len(each)<7)


		if ((any(x.isupper() for x in each) and any(x =='.' for x in each)) or each.isupper() == True) and (len(each)>1 and len(each)<7):
			pass
		else:
			each = each.lower()
		nextString+=each
		nextString+=' '
"""

	# Need to check for continous space and periods
	

	


