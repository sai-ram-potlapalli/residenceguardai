import json
import requests
from typing import List, Dict, Any
from utils.config import config
from modules.object_detection import detector
from modules.pdf_parser import parser
from utils.helpers import extract_confidence

class ViolationChecker:
    """LLM-based violation assessment system."""
    
    def __init__(self):
        # Initialize HuggingFace client only
        self.hf_api_key = config.HUGGINGFACE_API_TOKEN
        self.hf_model = config.LLM_MODEL_NAME
    
    def hf_chat_completion(self, prompt: str, max_tokens: int = 512, temperature: float = 0.1) -> str:
        """Call HuggingFace Inference API for text generation."""
        url = f"https://api-inference.huggingface.co/models/{self.hf_model}"
        headers = {
            "Authorization": f"Bearer {self.hf_api_key}",
            "Content-Type": "application/json"
        }
        
        # Format prompt for instruction-following models
        # Different models use different formats, so we'll try a generic approach
        formatted_prompt = f"""<|system|>
You are an expert housing policy compliance officer. Your job is to assess whether detected objects in a residence hall room violate any housing policies. 

You must:
1. Carefully analyze each detected object against the provided policy rules
2. Determine if there's a clear violation
3. Provide a confidence level (0.0 to 1.0) for your assessment
4. Recommend appropriate action
5. Be conservative - if you're unsure, mark as potential violation for human review

Respond in JSON format with the following structure:
{{
    "violation_found": boolean,
    "message": "clear explanation of your assessment",
    "confidence": float (0.0-1.0),
    "recommended_action": "specific action to take",
    "violating_objects": ["list of objects that violate policy"],
    "matching_rules": ["list of specific rules that were violated"],
    "severity": "low/medium/high"
}}
</s>
<|user|>
{prompt}
</s>
<|assistant|>"""
        
        payload = {
            "inputs": formatted_prompt,
            "parameters": {
                "max_new_tokens": max_tokens,
                "temperature": temperature,
                "return_full_text": False,
                "do_sample": True,
                "top_p": 0.9
            }
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()
            
            # Extract generated text from response
            if isinstance(result, list) and len(result) > 0:
                if "generated_text" in result[0]:
                    return result[0]["generated_text"]
                elif "generated_text" in result:
                    return result["generated_text"]
            elif isinstance(result, dict):
                if "generated_text" in result:
                    return result["generated_text"]
                elif "error" in result:
                    raise RuntimeError(f"HuggingFace API error: {result['error']}")
            
            # Fallback: return the raw result
            return str(result)
            
        except requests.exceptions.RequestException as e:
            print(f"Error calling HuggingFace API: {e}")
            raise
    
    def assess_violation(self, detected_objects: List[Dict[str, Any]], 
                        policy_rules: List[Dict[str, Any]], 
                        image_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Assess whether detected objects violate any policy rules.
        
        Args:
            detected_objects: List of objects detected in the image
            policy_rules: List of relevant policy rules from PDF
            image_context: Additional context about the image
            
        Returns:
            Violation assessment result
        """
        # Debug: Print what we're checking
        print(f"🔍 DEBUG: Checking {len(detected_objects)} detected objects for violations")
        for i, obj in enumerate(detected_objects):
            print(f"   {i+1}. {obj.get('object', 'Unknown')} (confidence: {obj.get('confidence', 0):.3f}, category: {obj.get('category', 'Unknown')})")
        
        if not detected_objects:
            return {
                "violation_found": False,
                "message": "No objects detected that require policy assessment.",
                "confidence": 1.0,
                "recommended_action": "No action required"
            }
        
        # First, check for hardcoded violations (fallback system)
        print("🔍 DEBUG: Checking hardcoded violations...")
        hardcoded_violations = self._check_hardcoded_violations(detected_objects)
        print(f"🔍 DEBUG: Hardcoded violation result: {hardcoded_violations['violation_found']}")
        
        if hardcoded_violations["violation_found"]:
            print("🚨 DEBUG: Hardcoded violation detected!")
            return hardcoded_violations
        
        if not policy_rules:
            return {
                "violation_found": False,
                "message": "No policy rules available for assessment.",
                "confidence": 0.0,
                "recommended_action": "Upload policy document for assessment"
            }
        
        # Prepare the assessment prompt
        prompt = self._create_assessment_prompt(detected_objects, policy_rules, image_context)
        
        try:
            # Use HuggingFace API
            if self.hf_api_key:
                content = self.hf_chat_completion(prompt)
            else:
                raise RuntimeError("No HuggingFace API key configured")
            
            # Parse the response
            try:
                # Try to extract JSON from the response
                # Look for JSON-like content in the response
                import re
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    json_str = json_match.group()
                    result = json.loads(json_str)
                else:
                    # If no JSON found, try parsing the whole response
                    result = json.loads(content)
                return result
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return self._parse_text_response(content)
                
        except Exception as e:
            print(f"Error in violation assessment: {e}")
            return {
                "violation_found": False,
                "message": f"Error during assessment: {str(e)}",
                "confidence": 0.0,
                "recommended_action": "Manual review required"
            }
    
    def _check_hardcoded_violations(self, detected_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Check for common violations using hardcoded rules as a fallback."""
        
        # Define common violations
        fire_hazards = {
            "candle", "candles", "lighter", "lighters", "matches", "match", 
            "incense", "incense stick", "burner", "burners", "torch", "torches",
            "firework", "fireworks", "sparkler", "sparklers"
        }
        
        prohibited_appliances = {
            "microwave", "toaster", "toaster oven", "hot plate", "hotplate", 
            "electric kettle", "kettle", "coffee maker", "coffeemaker",
            "rice cooker", "slow cooker", "crock pot", "crockpot",
            "air fryer", "airfryer", "grill", "grills", "panini press"
        }
        
        alcohol_items = {
            "beer", "wine", "liquor", "alcohol", "bottle", "bottles",
            "can", "cans", "drink", "drinks", "beverage", "beverages"
        }
        
        smoking_items = {
            "cigarette", "cigarettes", "cigar", "cigars", "pipe", "pipes",
            "vape", "vaping", "e-cigarette", "ecig", "hookah", "hookahs"
        }
        
        weapons = {
            "weapon", "weapons", "knife", "knives", "gun", "guns", "firearm", "firearms",
            "sword", "swords", "dagger", "daggers", "blade", "blades", "machete", "machetes",
            "axe", "axes", "bat", "bats", "club", "clubs", "brass knuckles", "knuckles",
            "taser", "tasers", "pepper spray", "mace", "stun gun", "stungun"
        }
        
        violating_objects = []
        matching_rules = []
        
        print(f"🔍 DEBUG: Checking {len(detected_objects)} objects against hardcoded rules")
        
        for obj in detected_objects:
            object_name = obj.get('object', '').lower()
            object_category = obj.get('category', '').lower()
            
            print(f"🔍 DEBUG: Checking object '{object_name}' (category: '{object_category}')")
            
            # Check weapons (highest priority)
            if object_name in weapons or any(weapon in object_name for weapon in weapons):
                print(f"🚨 DEBUG: WEAPON DETECTED: '{object_name}' matches weapon rules!")
                violating_objects.append(obj['object'])
                matching_rules.append("Weapon policy - weapons and dangerous items are strictly prohibited")
            
            # Check fire hazards
            elif object_name in fire_hazards or any(hazard in object_name for hazard in fire_hazards):
                print(f"🚨 DEBUG: FIRE HAZARD DETECTED: '{object_name}' matches fire hazard rules!")
                violating_objects.append(obj['object'])
                matching_rules.append("Fire safety policy - open flames and candles are prohibited")
            
            # Check prohibited appliances
            elif object_name in prohibited_appliances or any(appliance in object_name for appliance in prohibited_appliances):
                print(f"🚨 DEBUG: PROHIBITED APPLIANCE DETECTED: '{object_name}' matches appliance rules!")
                violating_objects.append(obj['object'])
                matching_rules.append("Appliance policy - cooking appliances are not allowed in residence halls")
            
            # Check alcohol
            elif object_name in alcohol_items or any(alcohol in object_name for alcohol in alcohol_items):
                print(f"🚨 DEBUG: ALCOHOL DETECTED: '{object_name}' matches alcohol rules!")
                violating_objects.append(obj['object'])
                matching_rules.append("Alcohol policy - alcoholic beverages are not permitted")
            
            # Check smoking items
            elif object_name in smoking_items or any(smoking in object_name for smoking in smoking_items):
                print(f"🚨 DEBUG: SMOKING ITEM DETECTED: '{object_name}' matches smoking rules!")
                violating_objects.append(obj['object'])
                matching_rules.append("Smoking policy - tobacco and vaping products are prohibited")
            else:
                print(f"✅ DEBUG: No violation detected for '{object_name}'")
        
        print(f"🔍 DEBUG: Found {len(violating_objects)} violating objects: {violating_objects}")
        
        if violating_objects:
            return {
                "violation_found": True,
                "message": f"🚨 CRITICAL POLICY VIOLATION DETECTED: {', '.join(violating_objects)} are strictly prohibited in residence halls.",
                "confidence": 0.99,
                "recommended_action": "IMMEDIATE REMOVAL REQUIRED - Contact campus security immediately",
                "violating_objects": violating_objects,
                "matching_rules": list(set(matching_rules)),  # Remove duplicates
                "severity": "critical"
            }
        
        return {
            "violation_found": False,
            "message": "No hardcoded violations detected.",
            "confidence": 0.8,
            "recommended_action": "Continue with policy assessment"
        }
    
    def _create_assessment_prompt(self, detected_objects: List[Dict[str, Any]], 
                                 policy_rules: List[Dict[str, Any]], 
                                 image_context: Dict[str, Any] = None) -> str:
        """Create a detailed prompt for violation assessment."""
        
        # Format detected objects
        objects_text = "\n".join([
            f"- {obj['object']} (confidence: {extract_confidence(obj['confidence']):.2%}, category: {obj['category']})"
            for obj in detected_objects
        ])
        
        # Format policy rules - escape any curly braces to avoid formatting conflicts
        rules_text = "\n".join([
            f"- {rule['rule_text'].replace('{', '{{').replace('}', '}}')}"
            for rule in policy_rules
        ])
        
        # Format image context
        context_text = ""
        if image_context:
            context_text = f"\nImage Context: {image_context.get('room_type', 'unknown room type')}"
        
        prompt = f"""
Please assess whether the following objects detected in a residence hall room violate any housing policies.

DETECTED OBJECTS:
{objects_text}

POLICY RULES:
{rules_text}
{context_text}

Please analyze each detected object against the policy rules and determine if there are any violations. Consider:
1. Whether the object is explicitly prohibited
2. Whether it poses a safety hazard
3. Whether it violates appliance or equipment policies
4. The context and severity of any violations

Provide your assessment in the specified JSON format.
"""
        return prompt
    
    def _parse_text_response(self, text: str) -> Dict[str, Any]:
        """Parse a text response when JSON parsing fails."""
        # Simple parsing logic for fallback
        violation_found = any(word in text.lower() for word in ["violation", "prohibited", "not allowed"])
        confidence = 0.5  # Default confidence
        
        return {
            "violation_found": violation_found,
            "message": text,
            "confidence": confidence,
            "recommended_action": "Manual review recommended",
            "severity": "medium"
        }
    
    def get_violation_summary(self, assessment_result: Dict[str, Any]) -> str:
        """Generate a human-readable summary of the violation assessment."""
        if not assessment_result.get("violation_found", False):
            return assessment_result.get("message", "No violations detected.")
        
        summary_parts = []
        
        # Add violation status
        summary_parts.append("🚨 POLICY VIOLATION DETECTED")
        
        # Add violating objects
        if "violating_objects" in assessment_result:
            objects = assessment_result["violating_objects"]
            if isinstance(objects, list) and objects:
                summary_parts.append(f"Violating objects: {', '.join(objects)}")
        
        # Add matching rules
        if "matching_rules" in assessment_result:
            rules = assessment_result["matching_rules"]
            if isinstance(rules, list) and rules:
                summary_parts.append(f"Policy rules violated: {', '.join(rules[:2])}")  # Show first 2 rules
        
        # Add severity
        severity = assessment_result.get("severity", "medium")
        summary_parts.append(f"Severity: {severity.upper()}")
        
        # Add confidence
        confidence = assessment_result.get("confidence", 0.0)
        summary_parts.append(f"Confidence: {extract_confidence(confidence):.1%}")
        
        # Add recommended action
        action = assessment_result.get("recommended_action", "Review required")
        summary_parts.append(f"Recommended action: {action}")
        
        return "\n".join(summary_parts)
    
    def check_single_object(self, object_name: str, object_category: str, 
                           confidence: float) -> Dict[str, Any]:
        """Check a single object against policy rules."""
        # Search for relevant rules
        query = f"{object_name} {object_category}"
        relevant_rules = parser.search_relevant_rules(query, n_results=3)
        
        # Create a mock detected object
        detected_object = {
            "object": object_name,
            "category": object_category,
            "confidence": confidence
        }
        
        return self.assess_violation([detected_object], relevant_rules)
    
    def get_compliance_report(self, image_path: str, pdf_path: str) -> Dict[str, Any]:
        """Generate a comprehensive compliance report for an image and policy document."""
        try:
            # Detect objects
            detected_objects = detector.detect_objects(image_path)
            detection_summary = detector.get_detection_summary(detected_objects)
            
            # Extract and index policy rules
            policy_summary = parser.get_policy_summary(pdf_path)
            parser.index_policy_rules(pdf_path, "uploaded_policy")
            
            # Search for relevant rules
            relevant_rules = []
            if detected_objects:
                for obj in detected_objects:
                    query = f"{obj['object']} {obj['category']}"
                    rules = parser.search_relevant_rules(query, n_results=2)
                    relevant_rules.extend(rules)
            
            # Remove duplicates
            unique_rules = []
            seen_texts = set()
            for rule in relevant_rules:
                if rule["rule_text"] not in seen_texts:
                    seen_texts.add(rule["rule_text"])
                    unique_rules.append(rule)
            
            # Assess violations
            image_context = detector.analyze_image_context(image_path)
            violation_assessment = self.assess_violation(detected_objects, unique_rules, image_context)
            
            return {
                "image_analysis": {
                    "detected_objects": detected_objects,
                    "detection_summary": detection_summary,
                    "image_context": image_context
                },
                "policy_analysis": {
                    "policy_summary": policy_summary,
                    "relevant_rules": unique_rules
                },
                "violation_assessment": violation_assessment,
                "compliance_status": "compliant" if not violation_assessment.get("violation_found", False) else "non_compliant"
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "compliance_status": "error"
            }

# Global checker instance
checker = ViolationChecker() 