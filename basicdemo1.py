__author__ = 'martin berridge'



from dag import DagMethod, DomainObj

class Greeter(DomainObj):
    @DagMethod
    def bonjour(self):
        return "bonjour"

    @DagMethod
    def tout(self):
            return " tout "

    @DagMethod
    def le_monde(self):
        return "le monde"

    @DagMethod
    def greeting(self):
        return self.bonjour() + self.tout()  + self.le_monde()

# ---------------------------------------------------------------------

def main():
    g = Greeter()

    # all DagMethods invalid - recalculated
    print g.greeting()
    # call DagMethods valid - return cached values only
    print g.greeting()

    # DagMethod bonjour overridden - all downstream nodes greeting invalidated and recalculated
    g.bonjour.set_value("guten tag")
    print g.greeting()

    # return DagMethod back to it's original value by invalidating it - all downstream nodes invalidated too (greeting)
    g.bonjour.invalidate()
    print g.greeting()


if __name__ == '__main__':
    main()

