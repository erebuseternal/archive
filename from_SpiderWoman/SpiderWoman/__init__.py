from .tracker import WikiTrackingDevice, VillainTracker
from .action import Action

"""
This is mainly an example of a class created from our scraper code.
But seeing as it actually is useful, I have placed it here.
"""

class WikiSpider:

    def __init__(self, base_url, starting_url, rule_file, weapons, hashes=[]):
        # the base url is the base url of your wiki site (no trailing /)
        # the starting url is the url you wish to start your crawl from
        # you will not scrape that page at first, it is just where you begin
        # (I do this so you don't have to worry about scraping the same page
        # twice if you start on the same page over and over again)
        # the rule file is the address of the css like file you wish to use
        # and weapons is a dictionary where the keys are the names you put in
        # your rule code, and the values are the function instances of the
        # functions used to process tags. (They take a tag as input, and should
        # return some value)
        # if you want to use the scraper again and again, after each scrape,
        # save self.villain_tracker.hashes somewhere, and when you scrape again,
        # pass it to the hashes input
        self.tracking_device = WikiTrackingDevice(base_url)
        seed = self.tracking_device.CreateSoup(starting_url)
        self.villain_tracker = VillainTracker(self.tracking_device, seed)
        self.villain_tracker.hashes = hashes
        self.action = Action()
        self.action.LoadPlan(rule_file)
        self.action.SetWeapons(weapons)

    def Go(self, num, store, is_worth=None):
        # num is the number of instances you want to get
        # you can pass in a function instance for is_worth
        # and it will be used to determine if a page you scraped will be
        # counted (it should only take (as input) a dictionary (the fields you scraped)).
        # the function passed in for store should take the same input, but should
        # be used to store those fields (note it will only be called if the
        # scraped document is counted by is_worth)
        count = 0
        while count < num:
            soup = self.villain_tracker.FindVillain()
            if not soup:    # find villain can return none if it has run out of pages
                break
            self.action.SetVillain(soup)
            self.action.Act()
            villain = self.action.DumpVillain()
            if is_worth:
                if is_worth(villain):
                    count += 1
                    store(villain)
            else:
                count += 1
                store(villain)
