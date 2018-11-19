#include <pybind11/pybind11.h>

namespace py = pybind11;

/**
 * Caster for nlohmann::json
 * todo extract to lib
 */

namespace pybind11 { namespace detail {
    template <> struct type_caster<nlohmann::json> {
    public:
        /**
         * This macro establishes the name 'json' in
         * function signatures and declares a local variable
         * 'value' of type json
         */
        PYBIND11_TYPE_CASTER(nlohmann::json, _("json"));

        /**
         * Conversion part 1 (Python -> C++)
         */
        bool load(handle src, bool) {
            throw std::runtime_error("Not implemented");
        }

        /**
         * Conversion part 2 (C++ -> Python)
         */
        static handle cast(nlohmann::json src, return_value_policy /* policy */, handle /* parent */) {
            return convert(src);
        }
    private:
        static handle convert(const nlohmann::json& element) {
            if (element.is_null()) {
                return py::none().release();

            } else if (element.is_boolean()) {
                return py::bool_(element).release();

            } else if (element.is_number_integer()) {
                return py::int_((int64_t)element).release();

            } else if (element.is_number_unsigned()) {
                return py::int_((uint64_t)element).release();

            } else if (element.is_number_float()) {
                return py::float_((double)element).release();

            } else if (element.is_string()) {
                return py::str((std::string)element).release();

            } else if (element.is_array()) {
                py::list result;
                for (auto const& subelement: element) {
                    result.append(convert(subelement));
                }
                return result.release();

            } else if (element.is_object()) {
                py::dict result;
                for (auto it = element.begin(); it != element.end(); ++it) {
                    result[convert(it.key())] = convert(it.value());
                }
                return result.release();
            }

            throw std::runtime_error("Unsupported json type");
        }
    };
}} // namespace pybind11::detail
