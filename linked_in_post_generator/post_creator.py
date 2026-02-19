""" 
    Module: post_creator.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 16-02-2026
"""
from llm_utils import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()


class PostGenerator:
    def __init__(self, length, language, tag, author):
        self.length = length
        self.language = language
        self.topic = tag
        self.author = author

    def length_resolver(self, length):
        if length == "Short":
            return "1 to 5 lines"
        if length == "Medium":
            return "6 to 8 lines"
        return "9 to 15 lines"

    def get_prompt(self):
        length_of_script = self.length_resolver(self.length)
        prompt = f"""
                    Create a linked in post using the following information. No preamble 
                    1. topic: {self.topic}
                    2. language: {self.language} , If the language is Hinglish , it means a mix of english and hindi.
                    the script generate should be always in english alphabet
                    3. length of the script: {length_of_script}
                """
        similar_posts = few_shot.get_filtered_post(self.length, self.language, self.topic, self.author)
        if similar_posts:
            prompt += "4. Use the following writing style to create the new post"
            for i, post in enumerate(similar_posts):
                post_content = post["text"]
                prompt += f"\n\n Example {i+1}: \n\n {post_content}"

                # I need max 2 example
                if i == 2:
                    break

        return prompt

    def generate_post(self):
        prompt = self.get_prompt()
        response = llm.invoke(prompt)
        return response.content


if __name__ == "__main__":
    pg = PostGenerator("Short", "Hinglish", "Productivity", "Muskan Handa")
    print(pg.generate_post())
