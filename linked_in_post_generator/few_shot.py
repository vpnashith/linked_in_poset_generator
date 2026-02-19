""" 
    Module: few_shot.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 15-02-2026
"""
import json
import pandas as pd


class FewShotPosts:
    def __init__(self, file_path="data/processed_data.json"):
        self.df = None
        self.unique_tags = None
        self.authors = None
        self.load_post(file_path)

    def load_post(self, file_path):
        with open(file_path, encoding="utf-8") as file:
            posts = json.load(file)
            self.df = pd.json_normalize(posts)
            self.df["length"] = self.df["line_count"].apply(self.length_category)

            available_tags = self.df["tags"].apply(lambda x: x).sum()
            self.unique_tags = set(available_tags)

            self.authors = set(self.df["author"].unique())

    def length_category(self, line_count):
        if line_count < 5:
            return "Short"
        if 5 <= line_count <= 10:
            return "Medium"
        return "Long"

    def get_unique_tags(self):
        return self.unique_tags

    def get_authors(self):
        return self.authors

    def get_filtered_post(self, length, language, tag, author_style):
        filtered_df = self.df[
            (self.df["language"] == language) &
            (self.df["length"] == length) &
            (self.df["tags"].apply(lambda tags: tag in tags)) &
            (self.df["author"] == author_style)
        ]
        return filtered_df.to_dict(orient="records")


if __name__ == "__main__":
    fs = FewShotPosts()
    # print(posts)
    print(fs.get_authors())
    print(fs.get_unique_tags())
    posts = fs.get_filtered_post("Short", "Hinglish", "Productivity", "Muskan Handa")
    print(posts)

