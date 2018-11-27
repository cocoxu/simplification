Contact: [Wei Xu](http://web.cse.ohio-state.edu/~weixu/) (Ohio State University)


Code, data and trained models from the following paper:

     @article{Xu-EtAl:2016:TACL,
     author = {Wei Xu and Courtney Napoles and Ellie Pavlick and Quanze Chen and Chris Callison-Burch},
     title = {Optimizing Statistical Machine Translation for Text Simplification},
     journal = {Transactions of the Association for Computational Linguistics},
     volume = {4},
     year = {2016},
     url = {https://cocoxu.github.io/publications/tacl2016-smt-simplification.pdf},
     pages = {401--415}
     }

### Data 
**./tacl2016-smt-simplification.pdf**    the paper

**./data/turkcorpus/**     tuning and test data 

    *.norm       tokenized sentences from English Wikipedia

    *.simp       tokenized, corresponding sentences from Simple English Wikipedia

    *.turk.0~7   8 reference simplifications by 8 different Amazon Mechanical Turkers 
    
**./data/systemoutputs/**  4 different system outputs compared in the paper

**./data/ppdb/ppdb-1.0-xl-all-simp.gz** (a 3.8G [file](http://www.cis.upenn.edu/~xwe/files/ppdb-1.0-xl-all-simp.gz))  paraphrase rules (PPDB 1.0) with added simplification-specific features 

**./data/ppdb/ppdb-1.0-xxxl-lexical-self-simp.gz** (a 27M [file](http://www.cis.upenn.edu/~xwe/files/ppdb-1.0-xxxl-lexical-self-simp.gz)) self-paraphrase lexical rules that map words to themselves, and help to copy input words into outputs

### Code 

**./SARI.py**   a stand-alone Python implementation of the SARI metric for text simplification evaluation

There is also a [Java implementation of SARI](https://github.com/apache/incubator-joshua/blob/master/src/main/java/org/apache/joshua/metrics/SARI.java) that is integrated as part of the Joshua's codebase. 

### Human Evaluation and Data Collection (Crowdsouring User Interface Design)

**./HIT_MTurk_crowdsourcing**  HTML interfaces designed for human evaluation of simplification systems, as well as parallel corpus collection (originally used on Amazon Mechnical Turk HITs)

### The Text Simplificaiton System 

The text simplification system was implemented into the MT toolkit [Joshua Decoder](http://joshua.incubator.apache.org/). 

**./ppdb-simplification-release-joshua5.0.zip** (a 281M [file](https://drive.google.com/file/d/0B1P1xW5xNISsdXdoX1RQNmVSSkE/view?usp=sharing)) The experiments in our TACL 2016 paper used the Joshua 5.0. Example scripts for training the simplification are under the directory **./bin/**. Note that **STAR is corpus-level version of SARI, SARI is sentence-level**. The **joshua_TACL2016.config** is also provided -- that is corresponding to the best system in our paper. You may find the [Joshua pipeline tutorial](http://joshua.incubator.apache.org/5.0/tutorial.html) useful.




