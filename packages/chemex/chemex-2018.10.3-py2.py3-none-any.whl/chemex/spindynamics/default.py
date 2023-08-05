import itertools
import re
import string

import lmfit as lf
from scipy import constants as cst

from chemex import parameters

OTHER_SPIN = {"i": "s", "s": "i"}

STATES = "abcd"

RE_VARNAME = re.compile(
    "^(?P<name>.+?)(_(?P<spin>[is]{1,2}))?(_(?P<state>[abcd]{1,2}))?$"
)


def create_params(basis, model, nuclei=None, conditions=None, constraints=None):
    """TODO"""

    fnames_k, params_k = create_params_k(model=model, conditions=conditions)
    fnames_lr, params_lr = create_params_lr(basis, conditions, nuclei)

    params_lr = set_thermal_factors(fnames_lr, params_lr, nuclei)

    if constraints == "hn_ap":
        fnames_lr, params_lr = set_hn_ap_constraints(
            fnames_lr, params_lr, nuclei=nuclei, conditions=conditions
        )

    if constraints == "nh":
        fnames_lr, params_lr = set_nh_constraints(fnames_lr, params_lr)

    fnames = dict(**fnames_k, **fnames_lr)

    # hack to add parameters depending on parameters not added yet
    params = lf.Parameters()
    params.add_many(*(lf.Parameter(fname) for fname in fnames.values()))
    params.update(params_lr)
    params.update(params_k)

    return fnames, params


def create_params_lr(basis, conditions, nuclei):
    names = get_default_names(basis)
    fnames = set_fnames(names, nuclei, conditions)
    params = buid_params(fnames)
    for name, fname in fnames.items():
        if name.endswith(("_b", "_c", "_d")):
            name_a = "".join((name[:-1], "a"))
            fname_a = fnames[name_a]
            params[fname].set(expr=fname_a)
    for state in "bcd":
        short_name = f"cs_{state}"
        short_name_expr = f"cs_a + dw_a{state}"
        parameters.set_param_expr(params, short_name, short_name_expr)
    return fnames, params


def get_default_names(basis):
    """TODO"""

    names = set()
    for name in basis._matrices:

        name_parsed = RE_VARNAME.match(name).groupdict()

        if not name.startswith(("k", "p", "w1", "carrier", "j_eff", "w_")):
            names.add(name)

            if name_parsed["name"] == "cs" and name_parsed["state"] != "a":
                name_dw = "dw_{spin}_a{state}".format(**name_parsed)
                names.add(name_dw)

    return names


def set_fnames(names=None, nuclei=None, conditions=None):
    """TODO"""

    if names is None:
        names = {}

    fnames = {}

    for name in names:
        name_parsed = RE_VARNAME.match(name).groupdict()

        short_name = "_".join(
            name_parsed[key]
            for key in ("name", "state")
            if name_parsed[key] is not None
        )

        definition = {"temperature": conditions.get("temperature", 0.0)}

        spin = name_parsed["spin"]

        if spin is None:
            spin = "is"

        definition["nuclei"] = nuclei[spin]

        if not name.startswith(("dw", "cs", "j")):
            definition["h_larmor_frq"] = conditions.get("h_larmor_frq", 1.0)

        fnames[name] = parameters.ParamName(short_name, **definition).to_full_name()

    return fnames


def buid_params(fnames):
    """TODO"""

    params = lf.Parameters()

    for name, full_name in fnames.items():
        param = lf.Parameter(full_name, value=0.0, vary=False)

        if name.startswith("p"):
            param.set(min=0.0, max=1.0)
        elif name.startswith("k"):
            param.set(min=0.0)
        elif name.startswith("r2"):
            param.set(value=10.0, min=0.0)
        elif name.startswith("r1"):
            param.set(value=1.0, min=0.0)
        elif name == "j":
            param.set(value=-93.0)

        params[full_name] = param

    return params


def set_thermal_factors(fnames, params, nuclei):
    """TODO"""

    for spin, state in itertools.product("is", STATES):

        theta = f"theta_{spin}_{state}"

        if theta in fnames:

            r1_expr = f"r1_{spin}_{state}"
            sigma = f"sigma_{state}"
            pop = f"p{state}"

            terms = []

            terms.append(
                "{g_ratio} * {r1_expr}".format(
                    g_ratio=nuclei.atoms[spin]["g_ratio"], r1_expr=fnames[r1_expr]
                )
            )

            if sigma in fnames:
                terms.append(
                    "{g_ratio} * {sigma}".format(
                        g_ratio=nuclei.atoms[OTHER_SPIN[spin]]["g_ratio"],
                        sigma=fnames[sigma],
                    )
                )

            expr = "{pop} * ({sum})".format(pop=fnames[pop], sum=" + ".join(terms))

            params[fnames[theta]].set(expr=expr)

    for state in STATES:

        theta = f"theta_is_{state}"

        if theta in fnames:

            pop = f"p{state}"

            terms = []

            for spin in "is":

                etaz = f"etaz_{spin}_{state}"

                if etaz in fnames:
                    terms.append(
                        "{gamma} * {etaz}".format(
                            gamma=nuclei.atoms[spin]["g_ratio"], etaz=fnames[etaz]
                        )
                    )

            expr = "{pop} * ({sum})".format(pop=fnames[pop], sum=" + ".join(terms))

            params[fnames[theta]].set(expr=expr)

    return params


