
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
    self.counter = GoogleAjaxSearchCounter()

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

class GoogleAjaxSearchCounter(object):

  url_base = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q='
  referrer = 'http://www.decontextualize.com/'

  def __init__(self):
    self.cache = dict()

  def get_count(self, term):
    import urllib2
    import urllib
    import json
    from time import sleep

    if term in self.cache:
      return self.cache[term]

    url = self.url_base + urllib.quote(term)
    print url
    request = urllib2.Request(url, None, {'Referer': self.referrer})
    response = urllib2.urlopen(request)

    results = json.load(response)
    print results
    count = results['responseData']['cursor']['estimatedResultCount']
    self.cache[term] = count

    sleep(0.25)

    return count

if __name__ == '__main__':

  agent = Agent()
  for card in ['friction', 'firefighters', 'george washington']:
    agent.deal(card)

  card = agent.pick('temperamental', GoogleHighestCriterion())

  print card

