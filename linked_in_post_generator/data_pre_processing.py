""" 
    Module: data_pre_processing.py
    
    Author: Nashith vp
    
    Description:
    
    Created On: 15-02-2026
"""
import json
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_core.prompts import PromptTemplate
from llm_utils import llm


class PreProcessing:
    def __init__(self, source_data_path, processed_data_path="data/processed_data.json"):
        self.source_data_path = source_data_path
        self.processed_data_path = processed_data_path

    @staticmethod
    def get_unified_tag(post_with_metadata):
        """The tag generated is maybe same semantic meaning, but it may be different words. So we unifi then"""
        """Eg: tags may be <job>, <Job Search>, <JOB_SEARCH>, <opportunity search>, etc ==> But all of this can be 
        consider as a <Job Search> tag"""
        unique_tags = set()
        for post in post_with_metadata:
            unique_tags.update(post["tags"])

        unique_tag_list = ", ".join(unique_tags)  # This is to give input for the query(prompt)

        # Template to make the tag list as unified
        template = ''' I will give you a list of tags. You need to unify tags with the following requirements,
                    1. Tags are unified and merged to create a shorter list. 
                       Example 1: "Jobseekers", "Job Hunting" can be all merged into a single tag "Job Search". 
                       Example 2: "Motivation", "Inspiration", "Drive" can be mapped to "Motivation"
                       Example 3: "Personal Growth", "Personal Development", "Self Improvement" can be mapped to "Self Improvement"
                       Example 4: "Scam Alert", "Job Scam" etc. can be mapped to "Scams"
                    2. Each tag should be follow title case convention. example: "Motivation", "Job Search"
                    3. Output should be a JSON object, No preamble
                    3. Output should have mapping of original tag and the unified tag. 
                       For example: {{"Jobseekers": "Job Search",  "Job Hunting": "Job Search", "Motivation": "Motivation}}
                    
                    Here is the list of tags: 
                    {tags}
                    '''
        pt = PromptTemplate.from_template(template)
        chain = pt | llm
        response = chain.invoke(input={"tags": unique_tag_list})

        try:
            json_parser = JsonOutputParser()
            json_data = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException
        return json_data

    @staticmethod
    def get_post_metadata(post):
        """Fetch the metadata based on requirement and """
        template = """
        I give you a linked in post. You need to extract the number of lines, which language the post is written and tags
        The response should satisfy the given criteria
        1. Return a valid JSON, No preamble
        2. JSON content should have exactly three keys: line_count, language and tags
        3. tags is an array of text tags. Extract maximum two tags.
        4. Language should be either English or Hinglish. Hinglish is post containing both hindi and english
        
        Here is the actual post you need to perform this task:
        {post}
        """
        pt = PromptTemplate.from_template(template)

        # chaining the llm to prompt template
        chain = pt | llm
        response = chain.invoke(input={"post": post})
        try:
            json_parser = JsonOutputParser()
            json_data = json_parser.parse(response.content)
        except OutputParserException:
            raise OutputParserException

        return json_data

    def process_post_data(self):
        """ Add the metadata to the posts"""
        post_with_metadata = []
        with open(self.source_data_path, encoding="utf-8") as post_data:
            posts = json.load(post_data)
            for post in posts:
                metadata = self.get_post_metadata(post["text"])
                post_with_metadata.append(post | metadata)
                # print(metadata)
        unified_tags = self.get_unified_tag(post_with_metadata)
        # print(unified_tags)

        for post in post_with_metadata:
            existing_tag = post["tags"]
            updated_unified_tag = {unified_tags.get(tag) for tag in existing_tag}
            post["tags"] = list(updated_unified_tag)
            # print(post["tags"])

        # json file for processed data
        with open(self.processed_data_path, encoding="utf-8", mode="w") as out_file:
            json.dump(post_with_metadata, out_file, indent=4)


if __name__ == "__main__":
    pre_process = PreProcessing("data/source_data.json")
    pre_process.process_post_data()
