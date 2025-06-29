import fitz  # PyMuPDF
import pdfplumber
import re
from typing import List, Dict, Any, Optional
from utils.helpers import clean_text, chunk_text

class PDFParser:
    """PDF parser for extracting and indexing housing policy rules."""
    
    def __init__(self):
        self.policy_rules = []
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize the parser components."""
        try:
            print("PDF Parser initialized successfully")
        except Exception as e:
            print(f"Error initializing PDF parser components: {e}")
            raise
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text content from PDF using multiple methods."""
        text_content = ""
        
        # Method 1: Try PyMuPDF first
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text_content += page.get_text()
            doc.close()
        except Exception as e:
            print(f"PyMuPDF extraction failed: {e}")
        
        # Method 2: Fallback to pdfplumber if PyMuPDF fails
        if not text_content.strip():
            try:
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text_content += page_text + "\n"
            except Exception as e:
                print(f"pdfplumber extraction failed: {e}")
        
        return clean_text(text_content)
    
    def extract_policy_rules(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract policy rules from PDF content."""
        text_content = self.extract_text_from_pdf(pdf_path)
        if not text_content:
            return []
        
        # Split text into chunks
        chunks = chunk_text(text_content, chunk_size=500, overlap=100)
        
        # Extract rules using pattern matching
        rules = []
        rule_patterns = [
            r'(?:prohibited|not allowed|forbidden|banned|restricted)[^.]*\.',
            r'(?:violation|violate|against policy)[^.]*\.',
            r'(?:must not|cannot|shall not|may not)[^.]*\.',
            r'(?:required|mandatory|must)[^.]*\.',
            r'(?:safety|fire|security)[^.]*\.',
            r'(?:appliance|equipment|device)[^.]*\.',
            r'(?:pet|animal|pet policy)[^.]*\.',
            r'(?:alcohol|drinking|beverage)[^.]*\.',
            r'(?:smoking|tobacco|vape)[^.]*\.',
            r'(?:candle|flame|fire|burning)[^.]*\.',
        ]
        
        for i, chunk in enumerate(chunks):
            for pattern in rule_patterns:
                matches = re.finditer(pattern, chunk, re.IGNORECASE)
                for match in matches:
                    rule_text = match.group().strip()
                    if len(rule_text) > 20:  # Filter out very short matches
                        rules.append({
                            "rule_text": rule_text,
                            "chunk_index": i,
                            "start_pos": match.start(),
                            "end_pos": match.end(),
                            "pattern_matched": pattern
                        })
        
        # Remove duplicates and sort by relevance
        unique_rules = []
        seen_texts = set()
        
        for rule in rules:
            normalized_text = re.sub(r'\s+', ' ', rule["rule_text"].lower())
            if normalized_text not in seen_texts:
                seen_texts.add(normalized_text)
                unique_rules.append(rule)
        
        return unique_rules
    
    def parse_policy_document(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Parse policy document and return extracted rules."""
        return self.extract_policy_rules(pdf_path)
    
    def extract_rules_from_text(self, text: str) -> List[Dict[str, Any]]:
        """Extract rules from plain text content."""
        if not text:
            return []
        
        # Split text into chunks
        chunks = chunk_text(text, chunk_size=500, overlap=100)
        
        # Extract rules using pattern matching
        rules = []
        rule_patterns = [
            r'(?:prohibited|not allowed|forbidden|banned|restricted)[^.]*\.',
            r'(?:violation|violate|against policy)[^.]*\.',
            r'(?:must not|cannot|shall not|may not)[^.]*\.',
            r'(?:required|mandatory|must)[^.]*\.',
            r'(?:safety|fire|security)[^.]*\.',
            r'(?:appliance|equipment|device)[^.]*\.',
            r'(?:pet|animal|pet policy)[^.]*\.',
            r'(?:alcohol|drinking|beverage)[^.]*\.',
            r'(?:smoking|tobacco|vape)[^.]*\.',
            r'(?:candle|flame|fire|burning)[^.]*\.',
        ]
        
        for i, chunk in enumerate(chunks):
            for pattern in rule_patterns:
                matches = re.finditer(pattern, chunk, re.IGNORECASE)
                for match in matches:
                    rule_text = match.group().strip()
                    if len(rule_text) > 20:  # Filter out very short matches
                        rules.append({
                            "rule_text": rule_text,
                            "chunk_index": i,
                            "start_pos": match.start(),
                            "end_pos": match.end(),
                            "pattern_matched": pattern
                        })
        
        return rules
    
    def index_policy_rules(self, pdf_path: str, pdf_name: str = "policy_document") -> bool:
        """Index policy rules in memory storage."""
        try:
            # Extract rules
            rules = self.extract_policy_rules(pdf_path)
            if not rules:
                print("No policy rules found in the PDF")
                return False
            
            # Store rules in memory
            for i, rule in enumerate(rules):
                rule_id = f"{pdf_name}_{i}"
                self.policy_rules.append({
                    "id": rule_id,
                    "rule_text": rule["rule_text"],
                    "metadata": {
                        "pdf_name": pdf_name,
                        "chunk_index": rule["chunk_index"],
                        "pattern": rule["pattern_matched"],
                        "rule_type": self._categorize_rule(rule["rule_text"])
                    }
                })
            
            print(f"Indexed {len(rules)} policy rules from {pdf_name}")
            return True
            
        except Exception as e:
            print(f"Error indexing policy rules: {e}")
            return False
    
    def search_relevant_rules(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for policy rules relevant to a query using simple text matching."""
        try:
            query_lower = query.lower()
            relevant_rules = []
            
            for rule in self.policy_rules:
                rule_text_lower = rule["rule_text"].lower()
                # Simple keyword matching
                if any(word in rule_text_lower for word in query_lower.split()):
                    relevant_rules.append({
                        "rule_text": rule["rule_text"],
                        "metadata": rule["metadata"],
                        "relevance_score": self._calculate_relevance(query_lower, rule_text_lower)
                    })
            
            # Sort by relevance and return top results
            relevant_rules.sort(key=lambda x: x["relevance_score"], reverse=True)
            return relevant_rules[:n_results]
            
        except Exception as e:
            print(f"Error searching rules: {e}")
            return []
    
    def _calculate_relevance(self, query: str, rule_text: str) -> float:
        """Calculate simple relevance score based on word overlap."""
        query_words = set(query.split())
        rule_words = set(rule_text.split())
        
        if not query_words:
            return 0.0
        
        overlap = len(query_words.intersection(rule_words))
        return overlap / len(query_words)
    
    def _categorize_rule(self, rule_text: str) -> str:
        """Categorize a policy rule based on its content."""
        text_lower = rule_text.lower()
        
        if any(word in text_lower for word in ["fire", "flame", "candle", "burning", "smoke"]):
            return "Fire Safety"
        elif any(word in text_lower for word in ["pet", "animal", "dog", "cat"]):
            return "Pet Policy"
        elif any(word in text_lower for word in ["alcohol", "drinking", "beer", "wine"]):
            return "Alcohol Policy"
        elif any(word in text_lower for word in ["smoking", "tobacco", "vape", "cigarette"]):
            return "Smoking Policy"
        elif any(word in text_lower for word in ["appliance", "microwave", "toaster", "heater"]):
            return "Appliance Policy"
        elif any(word in text_lower for word in ["noise", "quiet", "loud", "disturbance"]):
            return "Noise Policy"
        elif any(word in text_lower for word in ["guest", "visitor", "overnight"]):
            return "Guest Policy"
        elif any(word in text_lower for word in ["damage", "property", "furniture", "wall"]):
            return "Property Policy"
        else:
            return "General Policy"
    
    def get_policy_summary(self, pdf_path: str) -> Dict[str, Any]:
        """Generate a summary of the policy document."""
        try:
            text_content = self.extract_text_from_pdf(pdf_path)
            rules = self.extract_policy_rules(pdf_path)
            
            # Count rules by category
            categories = {}
            for rule in rules:
                category = self._categorize_rule(rule["rule_text"])
                if category not in categories:
                    categories[category] = 0
                categories[category] += 1
            
            return {
                "total_rules": len(rules),
                "categories": categories,
                "document_length": len(text_content),
                "rules_extracted": rules[:10]  # First 10 rules as examples
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def clear_database(self):
        """Clear all indexed policy rules."""
        try:
            self.policy_rules = []
            print("Policy rules database cleared")
        except Exception as e:
            print(f"Error clearing database: {e}")

# Global parser instance
parser = PDFParser() 