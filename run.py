import model

def main():

    fixtures = model.FixtureFactory()
    fixtures.load()
    fixtures.print()



main()