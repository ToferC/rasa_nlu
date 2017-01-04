# Author: toferc
# Python=3.5

import os
import json
import csv

# Enter your data directory here
data_dir = "./data/"

# Prepares data dictionary to include:
'''text, intent, entities
	entities is a list that includes dictionaries of:
		{start: int, end: int, value: str, entity: str}

	E.g:
		{
        "text": "i'm looking for a place in the north of town",
        "intent": "restaurant_search",
        "entities": [
          {
            "start": 31,
            "end": 36,
            "value": "north",
            "entity": "location"
          }
        ]
      },'''


def open_csv():
    # Open CSV file and create or add data into JSON file

    infile = input("Please enter your input file name (.csv): ")
    outfile = input("Please enter your output file name (.json): ")

    data_output = create_load_outfile(outfile)

    intents = []

    with open(os.path.join(data_dir, infile), "r+") as f:
        reader = csv.reader(f, delimiter=",", quotechar='"')
        for i, row in enumerate(reader):
            text, intent, *entities = row

            entity_list = []

            intents.append(intent)

            for entity in entities:
                start, end, value, entity_type = entity.split(",")
                entity_list.append(
                    {
                        "start": int(start),
                        "end": int(end),
                        "value": value,
                        "entity": entity_type
                    })

            data_output['rasa_nlu_data']['entity_examples'].append(
                {'text': text, 'intent': intent, 'entities': entity_list})

    save_json_file(outfile, data_output)


def enter_text():
    # Prompt user to enter text, identify intents, entities and values and write to rasa nlu JSON format

    intents = []
    entity_types = []

    outfile = input("Please enter your output file name (.json): ")

    data_output = create_load_outfile(outfile)
    print(data_output)

    print("Welcome. First enter your different types of intent. Just hit enter when you're finished.\n")

    while True:
        intents_input = input("Enter intent type: ").lower()
        if intents_input == "":
            break
        else:
            intents.append(intents_input)

    print("\nEnter your entity types.\n")

    while True:
        entities_input = input("Enter entity type: ").lower()
        if entities_input == "":
            break
        else:
            entity_types.append(entities_input)

    print(
        "\nGood. Now the setup is done. You will now enter a number of phrases.  Hit enter on a blank line when you are finished.")

    while True:
        text = input("\nEnter your text (or hit enter to end): ").lower()

        if text == "":
            break

        else:
            print("\nNow choose your intent from the list below:")
            for i, intent in enumerate(intents):
                print("{}: {}".format(i + 1, intent))

            intent_choice = intents[int(input("\nEnter the number corresponding to your intent: ")) - 1]
            print("Intent: {}".format(intent_choice))

            entities = []

            while True:
                print("")
                for i, word in enumerate(text.lower().split()):
                    print("{}: {}".format(i + 1, word))

                value = input("\nEnter the number corresponding to your entity, enter a phrase or hit return to skip: ")

                if value == "": # User wants to exit
                    break
                elif value in "1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20".split(): # User selected a single word
                    value = text.split()[int(value) - 1]
                else: # User entered a phrase
                    pass

                start = int(text.find(value))
                end = int(start + len(value))

                print("Choose your entity type.")
                for i, entity in enumerate(entity_types):
                    print("{}: {}".format(i + 1, entity))

                entity_type = entity_types[
                    int(input("\nChoose the number for your entity type or hit enter to pass: ")) - 1]

                entities.append({
                    "start": start,
                    "end": end,
                    "value": value,
                    "entity": entity_type
                })

            data_output['rasa_nlu_data']['entity_examples'].append(
                {'text': text, 'intent': intent_choice, 'entities': entities})

    save_json_file(outfile, data_output)


def create_load_outfile(outfile):
    # type: () -> object

    if os.path.isfile(os.path.join(data_dir, outfile)):
        add_to_file = input("It looks like this file already exists. Would you like to add to it? (y/n)")

        if add_to_file == "y":
            with open(os.path.join(data_dir, outfile)) as json_data:
                return json.load(json_data)

    else:
        return {"rasa_nlu_data": {"entity_examples": []}}


def save_json_file(outfile, data_output):
    # Save dictionary to rasa nlu JSON format
    with open(os.path.join(data_dir, outfile), 'w+') as f:
        json.dump(data_output, f, ensure_ascii=False)


if __name__ == "__main__":
    input_type = input("Would you like to import from a csv or enter text manually? (csv OR text) ")

    if input_type == "csv":
        open_csv()
    else:
        enter_text()
