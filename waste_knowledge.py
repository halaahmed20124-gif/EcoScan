# ============================================================
# EcoScan - Expanded Waste Knowledge Base
# ============================================================

WASTE_INFO = {

    # ========================================================
    # 1. CARDBOARD
    # ========================================================

    "Cardboard": {

        "category": "Paper & Cardboard",
        "recyclable": True,
        "action": "Recycle",

        "disposal":
            "Keep cardboard clean and dry and place it in "
            "the appropriate paper/cardboard recycling stream.",

        "disposal_options": [
            "Paper/cardboard recycling",
            "Community recycling collection",
            "School or university recycling points",
            "Reuse before recycling"
        ],

        "reuse":
            "Reuse boxes for storage, packaging, organization, "
            "moving, crafts, or educational projects.",

        "reuse_options": [
            "Storage boxes",
            "Packaging material",
            "Drawer organizers",
            "Moving boxes",
            "School projects",
            "Craft materials"
        ],

        "recycling_options": [
            "Repulping and paper fiber recovery",
            "Cardboard recycling",
            "Manufacturing recycled paper products",
            "Manufacturing new cardboard packaging"
        ],

        "preparation_steps": [
            "Keep cardboard dry",
            "Remove food contamination",
            "Remove plastic wrapping when possible",
            "Flatten large boxes",
            "Separate from general waste"
        ],

        "avoid": [
            "Do not recycle heavily food-contaminated cardboard",
            "Do not mix wet cardboard with dry recyclable paper"
        ],

        "impact":
            "Recycling cardboard reduces demand for virgin paper "
            "materials and helps recover useful fiber.",

        "environmental_benefits": [
            "Reduces virgin fiber demand",
            "Reduces landfill waste",
            "Supports material recovery",
            "Extends the useful life of paper fibers"
        ],

        "eco_score": 9,
        "impact_points": 7,
        "landfill_risk": "Medium",

        "recovery_method":
            "Repulping & Cardboard Recycling",

        "examples": [
            "Shipping boxes",
            "Cereal boxes",
            "Packaging cartons",
            "Corrugated cardboard"
        ],

        "biotech_options": [
            "Biological fiber treatment may be possible",
            "Fiber recovery through paper recycling is preferred"
        ]
    },


    # ========================================================
    # 2. FOOD ORGANICS
    # ========================================================

    "Food Organics": {

        "category": "Organic Waste",
        "recyclable": False,
        "action": "Compost",

        "disposal":
            "Separate food waste from recyclable materials and "
            "send it to an appropriate organic-waste or composting stream.",

        "disposal_options": [
            "Composting",
            "Community organic-waste collection",
            "Industrial composting",
            "Anaerobic digestion",
            "Organic waste treatment facilities"
        ],

        "reuse":
            "Suitable food scraps can be composted or processed "
            "through biological treatment to recover organic matter.",

        "reuse_options": [
            "Home composting where appropriate",
            "Community composting",
            "Composting facilities",
            "Organic matter recovery"
        ],

        "recycling_options": [
            "Composting",
            "Anaerobic digestion",
            "Biological treatment",
            "Organic matter recovery",
            "Biogas production through anaerobic digestion"
        ],

        "preparation_steps": [
            "Separate food waste from plastics and metals",
            "Remove non-organic contamination",
            "Use a suitable organic-waste container",
            "Keep hazardous materials out of the organic stream"
        ],

        "avoid": [
            "Do not mix food waste with recyclable paper",
            "Do not place batteries or chemicals in organic waste",
            "Do not contaminate compost with plastics"
        ],

        "impact":
            "Proper organic-waste treatment can reduce landfill "
            "disposal and recover useful organic matter.",

        "environmental_benefits": [
            "Reduces landfill disposal",
            "Recovers organic matter",
            "Can produce compost",
            "Can support soil improvement",
            "Anaerobic digestion can recover biogas"
        ],

        "eco_score": 9,
        "impact_points": 9,
        "landfill_risk": "High",

        "recovery_method":
            "Composting / Anaerobic Digestion",

        "examples": [
            "Fruit scraps",
            "Vegetable scraps",
            "Food leftovers",
            "Coffee grounds",
            "Eggshells"
        ],

        "biotech_options": [
            "Aerobic composting",
            "Anaerobic digestion",
            "Microbial decomposition",
            "Organic matter stabilization"
        ]
    },


    # ========================================================
    # 3. GLASS
    # ========================================================

    "Glass": {

        "category": "Glass",
        "recyclable": True,
        "action": "Recycle",

        "disposal":
            "Separate glass containers and follow local "
            "glass-recycling collection rules.",

        "disposal_options": [
            "Glass recycling collection",
            "Dedicated glass recycling bins",
            "Municipal recycling programs",
            "Reuse of suitable containers"
        ],

        "reuse":
            "Clean glass containers can sometimes be reused "
            "for storage, decoration, or other suitable purposes.",

        "reuse_options": [
            "Storage containers",
            "Decorative containers",
            "Plant containers",
            "Craft projects",
            "Organizing small items"
        ],

        "recycling_options": [
            "Glass crushing",
            "Glass cullet production",
            "Remelting",
            "Manufacturing new glass containers"
        ],

        "preparation_steps": [
            "Separate glass from other materials",
            "Empty the container",
            "Rinse when appropriate",
            "Follow local glass collection rules"
        ],

        "avoid": [
            "Do not mix unsuitable glass types unless accepted locally",
            "Handle broken glass carefully",
            "Do not place hazardous glass in ordinary recycling"
        ],

        "impact":
            "Glass can be recycled repeatedly without losing "
            "its basic material properties.",

        "environmental_benefits": [
            "Reduces demand for raw materials",
            "Supports material recovery",
            "Glass can be recycled repeatedly",
            "Reduces landfill disposal"
        ],

        "eco_score": 9,
        "impact_points": 8,
        "landfill_risk": "Low",

        "recovery_method":
            "Crushing & Glass Remelting",

        "examples": [
            "Glass bottles",
            "Glass jars",
            "Glass containers"
        ],

        "biotech_options": [
            "Biological treatment is not the primary pathway",
            "Material recycling is preferred"
        ]
    },


    # ========================================================
    # 4. METAL
    # ========================================================

    "Metal": {

        "category": "Metal",
        "recyclable": True,
        "action": "Recycle",

        "disposal":
            "Separate metal items and place them in the "
            "appropriate metal-recycling stream.",

        "disposal_options": [
            "Metal recycling",
            "Scrap-metal collection",
            "Municipal recycling",
            "Specialized metal recovery"
        ],

        "reuse":
            "Some metal containers and objects can be reused "
            "after appropriate cleaning and inspection.",

        "reuse_options": [
            "Storage containers",
            "Craft projects",
            "Organization containers",
            "Repair and reuse",
            "Metalworking projects"
        ],

        "recycling_options": [
            "Aluminum recycling",
            "Steel recycling",
            "Metal separation",
            "Metal melting and remanufacturing",
            "Scrap-metal recovery"
        ],

        "preparation_steps": [
            "Separate metal from other materials",
            "Empty containers",
            "Remove non-metal attachments when practical",
            "Follow local recycling rules"
        ],

        "avoid": [
            "Do not place hazardous containers in ordinary recycling",
            "Do not mix chemicals with recyclable metal"
        ],

        "impact":
            "Metal recycling can reduce the need for extracting "
            "and processing new raw materials.",

        "environmental_benefits": [
            "Reduces raw-material extraction",
            "Saves energy compared with producing some metals from ore",
            "Reduces landfill waste",
            "Supports material recovery"
        ],

        "eco_score": 10,
        "impact_points": 10,
        "landfill_risk": "Medium",

        "recovery_method":
            "Metal Separation & Recycling",

        "examples": [
            "Aluminum cans",
            "Steel cans",
            "Metal containers",
            "Scrap metal"
        ],

        "biotech_options": [
            "Biological treatment is not the primary pathway",
            "Material recovery and recycling are preferred"
        ]
    },


    # ========================================================
    # 5. MISCELLANEOUS TRASH
    # ========================================================

    "Miscellaneous Trash": {

        "category": "Mixed / Other Waste",
        "recyclable": False,
        "action": "Check Local Waste Rules",

        "disposal":
            "This category contains materials that may require "
            "additional identification before disposal.",

        "disposal_options": [
            "Manual identification",
            "Separate recyclable components",
            "Check local waste-management rules",
            "Specialized collection when required"
        ],

        "reuse":
            "Check whether the item can be repaired, reused, "
            "or separated into recyclable materials.",

        "reuse_options": [
            "Repair the item",
            "Reuse usable components",
            "Donate usable items",
            "Separate recyclable materials"
        ],

        "recycling_options": [
            "Depends on the material composition",
            "Separate plastic components",
            "Separate metal components",
            "Separate paper/cardboard components",
            "Specialized recycling when available"
        ],

        "preparation_steps": [
            "Identify the material",
            "Separate mixed components",
            "Check local collection rules",
            "Keep hazardous items separate"
        ],

        "avoid": [
            "Do not assume unknown waste is recyclable",
            "Do not mix hazardous waste with general waste"
        ],

        "impact":
            "Correct sorting prevents potentially recyclable "
            "materials from being unnecessarily landfilled.",

        "environmental_benefits": [
            "Improves waste sorting",
            "Reduces unnecessary landfill disposal",
            "Can recover recyclable components"
        ],

        "eco_score": 5,
        "impact_points": 4,
        "landfill_risk": "High",

        "recovery_method":
            "Material Separation / Waste-to-Energy / Landfill",

        "examples": [
            "Mixed packaging",
            "Unknown materials",
            "Non-standard waste items"
        ],

        "biotech_options": [
            "Depends on material composition",
            "Biological treatment should only be considered for suitable biodegradable material"
        ]
    },


    # ========================================================
    # 6. PAPER
    # ========================================================

    "Paper": {

        "category": "Paper",
        "recyclable": True,
        "action": "Recycle",

        "disposal":
            "Keep paper clean and dry and place it in the "
            "appropriate paper-recycling stream.",

        "disposal_options": [
            "Paper recycling",
            "Community recycling",
            "School recycling",
            "University recycling"
        ],

        "reuse":
            "Reuse one-sided sheets for notes, drafts, "
            "drawing, packaging, or educational activities.",

        "reuse_options": [
            "Notes",
            "Draft printing",
            "Drawing",
            "Paper crafts",
            "Packaging",
            "Educational activities"
        ],

        "recycling_options": [
            "Paper pulping",
            "Fiber recovery",
            "Recycled paper manufacturing",
            "Paperboard production"
        ],

        "preparation_steps": [
            "Keep paper dry",
            "Remove non-paper materials when possible",
            "Separate heavily contaminated paper",
            "Place in the correct recycling stream"
        ],

        "avoid": [
            "Do not recycle heavily contaminated paper",
            "Do not mix wet paper with dry recyclable paper"
        ],

        "impact":
            "Paper recycling helps reduce demand for virgin "
            "fiber and can save resources.",

        "environmental_benefits": [
            "Reduces virgin fiber demand",
            "Reduces landfill waste",
            "Supports material recovery",
            "Extends paper fiber use"
        ],

        "eco_score": 9,
        "impact_points": 7,
        "landfill_risk": "Medium",

        "recovery_method":
            "Paper Pulping & Fiber Recycling",

        "examples": [
            "Office paper",
            "Newspapers",
            "Notebooks",
            "Printed documents"
        ],

        "biotech_options": [
            "Biological processing may support fiber recovery",
            "Conventional paper recycling is the primary pathway"
        ]
    },


    # ========================================================
    # 7. PLASTIC
    # ========================================================

    "Plastic": {

        "category": "Plastic",
        "recyclable": True,
        "action": "Recycle",

        "disposal":
            "Check local recycling rules and separate accepted "
            "plastic items from general waste.",

        "disposal_options": [
            "Plastic recycling",
            "Material recovery facilities",
            "Community recycling collection",
            "Specialized plastic collection",
            "Reuse before recycling"
        ],

        "reuse":
            "Clean suitable plastic containers can sometimes "
            "be reused for storage, organization, or educational projects.",

        "reuse_options": [
            "Storage containers",
            "Organization containers",
            "Plant containers",
            "Craft projects",
            "Educational projects",
            "Packaging reuse"
        ],

        "recycling_options": [
            "Mechanical recycling",
            "Plastic sorting",
            "Shredding and reprocessing",
            "Pellet production",
            "Manufacturing recycled plastic products"
        ],

        "preparation_steps": [
            "Check the local recycling symbol or rules",
            "Empty the container",
            "Clean when appropriate",
            "Separate different materials when possible",
            "Keep hazardous contamination away from recycling"
        ],

        "avoid": [
            "Do not assume every type of plastic is accepted",
            "Do not recycle heavily contaminated plastic",
            "Do not mix hazardous materials with plastic recycling"
        ],

        "impact":
            "Recovering plastic through recycling can reduce "
            "demand for new plastic production and prevent waste "
            "from entering the environment.",

        "environmental_benefits": [
            "Reduces demand for virgin plastic",
            "Supports material recovery",
            "Reduces landfill disposal",
            "Can reduce plastic leakage into the environment"
        ],

        "eco_score": 8,
        "impact_points": 8,
        "landfill_risk": "High",

        "recovery_method":
            "Sorting, Mechanical Recycling & Reprocessing",

        "examples": [
            "Plastic bottles",
            "Food containers",
            "Packaging",
            "Plastic bags",
            "Plastic containers"
        ],

        "biotech_options": [
            "Research-based enzymatic treatment may apply to selected polymers",
            "Microbial degradation is an active research area",
            "Mechanical recycling remains the main practical pathway for many plastics"
        ]
    },


    # ========================================================
    # 8. TEXTILE TRASH
    # ========================================================

    "Textile Trash": {

        "category": "Textile",
        "recyclable": False,
        "action": "Reuse / Textile Collection",

        "disposal":
            "Donate, repair, reuse, or use a textile-collection "
            "service when available.",

        "disposal_options": [
            "Donation",
            "Repair",
            "Textile collection",
            "Fiber recovery",
            "Reuse"
        ],

        "reuse":
            "Old textiles can be reused as cleaning cloths "
            "or repurposed into other useful items.",

        "reuse_options": [
            "Cleaning cloths",
            "Bags",
            "Craft projects",
            "Repair materials",
            "Upcycling projects",
            "Donation"
        ],

        "recycling_options": [
            "Textile sorting",
            "Fiber recovery",
            "Mechanical shredding",
            "Fabric-to-fiber recycling",
            "Reuse and upcycling"
        ],

        "preparation_steps": [
            "Keep textiles dry",
            "Separate reusable clothing",
            "Repair items when possible",
            "Use textile collection points when available"
        ],

        "avoid": [
            "Do not throw reusable clothing away immediately",
            "Do not mix wet textiles with dry collection"
        ],

        "impact":
            "Extending textile life reduces the amount of "
            "material sent to landfill and reduces demand for new textiles.",

        "environmental_benefits": [
            "Extends product life",
            "Reduces landfill waste",
            "Supports reuse",
            "Recovers textile fibers"
        ],

        "eco_score": 8,
        "impact_points": 6,
        "landfill_risk": "Medium",

        "recovery_method":
            "Textile Sorting, Shredding & Fiber Recovery",

        "examples": [
            "Clothes",
            "Cotton fabric",
            "Old uniforms",
            "Fabric scraps",
            "Towels"
        ],

        "biotech_options": [
            "Biological treatment is not usually the primary pathway",
            "Research exists on biological processing of selected textile fibers"
        ]
    },


    # ========================================================
    # 9. VEGETATION
    # ========================================================

    "Vegetation": {

        "category": "Green Organic Waste",
        "recyclable": False,
        "action": "Compost",

        "disposal":
            "Separate plant material and use an appropriate "
            "composting or organic-waste pathway.",

        "disposal_options": [
            "Composting",
            "Green-waste collection",
            "Community composting",
            "Anaerobic digestion",
            "Organic matter recovery"
        ],

        "reuse":
            "Plant material can be composted, mulched, or "
            "processed to recover organic matter.",

        "reuse_options": [
            "Composting",
            "Mulching",
            "Garden soil amendment",
            "Green-waste processing",
            "Organic matter recovery"
        ],

        "recycling_options": [
            "Aerobic composting",
            "Anaerobic digestion",
            "Mulching",
            "Organic matter recovery"
        ],

        "preparation_steps": [
            "Separate plant material from plastic",
            "Remove non-organic materials",
            "Use a suitable green-waste collection system",
            "Keep hazardous materials out of organic waste"
        ],

        "avoid": [
            "Do not mix vegetation with plastics",
            "Do not place chemicals in organic waste",
            "Do not contaminate composting material"
        ],

        "impact":
            "Composting can return organic matter to the soil "
            "and reduce landfill disposal.",

        "environmental_benefits": [
            "Returns organic matter to soil",
            "Reduces landfill waste",
            "Supports compost production",
            "Can reduce organic waste transport to landfill"
        ],

        "eco_score": 9,
        "impact_points": 9,
        "landfill_risk": "Low",

        "recovery_method":
            "Aerobic Composting & Anaerobic Digestion",

        "examples": [
            "Leaves",
            "Grass",
            "Plant trimmings",
            "Branches",
            "Garden waste"
        ],

        "biotech_options": [
            "Aerobic composting",
            "Anaerobic digestion",
            "Microbial decomposition",
            "Organic matter stabilization"
        ]
    }
}


