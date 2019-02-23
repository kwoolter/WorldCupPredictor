import model
import cli

def main():

    # fixtures = model.FixtureFactory()
    # fixtures.load()
    # fixtures.print()

    c = cli.WCCLI()
    c.cmdloop()



if __name__ == "__main__":
    main()
