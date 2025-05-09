import subprocess
import json

def analyze_with_ai(symbol, prices, sentiment, news):
    try:
        # Prepare the payload
        payload = json.dumps({
            "ticker": symbol,
            "prices": prices,
            "sentiment": sentiment,
            "news": news[-10:]  # Limit to the last 10 news items
        })

        # Run the external AI process using the correct command
        proc = subprocess.run(
            ["ollama", "run", "dolphin3", "--json"],
            input=payload,
            text=True,
            capture_output=True,
            check=True
        )

        # Debugging: Print the output of the process
        print(f"STDOUT: {proc.stdout}")
        print(f"STDERR: {proc.stderr}")

        # Check if the output is empty
        if not proc.stdout.strip():
            raise ValueError("The external process returned empty output.")

        # Parse the JSON output
        return json.loads(proc.stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error calling external process: {e}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        raise

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Raw output: {proc.stdout}")
        raise