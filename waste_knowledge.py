# ==========================================
# EcoScan - Waste Knowledge Base
# ==========================================

WASTE_INFO = {
    "Cardboard": {
        "category": "Paper & Cardboard",
        "recyclable": True,
        "action": "Recycle",
        "disposal": "Keep cardboard clean and dry, then place it in the paper/cardboard recycling stream.",
        "reuse": "Reuse boxes for storage, packaging, or organization.",
        "impact": "Recycling cardboard reduces the demand for virgin paper materials.",
        "eco_score": 9,
        "impact_points": 7,
        "landfill_risk": "Medium",
        "recovery_method": "Repulping & Cardboard Recycling"
    },

    "Food Organics": {
        "category": "Organic Waste",
        "recyclable": False,
        "action": "Compost",
        "disposal": "Separate food waste from recyclable materials and send it to an appropriate organic-waste or composting stream.",
        "reuse": "Suitable food scraps can be composted into a soil amendment.",
        "impact": "Proper organic-waste treatment can reduce landfill disposal and recover useful organic matter.",
        "eco_score": 9,
        "impact_points": 9,
        "landfill_risk": "High",
        "recovery_method": "Composting"
    },

    "Glass": {
        "category": "Glass",
        "recyclable": True,
        "action": "Recycle",
        "disposal": "Separate glass containers and follow the local glass-recycling collection rules.",
        "reuse": "Clean glass containers can sometimes be reused for storage.",
        "impact": "Glass can be recycled repeatedly without losing its basic material properties.",
        "eco_score": 9,
        "impact_points": 8,
        "landfill_risk": "Low",
        "recovery_method": "Crushing & Glass Remelting"
    },

    "Metal": {
        "category": "Metal",
        "recyclable": True,
        "action": "Recycle",
        "disposal": "Separate metal items and place them in the appropriate metal-recycling stream.",
        "reuse": "Some metal containers can be reused after proper cleaning.",
        "impact": "Metal recycling can reduce the need for extracting and processing new raw materials.",
        "eco_score": 10,
        "impact_points": 10,
        "landfill_risk": "Medium",
        "recovery_method": "Metal Recycling"
    },

    "Miscellaneous Trash": {
        "category": "Mixed / Other Waste",
        "recyclable": False,
        "action": "Check Local Waste Rules",
        "disposal": "This category contains materials that may require additional identification before disposal.",
        "reuse": "Check whether the item can be repaired, reused, or separated into recyclable materials.",
        "impact": "Correct sorting prevents potentially recyclable materials from being unnecessarily landfilled.",
        "eco_score": 5,
        "impact_points": 4,
        "landfill_risk": "High",
        "recovery_method": "Waste-to-Energy / Landfill"
    },

    "Paper": {
        "category": "Paper",
        "recyclable": True,
        "action": "Recycle",
        "disposal": "Keep paper clean and dry and place it in the appropriate paper-recycling stream.",
        "reuse": "Reuse one-sided sheets for notes, drafts, or packaging.",
        "impact": "Paper recycling helps reduce demand for virgin fiber and can save resources.",
        "eco_score": 9,
        "impact_points": 7,
        "landfill_risk": "Medium",
        "recovery_method": "Paper Pulping & Recycling"
    },

    "Plastic": {
        "category": "Plastic",
        "recyclable": True,
        "action": "Recycle",
        "disposal": "Check the local recycling rules and separate accepted plastic items from general waste.",
        "reuse": "Clean suitable plastic containers can sometimes be reused for storage.",
        "impact": "Recovering plastic through recycling can reduce demand for new plastic production and prevent waste from entering the environment.",
        "eco_score": 8,
        "impact_points": 8,
        "landfill_risk": "High",
        "recovery_method": "Mechanical Recycling"

    },

    "Textile Trash": {
        "category": "Textile",
        "recyclable": False,
        "action": "Reuse / Textile Collection",
        "disposal": "Donate, repair, reuse, or use a textile-collection service when available.",
        "reuse": "Old textiles can be reused as cleaning cloths or repurposed into other items.",
        "impact": "Extending textile life reduces the amount of material sent to landfill.",
        "eco_score": 8,
        "impact_points": 6,
        "landfill_risk": "Medium",
        "recovery_method": "Textile Shredding & Fiber Recovery"
    },

    "Vegetation": {
        "category": "Green Organic Waste",
        "recyclable": False,
        "action": "Compost",
        "disposal": "Separate plant material and use an appropriate composting or organic-waste pathway.",
        "reuse": "Plant material can be composted to recover organic matter.",
        "impact": "Composting can return organic matter to the soil and reduce landfill disposal.",
        "eco_score": 9,
        "impact_points": 9,
        "landfill_risk": "Low",
        "recovery_method": "Aerobic Composting & Anaerobic Digestion"
    }

}



def get_waste_info(waste_name):
    """
    Return information about a detected waste category.
    """

    return WASTE_INFO.get(
        waste_name,
        {
            "category": "Unknown",
            "recyclable": False,
            "action": "Manual Review",
            "disposal": "Please inspect the item manually before disposal.",
            "reuse": "Check whether the item can be reused.",
            "impact": "No reliable environmental information is available for this category.",
            "eco_score": 0
        }
    )
# ==========================================
# Biotechnology Information
# ==========================================

def get_biotech_info(waste_type):

    organic_waste = [
        "Food Organics",
        "Vegetation"
    ]

    if waste_type in organic_waste:

        return {
            "is_organic": True,
            "title": "🧬 Biological Treatment",
            "process": (
                "Organic Waste → Separation → "
                "Biological Treatment → Composting → "
                "Organic Matter Recovery"
            ),
            "explanation": (
                "Microorganisms can naturally decompose "
                "organic waste and convert biodegradable "
                "material into more stable organic matter."
            )
        }

    return {
        "is_organic": False,
        "title": "🧬 Biotechnology Pathway",
        "process": "No biological treatment pathway is recommended.",
        "explanation": (
            "This waste category is not primarily "
            "biodegradable organic waste."
        )
    }
def calculate_eco_points(
    action,
    eco_score
):

    points = 0

    if action == "Recycle":
        points += 10

    elif action == "Compost":
        points += 12

    elif "Reuse" in action:
        points += 8

    points += eco_score

    return points