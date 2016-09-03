Contact: [Wei Xu](web.cse.ohio-state.edu/~weixu/) (Ohio State University)


Code, data and trained models from the following paper:

     "Optimizing Statistical Machine Translation for Text Simplification"
     Wei Xu, Courtney Napoles, Ellie Pavlick, Quanze Chen and Chris Callison-Burch
     In Transactions of the Association for Computational Linguistics (TACL) 2015

### Data 

**./data/turkcorpus/**     tuning and test data 

    *.norm       tokenized sentences from English Wikipedia

    *.simp       tokenized, corresponding sentences from Simple English Wikipedia

    *.turk.0~7   8 reference simplifications by 8 different Amazon Mechanical Turkers 
    
**./data/systemoutputs/**  4 different system outputs compared in the paper

### Code 

**./SARI.py**   a Python implementation of the SARI metric for text simplification evaluation

There is also a [Java implementation of SARI](https://github.com/apache/incubator-joshua/blob/master/src/main/java/org/apache/joshua/metrics/SARI.java) in the Joshua codebase. 

### The Text Simplificaiton System 

The text simplification system in the paper was implemented in an earlier version of [Joshua Decoder](http://joshua.incubator.apache.org/). 

We are working on integrating our text simplification system into the upcoming release of Joshua. 
