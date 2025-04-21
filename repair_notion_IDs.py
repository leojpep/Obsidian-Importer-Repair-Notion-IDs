# %% [markdown]
# # This script repairs the removed IDs in the filenames and foldernames of a notion html-export
# 
# 1. Find links in html files and map page names to IDs
# 2. rename files
# 3. rename folders

# %% [markdown]
# ## Import libraries

# %%
import os
import re
import urllib.parse  # Used for handling %20

# %% [markdown]
# ## Get root directory of notion html export

# %%
directory = None

while directory == None:
    root_path = str(input("Enter the path to your Notion export folder\n >>> "))
    root_path = os.path.abspath(root_path)

    if os.path.exists(root_path):
        directory = os.path.abspath(root_path)

print(f"Path set to {directory}")

# %% [markdown]
# ## Setup
# 
# - Define regex pattern
# - init mapping

# %%
regex_pattern = re.compile(r'\/([\w%20-]+)%20([a-f0-9]{32})')

# %%
map_name_to_id = {}    # Mapping of page_names to page_ids

# %% [markdown]
# ## Find links
# 
# - read all html files
# - find links with page name and id based on the regex pattern
# - map page name to id

# %%
for root, _, files in os.walk(directory):
    for file in files:
        if file.endswith(".html"):
            file_path = os.path.join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            matches = regex_pattern.findall(content)
            for match in matches:
                page_name = urllib.parse.unquote(match[0])
                page_id = match[1]
                # print(f"mapping: {page_name} -> {page_id}")

                if page_name in map_name_to_id and map_name_to_id[page_name] != page_id:
                    print(f"⚠️ Duplicate page name found with not matching page id: {page_name}\n {map_name_to_id[page_name]} != {page_id}")

                map_name_to_id[page_name] = page_id

print("🏁 Found all page names and ids\n")

# sort the dictionary by key (page name)
map_name_to_id = dict(sorted(map_name_to_id.items()))

for map in map_name_to_id:
    print(f"{map} -> {map_name_to_id[map]}")
# This script will search for all the HTML files in the given directory and its subdirectories.

# %% [markdown]
# ## Renaming files and folders
# 
# - walk through all folders and files again 
# - rename them based on the map {page name : page id}

# %%
for root, dirs, files in os.walk(directory):
    # rename files
    for file in files:
        filename = os.path.splitext(file)[0]  # Remove the file extension from the filename
        file_extension = os.path.splitext(file)[1]
        if filename in map_name_to_id:
            file_path = os.path.join(root, file)
            new_filename = f"{filename} {map_name_to_id[filename]}"
            new_file_path = os.path.join(root, new_filename + file_extension)

            if not os.path.exists(new_file_path):
                os.rename(file_path, new_file_path)
                print(f"✅ {filename} \t → \t {new_filename}")
            else:
                print(f"⚠️ File already exists: {new_file_path}")

    print("🏁 Renamed all files\n")

    # rename folders
    for dir in dirs:
        dirname = dir
        if dirname in map_name_to_id:
            dir_path = os.path.join(root, dirname)
            new_dirname = f"{dirname} {map_name_to_id[dirname]}"
            new_dir_path = os.path.join(root, new_dirname)

            if not os.path.exists(new_dir_path):
                os.rename(dir_path, new_dir_path)  # Uncommented this line
                print(f"✅ {dirname} \t → \t {new_dirname}")
            else:
                print(f"⚠️ Folder already exists: {new_dir_path}")
