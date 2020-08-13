inputq = "C:\Prashi\InformationRetrival\Project3\project3_data\project3_data\queries.txt"
import json
import urllib.request
import os
from langdetect import detect
from googletrans import Translator
translator = Translator()
#os.chdir('output')
#outfn = 'path_to_your_file.txt'
#count = 1



def characterEscape(query):
    q1 = query
    for character in ['\\', '+', '-', '&&', '||', '!', '(', ')', '{', '}', '[', ']', '^', '"', '~', '*', '?', ':', '/', ' ']:
        if character in q1:
            q1 = q1.replace(character, '\\' + character)
    return q1

def removeHashTag(text):
    return list(part[1:] for part in text.split() if part.startswith('#'))
               
def removeNumber(a):
    q1 = a.split(" ")
    s=''
    queryId = q1[0]
    q1.remove(q1[0])
    #print("q1",q1)
    for i in range(len(q1)):
        s = s + q1[i]+" "
    #print("S",s)
    return queryId,s
    
def addLangClause(query,ben,bde,bru,isBoost):
    lang_params = ["text_en","text_de","text_ru", "tweet_hashtags"]    
    q1 = query
    q1 = "query "+lang_params[0]+":"+q1+" OR "+lang_params[1]+":"+q1+" OR "+lang_params[2]+":"+q1
    if isBoost:
        if ben==1:
            q1 = q1+ "&bq:("+lang_params[0]+":"+query+")^2.5"
        elif bde==1:
            q1 = q1 +"&bq:("+lang_params[1]+":"+query+")^2.5"
        elif bru==1:
            q1 = q1+ "&bq:("+lang_params[2]+":"+query+")^2.5"
    #print("Q1",q1)
    return q1

def transalateQuery(en,de,ru,ben,bde,bru,isBoost):
    lang_params = ["text_en","text_de","text_ru", "tweet_hashtags"]
    q1 = "query "+lang_params[0]+":"+en+" OR "+lang_params[1]+":"+de+" OR "+lang_params[2]+":"+ru
    if isBoost:
        if ben==1:
            q1 = q1+ "&bq=("+lang_params[0]+":"+query+"^0.5)"
        elif bde==1:
            q1 = q1 +"&bq=("+lang_params[1]+":"+query+"^0.5)"
        elif bru==1:
            q1 = q1+ "&bq=("+lang_params[2]+":"+query+"^0.5)"
    #print("Q1",q1)
    return q1

def addRetweets(query):
    q1 = query
    rt= list(part[1:] for part in query.split() if part.startswith('a'))
    rt = [i for n, i in enumerate(rt) if i not in rt[:n]]
    rt1 = ''
    if len(rt) !=0:
        for id in range(len(rt)): 
            rt[id]= rt[id].replace('\\', '')
            rt1=rt1+rt[id]+"\\ "  
        if len(rt1) ==0:
            q1 = q1
        else:
            q1 = q1+"OR @:("+rt1+"^1)"
    return q1

def addHashTags(query):
    q1 = query
    hts = removeHashTag(query)
    hts = [i for n, i in enumerate(hts) if i not in hts[:n]] 
    ht = ''
    if len(hts) !=0:
        for id in range(len(hts)): 
            hts[id]= hts[id].replace('\\', '')
            ht=ht+hts[id]+"\\ "  
        if len(ht) ==0:
            q1 = q1
        else:
            q1 = q1+"OR tweet_hashtags:("+ht+"^3)"
    return q1

def detectQueryLang(query):
    sid = detect(query)
    isen =0 
    isde =0 
    isru = 0
    if sid == 'en':
            isen = 1
    elif sid == 'de':
            isde = 1
    elif sid == 'ru':
            isru = 1
    return isen,isde,isru

def getOtherLang(isen,isde,isru,query):
            if isen==1:
                en = characterEscape(query)
                translations = translator.translate(query, dest='de')
                de = characterEscape(translations.text)
                translations = translator.translate(query, dest='ru')
                ru = characterEscape(translations.text)
            elif isde==1:
                de = characterEscape(query)
                translations = translator.translate(query, dest='en')
                en = characterEscape(translations.text)
                translations = translator.translate(query, dest='ru')
                ru = characterEscape(translations.text)
            elif isru==1:
                ru=characterEscape(query)
                translations = translator.translate(query, dest='en')
                en = characterEscape(translations.text)
                translations = translator.translate(query, dest='de')
                de = characterEscape(translations.text)
            else:
                translations = translator.translate(query, dest='en')
                en = characterEscape(translations.text)
                translations = translator.translate(query, dest='de')
                de = characterEscape(translations.text)
                translations = translator.translate(query, dest='ru')
                ru = characterEscape(translations.text)
            return en,ru,de

models = ["BM25","DFR","LM"]
#models = ["LM"]
for model in models:
    #print("model",model)
    count = 1
    with open(inputq, encoding="utf-8") as f:
        soutfn = model + '/' + 'sample_query_output.txt'
        #soutfn = 'sample_query_output_'+model+ '.txt'
        soutf = open(soutfn,'w')
        for line in f:
            query = line.strip('\n')
            isen,isde,isru = detectQueryLang(query)
            en,ru,de = getOtherLang(isen,isde,isru,query)
            query=characterEscape(query)
            queryId,query=removeNumber(query)
            query=addLangClause(query,isen,isde,isru,0)
            #query=transalateQuery(en,de,ru,isen,isde,isru,0)
            query=addHashTags(query)
            #query=addRetweets(query)
            #print("query",query)
            print("QueryBeforeParsing",query)
            query = urllib.parse.quote(query)
            print("query",query)
            inurl = 'http://13.58.144.151:8983/solr/'+model+'/select?fl=id%2Cscore&q=' + query + '&indent=on&rows=20&wt=json'
            print("INURL",inurl)
            qid = str(count).zfill(3)
            
            outfn = model + '/' + qid+ '.txt'
            outf = open(outfn,'w')
            data = urllib.request.urlopen(inurl).read()
            print(data)
            docs = json.loads(data.decode('utf-8'))['response']['docs']
            rank = 1
            
            print("qid",qid)
            for doc in docs:
                outf.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + model + '\n')
                soutf.write(str(qid) + ' ' + 'Q0' + ' ' + str(doc['id']) + ' ' + str(rank) + ' ' + str(doc['score']) + ' ' + model + '\n')
                rank += 1
            outf.close()
            count += 1
    soutf.close()
