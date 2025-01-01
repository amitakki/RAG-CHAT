from typing import List
from src.domain.entities import Document

class PromptService:
    """
    Service for constructing and managing prompts.
    Contains reusable prompt engineering logic.
    """
    def construct_prompt_with_context(
        self,
        user_input: str,
        relevant_docs: List[Document],
        max_context_length: int = 2000
    ) -> str:
        """
        Constructs a prompt by combining user input with relevant context.
        
        Args:
            user_input: The user's question or input
            relevant_docs: List of relevant documents for context
            max_context_length: Maximum length of combined context
            
        Returns:
            str: The constructed prompt with context
        """
        # Combine relevant document content
        context_parts = [doc.content for doc in relevant_docs]
        combined_context = "\n\n".join(context_parts)
        
        # Truncate context if too long while preserving whole sentences
        if len(combined_context) > max_context_length:
            combined_context = self._truncate_to_sentences(
                combined_context,
                max_context_length
            )

        # Construct the final prompt
        prompt_template = (
            "Given the following context:\n\n"
            "{context}\n\n"
            "Answer the following question:\n"
            "{question}"
        )
        
        return prompt_template.format(
            context=combined_context,
            question=user_input
        )

    def _truncate_to_sentences(self, text: str, max_length: int) -> str:
        """Helper method to truncate text while preserving whole sentences"""
        if len(text) <= max_length:
            return text

        sentences = text.split('.')
        result = []
        current_length = 0

        for sentence in sentences:
            sentence_length = len(sentence) + 1  # +1 for the period
            if current_length + sentence_length > max_length:
                break
            result.append(sentence)
            current_length += sentence_length

        return '.'.join(result) + '.'