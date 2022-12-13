
class Item(object):
    def __init__(self, id, ownerID, title, status, startTime,endTime,startPrice,winningBid, SUID):
        self.id = id
        self.ownerID = ownerID
        self.title = title
        self.status = status
        self.startTime = startTime
        self.endTime = endTime
        self.startPrice = startPrice
        self.winningBid = winningBid
        self.SUID = SUID

    def __init__(self, id, ownerID, title):
        self.id = id
        self.ownerID = ownerID
        self.title = title