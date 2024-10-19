import requests
import json
import time


def stream_llm_response(query, chunk_size=1):
    url = "http://127.0.0.1:8000/api/llm/stream-rag"
    headers = {"accept": "application/json", "Content-Type": "application/json"}
    payload = {
        "body": query,
        "llm_id": "amazon.titan-text-premier-v1:0",
        "max_tokens": 512,
        "stop_sequences": [],
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 10,
    }

    with requests.post(
        url, headers=headers, data=json.dumps(payload), stream=True
    ) as response:
        if response.status_code == 200:
            # Stream the response content
            for line in response.iter_lines(chunk_size=chunk_size):
                if line:  # Filter out keep-alive new lines
                    decoded_line = line.decode("utf-8")
                    words = decoded_line.split()
                    for word in words:
                        yield word + " "
                        time.sleep(0.08)
        else:
            yield f"Error: {response.status_code}, {response.text}"
