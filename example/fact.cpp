#py MAX_N = 20

#py{

def cpp_fact(n, res):
    return cpp.define('FACT_{}'.format(n), res)

def gen_fact():
    acc = 1
    yield cpp_fact(0, 1)
    for n in range(1, MAX_N + 1):
        acc *= n
        yield cpp_fact(n, acc)

#py}

#py= gen_fact()

int main() {
    std::cout << FACT_1 << std::endl;
    std::cout << FACT_10 << std::endl;
    std::cout << FACT_20 << std::endl;
    return 0;
}
