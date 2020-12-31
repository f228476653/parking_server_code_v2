
import unittest
class UserServiceTest(unittest.TestCase):
    
    def setUp(self):
        self.p = self.P(0)

    def test(self):
        self.assertTrue(True)
    
    def testRay(self):
        print(self.p.x)
        self.p.x=1001
        self.p.y=3

        print("x == " + str(self.p.x))
        print("y == " + str(self.p.y))
        self.assertEquals(self.p.x,4)
        
    class P(object):
        
        y=0
        def __init__(self,x):
            self.x = x

        @property
        def x(self):
            self.__x = self.y+self.__x
            print("self.__x === "+ str(self.__x))
            return self.__x

        @x.setter
        def x(self, x):
            if x < 0:
                self.__x = 0
            elif x > 1000:
                print("self.__x === "+ str(self.__x))
                self.__x = 1000
            else:
                self.__x = x

if __name__ == '__main__':
    unittest.main()




