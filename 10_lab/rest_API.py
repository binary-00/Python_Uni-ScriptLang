import argparse
import requests


def get_cat_facts(num_facts):
    url = f"https://cat-fact.herokuapp.com/facts/random?animal_type=cat&amount={num_facts}&lang=en"
    response = requests.get(url)
    facts = response.json()
    for fact in facts:
        print(fact["text"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cat-facts", type=int, required=True)
    args = parser.parse_args()

    get_cat_facts(args.cat_facts)

# python rest_API.py --cat-facts 5
