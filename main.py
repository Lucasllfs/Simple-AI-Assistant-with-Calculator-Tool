import os
import re
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()

@tool
def calculator(expression: str) -> str:
    """Use this tool for mathematical calculations. 
    Input should be a mathematical expression like '2 + 3', '10 * 5', '100 / 4', etc.
    The tool can handle basic arithmetic operations: +, -, *, /, **, ()
    
    Args:
        expression: Mathematical expression to evaluate
    
    Returns:
        str: Result of the calculation or error message
    """
    try:
    # Removes spaces and validates the expression
        expression = expression.strip()
        
    # Validates if it contains only safe mathematical characters
        if not re.match(r'^[0-9+\-*/(). ]+$', expression):
            return f"Error: Invalid characters in expression '{expression}'. Only numbers and basic operators are allowed."
        
    # Evaluates the mathematical expression
        result = eval(expression)
        return f"The result of {expression} is {result}"
        
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error calculating '{expression}': {str(e)}"

class AIAssistant:
    """Simple AI Assistant with calculator capabilities."""
    
    def __init__(self):
    # Initializes the language model
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
    # List of available tools
        self.tools = [calculator]
        
    # Defines the prompt template for the ReAct agent
        self.prompt = PromptTemplate.from_template("""
You are a helpful AI assistant. You can answer questions using your knowledge or use tools when needed.

When you receive a mathematical question or calculation request, use the calculator tool.
For other questions, answer directly using your knowledge.

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")
        
    # Creates the ReAct agent
        self.agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
    # Creates the agent executor
        self.agent_executor = AgentExecutor(
            agent=self.agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=5
        )
    
    def ask(self, question: str) -> str:
        """Process a question and return the answer."""
        try:
            result = self.agent_executor.invoke({"input": question})
            return result["output"]
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main function to run the AI assistant."""
    
    # Checks if the API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found!")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY=your_api_key_here")
        return
    
    # Initializes the assistant
    print("Initializing AI Assistant with Calculator...")
    try:
        assistant = AIAssistant()
        print("Assistant ready!")
        print("You can ask mathematical questions or general questions.")
        print("Type 'quit' to exit.\n")
        
    #  Main interaction loop
        while True:
            try:
                question = input("🔹 You: ").strip()
                
                if question.lower() in ['quit', 'exit', 'bye']:
                    print("Goodbye!")
                    break
                
                if not question:
                    print("Please enter a question.")
                    continue
                
                print(f"\n🤖 Assistant:")
                answer = assistant.ask(question)
                print(f"{answer}\n")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
        print("Make sure you have a valid OpenAI API key and internet connection.")

if __name__ == "__main__":
    main()