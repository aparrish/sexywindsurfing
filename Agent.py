
class Agent(object):

  def __init__(self):
    self.hand = set()
    self.hand_history = list()

  def play(self, card):
    self.hand_history.append(self.hand.copy())
    self.hand.remove(card)

  def deal(self, card):
    self.hand.add(card)

  def pick(self, target, criterion):
    card = criterion.pick(target, self.hand)
    return card

class Criterion(object):

  def pick(self, target, sources):
    from random import choice
    return choice(list(sources))

class GoogleCriterion(object):

  def __init__(self):
    self.counter = GoogleSearchCounter()

  def pick(self, target, sources):

    scores = dict()
    for src in sources:
      source_count = self.counter.get_count('"%s"' % src)
      source_target_count = self.counter.get_count('%s "%s"' % (target, src))
      print 'count for "%s": %s' % (src, source_count) 
      print 'count for %s "%s": %s' % (target, src, source_target_count)
      scores[src] = float(source_target_count) / float(source_count)

    return self.choose_best(scores)

class GoogleHighestCriterion(GoogleCriterion):

  def choose_best(self, scores):
    import operator
    s = sorted(scores.iteritems(), key=operator.itemgetter(1), reverse=True)
    return s[0]      

class GoogleLowestCriterion(GoogleCriterion):

  def choose_best(self, scores):
    import operator
    s = sorted(scores.iteritems(), key=operator.itemgetter(1))
    return s[0]      

class GoogleSearchCounter(object):

  def __init__(self):
    self.cache = dict()

  def get_count(self, term):
    from xgoogle.search import GoogleSearch

    if term in self.cache:
      return self.cache[term]

    gs = GoogleSearch(term)
    count = gs.num_results
    self.cache[term] = count

    return count

if __name__ == '__main__':

  agent = Agent()
  for card in ['friction', 'firefighters', 'george washington']:
    agent.deal(card)

  card = agent.pick('temperamental', GoogleLowestCriterion())

  print card

