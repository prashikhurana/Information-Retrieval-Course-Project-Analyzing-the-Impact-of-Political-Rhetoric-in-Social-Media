import sys

dictionaryOfTerms = {}
dictionaryOfDocs = {}


class Node():
    def __init__(self, docNo=None, termsInDoc=None,next_node=None):
        #print("Getting a new node",docNo,termsInDoc)
        self.docNo = docNo
        self.termsInDoc = termsInDoc
        self.next_node = next_node

    def get_docNo(self):
        #print("Node: get_docNo",self.docNo)
        return self.docNo

    def getNextNode(self):
        #print("Node: getNextNode")
        return self.next_node

    def set_next(self, new_next):
        #print("Node: setNextNode")
        self.next_node = new_next
    
    def getTermsInDoc(self):
        #print("Node:termsInDoc",self.termsInDoc)
        return self.termsInDoc
    
    def updateTermsInDoc(self):
        #print("Node: updateTermsInDoc")
        self.termsInDoc = self.termsInDoc + 1

class LinkedList: 
    
    def __init__(self):  
        #print("LinkedList:start")
        self.head = None
        
    def sortedInsert(self, new_node): 
        #print("LinkedList:sortedInsert") 
        # Special case for the empty linked list  
        if self.head is None: 
            new_node.next_node = self.head 
            self.head = new_node 
  
        elif self.head.docNo >= new_node.docNo: 
            new_node.next_node = self.head 
            self.head = new_node 
  
        else : 
  
            # Locate the node before the point of insertion 
            current = self.head 
            while(current.next_node is not None and
                 current.next_node.docNo < new_node.docNo): 
                current = current.next_node
              
            new_node.next_node = current.next_node
            current.next_node = new_node 
            
    def append(self, new_data): 
 
       new_node = Node(new_data) 
     
       if self.head is None: 
            self.head = new_node 
            return
     
       last = self.head 
       while (last.next_node): 
           last = last.next_node
     
       last.next_node =  new_node 
    
    def insert(self, docNo,termsInDoc):
        #print("LinkedList: insert")
        new_node = Node(docNo,termsInDoc) 
        new_node.set_next(self.head)
        self.head = new_node
        #self.printList()
        return self

    def printList(self):
       #print("LinkedList: print")
       curr = self.head
       while curr:
           print("[",curr.get_docNo(),":",curr.getTermsInDoc(),"]")
           curr = curr.getNextNode()
           
    def getSize(self):
       size = 0
       curr = self.head
       while curr:
           size = size+1
           curr = curr.getNextNode()
       return size
        
    def getAnodeandUpdate(self,docId):
       #print("GET A NODE")
       #print(self.printList())
       curr = self.head
       while curr:
           if curr.get_docNo() == docId:
               curr.updateTermsInDoc()
               #print("[",curr.get_docNo(),":",curr.getTermsInDoc(),"]")
               return True
           curr = curr.getNextNode()
    
  
    def getOnlyPosting(term,self):
       l1 = list()
       curr = self.head
       while curr:
           l1.append(curr.get_docNo())
           curr = curr.getNextNode()
       
       return term,l1
       
    def getSingleNode(self):
        return self.head
    
    def getOnlyPostingAndOr(result):
       l1 = list()
       curr = result.head
       while curr:
           l1.append(curr.get_docNo())
           curr = curr.getNextNode()
       
       return l1
       
    def getTfFromLinkedList(termlist,docId):
       a=0
       curr = termlist.head
       while curr:
           if Node.get_docNo(curr) == docId:
               a = Node.getTermsInDoc(curr)
           curr = curr.getNextNode()
       return a
       
def addWordToIndex(word,docId):
   #print("ADDING WORD", word)
   if word in dictionaryOfTerms.keys():
       #print("WORD EXISTS IN DIC",word)
       vlist = dictionaryOfTerms[word]
       plist = vlist[1]
       #print("VLIST",
       #LinkedList.printList(plist)
       if isinstance(plist,LinkedList):
           #print("plist is instance of linked list")
           if LinkedList.getAnodeandUpdate(plist,docId):
               a=1
           else:
               vlist[0] = vlist[0] + 1
               #update doc frequency and posting list 
               ll = LinkedList()
               plist = LinkedList.sortedInsert(plist,Node(docId,1))
               
           #print("Update DocId")
           
           #else add the docId in a sorted way to the posting list, with termsInDoc as 1 
   else:
       #print("DIC ADD")
       ll = LinkedList()
       #print("LL",ll)
       ll = LinkedList.insert(ll,docId,1)
       #LinkedList.printList(ll)
       vlist = [1,ll]
       #print("DIC ADD:",vlist)
       dictionaryOfTerms[word] = vlist
       


