class Triple:
    def __init__(self, y, id, ad):
        self.y = y 
        self.id = id
        self.ad = ad
    def __str__(self):
        return ('y: '+ str(self.y) + '\nid: ' + str(self.id) + '\nad: '+ str(self.ad))
    def __repr__(self):
        return ('(y: '+ str(self.y) + ', id: ' + str(self.id) + ', ad: '+ str(self.ad)) + ')'
        # return str(self)
    

class Voucher:
    def __init__(self, id, Q, ct, rct):
        self.id = id
        self.Q = Q
        self.ct = ct
        self.rct = rct
        
    def __str__(self):
        return ('id: '+ str(self.id) + '\nQ: ' + str(self.Q) + '\nct: '+ str(self.ct) + '\nrct: '+ str(self.rct))