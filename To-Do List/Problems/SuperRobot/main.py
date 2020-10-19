instances = (AstromechDroid, MedicalDroid, BattleDroid, PilotDroid)

for instance in instances:
    print(issubclass(SuperRobot, instance))