def createInvertedIndex(text):
    docIdWords = text.split("\t")
    words = docIdWords[1].split()
    docId = docIdWords[0]
    #print("DOCID",docId)
    c = 0
    for word in words:
        c = c+1    
        addWordToIndex(word,docId)
        
    dictionaryOfDocs[docId] = c
          
        
def printDictionary(dictionaryOfTerms):
    print("DICTIONARY")
    for key in dictionaryOfTerms.keys():
        v = dictionaryOfTerms[key]
        print(key,":[",v[0],",")
        LinkedList.printList(v[1])
        print("]")
        
p1 = sys.argv[1]
f = open(p1, "r")
for x in f:
  createInvertedIndex(x)


def getListInString(text,l1,w1):
    if len(l1)==0:
         s = text+" "+"empty"
         w1.write(s)
    else:
        s = text+" "
        for i in range(len(l1)):
            s = s+l1[i]+" "
        w1.write(s)
    w1.write("\n")

def getListInStringA(l1,w1):
    s =""
    for i in range(len(l1)):
        s = s+l1[i]+" "
    w1.write(s)
    w1.write("\n")

def getPostingListForTerm(listOfTerms,w1):
    
    for x in range(len(listOfTerms)): 
        vlist = dictionaryOfTerms[listOfTerms[x]]
        term,l1=LinkedList.getOnlyPosting(listOfTerms[x],vlist[1])
        w1.write("GetPostings"+"\n")
        w1.write(term+"\n")
        p = "Postings list:"
        getListInString(p,l1,w1)
        #w1.write("Postings list:",*l1)


def DaatAnd(listOfTerms,w1):
    ec = 0
    totalcomp = 0
    listOfTermsc = listOfTerms
    listOfTermscI = listOfTerms.copy()
    w1.write("DaatAnd")
    w1.write("\n")
    getListInStringA(listOfTermsc,w1)
    #print(len(listOfTermsc))
    terms = SortByIncreasingFrequency(listOfTermsc)
    vlist = dictionaryOfTerms[listOfTermsc[0]]
    result = vlist[1]
    terms.pop(0)
    while len(terms)!=0 and LinkedList.getSize(result)!=0:
        vlist = dictionaryOfTerms[listOfTermsc[0]]
        ec,result = Intersect2PostingList(result, vlist[1])
        totalcomp = totalcomp +ec
        terms.pop(0)
    al = LinkedList.getOnlyPostingAndOr(result)
    p = "Results:"
    getListInString(p,al,w1)
    nD = "Number of documents in results: "+ str(LinkedList.getSize(result))
    w1.write(nD)
    w1.write("\n")
    nC = "Number of comparisons: " + str(totalcomp)
    w1.write (nC)
    w1.write("\n")
    r = getTfIdf(listOfTermscI,al)
    w1.write("TF-IDF")
    w1.write("\n")
    getListInString(p,r,w1)
    return al

def Intersect2PostingList(p1, p2):
    #LinkedList.printList(p1)
    #LinkedList.printList(p2)
    answer = LinkedList()
    comp= 0
    curr1 = LinkedList.getSingleNode(p1)
    curr2 = LinkedList.getSingleNode(p2)
    while curr1 !=None and curr2!=None:
          if curr1.get_docNo() == curr2.get_docNo():
             comp= comp+1 
             answer.append(curr1.get_docNo()) 
             curr1 = curr1.next_node
             curr2 = curr2.next_node
          elif curr1.get_docNo() < curr2.get_docNo():
              comp= comp+1
              curr1 = curr1.next_node
          elif curr1.get_docNo() > curr2.get_docNo():
              comp= comp+1
              curr2 = curr2.next_node
    #print ("Number of comparisons:",comp)
    return comp,answer

def DaatOr(listOfTerms,w1):
    ec = 0
    totalcomp = 0
    listOfTermsd = listOfTerms
    listOfTermscI = listOfTerms.copy()
    w1.write("DaatOr")
    w1.write("\n")
    #w1.write(*listOfTermsd)
    getListInStringA(listOfTermsd,w1)
    #print(len(listOfTermsd))
    terms = SortByIncreasingFrequency(listOfTermsd)
    vlist = dictionaryOfTerms[listOfTermsd[0]]
    result = vlist[1]
    terms.pop(0)
    while len(terms)!=0 and LinkedList.getSize(result)!=0:
        vlist = dictionaryOfTerms[listOfTermsd[0]]
        ec,result = OR2PostingList(result, vlist[1])
        totalcomp = totalcomp + ec
        terms.pop(0)
    ol = LinkedList.getOnlyPostingAndOr(result)
    p ="Results:"
    getListInString(p,ol,w1)
    nD = "Number of documents in results: "+ str(LinkedList.getSize(result))
    w1.write(nD)
    w1.write("\n")
    nC = "Number of comparisons: " + str(totalcomp)
    w1.write (nC)
    w1.write("\n")
    r = getTfIdfOR(listOfTermscI,ol)
    w1.write("TF-IDF")
    w1.write("\n")
    #w1.write("Results:",*r)
    getListInString(p,r,w1)
    return ol

