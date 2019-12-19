## This file can be used to generate the sentence representations with only main components

import nltk
import spacy
import re

nlp = spacy.load("en_core_web_sm")

## extracting POS tags
sent = "Bill plays a popular board game with his close friends."
nlpresult_pos = nltk.pos_tag(nltk.word_tokenize(sent))
print("NLP result POS: ", nlpresult_pos)

## extracting dependency parse trees 
nlpresult_parse = []
doc = nlp(sent)
for token in doc:
    nlpresult_parse.append("{2}({3}-{6}, {0}-{5})".format(token.text, token.tag_, token.dep_, token.head.text, token.head.tag_, token.i+1, token.head.i+1))

print("NLP result Dependency Parse: ", nlpresult_parse)    


## converting parse tress to ASP program    
asp_parse = []
for parse in nlpresult_parse:
    t1 = parse.split('(')[0]
    t2 = parse.split('(')[1].split(',')[0].split('-')[1]
    t3 = parse.split('(')[1].split(',')[1].split('-')[1][:-1] 
    asp_parse.append(t1 + '(' + t2 +',' + t3 + ')')
print("ASP program for parse: ", asp_parse)

## converting POS tags to ASP program
asp_tag = []
for i in range(len(nlpresult_pos)):
    asp_tag.append("pos_tag(" + str(i) + "," + nlpresult_pos[i][1].lower() + ")")
print("ASP program for POS tags: ", asp_tag)


## sentence structure and components recognition
r_subj = re.compile("nsubj.*")
r_obj = re.compile("dobj.*")
r_xcomp = re.compile("xcomp.*")
r_cop = re.compile("cop.*")
r_subjpass = re.compile("nsubjpass.*")
r_auxpass = re.compile("auxpass.*")


structures_templates = []
structures = []
components_dict = {}

if list(filter(r_subj.match, nlpresult_parse)) != []:
    structures_templates.append("structure(1,1)")
    result = list(filter(r_subj.match, nlpresult_parse))
    structures.append(result)
    verb = result[0].split('(')[1].split(',')[0].split('-')[0]
    subj = result[0].split('(')[1].split(',')[1].split('-')[0][1:]
    components_dict['verb'] = verb
    components_dict['subj'] = subj
    
if list(filter(r_subj.match, nlpresult_parse)) != [] and list(filter(r_obj.match, nlpresult_parse)) != []:
    structures_templates.append("structure(2,2)")
    result1 = list(filter(r_subj.match, nlpresult_parse))
    result2 = list(filter(r_obj.match, nlpresult_parse))
    structures.append(result1 + result2)
    obj = result2[0].split('(')[1].split(',')[1].split('-')[0][1:]
    components_dict['obj'] = obj
    
if list(filter(r_subj.match, nlpresult_parse)) != [] and list(filter(r_xcomp.match, nlpresult_parse)) != [] and list(filter(r_obj.match, nlpresult_parse)) !=[]:
    structures_templates.append("structure(3,3)")
    result1 = list(filter(r_subj.match, nlpresult_parse))
    result2 = list(filter(r_xcomp.match, nlpresult_parse))
    result3 = list(filter(r_obj.match, nlpresult_parse))
    structures.append(result1 + result2 + result3)
    verb1 = result1[0].split('(')[1].split(',')[0].split('-')[0]
    subj = result1[0].split('(')[1].split(',')[1].split('-')[0][1:]
    verb2 = result2[0].split('(')[1].split(',')[1].split('-')[0][1:]
    obj = result3[0].split('(')[1].split(',')[1].split('-')[0][1:]
    components_dict['verb_1'] = verb1
    components_dict['verb_2'] = verb2
    components_dict['subj'] = subj
    components_dict['obj'] = obj
    
if list(filter(r_subj.match, nlpresult_parse)) != [] and list(filter(r_cop.match, nlpresult_parse)) != []:
    structures_templates.append("structure(4,2)")
    result1 = list(filter(r_subj.match, nlpresult_parse))
    result2 = list(filter(r_cop.match, nlpresult_parse))
    structures.append(result1 + result2)
    subj = result1[0].split('(')[1].split(',')[1].split('-')[0][1:]
    components_dict['subj'] = subj
    o = result1[0].split('(')[1].split(',')[0].split('-')[0]
    pos = [item for item in nlpresult_pos if o in item]
    if 'jj' in pos[0].lower():
        components_dict['adj'] = o
    elif 'nn' in pos[0].lower():
        components_dict['obj'] = o
    elif 'nns' in pos[0].lower():
        components_dict['obj'] = o
    elif 'cd' in pos[0].lower():
        components_dict['obj'] = o
    
    
