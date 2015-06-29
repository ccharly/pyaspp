#py= cpp.define("salut", "LOL")

#py= cpp.define('ONE_AND_ONE', 1 + 1)

#py a_python_value = ''.join(['py', 'thon'])
#py= cpp.define('PYTHON', a_python_value)

#py{

def foo():
    for i in range(10):
        yield cpp.define('ITER' + str(i), i)

#py}

#py= foo()

int main() {
    return 0;
}
