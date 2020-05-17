from google.cloud import bigquery
import os


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/bensa/PycharmProjects/FootballAnalytics/utils/" \
                                               "football-basic-analysis-b33622003fb8.json"

query_all = """
        SELECT *
        FROM football-basic-analysis.football.players
        """


def get_data(query: str, client=bigquery.Client()):
    query_job = client.query(query)

    return query_job.to_dataframe()


