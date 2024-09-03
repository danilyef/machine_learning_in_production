import argilla as rg
import pandas as pd

client = rg.Argilla(api_url="http://0.0.0.0:6900", api_key="admin.apikey")

'''
docker run -d --name argilla -p 6900:6900 argilla/argilla-quickstart:v2.0.0rc1
'''


def create_nlp_dataset():
    guidelines = """
    You have a text in german language. These are emails to sent the Telecommunication company X, which must be 
    categorized into the following categories:
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
    - Other: everything that is not related to the above categories.
    """

    dataset_name = "client_email_category"
    settings = rg.Settings(
        guidelines=guidelines,
        fields=[
            rg.TextField(
                name="email",
                title="Email",
                use_markdown=False,
            ),
        ],
        questions=[
            rg.TextQuestion(
                name="email_category",
                title="Client Emil anotation",
                description="Please anotate client email to the company X",
                required=True,
                use_markdown=False,
            )
        ],
    )
    dataset = rg.Dataset(
        name=dataset_name,
        workspace="admin",
        settings=settings,
        client=client,
    )
    dataset.create()

    dataset = client.datasets(name=dataset_name)
    data = pd.read_parquet('synthetic_reviews.parquet')
    records = []
    for idx, row in data.iterrows():
        x = rg.Record(
            fields={
                "email": row["Email"],
            },
        )
        records.append(x)

    dataset.records.log(records, batch_size=100)


if __name__ == "__main__":
    create_nlp_dataset()