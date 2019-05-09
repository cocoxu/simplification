from nltk.stem.wordnet import WordNetLemmatizer

lmtzr = WordNetLemmatizer()
def getLemma(word):
	stemnoun = lmtzr.lemmatize(word)
	stemverb = lmtzr.lemmatize(word, 'v')
	
	if len(stemnoun) < len(stemverb):
		return stemnoun
	elif len(stemnoun) > len(stemverb):
		return stemverb
	else:
		if stemnoun != word:
			return stemnoun
		elif stemverb != word:
			return stemverb

	return word
	
class Similarity(object):

	def intersect (self, list1, list2) :
		cnt1 = Counter()
		cnt2 = Counter()
		for tk1 in list1:
			cnt1[tk1] += 1
		for tk2 in list2:
			cnt2[tk2] += 1    
			inter = cnt1 & cnt2
		
		return len(list(inter.elements()))
		
	#def idfCosine (self, list1, list2, worddf) :		
	#	self.intersect(list1, list2)

		 	
	def JaccardSimToken(self, tokens1, tokens2):
		
		v1 = {}
		v2 = {}
		
		for token1 in tokens1 :
			v1[token1] = v1.get(token1, 0.0) + 1.0
		for token2 in tokens2 :
			v2[token2] = v2.get(token2, 0.0) + 1.0
		
		#print "v1\t",
		#print v1 
		#print "v2\t",
		#print v2
			
		cSum = 0.0
		#print list(set(v1.keys()) & set(v2.keys()))
		for k in list(set(v1.keys()) & set(v2.keys())):
			cSum += 1
			#cSum += min ( v1.get(k, 0.0) , v2.get(k, 0.0))
		vSum = 0.0
		#print list(set(v1.keys()) | set(v2.keys()))
		for k in list(set(v1.keys()) | set(v2.keys())):
			vSum += 1
			#vSum += max ( v1.get(k, 0.0) , v2.get(k, 0.0))
			#vSum += v1.get(k, 0.0) + v2.get(k, 0.0)
		if vSum == 0 :
			vSum = 1
		return cSum / vSum

	#asymmetric Jacquard Similarity
	def aJaccardSimSents(self, sent1, sent2):
		
		sent1 = sent1.lower().replace('-',' ')  # split "cloth-like"
		sent2 = sent2.lower().replace('-',' ')
		pre_sent1 = sent1[:3]
		pre_sent2 = sent2[:3]
		
		#print pre_sent1
		#print pre_sent2
		if (pre_sent1 == "# #" and pre_sent2 != "# #") or (pre_sent1 != "# #" and pre_sent2 == "# #") :
			return 0.0


		stems1 = [getLemma(i) for i in sent1.split()]
		stems2 = [getLemma(i) for i in sent2.split()]
		
		#stems1 = sent1.split()
		#stems2 = sent2.split()
		
		#print stems1
		#print stems2
		
		return self.JaccardSimToken(stems1, stems2) 
		
		

	#asymmetric Jacquard Similarity
	def aJaccardSimToken(self, tokens1, tokens2):
		
		v1 = {}
		v2 = {}
		
		for token1 in tokens1 :
			v1[token1] = v1.get(token1, 0.0) + 1.0
		for token2 in tokens2 :
			v2[token2] = v2.get(token2, 0.0) + 1.0
			
		cSum = 0.0
		for k in list(set(v1.keys()) & set(v2.keys())):
			cSum += 1
			#cSum += min ( v1.get(k, 0.0) , v2.get(k, 0.0))
		vSum = 0.0
		for k in list(set(v1.keys())):
			vSum += 1
			#vSum += max ( v1.get(k, 0.0) , v2.get(k, 0.0))
			#vSum += v1.get(k, 0.0) + v2.get(k, 0.0)
		if vSum == 0 :
			vSum = 1
		return cSum / vSum



