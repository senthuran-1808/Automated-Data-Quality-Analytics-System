from backend.ai.prompt_builder import PromptBuilder
from backend.ai.ollama_client import OllamaClient
from backend.agents.intent_classifier import IntentClassifier


class AIAgent:

    @staticmethod
    def detect_intent(question):

        return IntentClassifier.classify(question)

    @staticmethod
    def ask(
        question,
        analysis,
        stats,
        outliers,
        rules
    ):

        intent = AIAgent.detect_intent(question)

        prompt = PromptBuilder.build(
            question,
            analysis,
            stats,
            outliers,
            rules,
            intent
        )

        return OllamaClient.ask(prompt)
    
    
    @staticmethod
    def summarize_dataset(
        analysis,
        stats,
        outliers,
        rules
    ):
        


        question = """
Summarize this dataset professionally.
Explain:
1. Dataset overview
2. Missing values
3. Duplicates
4. Outliers
5. Data quality score
6. Important observations
Keep it concise.
"""

        return AIAgent.ask(
            question,
            analysis,
            stats,
            outliers,
            rules
        )


    @staticmethod
    def cleaning_plan(
        analysis,
        stats,
        outliers,
        rules
    ):

        question = """
Create a step-by-step data cleaning plan.
Mention:
- Missing values
- Duplicate handling
- Outlier handling
- Encoding
- Scaling
- Feature engineering
"""

        return AIAgent.ask(
            question,
            analysis,
            stats,
            outliers,
            rules
        )


    @staticmethod
    def ml_readiness(
        analysis,
        stats,
        outliers,
        rules
    ):

        question = """
Evaluate whether this dataset is ready for machine learning.
Mention strengths, weaknesses and improvements.
"""

        return AIAgent.ask(
            question,
            analysis,
            stats,
            outliers,
            rules
        )
    
