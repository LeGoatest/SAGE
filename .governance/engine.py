from boot_validator import BootValidator
from invariant_validator import InvariantValidator
from semantic_conflict_validator import SemanticConflictValidator
from semantic_engine import SemanticEngine
from graph_generator import GraphGenerator
from derivation_compiler import DerivationCompiler

class SAGEEngine:
    def __init__(self):
        self.boot = BootValidator()
        self.invariant = InvariantValidator()
        self.conflict = SemanticConflictValidator()
        self.semantic = SemanticEngine()
        self.graph = GraphGenerator()
        self.derivation = DerivationCompiler()

    def boot_validate(self):
        self.boot.validate()

    def invariant_validate(self):
        self.invariant.validate()

    def conflict_validate(self):
        self.conflict.validate()

    def explain_violation(self, violated_rule_ids):
        return self.semantic.evaluate_violation(violated_rule_ids)

    def generate_graph(self):
        self.graph.generate()

    def analyze_derivation(self):
        self.derivation.analyze()
