import random
import re
import logging

logger = logging.getLogger(__name__)

class WriteHumanMimic:
    """
    Final-stage post-processor that mimics WriteHuman.ai's approach
    to reduce SurferSEO AI detection from 52% to <20%.
    
    Focuses on:
    - Reduced coherence smoothness
    - Simplified vocabulary/synonym downgrading  
    - Minor grammatical imperfections
    - Sentence length variety
    - Lower information density
    - Uncommon phrasing & mild awkwardness
    """
    
    def __init__(self, aggressiveness=0.4, seed=None):
        """
        Args:
            aggressiveness (float): 0.3 = subtle, 0.5 = stronger changes
            seed (int): For reproducibility in tests
        """
        self.aggressiveness = aggressiveness
        if seed is not None:
            random.seed(seed)
        
        # Academic -> Simpler synonym replacements
        self.synonym_downgrades = {
            "demonstrates": "shows",
            "facilitates": "helps",
            "establishes": "sets up",
            "encompasses": "includes",
            "constitutes": "makes up",
            "fosters": "encourages",
            "broadens": "widens",
            "perspectives": "views",
            "global": "world",
            "innovative": "new",
            "resilient": "tough",
            "essential": "very important",
            "particularly": "especially",
            "significantly": "a lot",
            "nevertheless": "but still",
            "furthermore": "also",
            "consequently": "so",
            "subsequently": "then",
            "optimization": "making better",
            "implementation": "putting in place",
            "consideration": "thinking about",
            "specification": "details",
            "utilization": "using",
            "enhancement": "improvement",
            "methodology": "method",
            "comprehensive": "complete",
            "fundamental": "basic",
            "substantial": "big",
            "remarkable": "great",
            "extraordinary": "amazing",
            "tremendous": "huge",
            "exceptional": "really good",
            "sophisticated": "advanced",
            "intricate": "complex",
            "predominant": "main",
            "intensive": "heavy",
            "extensive": "wide",
            "considerable": "quite a bit",
            "appropriate": "right",
            "sufficient": "enough",
            "inadequate": "not enough",
            "tremendous": "huge",
            "magnificent": "great",
            "spectacular": "amazing"
        }
        
        # Filler phrases to break smooth flow
        self.flow_breakers = [
            "in some cases",
            "you might say",
            "as it happens", 
            "if you think about it",
            "truth be told",
            "to be honest",
            "as a matter of fact",
            "believe it or not",
            "in my opinion",
            "from what I've seen",
            "if you ask me",
            "to put it simply",
            "in other words",
            "by the way",
            "come to think of it"
        ]
        
        # Redundancy phrases for lower information density
        self.redundancy_phrases = [
            "as mentioned before",
            "like I said",
            "in other words",
            "to put it another way",
            "what I mean is",
            "that is to say",
            "in simple terms",
            "basically"
        ]

    def _swap_synonyms(self, text):
        """Replace academic words with simpler alternatives"""
        for academic, simple in self.synonym_downgrades.items():
            if random.random() < self.aggressiveness:
                # Case-insensitive replacement with word boundaries
                pattern = rf"\b{re.escape(academic)}\b"
                text = re.sub(pattern, simple, text, flags=re.IGNORECASE)
        return text

    def _insert_flow_breakers(self, sentence):
        """Insert filler phrases to break smooth logical flow"""
        if random.random() < self.aggressiveness / 2:
            words = sentence.split()
            if len(words) > 5:  # Only break longer sentences
                # Insert at random position (not at start/end)
                pos = random.randint(2, len(words) - 2)
                filler = random.choice(self.flow_breakers)
                words.insert(pos, f"{filler},")
                return " ".join(words)
        return sentence

    def _add_redundancy(self, text):
        """Add redundant phrases to lower information density"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        enhanced = []
        
        for sentence in sentences:
            if random.random() < self.aggressiveness / 3:
                # Add redundancy phrase
                redundancy = random.choice(self.redundancy_phrases)
                sentence = f"{sentence.rstrip('.')}. {redundancy.capitalize()}, {sentence.lower()}"
            enhanced.append(sentence)
        
        return " ".join(enhanced)

    def _vary_sentence_length(self, text):
        """Create more sentence length variety (very short + very long)"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        varied = []
        
        for sentence in sentences:
            words = sentence.split()
            
            # Split long sentences randomly
            if len(words) > 15 and random.random() < self.aggressiveness:
                split_point = random.randint(len(words)//3, 2*len(words)//3)
                part1 = " ".join(words[:split_point]).rstrip('.,!?') + "."
                part2 = " ".join(words[split_point:])
                varied.extend([part1, part2])
            
            # Make some sentences very short
            elif len(words) > 8 and random.random() < self.aggressiveness / 2:
                # Take first few words as short sentence
                short_end = random.randint(3, 6)
                short = " ".join(words[:short_end]).rstrip('.,!?') + "."
                rest = " ".join(words[short_end:])
                varied.extend([short, rest])
            else:
                varied.append(sentence)
        
        return " ".join(varied)

    def _add_mild_imperfections(self, text):
        """Add very subtle grammatical imperfections"""
        # Occasionally remove articles
        if random.random() < self.aggressiveness / 4:
            text = re.sub(r'\bthe\s+(?=\w)', '', text, count=1)
        
        # Occasionally change "a" to "an" incorrectly (very subtle)
        if random.random() < self.aggressiveness / 5:
            text = re.sub(r'\ba\s+(?=[aeiou])', 'an ', text, count=1)
        
        return text

    def _uncommon_phrasing(self, text):
        """Replace common phrases with slightly awkward alternatives"""
        awkward_replacements = {
            r'\bin order to\b': 'so as to',
            r'\bas well as\b': 'along with',
            r'\bdue to the fact that\b': 'because of how',
            r'\bin addition to\b': 'besides',
            r'\bwith regard to\b': 'about',
            r'\bin terms of\b': 'when it comes to',
        }
        
        for pattern, replacement in awkward_replacements.items():
            if random.random() < self.aggressiveness / 3:
                text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text

    def process(self, text, min_words=0):
        """
        Apply WriteHuman-style processing to reduce SurferSEO detection
        
        Args:
            text (str): Input humanized text
            min_words (int): Skip processing if text is too short
            
        Returns:
            str: Enhanced text with WriteHuman-style quirks
        """
        if min_words and len(text.split()) < min_words:
            logger.info(f"Text too short ({len(text.split())} words), skipping WriteHuman processing")
            return text
        
        logger.info("🎭 Applying WriteHuman mimicry for SurferSEO evasion...")
        
        # Apply transformations in order
        text = self._swap_synonyms(text)
        text = self._vary_sentence_length(text)
        
        # Break into sentences for sentence-level processing
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        processed_sentences = []
        
        for sentence in sentences:
            sentence = self._insert_flow_breakers(sentence)
            processed_sentences.append(sentence)
        
        text = " ".join(processed_sentences)
        text = self._add_redundancy(text)
        text = self._add_mild_imperfections(text)
        text = self._uncommon_phrasing(text)
        
        logger.info("✅ WriteHuman mimicry complete")
        return text

    def get_stats(self):
        """Return processing statistics"""
        return {
            "aggressiveness": self.aggressiveness,
            "synonym_count": len(self.synonym_downgrades),
            "flow_breaker_count": len(self.flow_breakers)
        } 