#include <openssl/evp.h>
#include <openssl/err.h>

#include <string>
#include <iostream>

using namespace std;

using ustring = basic_string<unsigned char>;
using uchar_p = unsigned char*;

// ============================================================================

void hexdump(const ustring& str)
{
    cout << hex;
    for (auto i: str)
        cout << 0 + i;
    cout << endl;
}

// ============================================================================

int aes_gcm_encrypt(const ustring& plaintext, const ustring& key,
                    const ustring& iv, ustring& ciphertext)
{
    auto ctx = EVP_CIPHER_CTX_new();
    auto length = 0, aux = 0;

    EVP_EncryptInit_ex(ctx, EVP_aes_256_gcm(), nullptr, nullptr, nullptr);

    EVP_EncryptInit_ex(ctx, nullptr, nullptr, key.c_str(), iv.c_str());

    EVP_EncryptUpdate(ctx, &ciphertext[0], &aux,
                      plaintext.c_str(), plaintext.size());
    length = aux;

    EVP_EncryptFinal_ex(ctx, &ciphertext[aux], &aux);
    length += aux;

    auto tag = ustring((uchar_p)" ", 16);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_GET_TAG, 16, &tag[0]);
    //cout << tag.c_str() << endl;

    EVP_CIPHER_CTX_free(ctx);

    return length;
}

// ============================================================================

int aes_gcm_decrypt(const ustring& ciphertext, const ustring& key,
                    const ustring& iv, ustring& plaintext)
{
    auto ctx = EVP_CIPHER_CTX_new();
    auto length = 0, aux = 0;

    EVP_DecryptInit_ex(ctx, EVP_aes_256_gcm(), nullptr, nullptr, nullptr);
    EVP_DecryptInit_ex(ctx, nullptr, nullptr, key.c_str(), iv.c_str());

    EVP_DecryptUpdate(ctx, &plaintext[0], &aux, ciphertext.c_str(), ciphertext.size());
    length = aux;

    auto tag = ustring((uchar_p)" ", 16);
    EVP_CIPHER_CTX_ctrl(ctx, EVP_CTRL_GCM_SET_TAG, 16, &tag[0]);
    //cout << tag.c_str() << endl;

    auto ret = EVP_DecryptFinal_ex(ctx, &plaintext[aux], &aux);
    EVP_CIPHER_CTX_free(ctx);

    if (ret > 0)
    {
        length += aux;
        return length;
    }

    return -1;
}

// ============================================================================

int main(int argc, char* argv[])
{
    ERR_load_crypto_strings();

    auto key = ustring((uchar_p)"0123456789abcdef0123456789abcdef");
    auto iv  = ustring((uchar_p)"0123456789ab");
    auto plaintext  = ustring((uchar_p)"Hello, SSLWorld!\n");
    auto ciphertext = ustring((uchar_p)" ", size(plaintext));

    cout << "Plaintext = " << plaintext.c_str();
    cout << "Plaintext (hex) = "; hexdump(plaintext);

    aes_gcm_encrypt(plaintext, key, iv, ciphertext);
    cout << "Ciphertext (hex) = "; hexdump(ciphertext);

    auto plaintext2 = ustring((uchar_p)" ", size(plaintext));
    aes_gcm_decrypt(ciphertext, key, iv, plaintext2);

    cout << "Done decrypting!\n";
    cout << "Plaintext2 (hex) = "; hexdump(plaintext2);
    cout << "Plaintext2 = " << plaintext2.c_str() << endl;

    cout << ((plaintext2 == plaintext) ? "" : "Nu-i ");
    cout << "OK!\n";
}