"""Independent local diagnostics for openai/math, family 087.

These are algebra checks and finite numerical stress tests, NOT a proof of
Mahler's conjecture and NOT a Lean/Comparator replay. No network access needed.
Run: python diagnostics.py --output diagnostics.json
Dependencies: sympy, scipy, numpy, mpmath.
"""
from __future__ import annotations
import argparse
import json
import math
import platform
from pathlib import Path
import mpmath as mp
import numpy as np
import scipy
from scipy.integrate import quad
import sympy as sp

COMMIT = 'adc7f1241b42e322a6451854ab7e4b4c146bf78a'

def algebra_checks() -> dict:
    t, mu, delta = sp.symbols('t mu delta', positive=True)
    psi_prime = 1 + mu / (t + delta)
    target = 1 + mu * delta / (t + delta)**2
    assert sp.simplify(sp.diff(t * psi_prime, t) - target) == 0

    # Source coordinates are (u,x); target coordinates are (q,p).
    # p=-u-sum_j J_j(b_j.u,b_j.x)b_j and q=x.
    B = sp.Matrix(3, 2, sp.symbols('b0:6'))
    h = sp.symbols('h0:3')  # partial_v J_j, nonnegative in the paper
    d = sp.symbols('d0:3')  # partial_t J_j
    eye, zero = sp.eye(2), sp.zeros(2)
    M = eye + B.T * sp.diag(*h) * B
    N = B.T * sp.diag(*d) * B
    jac = zero.row_join(eye).col_join((-M).row_join(-N))
    omega = zero.row_join(eye).col_join((-eye).row_join(zero))
    expected = zero.row_join(M).col_join((-M).row_join(zero))
    remainder = (jac.T * omega * jac - expected).applyfunc(sp.simplify)
    assert remainder == sp.zeros(4)

    scale = sp.symbols('S', positive=True)
    source = sp.sqrt(scale) * sp.eye(4)
    target_p = sp.diag(1, 1, 1/scale, 1/scale)
    target_q = sp.diag(1/scale, 1/scale, 1, 1)
    for target_map in (target_p, target_q):
        assert (target_map.T * omega * target_map - omega / scale).applyfunc(sp.simplify) == sp.zeros(4)
    assert (source.T * omega * source - scale * omega).applyfunc(sp.simplify) == sp.zeros(4)

    v = sp.symbols('v', real=True)
    width_prime = -2/sp.pi * sp.atanh(sp.sin(sp.pi*v/2))
    assert sp.trigsimp(sp.diff(width_prime, v) + 1/sp.cos(sp.pi*v/2)) == 0
    return {
        'radial_derivative_identity': 'exact symbolic identity verified',
        'phase_map_pullback': 'exact symbolic matrix identity verified for an arbitrary 3-by-2 row matrix',
        'source_and_target_scaling': 'exact conformal factors S and 1/S verified',
        'lens_second_derivative': 'exact symbolic identity verified; cos(pi*t/2)>0 on (-1,1)',
    }

def lens_checks() -> dict:
    mp.mp.dps = 60
    def F(z):
        return 4/(1j*mp.pi**2)*(mp.polylog(2,1j*z)-mp.polylog(2,-1j*z))
    ts = ['-1', '-0.9999999999', '-0.999999', '-0.99', '-0.9', '-0.5', '0',
          '0.5', '0.9', '0.99', '0.999999', '0.9999999999', '1']
    records = []
    errors = []
    for text in ts:
        t = mp.mpf(text)
        right = F(mp.exp(1j*mp.pi*t/2))
        left = F(-mp.conj(mp.exp(1j*mp.pi*t/2)))
        err = max(abs(mp.im(right)-t), abs(mp.im(left)-t), abs(mp.re(right)+mp.re(left)))
        assert err < mp.mpf('1e-50')
        if abs(t) < 1:
            assert mp.re(right) > 0
        records.append({'t': text, 'half_width': mp.nstr(mp.re(right), 22),
                        'boundary_law_residual': mp.nstr(err, 8)})
        errors.append(err)
    return {'precision_decimal_digits': 60, 'sample_count': len(ts),
            'max_boundary_law_residual': mp.nstr(max(errors), 10), 'records': records}

