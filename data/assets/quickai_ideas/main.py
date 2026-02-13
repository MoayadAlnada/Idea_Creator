import os
import openai
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc.methods.posts import NewPost

# Ensure you have the GPT-3 and WordPress credentials set in your environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WORDPRESS_URL = os.getenv("WORDPRESS_URL")
WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")

openai.api_key = OPENAI_API_KEY

def generate_ai_ideas(prompt, number_of_ideas=5):
    """Uses GPT-3 to generate content ideas based on the prompt.

    Args:
        prompt (str): The input prompt for idea generation.
        number_of_ideas (int, optional): Number of ideas to generate. Defaults to 5.

    Returns:
        list: A list of content ideas.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate {number_of_ideas} creative content ideas about {prompt}",
            temperature=0.7,
            max_tokens=100,
            top_p=1.0,
            frequency_penalty=0.5,
            presence_penalty=0.0,
            n=number_of_ideas
        )
        ideas = [response.choices[i].text.strip() for i in range(len(response.choices))]
        return ideas
    except Exception as e:
        print(f"Error generating ideas with GPT-3: {e}")
        return []

def publish_to_wordpress(title, content):
    """Publishes a generated idea to WordPress.

    Args:
        title (str): The title of the post.
        content (str): The content of the post.
    """
    try:
        wp = Client(WORDPRESS_URL, WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = 'publish'
        post.id = wp.call(NewPost(post))
        print(f"Post '{title}' has been successfully published with ID: {post.id}")
    except Exception as e:
        print(f"Error publishing to WordPress: {e}")

def main():
    # Example usage
    prompt = input("Enter your prompt for content ideas: ")
    ideas = generate_ai_ideas(prompt)

    if ideas:
        print("Here are your AI-generated content ideas:")
        for idea in ideas:
            print(f"- {idea}")

        # Optionally, publish an idea to WordPress
        publish = input("Would you like to publish one of these ideas to WordPress? (yes/no): ").lower()
        if publish == 'yes':
            idea_index = int(input(f"Enter the index of the idea you'd like to publish (1-{len(ideas)}): ")) - 1
            if 0 <= idea_index < len(ideas):
                publish_to_wordpress(f"AI-Generated Idea: {prompt}", ideas[idea_index])
            else:
                print("Invalid index.")
    else:
        print("Failed to generate ideas. Please try again.")

if __name__ == "__main__":
    main()