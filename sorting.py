import json

# Load the current data
with open('manga.json', 'r') as f:
    data = json.load(f)

# Initialize the new data structure
new_data = {}

# Transform the data
for manga in data:
    # Find if the manga already exists in the new data
    existing_manga = new_data.get(manga["manga-id"])

    # If the manga doesn't exist, add it
    if existing_manga is None:
        existing_manga = {
            "title": manga["Title"],
            "cover_link": manga["cover"],  # Add the cover link here
            "chapters": []
        }
        new_data[manga["manga-id"]] = existing_manga

    # Add the chapter to the manga
    existing_manga["chapters"].append({
        "uid": manga["uid"],
        "number": manga["Chapter"],
        "images": manga["Images"]
    })

# Order the chapters by number
for manga in new_data.values():
    manga["chapters"].sort(key=lambda x: x["number"])

# Sort the manga by title
sorted_data = dict(sorted(new_data.items(), key=lambda item: item[1]["title"]))

# Save the sorted data
with open('manga.json', 'w') as f:
    json.dump(sorted_data, f, indent=4)