def OR2PostingList(p1, p2):
    answer = LinkedList()
    comp= 0
    curr1 = LinkedList.getSingleNode(p1)
    curr2 = LinkedList.getSingleNode(p2)
    while curr1 !=None and curr2!=None:
          if curr1.get_docNo() == curr2.get_docNo():
             comp= comp+1 
             answer.append(curr1.get_docNo()) 
             curr1 = curr1.next_node
             curr2 = curr2.next_node
          elif curr1.get_docNo() < curr2.get_docNo():
              comp= comp+1
              answer.append(curr1.get_docNo()) 
              curr1 = curr1.next_node
          else:
              answer.append(curr2.get_docNo()) 
              curr2 = curr2.next_node
    if curr1!=None and curr2 == None:
        while curr1 !=None:
             answer.append(curr1.get_docNo())  
             curr1 = curr1.next_node
    if curr1 ==None and curr2 != None:
        while curr2 !=None:
            answer.append(curr2.get_docNo())  
            curr2 = curr2.next_node
              
    return comp,answer

def SortByIncreasingFrequency(listll):
    return listll

def getTotalNumberOfDocuments(dictionaryOfDocs):
    return len(dictionaryOfDocs.keys())
        
def getTfIdf(listOfTerms,Al):
    #print(*listOfTerms)
    dictionaryTf = {}
    totalNumberOfDocs = getTotalNumberOfDocuments(dictionaryOfDocs)
    for t in range(len(listOfTerms)):
        term = listOfTerms[t]
        vlist = dictionaryOfTerms[term]
        df = vlist[0]
        termPostingListDocTf = vlist[1]
        docsWIthTermInIt = LinkedList.getSize(termPostingListDocTf)
        for i in range(len(Al)): 
            docId = Al[i]
            tf = LinkedList.getTfFromLinkedList(termPostingListDocTf,docId)
            TF = tf/dictionaryOfDocs[docId]
            IDF = totalNumberOfDocs/docsWIthTermInIt
            tfidf = TF*IDF
            if  docId in dictionaryTf.keys():
                v = dictionaryTf[docId]
                v = v+tfidf
                dictionaryTf[docId] = v
            else:
                dictionaryTf[docId] = tfidf
    
    a1_sorted_keys = sorted(dictionaryTf, key=dictionaryTf.get, reverse=True)
    ll = []
    for keys in a1_sorted_keys:
        ll.append(keys)
    return ll


def getTfIdfOR(listOfTerms,Al):
    #print(*listOfTerms)
    dictionaryTfOR = {}
    totalNumberOfDocs = getTotalNumberOfDocuments(dictionaryOfDocs)
    for t in range(len(listOfTerms)):
        term = listOfTerms[t]
        vlist = dictionaryOfTerms[term]
        df = vlist[0]
        termPostingListDocTf = vlist[1]
        docsWIthTermInIt = LinkedList.getSize(termPostingListDocTf)
        for i in range(len(Al)): 
            docId = Al[i]
            tf = LinkedList.getTfFromLinkedList(termPostingListDocTf,docId)
            TF = tf/dictionaryOfDocs[docId]
            IDF = totalNumberOfDocs/docsWIthTermInIt
            tfidf = TF*IDF
            if  docId in dictionaryTfOR.keys():
                v = dictionaryTfOR[docId]
                v = v+tfidf
                dictionaryTfOR[docId] = v
            else:
                dictionaryTfOR[docId] = tfidf
    
    a1_sorted_keys = sorted(dictionaryTfOR, key=dictionaryTfOR.get, reverse=True)
    ll = []
    for keys in a1_sorted_keys: 
        ll.append(keys)
    return ll

#printDictionary(dictionaryOfTerms)
    
def getQuery():
    c = 0
    filepath = sys.argv[3]
    f2 = sys.argv[2]
    with open(filepath) as fp:
        for line in fp:
            c = c+1
            global s
            listOfTermsa = []
            listOfTermso = []
            #print(line)
            terms =  line.split()
            for term in terms:
                #term = "'"+term+"'"
                listOfTermsa.append(term)
                listOfTermso.append(term)
            w1= open(f2,"a+")
            if c>=2:
                w1.write("\n")
            getPostingListForTerm(listOfTermsa,w1)
            DaatAnd(listOfTermsa,w1)
            DaatOr(listOfTermso,w1)
            w1.write("")
    fp.close()
    

getQuery()