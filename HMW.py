AI = input("Enter the AI you would like to use: (enter only groq or hf [default is groq])")
if "hf" in AI:
    from hf import generate_response
else:
    from groq import generate_response

def get_essay_details():
    print("\n=== AI Writing Assistant===\n")
    topic = input("What is the topic of your essay? ").strip()
    essay_type = input("What type of essay are you writing? ").strip()
    lengths = ["300 words", "900 words", "1200 words", "2000 words"]
    print("Select essay word count: ")
    for i, l in enumerate(lengths, 1): print(f"{i}) {l}")
    try:
        idx = int(input("> ").strip())
        length = lengths[idx - 1] if 1 <= idx <= len(lengths) else "300 words"
    except ValueError:
        length = "300 words"
    target_audience = input("Target audience (e.g., High school students): ").strip()
    tone = input("Enter the tone of the essay (informal, formal, conversational etc.): ")
    return {"topic": topic, "essay_type": essay_type, "length": length, "target_audience": target_audience, "tone": tone}

def generate_essay_content(details):
    try:
        temp = float(input("Enter temperature (0.1 structured, 0.7 creative): ").strip())
        if not (0.0 <= temp <= 1.0): raise ValueError
    except ValueError:
        print("Invalid temperature. Using 0.3.")
        temp = 0.3
    intro_p = f"Write an indroduction for an {details["essay_type"]} essay about {details["topic"]} that is{details["length"]} words long.The introduction should us 1/6 of that many words. It should be written in a {details["tone"]} tone for {details["target_audience"]}. Make it engaging so that it captures the reader."
    intro = generate_response(intro_p, temperature=temp, max_tokens = 512)
    print("\n=== Generated Introduction ===\n")
    print(intro)

    print("\nWould you like the body written as a full draft or step-by-step?")
    print("1) Full draft\n2) Step-by-step")
    choice = input("> ").strip()
    if choice == "1":
        body_p =f"Write the main for an {details["essay_type"]} essay about {details["topic"]} that is {details["length"]} words long.It should take up about 2/3 of those words. It should be written in a {details["tone"]} tone for {details["target_audience"]}."
        body = generate_response(body_p, temperature=temp, max_tokens=1024)
        print("\n=== Generated Full Body ===\n")
        print(body)
    else:
        for i in range(5):
            point = input("Enter the main point/ arguement for each paragraph or click enter to finish.")
            if not point:
                break
            paragraph = (f"Write the {i} paragraph of the main body for an {details["essay_type"]} essay about {details["topic"]} that is{details["length"]} words long. It should use between 1/6 and 1/3 words. It should be written in a {details["tone"]} tone for {details["target_audience"]}. It should be about {point}")
            body_step = generate_response(paragraph, temperature=temp, max_tokens=1024)
            print("\n=== Generated Step-by-Step Body ===\n")
            print(body_step)

    concl_p = f"Write an conclusion for an {details["essay_type"]} essay about {details["topic"]} that is {details["length"]} words long. It should use 1/6 words. It should be written in a {details["tone"]} tone for {details["target_audience"]}."
    concl = generate_response(concl_p, temperature=temp, max_tokens=1024)
    print("\n=== Generate conclusion ===\n")
    print(concl)

def feedback_and_refinement():
    try:
        rating = int(input("\nRate satisfaction (1-5): ").strip())
        if rating < 1 or rating > 5: raise ValueError
    except ValueError:
        print("Invalid rating. Using 3.")
        rating = 3
    if rating != 5:
        feedback = input("Provide feedback (tone, structure, etc.): )").strip()
        print(f"\nThank you for your feedback: {feedback}")
    else:
        print("\nThank you! The essay looks good.")

def run_activity():
    print("\nWelcome to the AI Writing Assistant!")
    details = get_essay_details()
    if not details["topic"] or not details["essay_type"]:
        print("Please provide at least topic and essay type to continue.")
        return
    generate_essay_content(details)
    feedback_and_refinement()

if __name__ == "__main__":
    run_activity()