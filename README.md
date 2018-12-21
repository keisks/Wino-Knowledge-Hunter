## Wino-Knowledge-Hunter (FOR FREE :star::smile_cat::star: !)

I provide a full pipeline for Emami et al. (2018) for free, since the original repo does not provide all the modules due to legal issues etc. 

:warning: N.B.
 
1. This is not a complete replicate. Although this may be an inferior version, I provide a full pipeline that uses free-of-charge search API so that everyone can try.

2. I tried to keep the original code (by Emami) as much as possible in order to make sure that the code works similarly to the original work. I am happy to answer questions, but you might want to ask the original author as well.


## Citation

If you use this repository, please cite the following papers.



## Procedure:
:warning: tested only on Python 2

1. (preprocessing) Run Stanford core nlp to parse the WSC sentences.

        $ mkdir winogradPlain
        $ python extract_wsc_sentence.py > winograd_plain.txt
        $ wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
        $ unzip ./stanford-corenlp-full-2018-10-05
        
    Now, set a path to ./stanford-corenlp-full-2018-10-05 in `parse_by_stanford.sh`, then.
        
        $ sh ./parse_by_stanford.sh

    This is currently very inefficient. It will take a while. 

2. Run Query Generation Module

        $ python moduleQueryGenerator.py standard

    Note: it supports only `standard` for now. (`synonym` isn't supported in this repo.)

3. Run (free) Knowledge Hunting Module

    Before running the script, you need an account (and API key) on [RapidAPI](https://rapidapi). Set your API key as an environment variable 
        
        $ export API_KEY_X_MASHAPE=YOUR-API-KEY

    and run
        
        $ python moduleKnowledgeHuntingForFree.py

    (option) If you have an account (and API key) for [Bing search](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/), you may also use it.
    
        $ export API_KEY_BING=YOUR-API-KEY
        $ python moduleKnowledgeHuntingForFree.py --bing (or --ensemble)
    
    N.B. Bing API is NOT free :moneybag::moneybag::moneybag::crying_cat_face: .


4. Run Antecedent Selection Module 

        $ python moduleAntecedentSelection.py standard

## Results:

AGQ:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 77
Precision: 0.56
Recall: 0.28
F1: 0.38

AGQ+F:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 80
Precision: 0.63
Recall: 0.29
F1:0.40

AGQS:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 114
Precision: 0.57
Recall: 0.42
F1: 0.48

AGQS+F
Traditional Setting Performance, no class restrictions: 
Number of Correct: 119
Precision:0.60
Recall:0.44
F1:0.51

MGQ:
Traditional Setting Performance, no class restrictions: 
Number of Correct: 118
Precision: 0.60
Recall: 0.43
F1: 0.50

