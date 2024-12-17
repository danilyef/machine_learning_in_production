# Homework 4: Versioning and labeling

## Tasks:

- PR1: Commit your data with DVC into the GitHub repo.
- PR2: Write code to deploy a labeling tool (e.g., Label Studio, Argilla), including README instructions.
- PR3: Write code to generate a synthetic dataset with ChatGPT.
- PR4: Write code to test your data after labeling (can use Cleanlab or Deepchecks)


### PR1: example

```bash
# Add the dataset to DVC tracking
dvc add data/dataset.parquet

# Commit the .gitignore and .dvc files
git add data/.gitignore data/dataset.parquet.dvc
git commit -m "Add dataset.parquet to DVC tracking"

# Push the data to remote storage
dvc push
```

### PR2: Instructions

You have a text in german language. These are emails to sent the Telecommunication company X, which must be categorized into the following categories:

**Annotation Instructions:**

- Bussines inquiry: everything that is related to the business of the company from company X business partners.
- Collection request: everything that is related to the collection of the debt for company X from privat clients. Could be proof pf payment or emails about
reopening closed accounts.
- Service request: everything that is related to the service of the company X.
- Cancelation: everything that is related to the cancelation of the service (contract termination, order cancellation etc.) of the company X. 
- Billing: everything that is related to the billing problems. Explanationf of the bill, sending copie of the bill, 
dispute a bill etc.
- Technical issue: everything that is related to the technical issues (Networking problems ,internet problems, website problems, etc.) of the company X.
- Payment method: everything that is related to the changes in the payment methods of the clients.
- Documents: inquiry about sendings copies of the contracts to clients.
- Other: everything that is not related to the above categories, including spam.


**General Annotation Guidelines:**

- Read the entire email carefully before categorizing.
- Choose only one category per email.
- If an email could fit multiple categories, select the most prominent or primary issue addressed.
- Pay attention to key phrases and context clues that indicate the email's purpose.
- If unsure, use the "Other" category.
- Be consistent in your categorization approach across all emails.
- If you encounter recurring themes that don't fit the existing categories, make a note for potential future category additions.
- Ignore salutations, signatures, and other non-content elements when determining the category.
- Consider the sender's intent and the main action they're requesting or information they're seeking.

### PR4: results

**Duplicate Issues**

- Cleanlab identified 6 duplicate issues in our dataset.
- All of them belong to category 4 or category 8.

**Label Issues**

- Cleanlab identified 4 label issues in our dataset.
- they all have score below 0.20 (which is quite low)
- Mislabeled emails belong to category 4 or category 2.
- Detailed analysis of label issues can be found in `label_issues_scores.csv` and `label_issues.csv`

**Outlier Issues**

- Cleanlab identified 1 outlier issue in our dataset.
- It belongs to category 1 and has a score lower than 0.20.
- Detailed analysis of outlier issues can be found in `outlier_issues_scores.csv` and `outlier_issues.csv`