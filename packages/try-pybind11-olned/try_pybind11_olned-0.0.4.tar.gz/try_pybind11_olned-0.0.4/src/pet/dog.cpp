#include <pet/dog.hpp>

std::string Dog::go(int n_times)
{
    std::string result;
    for (int i = 0; i < n_times; ++i)
    {
        if (i > 0)
        {
            result += ' ';
        }
        result += bark();
    }

    return result;
}

std::string Dog::bark() { return "woof!"; }
