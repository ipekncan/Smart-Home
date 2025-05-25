import google.generativeai as genai



genai.configure(api_key="AIzaSyBG-FpAJ4nBp_XrG5BrAqduOaFIND-eEqI")

model = genai.GenerativeModel("models/gemini-1.5-flash")

allowed_facts = {
    "cold_weather", "hot_weather", "arrived_home", "leaving_home",
    "sunrise", "sleeping"
}
def natural_language(text):
    prompt = (
        "You are a smart home assistant. Convert the user's sentence into ONE fact "
        "describing the situation or need. You MUST only choose from the following facts:\n"
        f"{', '.join(allowed_facts)}\n\n"
        "Return ONLY one of the above facts that best matches the user's sentence. "
        "Use lowercase and underscores only.\n"
        f"Input: \"{text}\"\nFact:"
    )
    response = model.generate_content(prompt)
    fact = response.text.strip().lower().replace(" ", "_")

    if fact not in allowed_facts:
        print(f"⚠️ '{fact}' is not in allowed facts. Ignored.")
        return None

    return fact


class SmartHomeAgent:
    def __init__(self):
        self.facts = set()
        self.rules = {}
        self.devices = {
            "heater": False,
            "door": False,
            "curtains": False,
            "television": False,
            "lamp": False,
        }

    def tell_fact(self, fact):
        self.facts.add(fact)
        print("Fact:", fact)

    def tell_rule(self, rule):
        cond, conc = rule.split("->")
        condition = cond.strip()
        conclusion = conc.strip()
        if condition not in self.rules:
            self.rules[condition] = []
        self.rules[condition].append(conclusion)
        print("Rule:", condition, "->", conclusion)

    def evaluate(self):
        actions = set()
        for condition, conclusions in self.rules.items():
            if condition in self.facts:
                for action_s in conclusions:
                   for action in action_s.split("&&"):
                       actions.add(action.strip())
        for action in actions:
            self.execute(action)

    def execute(self, action):
        # Heater
        if action == "turn_on_heater":
            if self.devices["heater"]:
                print("Heater is already on.")
            else:
                print("Action:"+action)
                self.devices["heater"] = True
        elif action == "turn_off_heater":
            if not self.devices["heater"]:
                print("Heater is already off.")
            else:
                print("Action:"+action)
                self.devices["heater"] = False

        # Door
        elif action == "open_door":
            if (self.devices["door"] == True):
                print("Door is already open.")
            else:
              print("Action:"+action)
              self.devices["door"] = True
        elif action == "close_door":
            if (self.devices["door"] == False):
                print("Door is already closed.")
            else:
              print("Action:"+action)
              self.devices["door"] = False
       #Lamps
        elif action == "turn_on_lamp":
            if (self.devices["lamp"] == True):
                print("Lamps are already on.")
            else:
              print("Action:"+action)
              self.devices["lamp"] = True
        elif action == "turn_off_lamp":
            if (self.devices["lamp"] == False):
                print("Lamps are already off.")
            else:
              print("Action:"+action)
              self.devices["lamp"] = False
        #Curtains
        elif action == "open_curtains":
            if (self.devices["curtains"] == True):
                print("Curtains are already open.")
            else:
              print("Action:"+action)
              self.devices["curtains"] = True
        elif action == "close_curtains":
            if (self.devices["curtains"] ==False):
                print("Curtains are already closed.")
            else:
                print("Action:" + action)
                self.devices["curtains"] = False
        #Television
        elif action == "turn_on_television":
            if (self.devices["television"] == True):
                print("Television is already open.")
            else:
                print("Action:"+action)
                self.devices["television"] = True
        elif action == "turn_off_television":
            if (self.devices["television"] == False):
                print("Television is already closed.")
            else:
                print("Action:"+action)
                self.devices["television"] = False



agent = SmartHomeAgent()
print("Welcome to SmartHome System. Press 'x' to exit.Press's' to see stats")

#RULES
agent.tell_rule("cold_weather->turn_on_heater")
agent.tell_rule("hot_weather->turn_off_heater")
agent.tell_rule("arrived_home->turn_on_lamp&&open_door")
agent.tell_rule("leaving_home->turn_off_lamp&&close_door")
agent.tell_rule("sunrise->open_curtains&&turn_on_television")
agent.tell_rule("sleeping->turn_off_television&&turn_off_lamp")


while True:
    command = input("Enter command: ")
    if command.lower() == "x":
        break
    elif command.lower() == "s":
        print("Current Device States:")
        for device, state in agent.devices.items():
            print(f" - {device}: {'ON' if state is True else 'OFF'}")
        continue
    else:
     fact = natural_language(command)
     agent.facts.clear()
     agent.tell_fact(fact)
     agent.evaluate()
