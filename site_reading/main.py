
# Part 1
#Import libraries
import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

# Load environment variables from envirenment file, if not ctreated add here key directly in a file called .env

load_dotenv(override=True)
api_key = "sk-proj-sdfsdfSDgsdg535vsdv3466vxcxcvxcvxcv4534ghgh" #os.getenv('OPENAI_API_KEY')


# Check the key

if not api_key:
    print("No API key was found - you api is not found please check it again")
else:
    print("API key found and looks good so far!")

#Set the environmet variable for API if it is already not set
os.environ['OPENAI_API_KEY'] = api_key
# Part 2

# check it's working correctly
from openai import OpenAI
openai = OpenAI()
# Message to OpenAi and check its response
message = "Hello, ChatGPT! my first start here!"
response = openai.chat.completions.create(model="gpt-4o-mini", messages=[{"role":"user", "content":message}])
print(response.choices[0].message.content)




# Part 3
# Create aClass for website crawling
# Pass header: Every site directly not allow to rad content so pass header also
headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Webcrawl:

    def __init__(self, url):
        """
        Comment: Create this Webcrawl object to craw site and beautify it.
        """
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
#Remove javascript and other scripts, css styles, images and input options
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)


# Part 4

# Type site url in the Webcrawl object

ed = Webcrawl("https://cnn.com")
print(ed.title)
print(ed.text)

# Part 5

# Define A function For Website summary by OpenAi Promt

def user_prompt_for(webcrawl):
    user_prompt = f"Your searched Wesite title: {webcrawl.title}"
    user_prompt += "\nContents: \
Summary of this website in markdown: \
News announcements: \n\n"
    user_prompt += webcrawl.text
    return user_prompt

# Part 6
print(user_prompt_for(ed))


# Part 7
# Create a Message: meassage for define a role to system(openai) and pass user(who using openai) query
messages = [
    {"role": "system", "content": "You are my assistant to give me information"},
    {"role": "user", "content": "What is the value of 9*4 ?"}
]
# Part 8
# To give you a preview -- calling OpenAI with system and user messages:

response = openai.chat.completions.create(model="gpt-4o-mini", messages=messages)
print(response.choices[0].message.content)

# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."
# Part 9
system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown."




# Part 10
# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]


# Part 11
# Try this out, and then try for a few more websites

messages_for(ed)


# Part 12
# And now: call the OpenAI API for summerization of content(website content) define opnai model and return content

def summarize(url):
    webcrawl = Webcrawl(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(webcrawl)
    )
    return response.choices[0].message.content
# Part 3
# Now pass the url to summarize content by api
summarize("https://cnn.com")



# Part 14
# Another function to display content in nicely

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))

# Part 15
# Call the function with site url
display_summary("https://cnn.com")
