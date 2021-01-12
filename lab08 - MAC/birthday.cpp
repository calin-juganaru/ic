#include <openssl/sha.h>

#include <stdlib.h>
#include <iostream>
#include <time.h>

#include <vector>
#include <string>
#include <unordered_map>

using namespace std;

constexpr auto N_BITS = 16;
constexpr auto LENGTH = 8;
constexpr auto MSGS = 1 << N_BITS;

// ============================================================================

int main()
{
    unsigned char md[20];

    srand(time(nullptr));

    while (true)
    {
        auto messages = vector<string>(MSGS);
        auto hashes = unordered_map<string, string>();

        for (auto& message: messages)
        {
            message.resize(LENGTH);

            for (auto& character: message)
                character = rand() % 256;

            SHA_CTX context;
            SHA1_Init(&context);
            SHA1_Update(&context, message.c_str(), LENGTH);
            SHA1_Final(md, &context);

            auto aux = to_string(static_cast<int>(md[0]))
                     + to_string(static_cast<int>(md[1]))
                     + to_string(static_cast<int>(md[2]))
                     + to_string(static_cast<int>(md[3]));

            if (hashes.contains(aux))
            {
                cout << "Gasiram coliziune: \n"
                     << "   hash = " << aux << endl
                     << "   msg1 = " << message << endl
                     << "   msg2 = " << hashes[aux] << endl;

                return 0;
            }
            else hashes[aux] = message;
        }
    }
}

// ============================================================================