# Winograd Schema Challenge Knowledge Hunting Module
# AUTHOR: Ali Emami

# Idea: 

Our  method  works  by  (i)  generating  queries  from  a  parsed  representation
of  a  Winograd  question,  (ii)  acquiring  rele- vant  knowledge  using  Information  Retrieval, and (iii) reasoning on the gathered knowledge.

# Procedure:

(i) Query Generation Module -- `moduleQueryGenerator.py`. Must be run using flags indicating query generation method ("standard" or "synonym", as in, through the command prompt:
Usage:
   #+BEGIN_SRC shell
   $ python moduleComponentExtractor.py {model} 
   #+END_SRC
   where `model` is the the type of model, either =standard= or =synonym=. It produces the set C, the set Q, and the set containing the first entities for the 273 Winograd Sentences by using the parsed CoreNLP representation of the Winograd sentences and various linguistic rules.

(ii) Knowledge Hunting Module -- Using the queries generated by the previous module, you may scrape whichever corpus/search engine for the evidence sentences. We omit this process for legal reasons. 

(iii) Antecedent Selection Module -- `moduleAntecedentSelection.py`. Must be run using flags indicating query generation method ("standard" or "synonym", as in, through the command prompt: "python moduleAntecedentSelection.py standard". It takes the information produced by the previous module and weighs each sentence retrieved for each Winograd sentence and scores them in order to make a coreference decision, in both the traditional and relaxed Winograd setting. The module prints out results for each of the settings in terms of P, R and F1. Since we do not provide the scraped sentences, this module relies on the existence of the scraped sentences and these must be provided.

# Results:

AGQ:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 77
Precision: 0.56
Recall: 0.28
F1: 0.38


AGQS:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 114
Precision: 0.57
Recall: 0.42
F1: 0.48


MGQ:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 118
Precision: 0.60
Recall: 0.43
F1: 0.50

