import factory
from faker import Faker
from app9 import Dataset, Row

fake = Faker()

# Define a factory class to generate instances of the Row data class
class RowFactory(factory.Factory):
    class Meta:
        model = Row

    # Define the fields of the Row data class and how they should be generated
    id = factory.Sequence(lambda n: n)
    date = factory.LazyFunction(
        lambda: fake.date_between(start_date="-5y", end_date="today")
    )
    target = factory.Faker("name")
    insult = factory.Faker("word")
    tweet = factory.Faker("text")


# Test function to verify the behavior of the average_tweet_length method
def test_average_tweet_length():
    # Generate a list of 10 Row objects using the RowFactory
    rows = RowFactory.build_batch(10)
    # Create a Dataset object from the list of rows
    dataset = Dataset(rows)
    expected_average = sum(len(row.tweet) for row in rows) / len(rows)
    assert dataset.average_tweet_length() == expected_average


def test_count_insults():
    # Generate a list of 3 Row objects with specific insult values
    rows = [RowFactory(insult="yes"), RowFactory(insult="no"), RowFactory(insult="yes")]
    dataset = Dataset(rows)
    assert dataset.count_insults() == 3


def test_count_tweets_per_target():
    rows = [RowFactory(target="A"), RowFactory(target="B"), RowFactory(target="A")]
    dataset = Dataset(rows)
    assert dataset.count_tweets_per_target() == {"A": 2, "B": 1}


def test_average_tweet_length_per_insult():
    rows = [
        RowFactory(insult="yes", tweet="12345"),
        RowFactory(insult="no", tweet="123"),
        RowFactory(insult="yes", tweet="1234567"),
    ]
    dataset = Dataset(rows)
    # Calculate the expected result
    expected_result = {"yes": (5 + 7) / 2, "no": 3}
    assert dataset.average_tweet_length_per_insult() == expected_result


def test_summarize():
    rows = [
        RowFactory(target="A", insult="yes"),
        RowFactory(target="B", insult="no"),
        RowFactory(target="A", insult="yes"),
    ]
    dataset = Dataset(rows)
    # Call the summarize method to get summary statistics for the dataset
    summary = dataset.summarize()
    # Assert that each summary statistic has the expected value
    assert summary["total_tweets"] == 3
    assert summary["total_targets"] == 2
    assert summary["total_insults"] == 2