****Resume Ranking WebApp****


**Overview**
A Resume ranking system based on comparing the JD with the text provided in the Resumes.

**Features**
Skills Fit Analysis:
-  Literal Comparison of the whole document with the JD.
-  Generates scores based on the similarity of documents with JD.
MultiModal Approach:
-  Three NLP model are available to choose from.
    - TF/IDF
    - Doc2Vec
    - BERT

**Getting Started**

Follow these steps to get the Resume Ranking System up and running:

Clone the Repository:

`git clone https://github.com/arbaazali872/resume_rank.git`

`cd resume_ranking`

Make the required changes in the .env file based on your PostgreSql credentials.

Run the command:

`docker-compose -f docker-compose.yml --env-file .env  up --build`
