'''
import click

@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for _ in range(count):
        click.echo('Hello, %s!' % name)

if __name__ == '__main__':
    hello()

'''

import click
from collections import Counter, defaultdict
from dataclasses import dataclass
import csv

# Define a data class to represent each row in the CSV file
@dataclass
class Row:
    id: str
    date: str
    target: str
    insult: str
    tweet: str


# Define a class to represent the dataset
class Dataset:
    def __init__(self, data):
        if isinstance(data, str):
            # Read the contents of the CSV file into a list of Row objects
            self.rows = []
            with open(data, newline="", encoding="utf-8") as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # skip header row
                for row in reader:
                    self.rows.append(Row(*row))
        elif isinstance(data, list):
            self.rows = data
        else:
            raise TypeError("data must be either a filename or a list of Row objects")

    def average_tweet_length(self) -> float:
        # Calculate the average length of tweets in the dataset
        total_length = sum(len(row.tweet) for row in self.rows)
        return total_length / len(self.rows)

    def count_insults(self) -> int:
        # Count the number of insults in the dataset
        return sum(1 for row in self.rows if row.insult)

    def count_tweets_per_target(self) -> Counter:
        # Count the number of tweets for each target in the dataset
        counter = Counter()
        for row in self.rows:
            counter[row.target] += 1
        return counter

    def average_tweet_length_per_insult(self) -> dict:
        # Calculate the average length of tweets for each insult in the dataset
        total_length = defaultdict(int)
        count = defaultdict(int)
        for row in self.rows:
            total_length[row.insult] += len(row.tweet)
            count[row.insult] += 1
        return {insult: total_length[insult] / count[insult] for insult in total_length}

    def summarize(self) -> dict:
        # Calculate summary statistics for the dataset
        summary = {
            "total_tweets": len(self.rows),
            "total_targets": len(set(row.target for row in self.rows)),
            "total_insults": len(set(row.insult for row in self.rows)),
            "average_tweet_length": self.average_tweet_length(),
        }
        return summary


@click.command()
@click.argument("filename", type=click.Path(exists=True))
@click.option(
    "--avg-tweet-len", is_flag=True, help="Calculate the average length of tweets"
)
@click.option("--count-insults", is_flag=True, help="Count the number of insults")
@click.option(
    "--count-tweets-per-target",
    is_flag=True,
    help="Count the number of tweets for each target",
)
@click.option(
    "--avg-tweet-len-per-insult",
    is_flag=True,
    help="Calculate the average length of tweets for each insult",
)
@click.option("--summarize", is_flag=True, help="Calculate summary statistics")
def main(
    filename,
    avg_tweet_len,
    count_insults,
    count_tweets_per_target,
    avg_tweet_len_per_insult,
    summarize,
):
    """Process a CSV dataset and generate a report"""
    # Create a Dataset object from the specified CSV file
    dataset = Dataset(filename)

    if avg_tweet_len:
        print(f"Average tweet length: {dataset.average_tweet_length()}")

    if count_insults:
        print(f"Number of insults: {dataset.count_insults()}")

    if count_tweets_per_target:
        print("\nNumber of tweets per target:")
        for target, count in dataset.count_tweets_per_target().items():
            print(f"{target}: {count}")

    if avg_tweet_len_per_insult:
        print("\nAverage tweet length per insult:")
        for insult, avg_length in dataset.average_tweet_length_per_insult().items():
            print(f"{insult}: {avg_length:.2f}")

    if summarize:
        print("\nSummary:")
        for stat, value in dataset.summarize().items():
            print(f"{stat}: {value}")


if __name__ == "__main__":
    main()
