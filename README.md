## Wino-Knowledge-Hunter (FOR FREE :star::smile_cat::star: !)

This repository provides a pipeline for Emami et al. (2018) for free without legal issues.

:warning: N.B.
 
1. This is not a complete replicate, but provides a full pipeline that uses (free-of-charge) search API so that everyone can try.

2. I tried to keep the original code (by Emami) as much as possible in order to make sure that the code works similarly to the original work. I am happy to answer questions, but you might want to ask the original authors first.


## Citation

If you use this repository, please cite the following papers.


## Procedure:
:warning: tested only on Python 2. Install pre-requisite modules by `pip install -r requirements.txt`.

1. (preprocessing) Run Stanford core nlp to parse the WSC sentences.

        $ mkdir winogradPlain (winoGrandeDevPlain)
        $ python extract_wsc_sentence.py > winograd_plain.txt
        $ wget http://nlp.stanford.edu/software/stanford-corenlp-full-2018-10-05.zip
        $ unzip ./stanford-corenlp-full-2018-10-05
        
    Now, set a path to ./stanford-corenlp-full-2018-10-05 in `parse_by_stanford.sh`, then.
        
        $ sh ./parse_by_stanford.sh

2. Run Query Generation Module

        (e.g.,)
        $ mkdir winoGrandeDevQuery
        $ python moduleQueryGenerator.py -m standard -i winogrande11DevXML -o winogrande11DevQuery

    Note: it supports only `standard` for now. (`synonym` isn't supported in this repo.)

3. Run (free) Knowledge Hunting Module

    Before running the script, you need an account (and API key) on [RapidAPI](https://rapidapi). Set your API key as an environment variable 
        
        $ export API_KEY_X_MASHAPE=YOUR-API-KEY

    and run
        
        $ python moduleKnowledgeHuntingForFree.py

    (not free option) If you have an account (and API key) for [Bing search](https://azure.microsoft.com/en-us/services/cognitive-services/bing-web-search-api/), you may also use it.
    
        $ export API_KEY_BING=YOUR-API-KEY
        $ python moduleKnowledgeHuntingForFree.py --api bing #(or --ensemble)

    (not free option) If you have an account for Google API, you may also use it. 

        $ export GOOGLE_DEVELOPER_KEY=YOUR-API-KEY
        $ export GOOGLE_CSE_KEY=YOUR-CSE-KEY
        (e.g.,)
        $ python moduleKnowledgeHuntingForFree.py -d winogrande11DevQuery --api google
    
    N.B. Bing and Google APIs are NOT free :moneybag::moneybag::moneybag::crying_cat_face: , but it MS provides a free trial with $200 credit (as of 2018/12).

4. Run Snippet Parsing Module 

        (e.g.,)
        $ python moduleSnippetParsing.py ./winoGrandeDevQuery

5. Run Antecedent Selection Module 

        (e.g.,)
        $ python moduleAntecedentSelection.py ./winoGrandeDevQuery