def angular_checks() -> dict:
    mp.mp.dps = 50
    rs = ['0.5', '0.7', '0.9', '0.99', '0.999999', '0.9999999999']
    ss = [mp.mpf(x) for x in ['1e-10', '1e-6', '0.001', '0.01', '0.1', '0.5']] + [mp.pi/2]
    c0 = 3*mp.sqrt(2)*mp.pi**2/8
    records = []
    for rt in rs:
        r = mp.mpf(rt)
        def A_tip(s):
            return 4/mp.pi**2 * mp.atan(2*r*mp.sin(s)/(1-r*r))
        for s in ss:
            gap = mp.quad(A_tip, [0, s])
            lhs = 1/A_tip(s)
            rhs = mp.pi/2 + c0*mp.sqrt((1-r)/gap)
            slack = rhs-lhs
            assert slack >= -mp.mpf('1e-40')
            records.append({'r': rt, 's': mp.nstr(s, 12), 'vertical_gap': mp.nstr(gap, 12),
                            'reciprocal_A': mp.nstr(lhs, 12), 'upper_bound': mp.nstr(rhs, 12),
                            'slack': mp.nstr(slack, 12)})
    return {'sample_count': len(records), 'all_tested_tip_bounds_hold': True, 'records': records}

def endpoint_checks() -> dict:
    # With H=k(1-a), remove the integrable endpoint singularity by
    # y=H*sin(theta)^2. This computes the exact I(k,a) integral numerically.
    def integral(k: int, H: float) -> tuple[float,float]:
        def integrand(theta):
            s2 = math.sin(theta)**2
            return 2*H*math.exp((2*k-1)*math.log1p(-(H/k)*s2))*s2
        return quad(integrand, 0, math.pi/2, epsabs=2e-12, epsrel=2e-12, limit=300)
    bound = 1 + math.pi/math.e
    records = []
    for k in [2,3,4,8,16,64,256,1024,4096]:
        Hs = {k*(1-a) for a in [.5,.75,.9,.99,.9999,1-1e-8]}
        Hs.update(H for H in [1e-8,1e-4,.01,.1,1,5,20,100] if H <= k/2)
        for H in sorted(Hs):
            value, error = integral(k,H)
            assert value >= -2e-10
            assert value <= min(bound, math.pi*H/2) + 2e-10
            records.append({'k': k, 'H': H, 'a': 1-H/k, 'I': value,
                            'quad_error_estimate': error, 'universal_upper_bound': bound})
    largest = max(records,key=lambda r:r['I'])
    return {'sample_count': len(records), 'universal_upper_bound': bound,
            'largest_observed': largest, 'records': records,
            'warning': 'Finite numerical tests do not prove the universal integral bound.'}

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, default=Path('diagnostics.json'))
    args = p.parse_args()
    result = {
        'source_repository': 'openai/math', 'source_commit': COMMIT,
        'status': 'LOCAL_DIAGNOSTICS_COMPLETED_NOT_A_FORMAL_PROOF',
        'lean_replay_performed': False,
        'full_dependency_axiom_audit_performed': False,
        'environment': {'python': platform.python_version(), 'numpy': np.__version__,
                        'scipy': scipy.__version__, 'sympy': sp.__version__, 'mpmath': mp.__version__},
        'algebra': algebra_checks(), 'lens': lens_checks(),
        'tip_angular_estimate': angular_checks(), 'moving_endpoint_integral': endpoint_checks(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['lens','tip_angular_estimate','moving_endpoint_integral']},indent=2))
    print('Lens samples:',result['lens']['sample_count'],'max residual:',result['lens']['max_boundary_law_residual'])
    print('Angular-tip samples:',result['tip_angular_estimate']['sample_count'])
    print('Endpoint samples:',result['moving_endpoint_integral']['sample_count'])
    print('Largest endpoint integral:',result['moving_endpoint_integral']['largest_observed'])
    print('Saved:', args.output)

if __name__ == '__main__':
    main()