def set_hn_ap_constraints(fnames, params, nuclei=None, conditions=None):

    name_s = nuclei.get("s")

    if name_s is None:
        return fnames, params

    attributes = conditions.copy()
    attributes.update({"nuclei": name_s})

    names = (f"r1_s_{state}" for state in STATES if f"r1_i_{state}" in fnames)
    fnames, params = _add_params(fnames, params, names, attributes)

    settings = {}

    for state in STATES:

        r1_s = f"r1_s_{state}"
        r1_i = f"r1_i_{state}"
        r2a_i = f"r2a_i_{state}"

        if r1_s not in fnames:
            continue

        expr_r1_s = None
        if state != "a":
            expr_r1_s = "{r1a_a}".format(**fnames)

        expr_r1_i = f"{{r1a_{state}}} - {{r1_s_{state}}}"
        expr_r2a_i = f"{{r2_i_{state}}} - {{r1_s_{state}}}"

        settings[r1_s] = {"value": 1.0, "min": 0.0, "vary": False, "expr": expr_r1_s}
        settings[r1_i] = {"expr": expr_r1_i.format(**fnames)}
        settings[r2a_i] = {"expr": expr_r2a_i.format(**fnames)}

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def set_nh_constraints(fnames, params):

    settings = {}

    for state in STATES:
        r2a_i = f"r2a_i_{state}"
        r2a_s = f"r2a_s_{state}"
        expr_r2a_i = f"{{r2_i_{state}}} + {{r1a_{state}}} - {{r1_i_{state}}}"
        expr_r2a_s = f"{{r2_s_{state}}} - {{r1_i_{state}}}"

        if r2a_i in fnames:
            settings[r2a_i] = {"expr": expr_r2a_i.format(**fnames)}

        if r2a_s in fnames:
            settings[r2a_s] = {"expr": expr_r2a_s.format(**fnames)}

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def create_params_k(model=None, conditions=None):
    """Update the experimental and fitting parameters depending on the model.

    """

    fnames = {}
    params = lf.Parameters()

    attributes = {
        key: conditions.get(key) for key in ("temperature", "p_total", "l_total")
    }

    states = string.ascii_lowercase[: model.state_nb]
    names = ["k{}{}".format(*pairs) for pairs in itertools.permutations(states, 2)]
    names.extend([f"p{state}" for state in states])

    fnames, params = _add_params(fnames, params, names, attributes)

    kinetic_models = {
        "2st.pb_kex": model_2st_pb_kex,
        "3st.pb_kex": model_3st_pb_kex,
        "4st.pb_kex": model_4st_pb_kex,
        "2st.eyring": model_2st_eyring,
        "3st.eyring": model_3st_eyring,
        "2st.binding": model_2st_binding,
    }

    kinetic_model = kinetic_models.get(model.name)

    if kinetic_model is None:
        print("Warning: The 'model' option should either be:")
        for model in sorted(kinetic_models):
            print(f"    - '{model}'")
        print("Set to the default value: '2st.pb_kex'.")
        kinetic_model = kinetic_models["2st.pb_kex"]

    fnames, params = kinetic_model(conditions, fnames, params)

    return fnames, params


