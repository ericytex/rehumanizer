import random
import re
import logging
import numpy as np
from typing import List, Tuple, Dict, Optional

# Try to import sentence transformers (optional dependency)
try:
    from sentence_transformers import SentenceTransformer
    SENTENCE_TRANSFORMERS_AVAILABLE = True
except ImportError:
    SENTENCE_TRANSFORMERS_AVAILABLE = False
    SentenceTransformer = None

logger = logging.getLogger(__name__)

class EnhancedWriteHumanMimic:
    """
    Advanced WriteHuman mimicry with semantic awareness and controlled aggressiveness.
    Balances undetectability with readability and coherence.
    """
    
    def __init__(self, aggressiveness=0.25, semantic_threshold=0.85, seed=None):
        """
        Args:
            aggressiveness (float): 0.2-0.3 for balanced approach (lower = more readable)
            semantic_threshold (float): Minimum cosine similarity to preserve (0.85+ recommended)
            seed (int): For reproducibility
        """
        self.aggressiveness = aggressiveness
        self.semantic_threshold = semantic_threshold
        if seed is not None:
            random.seed(seed)
        
        # Initialize semantic similarity model
        self.semantic_model = None
        if SENTENCE_TRANSFORMERS_AVAILABLE:
            try:
                self.semantic_model = SentenceTransformer('all-MiniLM-L6-v2')
                logger.info("✅ Semantic similarity model loaded successfully")
            except Exception as e:
                logger.warning(f"⚠️ Could not load semantic model: {e}")
        else:
            logger.info("⚠️ Sentence-transformers not available, using simplified semantic checking")
        
        # Controlled vocabulary downgrades (fewer, more strategic)
        self.strategic_replacements = {
            "demonstrates": "shows",
            "facilitates": "helps", 
            "remarkable": "great",
            "sophisticated": "advanced",
            "comprehensive": "complete",
            "particularly": "especially",
            "significantly": "a lot",
            "nevertheless": "but still",
            "furthermore": "also",
            "consequently": "so",
            "optimization": "improvement",
            "implementation": "setup",
            "utilization": "use"
        }
        
        # Subtle flow breakers (reduced set for better readability)
        self.subtle_fillers = [
            "in some cases",
            "you might say", 
            "to be honest",
            "from what I've seen",
            "in my opinion",
            "come to think of it"
        ]
        
        # Light redundancy phrases
        self.light_redundancy = [
            "in other words",
            "what I mean is",
            "basically"
        ]

    def _calculate_semantic_similarity(self, original: str, modified: str) -> float:
        """Calculate semantic similarity between original and modified text"""
        if not self.semantic_model:
            return 1.0  # Assume perfect similarity if model unavailable
        
        try:
            embeddings = self.semantic_model.encode([original, modified])
            similarity = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(similarity)
        except Exception as e:
            logger.warning(f"⚠️ Similarity calculation failed: {e}")
            return 1.0

    def _apply_strategic_synonyms(self, text: str) -> Tuple[str, List[str]]:
        """Apply strategic synonym replacements with semantic checking"""
        changes = []
        modified_text = text
        
        for original_word, replacement in self.strategic_replacements.items():
            if random.random() < self.aggressiveness:
                pattern = rf"\b{re.escape(original_word)}\b"
                if re.search(pattern, modified_text, re.IGNORECASE):
                    candidate = re.sub(pattern, replacement, modified_text, flags=re.IGNORECASE)
                    
                    # Check semantic similarity
                    similarity = self._calculate_semantic_similarity(text, candidate)
                    if similarity >= self.semantic_threshold:
                        modified_text = candidate
                        changes.append(f"{original_word} → {replacement}")
                    else:
                        logger.debug(f"Rejected synonym swap: {original_word} → {replacement} (similarity: {similarity:.3f})")
        
        return modified_text, changes

    def _add_subtle_flow_breaks(self, text: str) -> Tuple[str, List[str]]:
        """Add subtle flow breaks without destroying coherence"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        modified_sentences = []
        changes = []
        
        for sentence in sentences:
            if len(sentence.split()) > 10 and random.random() < self.aggressiveness / 2:
                words = sentence.split()
                # Insert filler in middle third of sentence (safer positioning)
                pos = random.randint(len(words)//3, 2*len(words)//3)
                filler = random.choice(self.subtle_fillers)
                words.insert(pos, f"{filler},")
                
                candidate_sentence = " ".join(words)
                
                # Check if this maintains meaning
                similarity = self._calculate_semantic_similarity(sentence, candidate_sentence)
                if similarity >= self.semantic_threshold:
                    modified_sentences.append(candidate_sentence)
                    changes.append(f"Added filler: {filler}")
                else:
                    modified_sentences.append(sentence)
            else:
                modified_sentences.append(sentence)
        
        return " ".join(modified_sentences), changes

    def _controlled_sentence_variation(self, text: str) -> Tuple[str, List[str]]:
        """Create controlled sentence length variation"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        modified_sentences = []
        changes = []
        
        for i, sentence in enumerate(sentences):
            words = sentence.split()
            
            # Only modify longer sentences and not too frequently
            if len(words) > 15 and random.random() < self.aggressiveness / 3:
                # Split at natural break points (conjunctions, commas)
                split_candidates = []
                for j, word in enumerate(words):
                    if word.lower() in ['and', 'but', 'however', 'therefore', 'moreover'] and j > 5:
                        split_candidates.append(j)
                
                if split_candidates:
                    split_point = random.choice(split_candidates)
                    part1 = " ".join(words[:split_point]).rstrip('.,!?') + "."
                    part2 = " ".join(words[split_point:])
                    
                    # Check semantic preservation
                    original_meaning = self._calculate_semantic_similarity(sentence, sentence)
                    combined_meaning = self._calculate_semantic_similarity(sentence, f"{part1} {part2}")
                    
                    if combined_meaning >= self.semantic_threshold:
                        modified_sentences.extend([part1, part2])
                        changes.append("Split long sentence")
                    else:
                        modified_sentences.append(sentence)
                else:
                    modified_sentences.append(sentence)
            else:
                modified_sentences.append(sentence)
        
        return " ".join(modified_sentences), changes

    def _add_light_redundancy(self, text: str) -> Tuple[str, List[str]]:
        """Add light redundancy for lower information density"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        modified_sentences = []
        changes = []
        
        for sentence in sentences:
            if random.random() < self.aggressiveness / 4:  # Very selective
                redundancy = random.choice(self.light_redundancy)
                candidate = f"{sentence.rstrip('.')}. {redundancy.capitalize()}, {sentence.lower()}"
                
                # Check if this maintains readability
                if len(candidate.split()) < len(sentence.split()) * 1.5:  # Don't make it too verbose
                    similarity = self._calculate_semantic_similarity(sentence, candidate)
                    if similarity >= self.semantic_threshold:
                        modified_sentences.append(candidate)
                        changes.append(f"Added redundancy: {redundancy}")
                    else:
                        modified_sentences.append(sentence)
                else:
                    modified_sentences.append(sentence)
            else:
                modified_sentences.append(sentence)
        
        return " ".join(modified_sentences), changes

    def process(self, text: str, min_words=200) -> Dict[str, any]:
        """
        Apply enhanced WriteHuman processing with semantic awareness
        
        Returns:
            Dict with processed text, similarity score, and change log
        """
        if min_words and len(text.split()) < min_words:
            logger.info(f"Text too short ({len(text.split())} words), skipping enhanced processing")
            return {
                "text": text,
                "similarity": 1.0,
                "changes": [],
                "aggressiveness_used": 0.0
            }
        
        logger.info("🎭 Applying Enhanced WriteHuman mimicry with semantic awareness...")
        
        original_text = text
        all_changes = []
        
        # Step 1: Strategic synonym replacements
        text, changes = self._apply_strategic_synonyms(text)
        all_changes.extend(changes)
        
        # Step 2: Subtle flow breaks
        text, changes = self._add_subtle_flow_breaks(text)
        all_changes.extend(changes)
        
        # Step 3: Controlled sentence variation
        text, changes = self._controlled_sentence_variation(text)
        all_changes.extend(changes)
        
        # Step 4: Light redundancy
        text, changes = self._add_light_redundancy(text)
        all_changes.extend(changes)
        
        # Calculate final similarity
        final_similarity = self._calculate_semantic_similarity(original_text, text)
        
        logger.info(f"✅ Enhanced WriteHuman complete - Similarity: {final_similarity:.3f}, Changes: {len(all_changes)}")
        
        return {
            "text": text,
            "similarity": final_similarity,
            "changes": all_changes,
            "aggressiveness_used": self.aggressiveness
        }

    def get_stats(self) -> Dict[str, any]:
        """Return processing statistics"""
        return {
            "aggressiveness": self.aggressiveness,
            "semantic_threshold": self.semantic_threshold,
            "replacement_count": len(self.strategic_replacements),
            "filler_count": len(self.subtle_fillers),
            "semantic_model_available": self.semantic_model is not None,
            "sentence_transformers_available": SENTENCE_TRANSFORMERS_AVAILABLE
        } 