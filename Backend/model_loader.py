import os
import random

# --- 1. AI Classification Module ---
def classify_image(filepath):
    """
    Analyzes the image and returns:
    1. Category (E-Waste, Plastic, etc.)
    2. Confidence Score (e.g., 92%)
    3. Components (e.g., Copper Coil, Circuit Board)
    """
    filename = os.path.basename(filepath).lower()

    # DEMO LOGIC: We map filenames to categories to ensure the presentation goes smoothly.
    # In a full production app, this is where 'model.predict()' would go.
    
    if any(x in filename for x in ['phone', 'laptop', 'mouse', 'keyboard', 'wire', 'electronic']):
        return "E-Waste", "92%", ["Plastic Shell", "Copper Coil", "Metal Frame", "Circuit Board"]
    
    elif any(x in filename for x in ['bottle', 'cup', 'jug', 'plastic']):
        return "Plastic", "96%", ["PET Plastic", "HDPE Cap", "Label Wrapper"]
    
    elif any(x in filename for x in ['can', 'tin', 'metal', 'iron', 'spoon']):
        return "Metal", "89%", ["Aluminum Body", "Steel Rim"]
    
    elif any(x in filename for x in ['shirt', 'cloth', 'jeans', 'fabric']):
        return "Cloth", "94%", ["Cotton Fiber", "Synthetic Button", "Polyester Thread"]
    
    else:
        # Default fallback if the system is unsure
        return "E-Waste", "85%", ["Mixed Materials", "Circuit Component"]

# --- 2. Recommendation Engine ---
def get_recommendation_logic(label, condition="Good"):
    """
    Decides whether to Sell, Donate, or Recycle based on Category.
    """
    if label == "E-Waste":
        return {
            "action": "Recycle / Sell",
            "desc": "This item contains valuable metals like gold and copper. Do not dispose of in regular trash.",
            "guideline": "Ensure all personal data is wiped before handing over.",
            "centers": get_nearby_centers("Recycler")
        }
    elif label == "Cloth":
        if condition == "Good":
            return {
                "action": "Donate",
                "desc": "This item appears to be in good condition. Local shelters are accepting clothing.",
                "guideline": "Wash and fold the item before donation.",
                "centers": get_nearby_centers("NGO")
            }
        else:
            return {
                "action": "Recycle",
                "desc": "The fabric is worn out. It can be shredded for textile recycling.",
                "guideline": "Remove buttons and zippers if possible.",
                "centers": get_nearby_centers("Recycler")
            }
    elif label == "Plastic":
        return {
            "action": "Recycle",
            "desc": "High-grade plastic. Can be processed into new materials.",
            "guideline": "Rinse the item and crush it to save space.",
            "centers": get_nearby_centers("Recycler")
        }
    else:
        return {
            "action": "Dispose Responsibly",
            "desc": "Check local municipal guidelines for this item.",
            "guideline": "Segregate from wet waste.",
            "centers": get_nearby_centers("Scrap Dealer")
        }

# --- 3. Resource Mapping (Mock DB) ---
def get_nearby_centers(center_type):
    """
    Returns a list of centers based on the type needed.
    Matches the 'Nearby Centers' screenshot in your report.
    """
    all_centers = [
        {"name": "GreenCycle Solutions", "type": "Recycler", "dist": "2.5 km", "lat": 22.7, "lng": 75.8},
        {"name": "EcoWaste Management", "type": "Scrap Dealer", "dist": "4.1 km", "lat": 22.8, "lng": 75.9},
        {"name": "Hope Foundation", "type": "NGO", "dist": "1.2 km", "lat": 22.6, "lng": 75.7},
        {"name": "City Recycling Unit", "type": "Recycler", "dist": "6.8 km", "lat": 22.9, "lng": 75.6}
    ]
    
    # Filter list based on what we are looking for (Recycler, NGO, etc.)
    if center_type == "Recycler":
        return [c for c in all_centers if c['type'] == 'Recycler']
    elif center_type == "NGO":
        return [c for c in all_centers if c['type'] == 'NGO']
    else:
        return all_centers[:3] # Return top 3 mixed