def model_2st_pb_kex(conditions, fnames, params):

    attributes = {
        key: conditions.get(key) for key in ("temperature", "p_total", "l_total")
    }

    names = ("kex_ab",)

    fnames, params = _add_params(fnames, params, names, attributes)

    settings = {
        "kex_ab": {"value": 200.0, "min": 0.0, "vary": True},
        "pa": {"expr": "1.0 - {pb}".format(**fnames)},
        "pb": {"value": 0.05, "min": 0.0, "max": 1.0, "vary": True},
        "kab": {"expr": "{kex_ab} * {pb}".format(**fnames)},
        "kba": {"expr": "{kex_ab} * {pa}".format(**fnames)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def model_2st_eyring(conditions, fnames, params):

    attributes = {key: conditions.get(key) for key in ("p_total", "l_total")}
    names = ("dh_b", "ds_b", "dh_ab", "ds_ab")
    fnames, params = _add_params(fnames, params, names, attributes)

    thermo = _define_thermo(conditions.get("temperature"))

    settings = {
        "dh_b": {"value": 6.5e03, "vary": True},
        "ds_b": {"value": 1.0e10},
        "dh_ab": {"value": 6.5e04, "vary": True},
        "ds_ab": {"value": 1.0e10},
        "pa": {"expr": "{kba} / ({kba} + {kab})".format(**fnames)},
        "pb": {"expr": "{kab} / ({kba} + {kab})".format(**fnames)},
        "kab": {"expr": _get_k_from_h_s("ab").format(**fnames, **thermo)},
        "kba": {"expr": _get_k_from_h_s("ba").format(**fnames, **thermo)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def model_2st_binding(conditions, fnames, params):

    attributes = {key: conditions.get(key) for key in ("temperature",)}
    names = ("kd", "kon", "koff")
    fnames, params = _add_params(fnames, params, names, attributes)

    p_total = conditions.get("p_total", 0.0)
    l_total = conditions.get("l_total", 0.0)
    delta = l_total - p_total
    extra = {"delta": delta, "l_total": l_total}

    expr_kab = (
        "{kon} * 0.5 * ({delta} - {kd} "
        "+ sqrt(({delta} - {kd}) ** 2 + 4.0 * {kd} * {l_total}))"
    )

    settings = {
        "kon": {"value": 1.0e7, "vary": True},
        "koff": {"value": 10.0, "vary": True},
        "kd": {"expr": "{koff} / {kon}".format(**fnames)},
        "pa": {"expr": "{kba} / ({kba} + {kab})".format(**fnames)},
        "pb": {"expr": "{kab} / ({kba} + {kab})".format(**fnames)},
        "kab": {"expr": expr_kab.format(**fnames, **extra)},
        "kba": {"expr": "{koff}".format(**fnames)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def model_3st_pb_kex(conditions, fnames, params):

    attributes = {
        key: conditions.get(key) for key in ("temperature", "p_total", "l_total")
    }
    names = ("kex_ab", "kex_ac", "kex_bc")
    fnames, params = _add_params(fnames, params, names, attributes)

    settings = {
        "pa": {"expr": "1.0 - {pb} - {pc}".format(**fnames)},
        "pb": {"value": 0.02, "min": 0.0, "max": 1.0, "vary": True},
        "pc": {"value": 0.02, "min": 0.0, "max": 1.0, "vary": True},
        "kex_ab": {"min": 0.0, "value": 200.0, "vary": True},
        "kex_ac": {"min": 0.0, "value": 0.0},
        "kex_bc": {"min": 0.0, "value": 200.0, "vary": True},
        "kab": {"expr": _get_k_from_kex_p("ab").format(**fnames)},
        "kba": {"expr": _get_k_from_kex_p("ba").format(**fnames)},
        "kac": {"expr": _get_k_from_kex_p("ac").format(**fnames)},
        "kca": {"expr": _get_k_from_kex_p("ca").format(**fnames)},
        "kbc": {"expr": _get_k_from_kex_p("bc").format(**fnames)},
        "kcb": {"expr": _get_k_from_kex_p("cb").format(**fnames)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def model_3st_eyring(conditions, fnames, params):

    attributes = {key: conditions.get(key) for key in ("p_total", "l_total")}
    names = ["dh_b", "dh_c", "dh_ab", "dh_ac", "dh_bc"]
    names.extend(["ds_b", "ds_c", "ds_ab", "ds_ac", "ds_bc"])
    fnames, params = _add_params(fnames, params, names, attributes)

    thermo = _define_thermo(conditions.get("temperature"))

    expr_pa = "{kba} * {kca} / ({kba} * {kca} + {kab} * {kca} + {kac} * {kba})"
    expr_pb = "{kab} * {kcb} / ({kab} * {kcb} + {kba} * {kcb} + {kbc} * {kab})"
    expr_pc = "{kbc} * {kac} / ({kbc} * {kac} + {kcb} * {kab} + {kca} * {kbc})"

    settings = {
        "dh_b": {"value": 6.5e03, "vary": True},
        "dh_c": {"value": 6.5e03, "vary": True},
        "dh_ab": {"value": 6.5e04, "vary": True},
        "dh_bc": {"value": 6.5e04, "vary": True},
        "dh_ac": {"value": 1.0e10},
        "ds_b": {"value": 1.0e10},
        "ds_c": {"value": 1.0e10},
        "ds_ab": {"value": 1.0e10},
        "ds_bc": {"value": 1.0e10},
        "ds_ac": {"value": 1.0e10},
        "kab": {"expr": _get_k_from_h_s("ab").format(**fnames, **thermo)},
        "kba": {"expr": _get_k_from_h_s("bs").format(**fnames, **thermo)},
        "kac": {"expr": _get_k_from_h_s("ac").format(**fnames, **thermo)},
        "kca": {"expr": _get_k_from_h_s("ca").format(**fnames, **thermo)},
        "kbc": {"expr": _get_k_from_h_s("bc").format(**fnames, **thermo)},
        "kcb": {"expr": _get_k_from_h_s("cb").format(**fnames, **thermo)},
        "pa": {"expr": expr_pa.format(**fnames)},
        "pb": {"expr": expr_pb.format(**fnames)},
        "pc": {"expr": expr_pc.format(**fnames)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def model_4st_pb_kex(conditions, fnames, params):

    attributes = {
        key: conditions.get(key) for key in ("temperature", "p_total", "l_total")
    }
    names = ("kex_ab", "kex_ac", "kex_ad", "kex_bc", "kex_bd", "kex_cd")
    fnames, params = _add_params(fnames, params, names, attributes)

    settings = {
        "pa": {"expr": "1.0 - {pb} - {pc} - {pd}".format(**fnames)},
        "pb": {"value": 0.02, "min": 0.0, "max": 1.0, "vary": True},
        "pc": {"value": 0.02, "min": 0.0, "max": 1.0, "vary": True},
        "pd": {"value": 0.02, "min": 0.0, "max": 1.0, "vary": True},
        "kex_ab": {"min": 0.0, "value": 200.0, "vary": True},
        "kex_ac": {"min": 0.0, "value": 0.0},
        "kex_ad": {"min": 0.0, "value": 0.0},
        "kex_bc": {"min": 0.0, "value": 200.0, "vary": True},
        "kex_bd": {"min": 0.0, "value": 0.0},
        "kex_cd": {"min": 0.0, "value": 200.0, "vary": True},
        "kab": {"expr": _get_k_from_kex_p("ab").format(**fnames)},
        "kba": {"expr": _get_k_from_kex_p("ba").format(**fnames)},
        "kac": {"expr": _get_k_from_kex_p("ac").format(**fnames)},
        "kca": {"expr": _get_k_from_kex_p("ca").format(**fnames)},
        "kad": {"expr": _get_k_from_kex_p("ad").format(**fnames)},
        "kda": {"expr": _get_k_from_kex_p("da").format(**fnames)},
        "kbc": {"expr": _get_k_from_kex_p("bc").format(**fnames)},
        "kcb": {"expr": _get_k_from_kex_p("cb").format(**fnames)},
        "kbd": {"expr": _get_k_from_kex_p("bd").format(**fnames)},
        "kdb": {"expr": _get_k_from_kex_p("db").format(**fnames)},
        "kcd": {"expr": _get_k_from_kex_p("cd").format(**fnames)},
        "kdc": {"expr": _get_k_from_kex_p("dc").format(**fnames)},
    }

    fnames, params = _apply_settings(fnames, params, settings)

    return fnames, params


def _add_params(fnames, params, names, attributes):
    for name in names:
        fname = _get_fullname(name, attributes=attributes)
        fnames[name] = fname
        params.add(name=fname, vary=False)

    return fnames, params


def _get_fullname(shortname, attributes=None):
    if attributes is None:
        attributes = {}
    return parameters.ParamName(shortname, **attributes).to_full_name()


def _apply_settings(fnames, params, settings):

    settings_filtered = {key: val for key, val in settings.items() if key in fnames}

    for name, setting in settings_filtered.items():
        fname = fnames[name]
        params[fname]._delay_asteval = True
        params[fname].set(**setting)

    for name in settings_filtered:
        fname = fnames[name]
        params[fname]._delay_asteval = False

    return fnames, params


def _get_k_from_kex_p(states):
    kwargs = {
        "kex": "{{kex_{}{}}}".format(*sorted(states)),
        "p1": "{{p{}}}".format(states[0]),
        "p2": "{{p{}}}".format(states[1]),
    }
    return "{kex} / (1.0 + {p1} / {p2}) if {p2} else 0.0".format(**kwargs)


def _get_k_from_h_s(states):
    expr_dh = "{{dh_{}{}}}".format(*sorted(states))
    expr_ds = "{{ds_{}{}}}".format(*sorted(states))
    if states[0] != "a":
        expr_dh += " - {{dh_{}}}".format(states[0])
        expr_ds += " - {{ds_{}}}".format(states[0])
    return "{{kbt_h}} * exp(-(({expr_dh}) - {{tk}} * ({expr_ds})) / {{rt}})".format(
        expr_dh=expr_dh, expr_ds=expr_ds
    )


def _define_thermo(celcius):
    tk = celcius + 273.15
    kbt_h = cst.k * tk / cst.h
    rt = cst.R * tk
    thermo = {"tk": tk, "kbt_h": kbt_h, "rt": rt}
    return thermo
