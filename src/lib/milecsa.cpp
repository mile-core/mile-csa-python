#include <Python.h>
#include <stdio.h>
#include "milecsa.hpp"
#include "json.hpp"

//#define __DUBUG_PRINT_ARGS__

static PyObject *PyErr_MileCsaError;

auto __error_handler = [](milecsa::result code, const std::string &error) mutable -> void {
    PyErr_SetString(PyErr_MileCsaError, error.c_str());
};

static PyObject* py_generate_key_pair(PyObject *self, PyObject *args)
{
    if (auto pair = milecsa::keys::Pair::Random(__error_handler))
    {
        return Py_BuildValue("{ssss}",
                             "public-key",
                             pair->get_public_key().encode().c_str(),
                             "private-key", pair->get_private_key().encode().c_str());
    }
    else {
        return NULL;
    }
}

static PyObject* py_generate_key_pair_with_secret_phrase(PyObject *self, PyObject *args)
{
    char *phrase;

    if (!PyArg_ParseTuple(args, "s", &phrase)) {
        PyErr_SetString(PyErr_MileCsaError, "secret phrase must be in args");
        return NULL;
    }

    if (auto pair = milecsa::keys::Pair::WithSecret(phrase, __error_handler))
    {
        return Py_BuildValue("{ssss}",
                             "public-key",
                             pair->get_public_key().encode().c_str(),
                             "private-key", pair->get_private_key().encode().c_str());
    }
    else {
        return NULL;
    }
}

static PyObject* py_generate_key_pair_from_private_key(PyObject *self, PyObject *args) {
    char *private_key;

    if (!PyArg_ParseTuple(args, "s", &private_key)) {
        PyErr_SetString(PyErr_MileCsaError, "secret phrase must be in args");
        return NULL;
    }

    if (auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler)) {
        return Py_BuildValue("{ssss}",
                             "public-key",
                             pair->get_public_key().encode().c_str(),
                             "private-key", pair->get_private_key().encode().c_str());
    } else {
        return NULL;
    }
}

static PyObject* py_create_transaction_transfer_assets(PyObject *self, PyObject *args)
{

#ifdef __DUBUG_PRINT_ARGS__
    PyObject_Print(args, stderr, Py_PRINT_RAW);
#endif

    char *dest;
    char *pk;
    char *private_key;
    int  assetCode;
    float amount;
    float fee;
    char *memo;
    uint256_t blockId;
    uint64_t transactionId;

    if (!PyArg_ParseTuple(args, "sssKKiffz", &pk, &private_key, &dest,
                          &blockId, &transactionId, &assetCode,
                          &amount, &fee, &memo)) {
        PyErr_SetString(PyErr_MileCsaError, "not enough args");
        return NULL;
    }

    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);

    if(!pair) return NULL;

    if(pair->get_public_key().encode() != pk) {
        PyErr_SetString(PyErr_MileCsaError, "public key mismatches private key");
        return NULL;
    }

     if (auto transfer = milecsa::transaction::Transfer<nlohmann::json>::CreateRequest(
            *pair,
            dest,
            blockId,
            transactionId,
            milecsa::assets::TokenFromCode(assetCode),
            amount,
            fee,
            memo == NULL ? "" : memo,
            __error_handler)) {


        return Py_BuildValue("s", transfer->get_body()->dump().c_str());
    }

    return NULL;
}

static PyObject* py_create_transaction_emission(PyObject *self, PyObject *args)
{

#ifdef __DUBUG_PRINT_ARGS__
    PyObject_Print(args, stderr, Py_PRINT_RAW);
#endif

    char *pk;
    char *private_key;
    int  assetCode;
    float fee;
    uint256_t blockId;
    uint64_t transactionId;

    if (!PyArg_ParseTuple(args,
                           "ssKKif",
                           &pk,
                           &private_key,
                           &blockId,
                           &transactionId,
                           &assetCode,
                           &fee)) {
        PyErr_SetString(PyErr_MileCsaError, "not enough args");
        return NULL;
    }

    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);

    if(!pair) return NULL;

    if(pair->get_public_key().encode() != pk) {
        PyErr_SetString(PyErr_MileCsaError, "public key mismatches private key");
        return NULL;
    }

     if (auto transfer = milecsa::transaction::Emission<nlohmann::json>::CreateRequest(
            *pair,
            blockId,
            transactionId,
            milecsa::assets::TokenFromCode(assetCode),
            fee,
            __error_handler)) {


        return Py_BuildValue("s", transfer->get_body()->dump().c_str());
    }

    return NULL;
}

