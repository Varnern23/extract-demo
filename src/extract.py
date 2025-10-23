"""
Part 1 — Structured Extraction

This script converts unstructured course text (e.g., “CSC 170 Programming and
Problem Solving 4 a T. Allen 1:50–3:50PM -M-W-F- OLIN 208”) into structured,
validated rows using a Pydantic model defined in schema.py.

In Part 1, your task is to:

- Write code in `extract_structured_record()` that uses your local LLM
  (through Ollama) to extract structured data following the schema.

- Pass SectionRow.model_json_schema() as the `format` argument when calling
  the model so it returns a valid JSON object.

- Parse the model output, validate it with SectionRow(**data), and return
  the resulting object.

For now, the provided stub runs end-to-end with a placeholder that returns
blank fields. This allows you to test the pipeline and see how the validation
and scoring work before adding your model logic.
"""

import csv
from pydantic import ValidationError
from schema import SectionRow
import ollama

MODEL = "gemma3:12b"
def query_ollama(prompt: str, model: str) -> str:
    """Call Ollama with the user prompt and return the reply text."""
    try:
        response = ollama.chat(model=model,
                               messages= [{"role": "user",
                                           "content": prompt}],
                                           format=SectionRow.model_json_schema())
        return response["message"]["content"]
    except ollama.ResponseError as e:
        print("Error: ", e.error)
def extract_structured_record(line: str) -> SectionRow:
    """
    Use an LLM to extract structured data for one course listing.
    
    TODO:
      - Write a prompt that tells the model what to extract.
      - Call your chosen Ollama model (e.g., gemma3:4b, granite3:2b, etc.).
      - Pass SectionRow.model_json_schema() so the model knows the expected format.
      - Parse the model's JSON response.
      - Validate the result with SectionRow(**data).
    """
    prompt = "return the following line in the form of exclusively a working JSON set up with the different categories: program (should be 3 capital letters), number(should be 3 numbers with the possibilty of an L at the end), section(just a lowercase letter and is always present), title(look for a string in title case), credits(look for a float), days(a list that may look like -m-w-f- if not present list as -------), times (if not given list as TBA), room(4 letters followed by 3 numbers if ot present list as TBA), faculty(someones first inital and last name), tags(Possible tags are: A, S, G, R, E1, E2, E3, D. Tags may or may not be present in the line. If no tags from this list appear, set tags to None. Tags are typically at the end of the line. Hey guy here you fucking dipshit stop putting none when there are in fact tags you blind whore) here is an example line: THR 117 Acting-I 3 a K. Anderson 12:40-2:10PM --T-R-- GRNT 502 E1, A, THR would be the program, 117 would be the number, the section would be a, the faculty would be K. Anderson, the times would be 12:40-2:10PM, the days would be --T-R--,  the room would be GRNT 502 and the tag for instance would be A in this situation be aware these will not always be in order in the following line :" + line 
    ans=query_ollama(prompt, MODEL)

    # The placeholder below produces an "empty" valid record.
    # It lets you test the pipeline without errors,
    # but it will score 0.00 on the evaluation.
    data = {
        "program": "",
        "number": "",
        "section": "",
        "title": "",
        "credits": 0.0,
        "days": "",
        "times": "",
        "room": "",
        "faculty": "",
        "tags": None,
    }
    print(ans)
    return SectionRow.model_validate_json(ans)


def process_file(in_path: str, out_path: str):
    """
    Read unstructured text from in_path, extract structured data for each line,
    and write results to out_path as a semicolon-delimited CSV.
    """
    with open(in_path, encoding="utf-8") as fin, open(out_path, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout, delimiter=";")

        # Write CSV header based on schema fields
        writer.writerow(SectionRow.model_fields.keys())

        count = 0
        limit = 150  # set a small limit for debugging; change to -1 for no limit ...

        for line in fin:
            if not line.strip():
                continue
            if count >= limit:  # or you could just remove these two lines for no limit
                break

            try:
                record = extract_structured_record(line)

                # Optional: view the validated record for debugging
                # print(record.model_dump_json(indent=2))

                writer.writerow(record.model_dump().values())

            except ValidationError as e:
                print("Validation test failed — skipping this line.")
                print(f"  Input: {line.strip()}")
                for err in e.errors():
                    loc = ".".join(str(x) for x in err["loc"])
                    msg = err["msg"]
                    val = err.get("input_value", "")
                    print(f"    Field: {loc} | Problem: {msg} | Value: {val}")

            except Exception as e:
                print(f"Unexpected error — skipping line: {line.strip()}")
                print(f"  {type(e).__name__}: {e}")

            count += 1


if __name__ == "__main__":
    # Process training data (Part 1)
    process_file("raw/training.txt", "out/sections_train.csv")

    # Later, after refinement, uncomment to process the test set (Part 2)
    # process_file("raw/testing.txt", "out/sections_test.csv")
