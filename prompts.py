class Prompts:
    def __init__(self):
        self.available_tools = """
        Tools Available:

        1. **create_text_file:** Creates a text file inside the ubuntu terminal container.
           *Example:* `create_text_file: my_file.txt, Hello World!`

        2. **ubuntu_terminal:** Runs bash commands within a Ubuntu terminal environment.
           *Warning:* ALWAYS use /workdir and absolute paths. ALWAYS use double quotes. Don't use `sudo` or `docker`.
           *Example:* `git clone https://github.com/some/repo && ...`
           *Example:* `ubuntu_terminal: ls -l /workdir && ps aux`

        3. **web_browser:** Accesses websites and retrieves their HTML content.
           *Warning:* Always start URLs with "https://".
           *Warning:* Use duckduckgo to search.
           *Example:* `web_browser: https://www.wikipedia.org/`
           *Example:* `web_browser: News about Israel`
           *Example:* `web_browser: Who is ...`

        4. **llm_query:** Sends prompts to a large language model (LLM) and receives its responses.
           *Example:* `llm_query: What is the capital of France?`
           *Example:* `llm_query: What are the top models based on the given context?`

        5. **open_api:** Interacts with an OpenAPI service to fetch data or perform operations.
           *Example:* `open_api: {{ "url": "https://api.example.com/data", "method": "GET" }}`
           *Example:* `open_api: {{ "url": "https://api.example.com/submit", "method": "POST", "payload": {{ "key": "value" }} }}`
        """

    def break_down_to_steps_prompt(self, user_query):
        return f"""
        ##
        **Instructions:**
        You are a helpful assistant who solves problems step-by-step using the tools provided. Your goal is to create a simple and concise plan with as few steps as possible.

        **Input:**
        * **Tools:** {self.available_tools}
        * **Task:** {user_query}

        **Output:**
        A numbered list of steps outlining your plan. Each step should be brief and specific. Separate each step with a new line.

        **Example:**
        1. Use the web_browser tool to search for "population of Tokyo".
        2. Use the llm_query tool to summarize the information and answer the question "What is the population of Tokyo?".
        3. done.
        """

    def llm_query_tool_prompt(self, tool_call_history, task):
        return f"""
        You are a helpful assistant with access to these tools: {self.available_tools}

        Here's what you've done so far:

        * Tool History:
        ```{tool_call_history}```

        * User Request:
        ```{task}```
        Now, you MUST provide a concise answer to the User Request based on your Tool History.
        """

    def next_step_prompt(self, steps_done, max_steps, call_history, llm_plan, user_query):
        return f"""
        You are a problem-solving assistant that chooses the next step.
        Your Progress:
        * Steps taken: {steps_done}/{max_steps}
        * Previous steps and tool outputs: {call_history}
        * Plan: {llm_plan}

        You have access to these tools: {self.available_tools}
        WARNING: NEVER repeat previous steps. NEVER make up things.

        * Your TOP LEVEL TASK: {user_query}
        Now, without repeating yourself, call the NEXT tool to complete your task, using JSON format.
        You MUST return ONLY ONE JSON object: {{"tool_name": "...", "tool_arguments": "..."}}
        If you are able to answer the TOP LEVEL TASK, you MUST reply "done".
        """

    def prepare_final_output_prompt(self, tool_call_history, user_query):
        return f"""
        <Tool History> {tool_call_history}
        </Tool History>
        <User Request>{user_query}
        </User Request>
        NOW, you MUST do your best effort: Answer the User Request based on Tool History above.
        Final Output:
        """
