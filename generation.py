import stanfordnlp
import nltk
from collections import deque 

nlp = stanfordnlp.Pipeline()
#sent = "He advocated for the independence of Gambia during the colonial era."
#sent = "He is defeated for many times in his life."
#sent = "“Bill wants to play a popular board game with his close friends."
#sent = "Rice is the seed of the grass species Oryza sativa (Asian rice) or Oryza glaberrima (African rice)."
#sent = "As a cereal grain, it is the most widely consumed staple food for a large part of the world human population, especially in Asia."
#sent = "It is the agricultural commodity with the third highest worldwide production (rice, 741.5 million tonnes in 2014), after sugarcane (1.9 billion tonnes) and maize (1.0 billion tonnes)."
#sent = "The decimal numeral systemm is the standard system for denoting integer and non-integer numbers"
#sent = "It is the extension to non-integer numbers of the Hindu Arabic numeral system."
sent = "The way of denoting numbers in the decimal system is often referred to as decimal notation."
#sent = "Alieu Ebrima Cham Joof (22 October 1924 2013 2 April 2011) commonly known as Cham Joof or Alhaji Cham Joof, was a Gambian historian, politician, author, trade unionist, broadcaster, radio programme director, scout master, Pan-Africanist, lecturer, columnist, activist and an African nationalist."
#sent = "The complements modify the meaning  of  the  main  components. "
#sent = "We extract all comments about people and replace compound sentences with simple sentences"
#sent = "we use statistical generation method to produce descriptions of tables or explanation and recommendation from users reviews of an item."
#sent = "it describes a system that can give reasonable and supportive evidence to the answer to a question asked to an image."
#sent = "We will focus on processing relative clauses and enriching the set of sentence structures, especially for compound and complex sentences."

doc = nlp(sent)
tokenized_sent = nltk.word_tokenize(sent)
nlpresult_pos = nltk.pos_tag(nltk.word_tokenize(sent))
print("NLP result POS: ", nlpresult_pos)


dependencies = doc.sentences[0].print_dependencies()
print(dependencies)

nlpresult_parse =[]
asp_parse = []

## converting parse tress to ASP program  
for dep in range(len(dependencies)):
    nlpresult_parse.append(dependencies[dep][-1] + "(" + dependencies[dep][1] + "," + str(dep+1) + ")") 
    asp_parse.append(dependencies[dep][-1] + "(" + tokenized_sent[int(dependencies[dep][1])-1] + "-" + dependencies[dep][1] + "," 
          + dependencies[dep][0] + "-" + str(dep+1) + ")")

print("NLP result Dependency Parse: ", nlpresult_parse)  
print("ASP program for parse: ", asp_parse)

## converting POS tags to ASP program
asp_tag = []
for i in range(len(nlpresult_pos)):
    asp_tag.append("pos_tag(" + str(i) + "," + nlpresult_pos[i][1].lower() + ")")
print("ASP program for POS tags: ", asp_tag)


structures_templates = []
structures = []
components_dict = {}


new_dependencies = []
for item in dependencies:
    new_item = (item[0] ,tokenized_sent[int(item[1])-1], item[2])
    new_dependencies.append(new_item)

print('dependencies: ', dependencies)
print('modified dependencies: ', new_dependencies)

subj = [item for item in new_dependencies if 'nsubj' in item]
obj = [item for item in new_dependencies if 'obj' in item]
xcomp = [item for item in new_dependencies if 'xcomp' in item]
cop = [item for item in new_dependencies if 'cop' in item]
nsubjpass = [item for item in new_dependencies if 'nsubj:pass' in item]
auxpass = [item for item in new_dependencies if 'aux:pass' in item]

if subj != []:
    structures_templates.append("structure(1,1)")
    structures.append(subj)
    
if subj != [] and obj != []:
    structures_templates.append("structure(2,2)")
    structures.append(subj + obj)
    
if subj != [] and cop != []:
    structures_templates.append("structure(4,2)")
    structures.append(subj + cop)

if nsubjpass != [] and auxpass != []:
    structures_templates.append("structure(5,2)")
    structures.append(nsubjpass + auxpass)

if subj != [] and obj != [] and xcomp != []:
    structures_templates.append("structure(3,3)")
    structures.append(subj + xcomp + obj)  
              
print("List of structures of a sentence: ", structures)
print("List of structure templates of a sentence: ", structures_templates)

sentence_structure = structures[-1]
sentence_template = structures_templates[-1]
print("Selected structure for this sentence is: ", sentence_structure)
print("Selected template for this sentence is: ", sentence_template)


## Main components recognition
if sentence_template == 'structure(1,1)':
    result = [item for item in new_dependencies if item[2]=='nsubj']
    components_dict['subj'] = result[0][0]
    components_dict['verb'] = result[0][1]

