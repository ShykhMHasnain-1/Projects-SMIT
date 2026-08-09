"""
Training Dataset for Scikit-Learn Civic Categorization Model.
Contains diverse real-world municipal complaint descriptions across categories.
"""

TRAINING_SAMPLES = [
    # Roads & Infrastructure
    ("Deep dangerous pothole on the main road causing car wheel damage.", "Roads & Infrastructure"),
    ("Asphalt is cracking and crumbling near the highway junction.", "Roads & Infrastructure"),
    ("Broken pavement sidewalk tripping elderly pedestrians near central market.", "Roads & Infrastructure"),
    ("Bridge guardrail damaged after vehicle crash yesterday.", "Roads & Infrastructure"),
    ("Speed bump has worn down completely, causing speeding issues.", "Roads & Infrastructure"),
    ("Unfinished road construction leaving sharp gravel and dust everywhere.", "Roads & Infrastructure"),
    
    # Water Supply
    ("Water pipeline underground burst spraying clean water onto street.", "Water Supply"),
    ("Low water pressure in residential building for three days straight.", "Water Supply"),
    ("Tap water coming out brown and muddy from public distribution supply.", "Water Supply"),
    ("Major sewage pipe blockage overflowing into backyard drainage.", "Water Supply"),
    ("Water tank valve leaking continuously at municipal reservoir station.", "Water Supply"),
    ("Broken water main flooding basement of local community center.", "Water Supply"),

    # Sanitation
    ("Garbage dumpster overflowing with household waste and plastic bags.", "Sanitation"),
    ("Uncollected trash piles attracting rodents and causing foul odor.", "Sanitation"),
    ("Public park litter bins have not been emptied for two weeks.", "Sanitation"),
    ("Illegal dumping of furniture and construction debris on alleyway.", "Sanitation"),
    ("Dead stray animal on roadside needs immediate sanitary removal.", "Sanitation"),
    ("Foul sewage smell spreading from dirty open drain near food market.", "Sanitation"),

    # Public Safety
    ("Exposed high voltage electrical wire hanging from broken utility pole.", "Public Safety"),
    ("Open manhole cover on unlit street presents fatal hazard to pedestrians.", "Public Safety"),
    ("Strong smell of gas leaking near apartment gas meter line.", "Public Safety"),
    ("Old vacant building wall showing major structural cracks ready to collapse.", "Public Safety"),
    ("Overhanging heavy tree branch dangerously close to power cables.", "Public Safety"),
    ("Chemical liquid spill from commercial vehicle leaking on public road.", "Public Safety"),

    # Street Lighting
    ("Street light pole #42 is dark and bulb is completely burned out.", "Street Lighting"),
    ("Entire street section pitch black due to flickering street light failure.", "Street Lighting"),
    ("Solar street light panel broken and not turning on at night.", "Street Lighting"),
    ("Short circuit in light pole junction box causing sparks at night.", "Street Lighting"),
    ("Street lights remaining ON during full daylight hours wasting energy.", "Street Lighting"),

    # Parks & Environment
    ("Public park grass overgrown and children playground swing broken.", "Parks & Environment"),
    ("Fallen tree blocking park walking trail after heavy thunderstorm.", "Parks & Environment"),
    ("Public park benches vandalized and wooden planks rotting.", "Parks & Environment"),
    ("Sprinkler system leaking water in city botanical gardens.", "Parks & Environment"),
    ("Weeds and wild bushes invading neighborhood community park.", "Parks & Environment"),
]
