# Model Card

## Model Details

- **Model Name**: distilbert/distilbert-base-german-cased (https://huggingface.co/distilbert/distilbert-base-german-cased)
- **Tokenizer Name**: DistilBERT tokenizer (https://huggingface.co/distilbert/distilbert-base-german-cased)
- **Version**: 1.0
- **Date**: 2024-09-04
- **Type**: Classification

## Intended Use

- **Primary Use**: Classification of the customer emails to the Company X
- **Intended Users**: Business Analysts, who are responsible for customer service

## Dataset

- **Dataset**: Emails from customers to the Company X
- **Preprocessing**: 

    - **Deletion of greetings, signatures, and footers:**
        1. Save common greetings and signatures in a text file.
        2. Use regular expressions for initial removal.
        3. Train NER network ([https://huggingface.co/flair/ner-german](https://huggingface.co/flair/ner-german)) for advanced detection.
    
    - **Anonymization of personal data:**
        - Utilize NER network ([https://huggingface.co/flair/ner-german](https://huggingface.co/flair/ner-german)).
    
    - **Replacement of specific elements:**
        - Replace dates, numbers, and URLs with universal tokens (`<DATE>`, `<NUMBER>`, `<URL>`).
        - Implement using regular expressions.
    
    - **Character filtering:**
        - Remove all non-ASCII characters, preserving German umlauts.
    
    - **Tokenization:**
        - Convert text words/tokens to integers.
        - Rationale: Neural networks require integer inputs rather than raw text.


## Dataset Details

| Label                    | Count   |
|--------------------------|---------|
| Cancelation              | 171,568 |
| Service Inquiry          | 62,424  |
| Billing                  | 41,632  |
| Other                    | 22,482  |
| Change Payment type      | 18,533  |
| Dbt/collection request   | 5,504   |
| Business Inquiry         | 3,634   |
| Network and Hardware     | 3,221   |
| Contracts                | 778     |


## Training Data

| Label                    | Count   |
|--------------------------|---------|
| Cancelation              | 137,254 |
| Service Inquiry          | 49,939  |
| Billing                  | 33,306  |
| Other                    | 17,986  |
| Change Payment type      | 14,826  |
| Dbt/collection request   | 4,403   |
| Business Inquiry         | 2,907   |
| Network and Hardware     | 2,577   |
| Contracts                | 622     |

## Evaluation Data

| Label                    | Count   |
|--------------------------|---------|
| Cancelation              | 34,314  |
| Service Inquiry          | 12,485  |
| Billing                  | 8,326   |
| Other                    | 4,496   |
| Change Payment type      | 3,707   |
| Dbt/collection request   | 1,101   |
| Business Inquiry         | 727     |
| Network and Hardware     | 644     |
| Contracts                | 156     |


## Metrics
- Log loss
- F1-score (macro average, because each class is equally important)
- Precision
- Recall


## Results

| Label                    | Precision | Recall | F1-Score | Support |
|--------------------------|-----------|--------|----------|---------|
| Change Payment type      | 0.92      | 0.93   | 0.93     | 3707    |
| Billing                  | 0.73      | 0.86   | 0.79     | 8326    |
| Dbt/collection request   | 0.47      | 0.44   | 0.45     | 1101    |
| Cancelation              | 0.93      | 0.98   | 0.96     | 34314   |
| Contracts                | 0.65      | 0.38   | 0.48     | 156     |
| Business Inquiry         | 0.63      | 0.19   | 0.29     | 727     |
| Service Inquiry          | 0.76      | 0.74   | 0.75     | 12485   |
| Other                    | 0.69      | 0.36   | 0.47     | 4496    |
| Network and Hardware     | 0.61      | 0.65   | 0.63     | 644     |
|--------------------------|-----------|--------|----------|---------|
| Accuracy                 |           |        | 0.85     | 65956   |
| Macro Avg                | 0.71      | 0.61   | 0.64     | 65956   |
| Weighted Avg             | 0.84      | 0.85   | 0.84     | 65956   |



## Additional Information

- **Wandb Report**: https://wandb.ai/daniil-yefimov/my_already_deleted_report
- **Contact**: Daniil Yefimov <daniil.yefimov92@gmail.com>