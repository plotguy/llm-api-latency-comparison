import openai
import random
import time
import typing as T
import json

SYSTEM_PROMPT = """
You are a helpful assistant that converts CSV to JSON.
"""

BASE_PROMPT = """
Convert the following CSV to a JSON object where each value is true. 

Example input: apple, banana, orange
Example output: {"apple": true, "banana": true, "orange": true}

Only output the JSON, do not include any other text.

The CSV is:
"""

WORDS = open('./WORDS').read().splitlines()

def _get_random_words():
    return ', '.join(random.choices(WORDS, k=3))

def _call_openai(client: openai.Client, prompt: str) -> T.Tuple[str, float]:
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def time_fn(fn, *args, **kwargs):
    start = time.time()
    result = fn(*args, **kwargs)
    end = time.time()
    return result, end - start

def check_is_valid_json(json_str: str) -> bool:
    try:
        json.loads(json_str)
        return True
    except json.JSONDecodeError:
        return False


if __name__ == "__main__":
    init_time_start = time.time()
    oai_client = openai.Client()
    print(f"Elapsed time to load OpenAI client: {time.time() - init_time_start}")

    for i in range(50):
        print(f"------------ {i} ---------------")
        new_prompt = f"{BASE_PROMPT}\n{_get_random_words()}"
        result, time_taken = time_fn(_call_openai, oai_client, new_prompt)
        is_valid_json = check_is_valid_json(result)
        print(f"OpenAI Time taken: {time_taken}")
        print(f"Is valid json: {is_valid_json}")
        time.sleep(1)