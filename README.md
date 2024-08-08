# Document Design: Email classification of the clients

---
## 1. Overview

**Problem**: Telecomunication Company X recieves approximately 5k emails per day from their clients about different topics. The current solution of the classification of these emails is to outsource this task to the company Y, which manually classifies emails into 9 categories (Categories are specified  by the business department of the company X). There are 3 main problem in this solution:

- It is expensive: company X must pay $$$ amount of money to the company Y.
- Classification is slow: people are quite slow in the task like classification of the email, so it can take a week of time what could be done in an hour by algorithm/machine.
- Classification quality: people can deliver suboptimal results in text classification (especially compared to classification of images) due to the lack of concentration or not knowing specifics of the telecommunication business.

**Solution**: replacement of the manually classification of the emails my ML algorithm.

**Desired outcome**: iterative progress due to the contract with company Y.
- First go live/deployment of the classifier must replace 20% of the manually classified emails.
- Second deployment of the classifier (in half a year) must replace 40% of the manually classified emails.
- Final goal: to replace at least 70% of the manually classified emails.

## 2. Motivation

**Benifits of the Solution**
- Reducing dependancy from the outsource company: we will be in charge of the classification process and its improvement.
- Cuting expanses: infracstructure set up will bee much cheaper than paying $$$ amount of money to the external party.
- Improving classification quality: ML algorithms are more robust in email classification than human beings.
- Improving classification speed: ML algorithms are much faster in email classification than human beings.

**Urgency and Impact**
- Due to the difficult economical situation in the world, it's improtant to act now in order to cut expanses and dependencies from the outsource companies.
- Reduction the gap between technological status of the company and state-of-the-art approaches will benefit company X right now and in the future.

## 3. Success metrics
- Cost reduction: saving 300000 euro per year (according to the estimation of the business department of the company X).

## 4. Requirements & Constraints

**Functional requirements:**
- In the first iteration 20% of the incomming emails per year have prediction confidence 90% or more.
- Final requirement: 70% of the incoming emails per year have prediction confidence 90% or more.
- Extraction of the client number id from the email, if provided.
- Extraction of the client number phone number, if provided.
- Saving classification results in database for futher usage.
  
**Technical requirements**
- Personal data of the clients (name, surname, email adress etc.) must be anonymized.
- Latency: 5 seconds per request.
- 1 email at time.
- Open Source only.

### 4.1 What's in-scope & out-of-scope?

**In-scope**
- Analysis of the client emails, which have .eml format

**Out-of-scope**
- Additional analysis of attached files like pdf, jpg, which can help in the prediction of the email. Will be implemented in the future version.

## 5. Methodology

### 5.1. Problem statement

This is a classical supervised classification problem, where subject combined with text of the email is an input label (transformed into integer tokens) and category number is an output label (from 0 to 8).

### 5.2. Data

**Training data**:
- Labeled emails by the outsource company Y.

**Input data**
- Client emails in the .eml format. 

### 5.3. Techniques

**Machine Learning technique**
- For the email classification we will start witt the BERT architecture, but distill one (https://huggingface.co/distilbert/distilbert-base-german-cased)

**Preprocessing**
- Deletion of the greetings, signatures and footers of the email.
- Anonymization of the personal data.
- Replacing dates, numbers, urls by the coressponding universal tokens (<DATE>, <NUMBER>, <URL>)
- Deletion all non-ascii characters except german umlauts.
- Tokinization of the text into the integer tokens.


### 5.4. Experimentation & Validation

**Dataset Strategy**

The whole dataset will be splitted into the 3 parts:
- Training dataset: will be used for the model training.
- Validation dataset: will be used for the hyperparameter tuning.
- Test dataset: will be used for the final prediction result estimation.

During the dataset split we will use stratified approach: each dataset contains approximately the same percentage of samples of each target class as the complete set. This will help us to maintain representativeness of among all 3 datasets.

**Technical Metric**
In our case prediction all 9 categories are equally important. That's why we will use f1-score macro average: calculate metrics for each label, and find their unweighted mean. 

**Additional Remarks**
The data among 9 categories are imbalanced (the biggest category contains 300k records, the smallest 1k records) which may lead ML model to become more biased towards the majority class. There is a big debate in ML and Statistical analysis community regarding Resampling like SMOTE (https://stats.stackexchange.com/questions/321970/imbalanced-data-smote-and-feature-selection), so for now we will use existing dataset without artificially generation of the new samples.

There is a modern-day approach of using LLMs for the email generation, but it's still questionable if we should use it for our task, because it will change the training distribution of the data (approximation of the real world emails distribution). That could lead to unknown consequences. This approach must be studied additionally in depth.

### 5.5. Human-in-the-loop

All prediction, with the confidence lower than 90% will be additionally checked by the trained specialist.

## 6. Implementation

### 6.1. High-level design

```mermaid
graph TD;
    A[External System] -->|Sends .eml file| B[Text Preprocessing];
    B -->|Preprocessed text| C[ML Model];
    C -->|Classification results| D[Web App];
    D -->|JSON Response| E[External System];

    subgraph Docker Containers
        B
        C
        D
    end

    D --> F{JSON Fields};
    F --> G[Predicted Category];
    F --> H[Probability of Predicted Category];
    F --> I[Client ID];
    F --> J[Client Phone Number];

```


### 6.2. Infra
- Service will be hosted on premise.
- CPU only.
- **Technology**: 3 Docker Containers (ML Prediction, Text Cleaning, Web App) combined together by docker-compose yaml file.
- **Storage**: Jfrog Artifactory.

### 6.3. Performance (Throughput, Latency)

How will your system meet the throughput and latency requirements? Will it scale vertically or horizontally?
- **Throughput**: Staheholders requirement is to process 1 email at time (bo batch processing).
- **Latency:** there is no hard requirements, it should be reasonable (5 seconds per email).
- **Scaling:** if needed, we will start with vertical scaling.

### 6.4. Security

- We will provide our email classification service as an API, allowing seamless integration. The system responsible for retrieving emails will call this API to classify emails.
- 
- Additional Firewall rules.

### 6.5. Data privacy

Sensetive data will be masked by special tokens (Example: Khreschatyk 1, Kyiv will be marked as <LOCATION>) by the Neural Network (https://huggingface.co/flair/ner-german), spacy NER recognitions (english and german) and regex.

### 6.6. Monitoring & Alarms

- **Event logs**: Every classified record will be saved into the oracle database.
- **Monitoring**: Docker health check will be implemented for each container. If one of the containers will fail, notification will be send to the developer group. Grafana for monitoring
  
### 6.7. Integration points

How will your system integrate with upstream data and downstream users?

### 6.8. Risks & Uncertainties

- Not all sensetive data might be covered.
- Clients (id) could be wrong identified or not identidied at all.


