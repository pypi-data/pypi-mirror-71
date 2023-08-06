# BIDS_Terms


## Project Description 

<p align="center">
  <img width="300" height="300" src="https://github.com/nqueder/bids_terms_to_pdf_table/blob/master/img/BIDS-TERMS.png">
</p>






In this project we aim to create a user friendly python tool for creating and exporting BIDS specification terms in PDF form tables for incorporation into the BIDS specification documents. This project is a part of the effort of the [NIDM-Terms project](https://scicrunch.org/nidm-terms/about/project) allowing the the BIDS working group to select amongst our curated [BIDS terms](https://github.com/NIDM-Terms/terms/tree/master/terms/BIDS_Terms) , search our information resource “[Interlex](https://scicrunch.org/nidm-terms)” for existing BIDS terms, or add a new BIDS term, which will constantly result in term dictionary in JSON-LD form added to our family of [BIDS Specification terms](https://github.com/NIDM-Terms/terms/tree/master/terms/BIDS_Terms). The user will be able to select which [properties](https://github.com/nqueder/terms/tree/patch-2/terms) he/she would like to include in the table (e.g. description, label, comment, etc..). The user will then have a PDF table of the chosen/added terms and their properties as an output. Such an effort will provide the BIDS working group with a user-friendly tool to build tables for the BIDS documentation while ensuring they have not re-purposed an existing BIDS specification term giving it conflicting definitions.  




### Purpose and Goals of The Project:

* Provide the BIDS community with a tool to create PDF tables for their BIDS specification documents.
* Create well structured and clear instructions on how to use our tool.
* Facilitate community engagement through adding missing BIDS specification terms for further use to enhance our ability to search across brain Initiative datasets.
* Create JSON-LD file for new [terms](https://github.com/NIDM-Terms/terms/tree/master/terms/BIDS_Terms).
* Create an automated way to push newly created JSON-LD files to the Interlex information resource (see: https://scicrunch.org/nidm-terms).


<p align="center">
  <img width="724" height="412" src="https://github.com/nqueder/bids_terms_to_pdf_table/blob/master/img/SampleTable.png">
</p>

#### Story board:

![](img/StoryBoard.png)

### Interlex API Key:

To be able to search and query BIDS terms in Interlex, an Interlex account and an API key are required. Here’s how you can obtain one:
* Create a [Scicrunch](https://scicrunch.org/nidm-terms) account if don’t have one already
* Once your account is all set, go to MY ACCOUNT in the top right corner and click on API Keys
* Enter your password
* Click on “Generate an API key” and under key you will have your new API key!



### Related readings and links:
* Our NIDM-Terms website (https://scicrunch.org/nidm-terms)
* Our NIDM-terms github repository (https://github.com/NIDM-Terms/terms)
* For additional information on the background for this project see BIDS specification issue 423 (https://github.com/bids-standard/bids-specification/issues/423)


# Install

* conda create -n pynidm_py3 python=3
* source activate pynidm_py3
* cd bids_term_to_pdf_table
* python setup.py install

# Running the script

* bids_term_to_table -in [PATH TO bids_term_to_pdf_table cloned repo] -out [OUTPUT DIRECTORY]

