# Document Design: Email classification of the clients

---
## 1. Overview

**Problem**: Telecomunication Company X recieves approximately 5k emails per day from their clients about different topics. The current solution of the classification of these emails is to outsource this task to the company Y, which manually classifies emails into 10 categories (Categories are specified  by the business department of the company X). There are 3 main problem in this solution:

- It is expensive: company X must pay $$$ amount of money to the company Y
- Classification is slow: people are quite slow in the task like classification of the email, so it can take a week of time what could be done in an hour by algorithm/machine.
- Classification quality: people can deliver suboptimal results in text classification (especially compared to classification of images) due to the lack of concentration or not knowing specifics of the telecommunication business.

**Solution**: replacement of the manually classification of the emails my ML algorithm

**Desired outcome**: iterative progress due to the contract with company Y.
- First go live/deployment of the classifier must replace 20% of the manually classified emails.
- Second deployment of the classifier (in half a year) must replace 40% of the manually classified emails.
- Final goal: to replace 70% of the manually classified emails.

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
- Cost reduction: saving 300000 euro per year (according to the estimation of the business department of the company X)

## 4. Requirements & Constraints
Functional requirements are those that should be met to ship the project. They should be described in terms of the customer perspective and benefit. (See [this](https://eugeneyan.com/writing/ml-design-docs/#the-why-and-what-of-design-docs) for more details.)

Non-functional/technical requirements are those that define system quality and how the system should be implemented. These include performance (throughput, latency, error rates), cost (infra cost, ops effort), security, data privacy, etc.

Constraints can come in the form of non-functional requirements (e.g., cost below $`x` a month, p99 latency < `y`ms)

**Functional requirements:**
- In the first iteration 20% of the incomming emails per year have prediction confidence 90% or more.
- Final requirement: 70% of the incoming emails per year have prediction confidence 90% or more.
- Extraction of the client number id from the email, if provided.
- Extraction of the client number phone number, if provided
  
**Technical requirements**
- Personal data of the clients (name, surname, email adress etc.) must be anonymized.
- Latency: 5 seconds per request.
- Open Source only.

### 4.1 What's in-scope & out-of-scope?

**In-scope**
- Analysis of the client emails, which have .eml format

**Out-of-scope**
- Additional analysis of attached files like pdf, jpg, which can help in the prediction of the email. Will be implemented in the future version.

## 5. Methodology

### 5.1. Problem statement

This is a classical supervised classification problem, where subject combined with text of the email is an input label (transformed into integer tokens) and category number is an output label (from 1 to 10) 

### 5.2. Data

What data will you use to train your model? What input data is needed during serving?
**Training data**:
- Labeled emails by the outsource company Y.

**Input data**
- Client emails in the .eml format. 

### 5.3. Techniques

What machine learning techniques will you use? How will you clean and prepare the data (e.g., excluding outliers) and create features?

### 5.4. Experimentation & Validation

How will you validate your approach offline? What offline evaluation metrics will you use?

If you're A/B testing, how will you assign treatment and control (e.g., customer vs. session-based) and what metrics will you measure? What are the success and [guardrail](https://medium.com/airbnb-engineering/designing-experimentation-guardrails-ed6a976ec669) metrics?

### 5.5. Human-in-the-loop

How will you incorporate human intervention into your ML system (e.g., product/customer exclusion lists)?

## 6. Implementation

### 6.1. High-level design

![](https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/Data-flow-diagram-example.svg/1280px-Data-flow-diagram-example.svg.png)

Start by providing a big-picture view. [System-context diagrams](https://en.wikipedia.org/wiki/System_context_diagram) and [data-flow diagrams](https://en.wikipedia.org/wiki/Data-flow_diagram) work well.

### 6.2. Infra

How will you host your system? On-premise, cloud, or hybrid? This will define the rest of this section

### 6.3. Performance (Throughput, Latency)

How will your system meet the throughput and latency requirements? Will it scale vertically or horizontally?

### 6.4. Security

How will your system/application authenticate users and incoming requests? If it's publicly accessible, will it be behind a firewall?

### 6.5. Data privacy

How will you ensure the privacy of customer data? Will your system be compliant with data retention and deletion policies (e.g., [GDPR](https://gdpr.eu/what-is-gdpr/))?

### 6.6. Monitoring & Alarms

How will you log events in your system? What metrics will you monitor and how? Will you have alarms if a metric breaches a threshold or something else goes wrong?

### 6.7. Cost
How much will it cost to build and operate your system? Share estimated monthly costs (e.g., EC2 instances, Lambda, etc.)

### 6.8. Integration points

How will your system integrate with upstream data and downstream users?

### 6.9. Risks & Uncertainties

Risks are the known unknowns; uncertainties are the unknown unknows. What worries you and you would like others to review?

## 7. Appendix

### 7.1. Alternatives

What alternatives did you consider and exclude? List pros and cons of each alternative and the rationale for your decision.

### 7.2. Experiment Results

Share any results of offline experiments that you conducted.

### 7.3. Performance benchmarks

Share any performance benchmarks you ran (e.g., throughput vs. latency vs. instance size/count).

### 7.4. Milestones & Timeline

What are the key milestones for this system and the estimated timeline?

### 7.5. Glossary

Define and link to business or technical terms.

### 7.6. References

Add references that you might have consulted for your methodology.
