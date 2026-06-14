import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.evaluation.benchmark_dataset import BenchmarkDataset, BenchmarkItem, ContradictionLevel, Evidence

logging.basicConfig(level=logging.INFO)

def generate_samples():
    dataset = BenchmarkDataset("scirag_cdc_benchmark")

    # We'll use templates to systematically generate 50 diverse items
    # 10 templates * 5 variations = 50 distinct items
    templates = [
        {
            "q": "What is the population of {entity} as of the 2025 census?",
            "ans": "{val} million",
            "base_ev": "The 2025 official census reported the population of {entity} at exactly {val} million.",
            "clean_ev": "{entity} reached a milestone of {val} million residents this year.",
            "l1_ev": "{entity} reached a milestone of {val_alt} million residents this year.",
            "l2_ev": "{entity_alt} reached a milestone of {val} million residents this year.",
            "l3_ev": "New data suggests {entity}'s population is nowhere near {val} million and is rapidly declining.",
            "l4_ev": "There is no record of a 2025 census for {entity}, and the population figure of {val} million is completely fabricated.",
            "vars": [
                ("Metropolis", "5.0", "5.1", "Gotham"),
                ("Neo-Tokyo", "12.4", "12.5", "Kyoto"),
                ("New London", "8.9", "9.0", "Manchester"),
                ("San Angeles", "6.2", "6.3", "Bay City"),
                ("Mega City One", "400.0", "401.0", "Texas City")
            ]
        },
        {
            "q": "Who was appointed as the CEO of {entity} in January 2024?",
            "ans": "{val}",
            "base_ev": "In January 2024, the board unanimously appointed {val} as the new CEO of {entity}.",
            "clean_ev": "{val} takes the helm as {entity}'s CEO following the January board meeting.",
            "l1_ev": "{val} takes the helm as {entity}'s CEO, earning a $500K bonus, following the January board meeting.", # Slight nuance
            "l2_ev": "{val_alt} takes the helm as {entity}'s CEO following the January board meeting.",
            "l3_ev": "The CEO position at {entity} remains vacant as {val} declined the offer.",
            "l4_ev": "{entity} dissolved in late 2023, making the appointment of {val} or anyone else impossible.",
            "vars": [
                ("GlobalTech", "Alice Smith", "Bob Jones", "TechCorp"),
                ("InnoVate", "Sarah Connor", "John Connor", "Cyberdyne"),
                ("Stark Industries", "Pepper Potts", "Tony Stark", "Wayne Enterprises"),
                ("Wayne Enterprises", "Lucius Fox", "Bruce Wayne", "Stark Industries"),
                ("Massive Dynamic", "Nina Sharp", "William Bell", "Fringe Division")
            ]
        },
        {
            "q": "What were the clinical trial results for the drug {entity}?",
            "ans": "The drug was shown to be {val}.",
            "base_ev": "Phase 3 clinical trials demonstrated that {entity} is {val} in treating the condition.",
            "clean_ev": "Researchers confirmed the {val} nature of {entity} across a diverse patient group.",
            "l1_ev": "Researchers confirmed the {val} nature of {entity} across a diverse patient group of 1000 people (originally 500).",
            "l2_ev": "Researchers confirmed the {val} nature of {entity_alt} across a diverse patient group.",
            "l3_ev": "Researchers concluded that {entity} is completely ineffective and indistinguishable from placebo.",
            "l4_ev": "{entity} was banned from clinical trials due to severe toxicity, making any efficacy claims fraudulent.",
            "vars": [
                ("Novocillin", "highly effective", "somewhat effective", "Penicillin"),
                ("CureAll", "moderately effective", "barely effective", "Placebex"),
                ("HealPill", "completely effective", "mostly effective", "HarmPill"),
                ("MiracleMeds", "partially effective", "minimally effective", "SnakeOil"),
                ("Panacea", "universally effective", "largely effective", "Elixir")
            ]
        },
        {
            "q": "What was the outcome of the {entity} mission?",
            "ans": "The mission {val}.",
            "base_ev": "The {entity} mission concluded with a {val} landing and safe return of the crew.",
            "clean_ev": "Astronauts celebrated a {val} execution of the {entity} lunar landing.",
            "l1_ev": "Astronauts celebrated a {val} execution of the {entity} lunar landing after a 5 minute delay.",
            "l2_ev": "Astronauts celebrated a {val} execution of the {entity_alt} lunar landing.",
            "l3_ev": "The {entity} mission encountered severe anomalies, barely returning the crew alive.",
            "l4_ev": "Tragically, the {entity} mission failed entirely, resulting in the loss of the lunar lander.",
            "vars": [
                ("Artemis V", "successful", "partial", "Apollo 18"),
                ("Mars One", "flawless", "bumpy", "Mars Two"),
                ("Jupiter Probe", "perfect", "delayed", "Saturn Probe"),
                ("Voyager 3", "triumphant", "routine", "Pioneer 12"),
                ("Hubble 2", "spectacular", "subpar", "Webb 2")
            ]
        },
        {
            "q": "In what year was the {entity} signed?",
            "ans": "{val}",
            "base_ev": "The historic {entity} was officially signed by all delegates in {val}.",
            "clean_ev": "Historians note that the signing of the {entity} in {val} marked a new era of peace.",
            "l1_ev": "Historians note that the signing of the {entity} in {val_alt} marked a new era of peace.",
            "l2_ev": "Historians note that the signing of the {entity_alt} in {val} marked a new era of peace.",
            "l3_ev": "The {entity} was never actually signed; it remained a draft proposal indefinitely.",
            "l4_ev": "No such treaty as the {entity} ever existed in recorded history.",
            "vars": [
                ("Treaty of Nova", "2031", "2032", "Treaty of Sol"),
                ("Lunar Accords", "2045", "2046", "Martian Accords"),
                ("Europa Pact", "2088", "2089", "Titan Pact"),
                ("Alpha Centauri Agreement", "2150", "2151", "Proxima Agreement"),
                ("Galactic Charter", "2200", "2201", "Universal Charter")
            ]
        },
        {
            "q": "What is the capital of {entity}?",
            "ans": "{val}",
            "base_ev": "The official capital of the newly formed republic of {entity} is {val}.",
            "clean_ev": "Citizens of {entity} are proud of their capital city, {val}.",
            "l1_ev": "Citizens of {entity} are proud of their capital city, {val}, which has a population of 2 million.",
            "l2_ev": "Citizens of {entity} are proud of their capital city, {val_alt}.",
            "l3_ev": "{entity} is a decentralized state and officially has no designated capital city.",
            "l4_ev": "{entity} is not a real region and has no capital.",
            "vars": [
                ("Cascadia", "Portland", "Seattle", "Pacifica"),
                ("New Texas", "Austin", "Houston", "Old Texas"),
                ("Europa Prime", "Base One", "Base Two", "Ganymede"),
                ("Mars Republic", "Olympus", "Cydonia", "Venus Colony"),
                ("Titan State", "Huygens", "Cassini", "Enceladus")
            ]
        },
        {
            "q": "What is the melting point of {entity}?",
            "ans": "{val} degrees Celsius",
            "base_ev": "Scientific measurements confirm the melting point of {entity} is exactly {val} degrees Celsius.",
            "clean_ev": "When heated to {val} degrees Celsius, {entity} transitions to a liquid state.",
            "l1_ev": "When heated to {val_alt} degrees Celsius, {entity} transitions to a liquid state.",
            "l2_ev": "When heated to {val} degrees Celsius, {entity_alt} transitions to a liquid state.",
            "l3_ev": "{entity} sublimates directly to a gas and does not have a standard melting point.",
            "l4_ev": "{entity} is a purely theoretical element that cannot exist in physical form to melt.",
            "vars": [
                ("Vibranium", "3000", "3010", "Adamantium"),
                ("Unobtainium", "5000", "5050", "Kryptonite"),
                ("Mithril", "2500", "2520", "Orichalcum"),
                ("Element 115", "1000", "1005", "Element 116"),
                ("Neutronium", "1000000", "1000005", "Protonium")
            ]
        },
        {
            "q": "Who won the Best Actor award for the movie {entity} in 2026?",
            "ans": "{val}",
            "base_ev": "The academy awarded Best Actor to {val} for his performance in {entity}.",
            "clean_ev": "{val}'s role in {entity} earned him the prestigious Best Actor trophy in 2026.",
            "l1_ev": "{val}'s role in {entity} earned him the prestigious Best Actor trophy in 2027.",
            "l2_ev": "{val_alt}'s role in {entity} earned him the prestigious Best Actor trophy in 2026.",
            "l3_ev": "The Best Actor category was cancelled in 2026, and no award was given for {entity}.",
            "l4_ev": "The movie {entity} was never released, making any awards impossible.",
            "vars": [
                ("Cyber Heist", "Tom Hardy", "Chris Evans", "Neon Dreams"),
                ("The Last Martian", "Matt Damon", "Brad Pitt", "The First Martian"),
                ("Time Loop", "Keanu Reeves", "Tom Cruise", "Space Loop"),
                ("AI Rising", "Oscar Isaac", "Rami Malek", "Robot Fall"),
                ("Virtual Reality", "Leonardo DiCaprio", "Christian Bale", "Actual Reality")
            ]
        },
        {
            "q": "What is the GDP of {entity} in 2025?",
            "ans": "{val} trillion dollars",
            "base_ev": "The World Bank reported the 2025 GDP of {entity} as {val} trillion dollars.",
            "clean_ev": "Economic data confirms {entity}'s GDP reached {val} trillion dollars this year.",
            "l1_ev": "Economic data confirms {entity}'s GDP reached {val_alt} trillion dollars this year.",
            "l2_ev": "Economic data confirms {entity_alt}'s GDP reached {val} trillion dollars this year.",
            "l3_ev": "{entity}'s economy completely collapsed in 2025, rendering its GDP essentially zero.",
            "l4_ev": "{entity} is not a recognized economic entity and does not have a measurable GDP.",
            "vars": [
                ("Atlantis", "2.5", "2.6", "Lemuria"),
                ("El Dorado", "5.0", "5.1", "Shangri-La"),
                ("Wakanda", "10.0", "10.5", "Genosha"),
                ("Latveria", "1.2", "1.3", "Symkaria"),
                ("Krakoa", "8.0", "8.2", "Arakko")
            ]
        },
        {
            "q": "Who is the author of the bestselling novel {entity}?",
            "ans": "{val}",
            "base_ev": "The bestselling novel {entity} was written by acclaimed author {val}.",
            "clean_ev": "Critics praised {val}'s masterpiece, {entity}, for its profound narrative.",
            "l1_ev": "Critics praised {val}'s 500-page masterpiece, {entity}, for its profound narrative.",
            "l2_ev": "Critics praised {val_alt}'s masterpiece, {entity}, for its profound narrative.",
            "l3_ev": "The true authorship of {entity} remains a heavily disputed mystery, with {val} denying involvement.",
            "l4_ev": "The novel {entity} was entirely generated by AI, and {val} is a fictitious persona.",
            "vars": [
                ("The Quantum Thief", "Hannu Rajaniemi", "Alastair Reynolds", "The Causal Angel"),
                ("Neuromancer", "William Gibson", "Neal Stephenson", "Snow Crash"),
                ("Dune", "Frank Herbert", "Isaac Asimov", "Foundation"),
                ("Hyperion", "Dan Simmons", "Arthur C. Clarke", "Endymion"),
                ("Snow Crash", "Neal Stephenson", "William Gibson", "Neuromancer")
            ]
        }
    ]

    item_idx = 1
    for t in templates:
        for var_set in t["vars"]:
            entity, val, val_alt, entity_alt = var_set
            
            kwargs = {
                "entity": entity,
                "val": val,
                "val_alt": val_alt,
                "entity_alt": entity_alt
            }
            
            item = BenchmarkItem(
                id=f"q{item_idx}",
                question=t["q"].format(**kwargs),
                true_answer=t["ans"].format(**kwargs),
            )
            
            base_ev = Evidence(t["base_ev"].format(**kwargs), "Source A", 0.95)
            
            # Level 0: Clean
            item.evidence_by_level[ContradictionLevel.LEVEL_0_CLEAN] = [
                base_ev,
                Evidence(t["clean_ev"].format(**kwargs), "Source B", 0.9)
            ]
            
            # Level 1: Numeric/Minor
            item.evidence_by_level[ContradictionLevel.LEVEL_1_NUMERIC] = [
                base_ev,
                Evidence(t["l1_ev"].format(**kwargs), "Source B", 0.9)
            ]
            
            # Level 2: Entity
            item.evidence_by_level[ContradictionLevel.LEVEL_2_ENTITY] = [
                base_ev,
                Evidence(t["l2_ev"].format(**kwargs), "Source B", 0.9)
            ]
            
            # Level 3: Semantic
            item.evidence_by_level[ContradictionLevel.LEVEL_3_SEMANTIC] = [
                base_ev,
                Evidence(t["l3_ev"].format(**kwargs), "Source B", 0.9)
            ]
            
            # Level 4: Factual
            item.evidence_by_level[ContradictionLevel.LEVEL_4_FACTUAL] = [
                base_ev,
                Evidence(t["l4_ev"].format(**kwargs), "Source B", 0.9)
            ]
            
            dataset.add_item(item)
            item_idx += 1

    
    # Save to the benchmark root directory
    output_dir = Path(__file__).parent.parent / "benchmark"
    dataset.save_to_disk(str(output_dir))

if __name__ == "__main__":
    generate_samples()