if sentence_template == 'structure(2,2)':
    result = [item for item in new_dependencies if item[2]=='nsubj']
    components_dict['subj'] = result[0][0]
    components_dict['verb'] = result[0][1]
    result1 = [item for item in new_dependencies if item[2]=='obj']
    components_dict['obj'] = result1[0][0]

if sentence_template == 'structure(5,2)':
    result = [item for item in new_dependencies if item[2]=='nsubj:pass']
    components_dict['subj'] = result[0][0]
    components_dict['verb'] = result[0][1]

if sentence_template == 'structure(4,2)':
    result = [item for item in new_dependencies if item[2]=='nsubj']
    components_dict['subj'] = result[0][0]
    pos_tag = nltk.pos_tag([result[0][1]])
    if 'jj' in pos_tag[0][1].lower():
        components_dict['adj'] = result[0][1]
    else:
        components_dict['obj'] = result[0][1]

if sentence_template == 'structure(3,3)':
    result = [item for item in new_dependencies if item[2]=='nsubj']
    components_dict['subj'] = result[0][0]
    components_dict['verb-1'] = result[0][1]
    result1 = [item for item in new_dependencies if item[2]=='xcomp']
    components_dict['verb-2'] = result1[0][0]
    result2 = [item for item in new_dependencies if item[2]=='obj']
    components_dict['obj'] = result2[0][0]
        

print("Main components: ", components_dict)            

## main representation construction
if sentence_template == 'structure(1,1)':
    rep = components_dict['subj'] + ' ' + components_dict['verb']
    print("rep: " ,rep)
 
if sentence_template == 'structure(2,2)':
    rep = components_dict['subj'] + ' ' + components_dict['verb'] + ' ' + components_dict['obj']
    print("rep: " ,rep)
     
if sentence_template == 'structure(3,3)':
    rep = components_dict['subj'] + ' ' + components_dict['verb-1'] + ' ' + components_dict['verb-2'] + ' ' + components_dict['obj']
    print("rep: " ,rep)
 
if sentence_template == 'structure(4,2)':
    if 'adj' in components_dict:
        rep = components_dict['subj'] + ' ' + components_dict['adj'] 
    elif 'obj' in components_dict:
        rep = components_dict['subj'] + ' ' + components_dict['obj']
    print("rep: " ,rep)
 
if sentence_template == 'structure(5,2)':
    rep = components_dict['subj'] + ' ' + components_dict['verb']
    print("rep: " ,rep)

q = deque() 

## all cases
it = [item for item in new_dependencies if ('nsubj' in item[2])]
ind = new_dependencies.index(it[0])

results = [item for item in new_dependencies if (item[2]=='case' and new_dependencies.index(item) > ind)]
 
prep_list =[]
for i in range(len(results)):
    case_phrase = ''
    case_phrase =  results[i][0] + ' ' +  results[i][1]
    prep_list.append(case_phrase)


 
rep = rep + ' ' + ' '.join(prep_list) 
rep_tokens = nltk.word_tokenize(rep)
for token in rep_tokens:
    q.append(token)
print(q)

while len(q) != 0:
    new_token = ''
    tok = q.popleft()
    ## compound nouns
    results = [item for item in new_dependencies if (item[2]=='compound' and item[1] == tok)]
    noun_phrase = ''
    for i in range(len(results)):
        components_dict['compound%s'%i] = results[i][0]
        q.append(results[i][0])
        noun_phrase =  noun_phrase + ' ' + results[i][0]
    
    
    new_token = noun_phrase + ' ' + tok
      
    ## adjective phrases    
    results = [item for item in new_dependencies if (item[2]=='amod' and item[1] == tok)]
    adj_phrase = '' 
    for i in range(len(results)):
        components_dict['adj-mod%s'%i] = results[i][0]
        q.append(results[i][0])
        adj_phrase =  adj_phrase + ' ' + results[i][0]
    new_token = adj_phrase + ' ' + new_token
    
      
    ## adverbial phrases
    results = [item for item in new_dependencies if (item[2]=='advmod' and item[1] == tok)]
    adv_phrase = ''
    for i in range(len(results)):
        components_dict['adv-mod%s'%i] = results[i][0]
        q.append(results[i][0])
        adv_phrase =  adv_phrase + ' ' + results[i][0]
    new_token = adv_phrase + ' ' + new_token
     
     
    
    ## conjunction
    results = [item for item in new_dependencies if (item[2]=='conj' and item[1] == tok)]
    conj_phrase = ''
    for i in range(len(results)):
        components_dict['conj%s'%i] = results[i][0]
        q.append(results[i][0])
        conj_phrase =  conj_phrase + ' ' + results[i][0]
    new_token = new_token + ' ' + conj_phrase
    
    rep = rep.replace(tok,new_token)

rep = ' '.join(nltk.word_tokenize(rep))
print(rep)    

