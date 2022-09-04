from dataclasses import dataclass, field

@dataclass
class Exclusive:
    
    def renderStr(self):
        return f"\tconstraint exclusive;\n"