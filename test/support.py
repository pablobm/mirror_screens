print __package__

def fixture(name):
    return open("./test/data/" + name).read()
