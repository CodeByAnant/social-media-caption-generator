import requests
import json
import os
import time

from dotenv import load_dotenv
import os

load_dotenv()  # loads .env file
api_key = os.getenv("GEMINI_API_KEY")

API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

def generate_social_media_post(topic: str, keywords: str = "") -> dict:
    """
    Generates a social media post using the Gemini API with robust error handling.
    """
    if not topic:
        print("Error: Topic cannot be empty.")
        return None
        
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("Error: Please set your GEMINI_API_KEY in the script or as an environment variable.")
        return None

    
    prompt = f"""
    You are an expert social media manager. Your task is to generate an engaging social media post about "{topic}".

    The post must include:
    1. A main body of text with 2-3 relevant emojis integrated naturally.
    2. A blank line after the main text.
    3. A list of 3-5 relevant hashtags, each starting with '#'.
    """
    
    if keywords:
        prompt += f"\n\nPlease naturally incorporate the following keywords: {keywords}."
    
    prompt += """
    Example format:
    [POST TEXT WITH EMOJIS]

    #hashtag1 #hashtag2 #hashtag3
    """

    
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    headers = {
        "Content-Type": "application/json"
    }

    print("Generating post with Gemini, please wait...")

    
    retries = 5
    delay = 2  
    for i in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=20)
            
           
            response.raise_for_status()

            result = response.json()
            if "candidates" in result and result["candidates"]:
                generated_text = result["candidates"][0]["content"]["parts"][0]["text"]
                return parse_generated_text(generated_text)
            else:
                print("Error: Received an unexpected response format from the API.")
                print("Full response:", result)
                return None

        
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code
            
            
            if status_code == 400:
                print(f"CRITICAL ERROR ({status_code}): Bad Request. This might be due to an invalid API key or a malformed request.")
                print(f"API Response: {e.response.text}")
                return None 
            elif 400 <= status_code < 500 and status_code != 429:
                print(f"CRITICAL ERROR ({status_code}): Client error.")
                print(f"API Response: {e.response.text}")
                return None 

           
            print(f"Error ({status_code}): {e}. Retrying in {delay} seconds...")
            if i == retries - 1:
                break 
            time.sleep(delay)
            delay *= 2 

        except requests.exceptions.RequestException as e:
            print(f"Network Error: {e}. Retrying in {delay} seconds...")
            if i == retries - 1:
                break
            time.sleep(delay)
            delay *= 2
            
    print("Failed to get a response after multiple retries.")
    return None


def parse_generated_text(text: str) -> dict:
    """
    Parses the raw text from the API into post text and hashtags.
    """
    lines = text.strip().split('\n')
    post_lines, hashtag_lines = [], []
    found_hashtags = False
    for line in lines:
        if '#' in line:
            words = line.strip().split()
            if all(word.startswith('#') for word in words):
                 found_hashtags = True
        if found_hashtags:
            hashtag_lines.append(line.strip())
        else:
            post_lines.append(line)
    post_text = "\n".join(post_lines).strip()
    all_hashtags = []
    for h_line in hashtag_lines:
        all_hashtags.extend([tag for tag in h_line.split() if tag.startswith('#')])
    return {"post_text": post_text, "hashtags": all_hashtags}

def main():
    """
    Main function to run the script.
    """
    print("--- Social Media Post Generator (using Gemini) ---")
    try:
        user_topic = input("Enter a topic for your social media post: ")
        user_keywords = input("Enter any keywords to include (optional, comma-separated): ")
        post_data = generate_social_media_post(user_topic, keywords=user_keywords)
        if post_data:
            print("\n" + "="*50)
            print("🎉 Here is your generated post: 🎉")
            print("="*50 + "\n")
            print(post_data["post_text"])
            print("\n" + " ".join(post_data["hashtags"]))
            print("\n" + "="*50)
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()