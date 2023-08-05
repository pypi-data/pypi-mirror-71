static double __Pyx__PyObject_AsDouble(PyObject* obj) {
    PyObject* float_value;
#if !CYTHON_USE_TYPE_SLOTS
    float_value = PyNumber_Float(obj);  if ((0)) goto bad;
    (void)__Pyx_PyObject_CallOneArg;
#else
    PyNumberMethods *nb = Py_TYPE(obj)->tp_as_number;
    if (likely(nb) && likely(nb->nb_float)) {
        float_value = nb->nb_float(obj);
        if (likely(float_value) && unlikely(!PyFloat_Check(float_value))) {
            PyErr_Format(PyExc_TypeError,
                "__float__ returned non-float (type %.200s)",
                Py_TYPE(float_value)->tp_name);
            Py_DECREF(float_value);
            goto bad;
        }
    } else if (PyUnicode_CheckExact(obj) || PyBytes_CheckExact(obj)) {
#if PY_MAJOR_VERSION >= 3
        float_value = PyFloat_FromString(obj);
#else
        float_value = PyFloat_FromString(obj, 0);
#endif
    } else {
        float_value = __Pyx_PyObject_CallOneArg((PyObject*)&PyFloat_Type, obj);
    }
#endif
    if (likely(float_value)) {
        double value = PyFloat_AS_DOUBLE(float_value);
        Py_DECREF(float_value);
        return value;
    }
bad:
    return (double)-1;
}

