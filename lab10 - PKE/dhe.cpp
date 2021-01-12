#include <openssl/bio.h>
#include <openssl/bn.h>
#include <openssl/dh.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/pem.h>
#include <openssl/rand.h>

#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <fcntl.h>
#include <unistd.h>
#include <getopt.h>

#include <iostream>
#include <string>

using namespace std;

constexpr auto LENGTH = 256;

#define MAXSIZE 4096
#define PUB_KEY_LEN 256
#define ERR_SOCKET 2
#define ERR_CONN 3

#define CHECK(assertion, call_description)  \
  do {                                      \
    if (!(assertion)) {                     \
      fprintf(stderr, "(%s, %d): ",         \
        __FILE__, __LINE__);                \
      perror(call_description);             \
      exit(EXIT_FAILURE);                   \
    }                                       \
  } while(0)


/**
 * Open file <filename>, read public Diffie-Hellman parameters P and G and store them in <pdhm>
 * @param pdhm Diffie-Hellman key exchange context
 * @param filename file from which to read P and G
 */
DH* __read_pg_from_file(const char* filename)
{
    BIO* pbio;
    DH* pdh;

    /* Get DH modulus and generator (P and G) */
    pbio = BIO_new_file(filename, "r");
    CHECK(pbio != NULL, "BIO_new_file");

    /* Read P and G from f */
    pdh = PEM_read_bio_DHparams(pbio, NULL, NULL, NULL);
    CHECK(pdh != NULL, "PEM_read_bio_DHparams");

    BIO_free(pbio);
    return pdh;
}

void my_receive(int sockfd, char * buffer, int length) {
    int bytes_received = 0;
    int rc;
    while (bytes_received < length) {
        rc = recv(sockfd, buffer + bytes_received, length - bytes_received, 0);
        CHECK(rc >= 0, "recv");

        bytes_received += rc;
    }
}

int main(int argc, char* argv[])
{
    int opt = 0,  ret = 0;
    int file_fd, file_size;
    int k, n, len, total = 0;

    unsigned char buf_pubkey_ours[256];
    auto buf_pubkey_theirs = string(LENGTH, 0);
    unsigned char buf_secret_key[256];

    BIGNUM *pub_key, *priv_key, *pub_key_theirs;

    auto server_port = 1337u;
    auto server_addr = sockaddr_in();
    auto server_len = socklen_t();

    auto server_ip = "127.0.0.1"s;
    auto filename = "recv_file";

    auto client_sockfd = 0;
    timeval start, connect_done, transfer_done;

    while ((opt = getopt(argc, argv, "i:p:f:")) != -1)
    {
        switch (opt)
        {
            case 'i':
                server_ip = optarg;
                break;
            case 'p':
                server_port = atoi(optarg);
                break;
            case 'f':
                filename = optarg;
                break;
            default:
                fprintf(stderr, "Usage %s [-i SERVER_IP] [-p PORT] [-f RECV_FILENAME]\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }

    DH* tdh = __read_pg_from_file("dhparam.pem");

    // TODO 1: obtain DH public key from the parameters already saved in tdh
    DH_generate_key(tdh);

    // TODO 2: obtain the public and private keys in the BIGNUM structs
    DH_get0_key(tdh, const_cast<const BIGNUM**>(&pub_key),
                     const_cast<const BIGNUM**>(&priv_key));

    // Export public key to binary and print it
    n =  BN_num_bytes(pub_key);
    cout << "[client] Pub key has " << n << " bytes\n";
    CHECK(PUB_KEY_LEN == n, "DH PUB KEY LEN");
    BN_bn2bin(pub_key, buf_pubkey_ours);
    cout << "[client] Our public key is: ";

    cout.setf(ios::hex, ios::basefield);
    for (const auto& k: buf_pubkey_ours)
        cout << 0 + k; cout << endl;
    cout.unsetf(ios::hex);

    /* Open a TCP socket */
    client_sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (client_sockfd < 0)
    {
        perror("Error in socket()");
        exit(ERR_SOCKET);
    }

    /* Setup sockaddr_in struct */
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = inet_addr(server_ip.c_str());
    server_addr.sin_port = htons(server_port);

    server_len = sizeof(server_addr);

    file_fd = open(filename, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    CHECK(file_fd >= 0, "open");

    /* Connect */
    gettimeofday(&start, nullptr);
    ret = connect(client_sockfd, (sockaddr*)&server_addr, server_len);
    gettimeofday(&connect_done, nullptr);
    CHECK(ret >= 0, "connect");

    printf("[client] Connected to %d\n", server_port);

    // Send our public key
    printf("[client] Sending public key...\n");
    len = send(client_sockfd, buf_pubkey_ours, n, 0);
    CHECK(len >= 0, "send");

    // Get the other party public key
    my_receive(client_sockfd, &buf_pubkey_theirs[0], LENGTH);
    cout << "[client] Received public key from server...\n";
    cout << "[client] The received public key is: ";

    cout.setf(ios::hex, ios::basefield);
    for (const auto& k: buf_pubkey_theirs)
        cout << 0 + k; cout << endl;
    cout.unsetf(ios::hex);

    BN_bin2bn(reinterpret_cast<const unsigned char*>(buf_pubkey_theirs.c_str()),
              buf_pubkey_theirs.size(), pub_key_theirs);

    // TODO 4: compute the secret key from our DH structure and the other party public key
    // return the length in the integer n, although we expect it to be PUB_KEY_LEN
    DH_compute_key(buf_secret_key, pub_key, tdh);

    cout << "[client] Exchanged secret key has " << n << " bytes\n";
    cout << "[client] The exchanged secret key is: ";
    cout.setf(ios::hex, ios::basefield);
    for (const auto& k: buf_secret_key)
        cout << 0 + k; cout << endl;
    cout.unsetf(ios::hex);

    DH_free(tdh);
}