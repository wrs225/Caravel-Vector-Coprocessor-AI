import os
import re
import csv
from colorama import Fore, Style


def categorize_prompts(module):
    directory = os.path.join("..", "prompts_attempt_two")
    files = os.listdir(directory)
    module_files = [file for file in files if module in file]
    categorized_prompts = []
    p = 0

    prompts = []
    for i, file in enumerate(module_files):
        file_path = os.path.join(directory, file)
        with open(file_path, "r") as f:
            content = f.read()
        prompts += re.split("[Uu]ser", content)
        # split all of the prompts if they contain "user" as well

    csv_file_path = os.path.join(os.getcwd(), module, f"{module}.csv")
    if os.path.exists(csv_file_path):
        with open(csv_file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            num_entries = sum(1 for row in reader) - 1
    else:
        with open(csv_file_path, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Prompt #", "Category", "Issue"])
        num_entries = 0

    for i, prompt in enumerate(prompts[num_entries:]):
        sliced_prompt = prompt.split("\n", 2)
        if len(sliced_prompt) == 3:
            print(
                f"{Fore.GREEN}Prompt: {sliced_prompt[0]}\n{Fore.BLUE}Response: {sliced_prompt[1]}\n{Fore.GREEN}Next Prompt: {sliced_prompt[2]}\n{Style.RESET_ALL}"
            )
        else:
            print(f"{Fore.GREEN}Prompt: {sliced_prompt[0]}\n{Style.RESET_ALL}")
        prompt_issues_str = "\n".join(
            f"{i+1}. {issue}" for i, issue in enumerate(PROMPT_ISSUES)
        )
        category = input(
            f"{Fore.YELLOW}Please categorize this prompt based on the following issues:\n{prompt_issues_str}\nYour choice: {Style.RESET_ALL}"
        )
        prompt_file_path = os.path.join(os.getcwd(), module, f"prompt_{i}.txt")
        with open(prompt_file_path, "w") as prompt_file:
            prompt_file.write(prompt)
        while not (
            category.isdigit() and int(category) in range(1, len(PROMPT_ISSUES) + 1)
        ):
            category = input(
                f"{Fore.RED}Invalid category. Please try again: {Style.RESET_ALL}"
            )
            if category.isdigit() and int(category) in range(1, len(PROMPT_ISSUES) + 1):
                break

        with open(csv_file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([p, int(category) - 1, PROMPT_ISSUES[int(category) - 1]])
        categorized_prompts.append((sliced_prompt, category))
        p += 1
    return categorized_prompts


PROMPT_ISSUES = [
    "Initial",
    "Bug / Testbench",
    "Bug / Non-Synth",
    "Bug / Verilator",
    "Noop",
    "Design Violation",
    "Design Modification",
    "GPT Wrangling",
    "skip",
]


list_of_modules = ["FP_Adder", "Decoder", "FP_Multiplier"]

for module in list_of_modules:
    os.makedirs(os.path.join(os.getcwd(), module), exist_ok=True)

for module in list_of_modules:
    categorize_prompts(module)
