# Resume Ranking WebApp

## Overview

A Resume ranking system based on comparing the JD with the text provided in the Resumes.

## Features

### Skills Fit Analysis:
- Literal comparison of the whole document with the JD.
- Generates scores based on the similarity of documents with JD.

### MultiModal Approach:
- Three NLP models are available to choose from:
  - TF/IDF
  - Doc2Vec
  - BERT

## Model Comparison

| Component               | TF/IDF                               | Doc2Vec                            | BERT                                 |
|-------------------------|--------------------------------------|------------------------------------|--------------------------------------|
| **Algorithm Type**      | Statistical                          | Neural Network                     | Transformer                          |
| **Training Data Requirements** | Low                           | Moderate                           | High                                 |
| **Accuracy**            | Moderate                             | High                               | Very High                            |
| **Computation Time**    | Low                                  | Moderate                           | High                                 |


https://github.com/user-attachments/assets/db7736ca-22bb-453a-a9ba-2f008006290d


## **Getting Started**

Follow these steps to get the Resume Ranking System up and running:

- Clone the Repository:

`git clone https://github.com/arbaazali872/resume_rank.git`

- Create and activate a virtual environment


Windows:

`python -m venv env`

`env\Scripts\activate`


Linux:

`sudo apt install python3-venv`

`python3 -m venv env`

`source env/bin/activate`


- Go to the main repository

`cd resume_ranking`

- Make the required changes in the .env file based on your PostgreSql credentials.

- Run the command:

`docker-compose -f docker-compose.yml --env-file .env  up --build`
