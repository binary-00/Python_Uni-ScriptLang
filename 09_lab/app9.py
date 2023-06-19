import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from openpyxl import Workbook
from typing import List

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

    def write_to_xlsx(self, filename: str):
        # Write the data to an XLSX file using the openpyxl library
        wb = Workbook()
        ws = wb.active

        # Write the header row
        ws.append(["ID", "Date", "Target", "Insult", "Tweet"])

        # Write the data rows
        for row in self.rows:
            ws.append([row.id, row.date, row.target, row.insult, row.tweet])

        # Save the workbook to the specified file
        wb.save(filename)


if __name__ == "__main__":
    # Define a command-line interface with the filename, -o, and -h options
    parser = argparse.ArgumentParser(
        description="Process a CSV dataset and generate a report"
    )
    parser.add_argument("filename", type=str, help="CSV file to read")
    parser.add_argument(
        "-o", "--output", type=str, help="XLSX file to write (optional)"
    )
    args = parser.parse_args()

    # Create a Dataset object from the specified CSV file
    dataset = Dataset(args.filename)

    if args.output:
        # If the -o option is specified, write the data to an XLSX file
        dataset.write_to_xlsx(args.output)
    else:
        # Otherwise, print the results of various aggregation and statistical operations on the data
        #  print(f'Average tweet length: {dataset.average_tweet_length()}')
        #  print(f'Number of insults: {dataset.count_insults()}')

        #  print('\nNumber of tweets per target:')
        #  for target, count in dataset.count_tweets_per_target().items():
        #      print(f'{target}: {count}')

        #  print('\nAverage tweet length per insult:')
        #  for insult, avg_length in dataset.average_tweet_length_per_insult().items():
        #      print(f'{insult}: {avg_length:.2f}')

        print("\nSummary:")  #
        for stat, value in dataset.summarize().items():
            print(f"{stat}: {value}")
