import os
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI, AuthenticationError, APIError, RateLimitError

# Load environment variables from this project folder.
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

# Create OpenRouter client
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set. Please add it to your .env file.")

model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

client = OpenAI(
    api_key=api_key,
    base_url="https://openrouter.ai/api/v1"
)

# Ensure reports folder exists
if not os.path.exists("reports"):
    os.makedirs("reports")


def run_research(topic):
    """
    Generates a structured research report for a given topic.
    Saves the report to a file and returns the result.
    """

    # Keep prompt short to reduce token usage
    prompt = f"""
Write a structured research summary on:
{topic}

Sections:
1. Introduction
2. Key Concepts
3. Real-world Applications
4. Conclusion
"""

    max_retries = 3
    wait_time = 60  # seconds

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=2000
            )

            report_text = response.choices[0].message.content

            # Save report
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"reports/{topic.replace(' ', '_')}_{timestamp}.txt"

            with open(filename, "w", encoding="utf-8") as f:
                f.write(report_text)

            return report_text

        except RateLimitError as e:
            # Handle rate limit / quota errors
            if attempt < max_retries - 1:
                print(f"Rate limit hit. Waiting {wait_time} seconds before retry (attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                return f"Error: API rate limit exceeded after {max_retries} attempts. Please try again later."

        except AuthenticationError as e:
            # Invalid API key
            return f"Error: Invalid API key. Please check your OPENROUTER_API_KEY environment variable. Details: {str(e)}"

        except APIError as e:
            # Network or other API errors
            error_message = str(e)
            if "network" in error_message.lower() or "connection" in error_message.lower():
                if attempt < max_retries - 1:
                    print(f"Network error. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    return f"Error: Network error persisted after {max_retries} attempts. Please check your connection."
            else:
                return f"Error: API error occurred: {error_message}"

        except Exception as e:
            # Unexpected errors
            error_message = str(e)
            return f"Error occurred: {error_message}"


# Run from terminal
if __name__ == "__main__":
    topic = input("Enter topic: ")
    result = run_research(topic)
    print(result)