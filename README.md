# AI Assistant with Calculator Tool

A simple AI assistant that answers general questions and performs mathematical calculations automatically using LangChain and OpenAI GPT-3.5 Turbo.

## 🎯 Objective

Create an assistant that automatically identifies when to use an external tool (calculator) or answer with its own knowledge, demonstrating smart integration between LLM and tools.

## 🛠️ Model and Configuration

### **Model:** OpenAI GPT-3.5 Turbo
- **Why:** Ideal balance between cost, speed, and reasoning capability
- **Configuration:** `temperature=0` for consistent answers

### **Framework:** LangChain with ReAct Pattern
- **ReAct Agent:** Enables reasoning before deciding to use tools
- **AgentExecutor:** Manages the Thought → Action → Observation cycle
- **Custom Tool:** Calculator with security validation

## 📋 How to Run the Code

### **1. Environment Preparation**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate
```

### **2. Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3. API Key Configuration**

1. **Get your OpenAI key:**
   - Go to: https://platform.openai.com/api-keys
   - Log in to your account
   - Click "Create new secret key"
   - Copy the key (format: `sk-proj-...`)

2. **Create configuration file:**
```bash
# Create .env file in project root
echo "OPENAI_API_KEY=sk-proj-your-key-here" > .env
```

### **4. Run the Assistant**

```bash
python main.py
```

### **5. Test Features**

```bash
# Math test
🔹 You: 23 * 3

# General knowledge test
🔹 You: What is Artefact and what is its business model?

# Company-related calculation
🔹 You: If Artefact has projects worth 500000 reais and a margin of 25%, what is the profit?

# Exit
🔹 You: quit
```

## 🧠 Implementation Logic

### **Solution Architecture**

```
User Input
       ↓
   GPT-3.5 Turbo (ReAct Agent)
       ↓
   Question Analysis
       ↓
┌─────────────────┬─────────────────┐
│  Is Math?       │  Is General?    │
│       ↓         │       ↓         │
│ Calculator Tool │ Model Knowledge │
│       ↓         │       ↓         │
│   Result        │       ↓         │
└─────────┬───────┴───────┬─────────┘
          ↓               ↓
      Integrated Final Answer
```

### **Main Components**

1. **Calculator Tool (@tool decorator):**
   - Uses regex validation for security (`^[0-9+\-*/(). ]+$`)
   - Handles errors (division by zero, invalid syntax)

2. **AIAssistant Class:**
   - Initializes GPT-3.5 Turbo with optimized settings
   - Creates ReAct agent with custom prompt
   - Manages execution and error handling

3. **ReAct Agent:**
   - **Thought:** Analyzes if it's a calculation or general question
   - **Action:** Decides to use calculator or answer directly
   - **Observation:** Processes tool result
   - **Final Answer:** Integrates final response

### **Decision Flow**

```python
# Example: "128 * 46"
Thought: "This is a pure mathematical expression"
Action: calculator
Action Input: "128 * 46"
Observation: "The result of 128 * 46 is 5888"
Final Answer: "The result of 128 * 46 is 5888"

# Example: "Who was Einstein?"
Thought: "This is a general knowledge question"
Final Answer: "Albert Einstein was a German theoretical physicist..."
```

### **Security Validations**

- **Regex Validation:** Only accepts `[0-9+\-*/(). ]`
- **Eval Safety:** Expressions are pre-validated before execution
- **Error Handling:** Captures division by zero and syntax errors
- **Input Sanitization:** Removes spaces and invalid characters

## 📚 What I Learned

### **Technical Concepts Mastered**

1. **LangChain Architecture:**
   - How to structure intelligent agents
   - Difference between tools, agents, and executors
   - ReAct pattern for reasoning + acting

2. **OpenAI Integration:**
   - Optimized configuration of ChatOpenAI
   - Token and cost management
   - Temperature settings for consistency

3. **Tool Development:**
   - Creating custom tools
   - Schema validation
   - Robust error handling

4. **Prompt Engineering:**
   - Structuring prompts for agents
   - Balancing flexibility and precision
   - Proper ReAct formatting

### **Technical Challenges Overcome**

1. **Agent Decision Making:** Prompt engineering for correct decisions
2. **Security Concerns:** Safe validation of mathematical expressions
3. **Error Recovery:** Graceful handling of API and parsing failures

## 🚀 What I Would Do Differently With More Time

### **Feature Expansions**

1. **Additional Tools:**
   ```python
   # Weather API
   def get_weather(city: str) -> str:
       """Get current weather for a city"""
   # Currency Converter
   def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
       """Convert between currencies using live rates"""
   # Web Search
   def web_search(query: str) -> str:
       """Search the web for current information"""
   ```

2. **Improved Interface:**
   - **Streamlit Web App:** More user-friendly graphical interface
   - **Chat History:** Conversation persistence
   - **Export Options:** Save conversations as PDF/TXT
   - **Voice Input/Output:** Integration with speech APIs

3. **Advanced Intelligence:**
   - **Context Memory:** Remember previous conversations
   - **User Profiling:** Adapt responses to the user
   - **Multi-language:** Support for multiple languages
   - **Sentiment Analysis:** Detect tone and adapt response

---

## 📊 Final Project Structure

```
ai-assistant-calculator/
│
├── main.py              # Main code
├── requirements.txt     # Python dependencies  
├── .env                # API keys (do not version!)
├── .env.example        # Configuration template
├── README.md           # This documentation
└── .gitignore          # Protects sensitive files
```

## 🎯 Conclusion

This project demonstrates a **simple yet robust** implementation of an AI assistant with reasoning and external tool usage capabilities. The solution is **extensible**, **secure**, and **production-ready**, following best practices with LangChain and OpenAI.

---

**Lucas Lima Felix da Silva - Developed for Artefact Technical Challenge - AI Engineer Full-Stack**