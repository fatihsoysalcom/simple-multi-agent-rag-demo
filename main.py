import re

# --- Knowledge Base --- 
# This simulates an external database of information that an LLM might not have.
KNOWLEDGE_BASE = [
    "Paris is the capital of France and its largest city. It is known for its art, fashion, gastronomy, and culture.",
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It was completed in 1889.",
    "Mars is the fourth planet from the Sun and the second-smallest planet in the Solar System, after Mercury.",
    "The French Revolution was a period of far-reaching social and political upheaval in France that lasted from 1789 until 1799.",
    "Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals.",
    "Retrieval-Augmented Generation (RAG) is an AI framework for improving the relevancy and factual accuracy of generative AI models by grounding them with facts from external data sources.",
    "Multi-agent systems involve multiple interacting intelligent agents within an environment.",
    "Simulations are imitations of some real-world process or system over time."
]

def retrieve_context(query: str, knowledge_base: list[str], top_k: int = 2) -> list[str]:
    """
    Simulates the retrieval step of RAG.
    Finds documents in the knowledge base relevant to the query using simple keyword matching.
    """
    query_words = set(query.lower().split())
    scores = []
    for i, doc in enumerate(knowledge_base):
        doc_words = set(re.findall(r'\b\w+\b', doc.lower())) # Extract words from document
        match_count = len(query_words.intersection(doc_words))
        if match_count > 0:
            scores.append((match_count, doc))
    
    # Sort by match count in descending order and return top_k documents
    scores.sort(key=lambda x: x[0], reverse=True)
    return [doc for score, doc in scores[:top_k]]

def generate_response(query: str, context: list[str]) -> str:
    """
    Simulates the generation step of RAG.
    Combines the query with retrieved context to form an augmented prompt.
    A real LLM would then process this prompt to generate a coherent answer.
    """
    if not context:
        return f"Agent could not find relevant information for: '{query}'. No context retrieved."

    # This is the "augmented prompt" that would be sent to a real LLM.
    # The LLM uses this combined information to generate a more accurate response.
    augmented_prompt = (
        f"Original User Query: {query}\n\n"
        f"Retrieved Context:\n" + "\n".join([f"- {c}" for c in context]) + "\n\n"
        f"Based on the provided context, generate a concise and accurate answer to the user's query."
    )

    # --- SIMULATED LLM RESPONSE ---
    # In a real RAG system, a Large Language Model (LLM) would take the
    # 'augmented_prompt' and generate a human-like response by synthesizing
    # information from the query and the retrieved context.
    # For this example, we'll provide a placeholder response that shows the
    # augmented prompt and a simple, hardcoded "answer" if keywords match.

    simulated_llm_output_prefix = (
        f"Simulated LLM processing the augmented prompt:\n"
        f"  Query: '{query}'\n"
        f"  Context used: {len(context)} relevant documents.\n"
        f"  A real LLM would now synthesize these into an answer like: "
    )
    
    lower_query = query.lower()
    for doc in context:
        lower_doc = doc.lower()
        if "capital of france" in lower_query and "paris is the capital of france" in lower_doc:
            return simulated_llm_output_prefix + "The capital of France is Paris."
        if "french revolution" in lower_query and "1789 until 1799" in lower_doc:
            return simulated_llm_output_prefix + "The French Revolution lasted from 1789 until 1799."
        if "what is mars" in lower_query and "fourth planet from the sun" in lower_doc:
            return simulated_llm_output_prefix + "Mars is the fourth planet from the Sun."
        if "what is rag" in lower_query and "retrieval-augmented generation is an ai framework" in lower_doc:
            return simulated_llm_output_prefix + "RAG is an AI framework for improving generative AI models."
        if "eiffel tower" in lower_query and "completed in 1889" in lower_doc:
            return simulated_llm_output_prefix + "The Eiffel Tower was completed in 1889."
        if "what is ai" in lower_query and "intelligence demonstrated by machines" in lower_doc:
            return simulated_llm_output_prefix + "AI is intelligence demonstrated by machines."
        if "multi-agent systems" in lower_query and "multiple interacting intelligent agents" in lower_doc:
            return simulated_llm_output_prefix + "Multi-agent systems involve multiple interacting intelligent agents."

    return simulated_llm_output_prefix + "A comprehensive answer based on the context."


# --- Multi-Agent Simulation ---

class Agent:
    """
    Represents an autonomous agent in a simulation.
    Each agent can query the RAG system to get information.
    """
    def __init__(self, name: str):
        self.name = name

    def ask_question(self, question: str, knowledge_base: list[str]) -> None:
        """
        An agent asks a question, triggering the RAG process.
        This demonstrates how multiple agents can leverage RAG.
        """
        print(f"\n--- {self.name} asks: '{question}' ---")
        
        # Step 1: Retrieve relevant context from the knowledge base
        retrieved_context = retrieve_context(question, knowledge_base)
        print(f"  [RAG] Retrieved Context ({len(retrieved_context)} docs):")
        for doc in retrieved_context:
            print(f"    - {doc[:70]}...") # Show a snippet
        
        # Step 2: Generate a response using the query and retrieved context
        response = generate_response(question, retrieved_context)
        print(f"  [RAG] Agent's Response: {response}")

if __name__ == "__main__":
    print("--- Multi-Agent RAG Simulation Start ---")

    # Define different agents, each potentially with different information needs
    agent_historian = Agent("Historian Agent")
    agent_scientist = Agent("Scientist Agent")
    agent_tourist = Agent("Tourist Agent")

    # Each agent asks a question, simulating their dynamic information needs
    agent_historian.ask_question("When was the French Revolution?", KNOWLEDGE_BASE)
    agent_scientist.ask_question("What is Mars?", KNOWLEDGE_BASE)
    agent_tourist.ask_question("What is the capital of France?", KNOWLEDGE_BASE)
    agent_scientist.ask_question("What is RAG?", KNOWLEDGE_BASE)
    agent_historian.ask_question("Tell me about the Eiffel Tower.", KNOWLEDGE_BASE)
    agent_tourist.ask_question("What is AI?", KNOWLEDGE_BASE)
    agent_scientist.ask_question("What are multi-agent systems?", KNOWLEDGE_BASE)
    agent_tourist.ask_question("What is the weather like today?", KNOWLEDGE_BASE) # Query for which no context exists

    print("\n--- Multi-Agent RAG Simulation End ---")
