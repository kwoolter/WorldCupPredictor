import model

def main():

    fixtures = model.FixtureFactory()
    fixtures.load()
    fixtures.print()


if __name__ == "__main__":
    main()