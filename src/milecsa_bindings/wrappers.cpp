#include <stdio.h>
#include <optional>
#include <map>
#include <string>

#include "milecsa.hpp"
#include "json.hpp"

using std::string;
using std::map;
using std::optional;


auto __error_handler = [](milecsa::result code, const std::string &error) mutable -> void {
   throw std::runtime_error(error);
};


static map<string, string> pairMap(const milecsa::keys::Pair& pair)
{
    return {
        {"public-key", pair.get_public_key().encode()},
        {"private-key", pair.get_private_key().encode()},
    };
}


static map<string, string> py_generate_key_pair()
{
    auto pair = milecsa::keys::Pair::Random(__error_handler);
    if (!pair) {
        throw std::runtime_error("Key pair generation error");
    }

    return pairMap(*pair);
}


static map<string, string> py_generate_key_pair_with_secret_phrase(const string& phrase)
{
    auto pair = milecsa::keys::Pair::WithSecret(phrase, __error_handler);
    if (!pair)
    {
        throw std::runtime_error("Key pair generation error");
    }

    return pairMap(*pair);
}


static map<string, string> py_generate_key_pair_from_private_key(const string& private_key)
{
    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);
    if (!pair) {
        throw std::runtime_error("Key pair generation error");
    }

    return pairMap(*pair);
}


static milecsa::keys::Pair requireKeyPair(const string& private_key, const string& public_key) {
    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);
    if(!pair) {
        throw std::invalid_argument("Invalid private key");
    };

    if(pair->get_public_key().encode() != public_key) {
        throw std::invalid_argument("Public key mismatches private key");
    }

    return *pair;
}


static nlohmann::json py_create_transaction_transfer_assets(
    const string& public_key,
    const string& private_key,
    const string& destination_public_key,
    uint64_t block_id, //todo uint256_t
    uint64_t transaction_id,
    int asset_code,
    float amount,
    float fee,
    const string& memo
) {
    auto pair = requireKeyPair(private_key, public_key);
    auto request = milecsa::transaction::Transfer<nlohmann::json>::CreateRequest(
        pair,
        destination_public_key,
        block_id,
        transaction_id,
        milecsa::assets::TokenFromCode(asset_code),
        amount,
        fee,
        memo,
        __error_handler
    );

    if (!request) {
        throw std::runtime_error("Failed to create transaction");
    }

    return *request->get_body();
}


static nlohmann::json py_create_transaction_emission(
    const string& public_key,
    const string& private_key,
    uint64_t block_id, //todo uint256_t
    uint64_t transaction_id,
    int asset_code,
    float fee
) {
    auto pair = requireKeyPair(private_key, public_key);
    auto request = milecsa::transaction::Emission<nlohmann::json>::CreateRequest(
        pair,
        block_id,
        transaction_id,
        milecsa::assets::TokenFromCode(asset_code),
        fee,
        __error_handler
    );
    if (!request) {
        throw std::runtime_error("Failed to create transaction");
    }

    return *request->get_body();
}


static nlohmann::json py_create_transaction_register_node(
    const string& public_key,
    const string& private_key,
    const string& node_address,
    uint64_t block_id, //todo uint256_t
    uint64_t transaction_id,
    int asset_code,
    float amount
) {
    auto pair = requireKeyPair(private_key, public_key);
    auto request = milecsa::transaction::Node<nlohmann::json>::CreateRegisterRequest(
        pair,
        node_address,
        block_id,
        transaction_id,
        milecsa::assets::TokenFromCode(asset_code),
        amount,
        __error_handler
    );
    if (!request) {
        throw std::runtime_error("Failed to create transaction");
    }

    return *request->get_body();
}


static nlohmann::json py_create_transaction_unregister_node(
    const string& public_key,
    const string& private_key,
    const string& node_address,
    uint64_t block_id, //todo uint256_t
    uint64_t transaction_id
) {
    auto pair = requireKeyPair(private_key, public_key);
    auto request = milecsa::transaction::Node<nlohmann::json>::CreateUnregisterRequest(
        pair,
        node_address,
        block_id,
        transaction_id,
        __error_handler
    );
    if (!request) {
        throw std::runtime_error("Failed to create transaction");
    }

    return *request->get_body();
}
