#include <pet/animal.hpp>


std::string call_go(Animal *animal) {
    return animal->go(3);
}

std::string get_name(Animal *animal) {
    return animal->name();
}