if list(filter(r_subjpass.match, nlpresult_parse)) != [] and list(filter(r_auxpass.match, nlpresult_parse)) != []:
    structures_templates.append("structure(5,2)")
    result1 = list(filter(r_subjpass.match, nlpresult_parse))
    result2 = list(filter(r_auxpass.match, nlpresult_parse))
    structures.append(result1 + result2)
    verb = result1[0].split('(')[1].split(',')[0].split('-')[0]
    subj = result1[0].split('(')[1].split(',')[1].split('-')[0][1:]
    components_dict['verb'] = verb
    components_dict['subj'] = subj

print("List of structures of a sentence: ", structures)
print("List of structure templates of a sentence: ", structures_templates)

sentence_structure = structures[-1]
sentence_template = structures_templates[-1]
print("Selected structure for this sentence is: ", sentence_structure)
print("Selected template for this sentence is: ", sentence_template)

print("Components of the sentence: ", components_dict)


## complement components recognition
r_compound = re.compile("compound.*")
r_adjmod = re.compile("amod.*")
r_conjunction= re.compile("conj.*")
r_nmod = re.compile("nmod.*")
r_case = re.compile("comp.*")
r_advmod = re.compile("advmod.*")

potential_components = []
for i in nlpresult_parse:
    item = [i]
    if list(filter(r_compound.match, item)) != []:
        potential_components.append(list(filter(r_compound.match, item)))

    
    if list(filter(r_adjmod.match, item)) != []:
        potential_components.append(list(filter(r_adjmod.match, item)))

    
    if list(filter(r_conjunction.match, item)) != []:
        potential_components.append(list(filter(r_conjunction.match, item)))

    
    if list(filter(r_nmod.match, item)) != [] and list(filter(r_case.match, item)) != []:    
        potential_components.append(list(filter(r_nmod.match, item)) + list(filter(r_case.match, item)))

    
    if list(filter(r_advmod.match, item)) != []:
        potential_components.append(list(filter(r_advmod.match, item)))

        

print("Potential components: ", potential_components)
print(components_dict)

complex_tokens = []
for p in potential_components:
    first = p[0].split('(')[1].split(',')[0].split('-')[0]
    if first not in complex_tokens:
        complex_tokens.append(first)
    second = p[0].split('(')[1].split(',')[1].split('-')[0][1:]
    if second not in complex_tokens:
        complex_tokens.append(second)
print("Complex tokens: ", complex_tokens)

if sentence_template == 'structure(1,1)':
    if components_dict['subj'] in complex_tokens:
        result = [item for item in potential_components if components_dict['subj'] in item]
        
    rep = components_dict['subj'] + ' ' + components_dict['verb']
    print("rep: " ,rep)

if sentence_template == 'structure(2,2)':
    if components_dict['obj'] in complex_tokens:
        result = [item for item in potential_components if components_dict['obj'] in item[0]]
        if list(filter(r_adjmod.match, nlpresult_parse)) != []:
            result1 = list(filter(r_adjmod.match, result))
            adj = result1[0].split('(')[1].split(',')[1].split('-')[0][1:]
        
        if list(filter(r_adjmod.match, nlpresult_parse)) != []:
            result1 = list(filter(r_adjmod.match, result))
            adj = result1[0].split('(')[1].split(',')[1].split('-')[0][1:]
    
    
    rep = components_dict['subj'] + ' ' + components_dict['verb'] + ' ' + components_dict['obj']
    print("rep: " ,rep)
    
if sentence_template == 'structure(3,3)':
    rep = components_dict['subj'] + ' ' + components_dict['verb_1'] + ' ' + components_dict['verb_2'] + ' ' + components_dict['obj']
    print("rep: " ,rep)

if sentence_template == 'structure(4,2)':
    if components_dict['adj'] != []:
        rep = components_dict['subj'] + ' ' + components_dict['adj'] 
    else:
        rep = components_dict['subj'] + ' ' + components_dict['obj']
    print("rep: " ,rep)

if sentence_template == 'structure(5,2)':
    rep = components_dict['subj'] + ' ' + components_dict['verb']
    print("rep: " ,rep)
        


