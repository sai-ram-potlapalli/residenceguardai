import torch
from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import numpy as np
from typing import List, Dict, Any, Tuple
import os
from utils.config import config

class ObjectDetector:
    """CLIP-based object detection for violation identification."""
    
    _instance = None
    _model_loaded = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ObjectDetector, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._model_loaded:
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.model, self.processor = None, None
            
            # General objects that might be found in rooms
            self.general_objects = [
                # Furniture
                "bed", "desk", "chair", "table", "dresser", "bookshelf", "lamp", "mirror",
                "sofa", "couch", "nightstand", "wardrobe", "closet", "drawer",
                
                # Electronics
                "computer", "laptop", "phone", "television", "tv", "speaker", "headphones",
                "charger", "cable", "wire", "outlet", "switch", "light bulb",
                
                # Decorations
                "plant", "flower", "vase", "picture", "photo", "poster", "painting",
                "curtain", "blind", "rug", "carpet", "pillow", "blanket", "sheet",
                
                # Personal items
                "book", "notebook", "pen", "pencil", "bag", "backpack", "clothing",
                "shoes", "hat", "jewelry", "watch", "wallet", "keys",
                
                # Kitchen items
                "cup", "glass", "plate", "bowl", "utensil", "fork", "spoon", "knife",
                "bottle", "can", "container", "box", "bag", "food",
                
                # Bathroom items
                "towel", "soap", "toothbrush", "toothpaste", "shampoo", "conditioner",
                "mirror", "sink", "toilet", "shower", "bath",
                
                # Storage
                "box", "bin", "basket", "shelf", "rack", "hook", "hanger",
                "cabinet", "drawer", "container", "bag", "case",
                
                # Miscellaneous
                "clock", "calendar", "paper", "document", "folder", "binder",
                "scissors", "tape", "glue", "marker", "highlighter"
            ]
            
            # Violation-specific objects (higher priority)
            self.violation_objects = [
                # Prohibited items
                "candle", "lit candle", "burning candle", "incense", "incense stick",
                "vape", "vaping device", "e-cigarette", "electronic cigarette",
                "pet", "dog", "cat", "bird", "hamster", "fish tank", "aquarium",
                "alcohol", "beer bottle", "wine bottle", "liquor bottle",
                "drug paraphernalia", "bong", "pipe", "rolling papers",
                "weapon", "knife", "gun", "firearm", "sword",
                
                # Safety hazards
                "covered smoke detector", "smoke detector with cover",
                "open flame", "fire", "burning", "flame",
                "extension cord", "power strip", "overloaded outlet",
                "blocked exit", "blocked door", "blocked window",
                "damaged furniture", "broken furniture", "hole in wall",
                
                # Unauthorized appliances
                "microwave", "toaster", "toaster oven", "hot plate",
                "space heater", "heater", "electric heater",
                "air conditioner", "window unit", "portable ac",
                "refrigerator", "mini fridge", "freezer",
                "washing machine", "dryer", "dishwasher",
                
                # Behavioral violations
                "graffiti", "wall writing", "damaged wall",
                "unauthorized modification", "modified outlet",
                "excessive trash", "messy room", "cluttered room",
                "unauthorized furniture", "loft bed", "bunk bed",
                "unauthorized decoration", "posters covering walls"
            ]
            
            # Combine all objects for detection
            self.all_objects = self.violation_objects + self.general_objects
            
            self._load_model()
            ObjectDetector._model_loaded = True
    
    def _load_model(self):
        """Load the CLIP model using transformers."""
        try:
            print(f"Loading CLIP model on {self.device}...")
            model_name = "openai/clip-vit-base-patch32"
            self.model = CLIPModel.from_pretrained(model_name).to(self.device)
            self.processor = CLIPProcessor.from_pretrained(model_name)
            print("CLIP model loaded successfully!")
        except Exception as e:
            print(f"Error loading CLIP model: {e}")
            raise
    
    def detect_objects(self, image_path: str, confidence_threshold: float = 0.1) -> List[Dict[str, Any]]:
        """
        Detect objects in an image that might violate housing policies.
        
        Args:
            image_path: Path to the image file
            confidence_threshold: Minimum confidence score for detection
            
        Returns:
            List of detected objects with confidence scores
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Prepare inputs
            inputs = self.processor(
                text=self.all_objects,
                images=image,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits_per_image = outputs.logits_per_image
                probs = logits_per_image.softmax(dim=-1)
            
            # Get top matches
            top_indices = probs[0].argsort(descending=True)
            detected_objects = []
            
            # Debug: Print top 10 scores
            print(f"🔍 Debug: Top 10 object scores:")
            for i in range(min(10, len(top_indices))):
                idx = top_indices[i]
                confidence = probs[0][idx].item()
                print(f"   {i+1}. {self.all_objects[idx]}: {confidence:.4f}")
            
            for idx in top_indices:
                confidence = probs[0][idx].item()
                if confidence >= confidence_threshold:
                    detected_objects.append({
                        "object": self.all_objects[idx],
                        "confidence": confidence,
                        "category": self._categorize_object(self.all_objects[idx])
                    })
            
            print(f"📊 Found {len(detected_objects)} objects above threshold {confidence_threshold}")
            return detected_objects
            
        except Exception as e:
            print(f"Error in object detection: {e}")
            return []
    
    def _categorize_object(self, object_name: str) -> str:
        """Categorize detected objects into violation types or general categories."""
        object_lower = object_name.lower()
        
        # Check for violation categories first
        if any(word in object_lower for word in ["candle", "incense", "flame", "fire", "burning"]):
            return "Fire Hazard"
        elif any(word in object_lower for word in ["vape", "e-cigarette", "smoking"]):
            return "Smoking Violation"
        elif any(word in object_lower for word in ["pet", "dog", "cat", "bird", "hamster", "fish"]):
            return "Pet Violation"
        elif any(word in object_lower for word in ["alcohol", "beer", "wine", "liquor"]):
            return "Alcohol Violation"
        elif any(word in object_lower for word in ["weapon", "knife", "gun", "firearm"]):
            return "Weapon Violation"
        elif any(word in object_lower for word in ["smoke detector", "detector"]):
            return "Safety Violation"
        elif any(word in object_lower for word in ["microwave", "toaster", "heater", "appliance"]):
            return "Appliance Violation"
        elif any(word in object_lower for word in ["graffiti", "damage", "hole", "broken"]):
            return "Property Damage"
        
        # General object categories
        elif any(word in object_lower for word in ["bed", "desk", "chair", "table", "dresser", "bookshelf", "sofa", "couch"]):
            return "Furniture"
        elif any(word in object_lower for word in ["computer", "laptop", "phone", "television", "tv", "speaker", "headphones"]):
            return "Electronics"
        elif any(word in object_lower for word in ["plant", "flower", "vase", "picture", "photo", "poster", "painting"]):
            return "Decorations"
        elif any(word in object_lower for word in ["book", "notebook", "pen", "pencil", "bag", "backpack", "clothing"]):
            return "Personal Items"
        elif any(word in object_lower for word in ["cup", "glass", "plate", "bowl", "utensil", "fork", "spoon", "knife"]):
            return "Kitchen Items"
        elif any(word in object_lower for word in ["towel", "soap", "toothbrush", "toothpaste", "shampoo", "conditioner"]):
            return "Bathroom Items"
        elif any(word in object_lower for word in ["box", "bin", "basket", "shelf", "rack", "hook", "hanger"]):
            return "Storage"
        elif any(word in object_lower for word in ["clock", "calendar", "paper", "document", "folder", "binder"]):
            return "Office Items"
        else:
            return "Other"
    
    def get_detection_summary(self, detected_objects: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a summary of detected violations."""
        if not detected_objects:
            return {
                "violation_detected": False,
                "message": "No policy violations detected in the image.",
                "objects": []
            }
        
        # Group by category
        categories = {}
        for obj in detected_objects:
            category = obj["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(obj)
        
        # Get highest confidence object
        highest_confidence = max(detected_objects, key=lambda x: x["confidence"])
        
        return {
            "violation_detected": True,
            "message": f"Detected {highest_confidence['object']} (confidence: {highest_confidence['confidence']:.2%})",
            "objects": detected_objects,
            "categories": categories,
            "primary_violation": highest_confidence
        }
    
    def analyze_image_context(self, image_path: str) -> Dict[str, Any]:
        """Analyze the overall context of the image."""
        try:
            image = Image.open(image_path)
            
            # Basic image analysis
            width, height = image.size
            aspect_ratio = width / height
            
            # Determine room type based on image characteristics
            room_type = "unknown"
            if aspect_ratio > 1.5:
                room_type = "hallway or corridor"
            elif aspect_ratio < 0.7:
                room_type = "tall room or stairwell"
            else:
                room_type = "standard room"
            
            return {
                "image_size": (width, height),
                "aspect_ratio": aspect_ratio,
                "room_type": room_type,
                "file_size": os.path.getsize(image_path)
            }
            
        except Exception as e:
            return {"error": str(e)}

# Global detector instance
detector = ObjectDetector() 