# ============================================================
# Get Waste Information
# ============================================================

def get_waste_info(waste_name):

    return WASTE_INFO.get(
        waste_name,
        {
            "category": "Unknown",
            "recyclable": False,
            "action": "Manual Review",
            "disposal": "Please inspect the item manually before disposal.",
            "disposal_options": [
                "Manual identification",
                "Check local waste-management rules"
            ],
            "reuse": "Check whether the item can be reused.",
            "reuse_options": [
                "Repair",
                "Reuse",
                "Separate recyclable components"
            ],
            "recycling_options": [],
            "preparation_steps": [],
            "avoid": [],
            "impact": "No reliable environmental information is available for this category.",
            "environmental_benefits": [],
            "eco_score": 0,
            "impact_points": 0,
            "landfill_risk": "Unknown",
            "recovery_method": "Manual Review",
            "examples": [],
            "biotech_options": []
        }
    )


# ============================================================
# Biotechnology Information
# ============================================================

def get_biotech_info(waste_type):

    organic_waste = [
        "Food Organics",
        "Vegetation"
    ]

    if waste_type in organic_waste:

        info = WASTE_INFO[waste_type]

        return {
            "is_organic": True,

            "title": "🧬 Biological Treatment",

            "process":
                "Separation → Biological Treatment → "
                "Composting / Anaerobic Digestion → "
                "Organic Matter Recovery",

            "explanation":
                "Microorganisms can naturally decompose "
                "biodegradable organic waste and convert it "
                "into more stable organic matter.",

            "options":
                info.get("biotech_options", [])
        }

    info = WASTE_INFO.get(waste_type, {})

    return {
        "is_organic": False,

        "title": "🧬 Biotechnology Pathway",

        "process":
            "No primary biological treatment pathway recommended.",

        "explanation":
            "This waste category is not primarily "
            "biodegradable organic waste. Material recovery "
            "or specialized treatment is generally more appropriate.",

        "options":
            info.get("biotech_options", [])
    }


# ============================================================
# EcoPoints
# ============================================================

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
