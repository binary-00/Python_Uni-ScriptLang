import wikipedia
wiki = str(input("Enter the topic name: "))
print(wikipedia.page(wiki).summary)