static PyObject* py_create_transaction_register_node(PyObject *self, PyObject *args)
{
    char *nodeAddress;
    char *pk;
    char *private_key;
    int  assetCode;
    float amount;
    uint256_t blockId;
    uint64_t transactionId;

    if (!PyArg_ParseTuple(args, "sssKKif",
                            &pk,
                            &private_key,
                             &nodeAddress,
                             &blockId,
                             &transactionId,
                             &assetCode,
                             &amount)) {
      PyErr_SetString(PyErr_MileCsaError, "not enough args");
      return NULL;
    }

    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);

    if(!pair) return NULL;

    if(pair->get_public_key().encode() != pk) {
        PyErr_SetString(PyErr_MileCsaError, "public key mismatches private key");
        return NULL;
    }

    if (auto transfer = milecsa::transaction::Node<nlohmann::json>::CreateRegisterRequest(
            *pair,
            nodeAddress,
            blockId,
            transactionId,
            milecsa::assets::TokenFromCode(assetCode),
            amount,
            __error_handler)) {


        return Py_BuildValue("s", transfer->get_body()->dump().c_str());
    }

    return NULL;
}


static PyObject* py_create_transaction_unregister_node(PyObject *self, PyObject *args)
{

    char *nodeAddress;
    char *pk;
    char *private_key;
    uint256_t blockId;
    uint64_t transactionId;

    if (!PyArg_ParseTuple(args, "sssKK", &pk, &private_key, &nodeAddress, &blockId, &transactionId)) {
      PyErr_SetString(PyErr_MileCsaError, "not enough args");
      return NULL;
    }

    auto pair = milecsa::keys::Pair::FromPrivateKey(private_key, __error_handler);

    if(!pair) return NULL;

    if(pair->get_public_key().encode() != pk) {
        PyErr_SetString(PyErr_MileCsaError, "public key mismatches private key");
        return NULL;
    }

    if (auto transfer = milecsa::transaction::Node<nlohmann::json>::CreateUnregisterRequest(
            *pair,
            nodeAddress,
            blockId,
            transactionId,
            __error_handler)) {


        return Py_BuildValue("s", transfer->get_body()->dump().c_str());
    }

    return NULL;
}


static PyMethodDef milecsaMethods[] = {
      {"__key_pair", py_generate_key_pair, METH_NOARGS, "Mile"},
      {"__key_pair_with_secret_phrase", py_generate_key_pair_with_secret_phrase, METH_VARARGS, "Mile"},
      {"__key_pair_from_private_key", py_generate_key_pair_from_private_key, METH_VARARGS, "Mile"},
      {"__transfer_assets", py_create_transaction_transfer_assets, METH_VARARGS, "Mile"},
      {"__emission", py_create_transaction_emission, METH_VARARGS, "Mile"},
      {"__register_node", py_create_transaction_register_node, METH_VARARGS, "Mile"},
      {"__unregister_node", py_create_transaction_unregister_node, METH_VARARGS, "Mile"},
      {NULL, NULL, 0, NULL}
};

static struct PyModuleDef __milecsa =
        {
                PyModuleDef_HEAD_INIT,
                "__milecsa",   /* name of module */
                "",          /* module documentation, may be NULL */
                -1,          /* size of per-interpreter state of the module, or -1 if the module keeps state in global variables. */
                milecsaMethods
        };

PyMODINIT_FUNC PyInit___milecsa(void)
{

    PyObject *m;

    m = PyModule_Create(&__milecsa);
    if (m == NULL)
        return NULL;

    PyErr_MileCsaError = PyErr_NewException("milecsa.error", NULL, NULL);
    Py_INCREF(PyErr_MileCsaError);
    PyModule_AddObject(m, "error", PyErr_MileCsaError);

    return m;
}
