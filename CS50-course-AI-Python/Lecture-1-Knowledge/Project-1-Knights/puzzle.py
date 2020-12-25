from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    Or(AKnight, AKnave),  # This is the claim that A is either a Knight or a Knave.
    Not(And(AKnight, AKnave)),  # Since the previous or is inclusive, we have to remove the case of A being both,
    # a Knight and a Knave.
    Biconditional(And(AKnight, AKnave), AKnight)  # Here we set that the statement is true IF AND ONLY IF A is a Knight.
    # Here the statement is simply And(AKnight, AKnave).
)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),  # Again, Neither A nor B can be both Knight and Knaves.
    Biconditional(And(AKnave, BKnave), AKnight)  # Again, we set that the statement is true
    # if and only if A is a Knight.
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Biconditional(Or(And(AKnave, BKnave), And(AKnight, BKnight)), AKnight),  # The claim of A.
    Biconditional(Or(And(AKnave, Not(BKnave)), And(AKnight, Not(BKnight))), BKnight)  # The claim of B.
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    Or(AKnight, AKnave),
    Not(And(AKnight, AKnave)),
    Or(BKnight, BKnave),
    Not(And(BKnight, BKnave)),
    Or(CKnight, CKnave),
    Not(And(CKnight, CKnave)),
    Biconditional(Or(And(AKnave, AKnight), And(Not(AKnave), AKnave)), BKnight),  # If A says that he is a Knave
    # (being a Knight or a Knave), then B is a Knight.
    Biconditional(CKnave, BKnight),  # If C is a knave, then B is a Knight.
    Biconditional(AKnight, CKnight)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
