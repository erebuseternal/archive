from SpiderWoman.action import Action
from SpiderWoman.tracker import VillainTracker, WikiTrackingDevice
import re
import sys

num = int(sys.argv[1])

tracking_device = WikiTrackingDevice('https://marvel.wikia.com')
seed = tracking_device.CreateSoup('http://marvel.wikia.com/wiki/Jessica_Jones_%28Earth-616%29')
villaintracker = VillainTracker(tracking_device, seed)

def scarlet(tag):
    return 'scarlet'

def is_there(tag):
    content = tag.get_text()
    ex = re.compile('(?i)scarlet')
    match = re.search(ex, content)
    if match:
        return 1
    else:
        return 0

weapons = {'scarlet' : scarlet, 'is_there' : is_there}


action = Action()
action.LoadPlan('findscarlet.css')
action.SetWeapons(weapons)

sum = 0.0
count = 0.0
for i in range(0, num):
    villain = villaintracker.FindVillain()
    if not villain:
        break
    count += 1
    print("That's villain: %s" % count)
    action.SetVillain(villain)
    action.Act()
    results = action.DumpVillain()
    if results['scarlet'][0] == 1:
        sum += 1

print(sum / count)
