from Engine.User import User

if __name__ == "__main__":
    # The client code.

    hello = Hello()
    world = World()

    observer_a = User("doctor")
    hello.attach(observer_a)

    observer_b = User("nurse")
    world.attach(observer_b)

    observer_c = User("participant")
    hello.attach(observer_c)
    world.attach(observer_c)

    hello.exec()
    world.exec()

    world.detach(observer_c)

    world.exec()
