from abc import ABC, abstractmethod

class AmazonClient(ABC):
    @abstractmethod
    def getAllOrderIDs(self, pages):
        raise NotImplementedError
    
    @abstractmethod
    def getInvoicePage(self, orderID):
        raise NotImplementedError