from SexyWindsurfing import Agent

# command-line interface for SEXY WINDSURFING

import re

def get_input(regex, prompt):

  import re
  import readline
  matching_input = str()
  while True:
    input = raw_input(prompt).strip()
    mobj = re.search(regex, input)
    if mobj == None:
      print "Unrecognized response.\n"
    else:
      matching_input = mobj.group()
      break
 
  return matching_input

agent = Agent(GoogleLowestCriterion())

cards_comma_sep = get_input(r"^.+$", "Comma-separated list of initial cards: ")
for card in re.split(r"\s*,\s*", cards_comma_sep):
  agent.deal(card)

while True:
  yn = get_input(r"^(y|n)$", "Is the agent the judge this round? (y/n) ")
  if yn == 'y':
    target = get_input(r"^.+$", "Word to judge: ")
    cards_comma_sep = get_input(r"^.+$",
      "Comma-separated list of competitor's responses: ")
    card = agent.judge(target, re.split(r"\s*,\s*", cards_comma_sep))
    print "Agent chooses: " + card
  else:
    target = get_input(r"^.+$", "Word to target: ")
    card = agent.pick(target)
    print "Agent chooses this card: " + card
    next_card = get_input(r"^.+$", "Next word: ")
    agent.deal(next_card)

