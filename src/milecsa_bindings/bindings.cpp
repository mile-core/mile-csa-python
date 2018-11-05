#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <stdio.h>
#include "wrappers.cpp"

namespace py = pybind11;

using namespace pybind11::literals;


PYBIND11_MODULE(__milecsa, m) {
    m.doc() = ""; // optional module docstring

    m.def(
        "__key_pair",
        &py_generate_key_pair,
        "Generate key pair"
    );

    m.def(
        "__key_pair_with_secret_phrase",
        &py_generate_key_pair_with_secret_phrase,
        "Generate key pair from secret phrase",
        "phrase"_a
    );

    m.def(
        "__key_pair_from_private_key",
        &py_generate_key_pair_from_private_key,
        "Generate key pair from private key",
        "private_key"_a
    );

    m.def(
        "__transfer_assets",
        &py_create_transaction_transfer_assets,
        "Create transfer asset transaction body",
        "public_key"_a,
        "private_key"_a,
        "destination_public_key"_a,
        "block_id"_a,
        "transaction_id"_a,
        "asset_code"_a,
        "amount"_a,
        "fee"_a,
        "memo"_a = ""
    );

    m.def(
        "__emission",
        &py_create_transaction_emission,
        "Create emission transaction body",
        "public_key"_a,
        "private_key"_a,
        "block_id"_a,
        "transaction_id"_a,
        "asset_code"_a,
        "fee"_a
    );

    m.def(
        "__register_node",
        &py_create_transaction_register_node,
        "Create register node transaction body",
        "public_key"_a,
        "private_key"_a,
        "node_address"_a,
        "block_id"_a,
        "transaction_id"_a,
        "asset_code"_a,
        "amount"_a
    );

    m.def(
        "__unregister_node",
        &py_create_transaction_unregister_node,
        "Create unregister node transaction body",
        "public_key"_a,
        "private_key"_a,
        "node_address"_a,
        "block_id"_a,
        "transaction_id"_a
    );
}
