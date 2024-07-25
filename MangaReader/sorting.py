# import json
# from itertools import groupby
# from operator import itemgetter

# def sort_json():
    
#     with open('manga.json', 'r') as f:
#         data = json.load(f)

#     # Convert "Chapter" to float and sort the data by "Title" and "Chapter"
#     for item in data:
#         item['Chapter'] = float(item['Chapter'])
#     data.sort(key=itemgetter('Title', 'Chapter'))

#     # Group the data by "Title"
#     grouped_data = {}
#     for key, group in groupby(data, key=itemgetter('Title')):
#         group_list = list(group)
#         for item in group_list:
#             del item['Title']
#         grouped_data[key] = group_list

#     with open('manga.json', 'w') as f:
#         json.dump(grouped_data, f, indent=4)

# sort_json()
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

# Save the new data
with open('manga.json', 'w') as f:
    json.dump(new_data, f, indent=4)