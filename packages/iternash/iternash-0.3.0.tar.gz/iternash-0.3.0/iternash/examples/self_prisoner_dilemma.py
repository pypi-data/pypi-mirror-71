#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __coconut_hash__ = 0x75994d61

# Compiled with Coconut version 1.4.3-post_dev28 [Ernest Scribbler]

# Coconut Header: -------------------------------------------------------------

from __future__ import print_function, absolute_import, unicode_literals, division
import sys as _coconut_sys, os.path as _coconut_os_path
_coconut_file_path = _coconut_os_path.dirname(_coconut_os_path.dirname(_coconut_os_path.abspath(__file__)))
_coconut_cached_module = _coconut_sys.modules.get(str("__coconut__"))
if _coconut_cached_module is not None and _coconut_os_path.dirname(_coconut_cached_module.__file__) != _coconut_file_path:
    del _coconut_sys.modules[str("__coconut__")]
_coconut_sys.path.insert(0, _coconut_file_path)
from __coconut__ import *
from __coconut__ import _coconut, _coconut_MatchError, _coconut_igetitem, _coconut_base_compose, _coconut_forward_compose, _coconut_back_compose, _coconut_forward_star_compose, _coconut_back_star_compose, _coconut_forward_dubstar_compose, _coconut_back_dubstar_compose, _coconut_pipe, _coconut_back_pipe, _coconut_star_pipe, _coconut_back_star_pipe, _coconut_dubstar_pipe, _coconut_back_dubstar_pipe, _coconut_bool_and, _coconut_bool_or, _coconut_none_coalesce, _coconut_minus, _coconut_map, _coconut_partial, _coconut_get_function_match_error, _coconut_base_pattern_func, _coconut_addpattern, _coconut_sentinel, _coconut_assert, _coconut_mark_as_match
if _coconut_sys.version_info >= (3,):
    _coconut_sys.path.pop(0)

# Compiled Coconut: -----------------------------------------------------------

from math import log
from math import exp
from math import ceil

from iternash import Game
from iternash import agent
from iternash import hist_agent
from iternash import debug_all_agent
from iternash import iterator_agent
from iternash.util import repeat

import numpy as np
from matplotlib import pyplot as plt
from tqdm import tqdm


# = GENERIC UTILS =

C = 0
D = 1


def coop_with_prob(p):
    return np.random.binomial(1, 1 - p)


common_params = dict(INIT_C_PROB=0.5, PD_PAYOFFS=[[2, 3], [-1, 0],])


a_hist_1step = hist_agent("a_hist", "a", maxhist=1)


@agent(name="r")
def self_pd_reward(env):
    if env["a_hist"]:
        a1 = env["a_hist"][-1]
    else:
        a1 = coop_with_prob(env["INIT_C_PROB"])
    a2 = env["a"]
    return env["PD_PAYOFFS"][a1][a2]


# = POLICY GRADIENT GAME =

pol_grad_params = common_params.copy()
pol_grad_params.update(POL_GRAD_LR=0.01, CLIP_EPS=0.01)


@agent(name="a")
def pol_grad_act(env):
    return coop_with_prob(env["pc"])


@agent(name="pc", default=np.random.random())
def pol_grad_update(env):
    lr = env["POL_GRAD_LR"]
    eps = env["CLIP_EPS"]
    a = env["a"]
    th = env["pc"]
# grad[th] E[r(a) | a~pi[th]]
# = sum[a] grad[th] p(a|pi[th]) r(a)
# = sum[a] r(a) grad[th] p(a|pi[th])
# = sum[a] r(a) p(a|pi[th]) grad[th] log(p(a|pi[th]))
# = E[r(a) grad[th] log(p(a|pi[th]) | a~pi[th]]
    if a == C:
# grad[th] log(p(C|pi[th]))
# = grad[th] log(th)
# = 1/th
        th += lr * env["r"] * (1 / th)
    elif a == D:
# grad[th] log(p(D|pi[th])
# = grad[th] log(1 - th)
# = -1/(1 - th)
        th += lr * env["r"] * (-1 / (1 - th))
    else:
        raise ValueError("got invalid action {_coconut_format_0}".format(_coconut_format_0=(a)))
    return np.clip(th, eps, 1 - eps)


@agent(name="pc", default=np.random.random())
def pol_grad_decoupled_update(env):
    lr = env["POL_GRAD_LR"]
    eps = env["CLIP_EPS"]
    th = env["pc"]
    k = coop_with_prob(th)
    if k == C:
        th += lr * env["r"] * (1 / th)
    elif k == D:
        th += lr * env["r"] * (-1 / (1 - th))
    else:
        raise ValueError("got invalid action {_coconut_format_0}".format(_coconut_format_0=(a)))
    return np.clip(th, eps, 1 - eps)


pol_grad_game = Game("pol_grad", pol_grad_act, self_pd_reward, pol_grad_update, a_hist_1step, **pol_grad_params)


pol_grad_decoupled_game = Game("pol_grad_decoupled", pol_grad_act, self_pd_reward, pol_grad_decoupled_update, a_hist_1step, **pol_grad_params)


# = Q LEARNING GAME =

ql_params = common_params.copy()
ql_params.update(EXPLORE_EPS=0.1, BOLTZ_TEMP=1, QL_LR=0.01)


@agent(name="pc")
def eps_greedy_pc(env, eps=None):
    """Get the epsilon greedy probability of cooperation."""
    eps = env["EXPLORE_EPS"] if eps is None else eps
    QC = env["qs"][C]
    QD = env["qs"][D]

    prob_coop = eps / 2
    if QC == QD:
        prob_coop += (1 - eps) / 2
    elif QC > QD:
        prob_coop += 1 - eps
    return prob_coop


@agent(name="pc")
def boltz_pc(env, temp=None):
    temp = env["BOLTZ_TEMP"] if temp is None else temp
    QC = env["qs"][C]
    QD = env["qs"][D]
    zc = exp(QC / temp)
    zd = exp(QD / temp)
    return zc / (zc + zd)


@agent(name="pc")
def eps_greedy_decay_pc(env):
    return eps_greedy_pc(env, eps=1 / env["M"])


@agent(name="a")
def ql_pc_act(env):
    return coop_with_prob(env["pc"])


@agent(name="a")
def ql_boltz_act(env):
    GUMB_C = env["BOLTZ_TEMP"]
    qs = np.array(env["qs"], dtype=float)
    zs = np.random.gumbel(size=qs.shape)
    return np.argmax(qs + GUMB_C * zs)


@agent(name="qs", default=[0, 0], extra_defaults=dict(q_sums=[0, 0], q_counts=[0, 0]))
def ql_true_avg_update(env):
    a = env["a"]
    env["q_sums"][a] += env["r"]
    env["q_counts"][a] += 1
    env["qs"][a] = env["q_sums"][a] / env["q_counts"][a]
    return env["qs"]


@agent(name="qs", default=[0, 0])
def ql_run_avg_update(env):
    a = env["a"]
    al = env["QL_LR"]
    if env.get("QL_LR_DECAY"):
        al /= env["M"]
    if env.get("QL_LR_CORRECTION"):
        prob_a = env["pc"] if a == C else 1 - env["pc"]
        al /= prob_a
    env["qs"][a] = (1 - al) * env["qs"][a] + al * env["r"]
    return env["qs"]


M_counter = iterator_agent("M", count(2), default=1)


@agent(name="qs", default=[0, 0])
def ql_decoupled_update(env):
    M = env["M"]
    al_init = env["QL_LR"]

    num_actions = 2
    k_eps = max(1 / M, al_init * num_actions)
    prob_k_coop = eps_greedy_pc(env, eps=k_eps)
    k = coop_with_prob(prob_k_coop)

    al = al_init
    if env.get("QL_LR_DECAY"):
        al /= env["M"]
    if env.get("QL_LR_CORRECTION"):
        if k == C:
            prob_k = prob_k_coop
        else:
            prob_k = 1 - prob_k_coop
        al /= prob_k
    env["qs"][k] = (1 - al) * env["qs"][k] + al * env["r"]
    return env["qs"]


ql_eps_greedy_true_avg_game = Game("ql_eps_greedy_true_avg", eps_greedy_pc, ql_pc_act, self_pd_reward, ql_true_avg_update, a_hist_1step, **ql_params)


ql_eps_greedy_run_avg_game = Game("ql_eps_greedy_run_avg", eps_greedy_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, **ql_params)


ql_boltz_run_avg_game = Game("ql_boltz_run_avg", boltz_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, **ql_params)


ql_boltz_true_avg_game = Game("ql_boltz_true_avg", boltz_pc, ql_pc_act, self_pd_reward, ql_true_avg_update, a_hist_1step, **ql_params)


ql_eps_greedy_decay_run_avg_decoupled_lr_decay_correction_game = Game("ql_eps_greedy_decay_run_avg_decoupled_lr_decay_correction", eps_greedy_decay_pc, ql_pc_act, self_pd_reward, ql_decoupled_update, a_hist_1step, M_counter, QL_LR_DECAY=True, QL_LR_CORRECTION=True, **ql_params)


ql_eps_greedy_decay_run_avg_decoupled_game = Game("ql_eps_greedy_decay_run_avg_decoupled", eps_greedy_decay_pc, ql_pc_act, self_pd_reward, ql_decoupled_update, a_hist_1step, M_counter, **ql_params)


ql_eps_greedy_decay_true_avg_game = Game("ql_eps_greedy_decay_true_avg", eps_greedy_decay_pc, ql_pc_act, self_pd_reward, ql_true_avg_update, a_hist_1step, M_counter, **ql_params)


ql_eps_greedy_decay_run_avg_game = Game("ql_eps_greedy_decay_run_avg", eps_greedy_decay_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, M_counter, **ql_params)


ql_eps_greedy_decay_run_avg_lr_decay_correction_game = Game("ql_eps_greedy_decay_run_avg_lr_decay_correction", eps_greedy_decay_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, M_counter, QL_LR_DECAY=True, QL_LR_CORRECTION=True, **ql_params)


ql_eps_greedy_run_avg_lr_decay_correction_game = Game("ql_eps_greedy_run_avg_lr_decay_correction", eps_greedy_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, M_counter, QL_LR_DECAY=True, QL_LR_CORRECTION=True, **ql_params)


ql_eps_greedy_run_avg_lr_decay_game = Game("ql_eps_greedy_run_avg_lr_decay", eps_greedy_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, M_counter, QL_LR_DECAY=True, **ql_params)


ql_eps_greedy_run_avg_lr_correction_game = Game("ql_eps_greedy_run_avg_lr_correction", eps_greedy_pc, ql_pc_act, self_pd_reward, ql_run_avg_update, a_hist_1step, M_counter, QL_LR_CORRECTION=True, **ql_params)


# = MAIN =

def plot_pc(game, num_steps=10000):
    """Plot pc over time in the given game."""
    game = game.copy_with_agents(hist_agent("pc_hist", "pc"))
    game.run(num_steps)

    fig, axs = plt.subplots(1, 2)

    xs = range(1, len(game.env["pc_hist"]) + 1)
    game.plot(axs[0], xs, "pc_hist")
    axs[0].set(xlabel="t", ylabel="P(C)")

    log_xs = (list)(map(log, xs))
    game.plot(axs[1], log_xs, "pc_hist")
    axs[1].set(xlabel="log(t)", ylabel="P(C)")

    plt.show()


def plot_qc_qd(game, num_steps=10000):
    """Plot qc and qd over time in the given game."""
    game = game.copy_with_agents(hist_agent("qc_hist", lambda env: env["qs"][C]), hist_agent("qd_hist", lambda env: env["qs"][D]))
    game.run(num_steps)

    fig, axs = plt.subplots(1, 2)

    xs = range(1, len(game.env["qc_hist"]) + 1)
    game.plot(axs[0], xs, "qc_hist")
    game.plot(axs[0], xs, "qd_hist")
    axs[0].set(xlabel="t", ylabel="qs")
    axs[0].legend()

    log_xs = (list)(map(log, xs))
    game.plot(axs[1], log_xs, "qc_hist")
    game.plot(axs[1], log_xs, "qd_hist")
    axs[1].set(xlabel="log(t)", ylabel="qs")
    axs[1].legend()

    plt.show()


def run_experiment(game, num_iters=500, num_steps=5000, bucket_size=0.01, pc_calc_steps=500):
    """Measure limiting behavior for the given game."""
    game = game.copy_with_agents(hist_agent("pc_hist", "pc", maxhist=pc_calc_steps))
    buckets = [0] * int(1 / bucket_size)
    print("Running experiment for {_coconut_format_0}...".format(_coconut_format_0=(game.name)))
    for _ in tqdm(range(num_iters)):
        game.run(num_steps, use_tqdm=False)
        pc_hist = game.env["pc_hist"]
        ave_pc = sum(pc_hist) / len(pc_hist)
        bucket = int(ave_pc // bucket_size)
        if bucket == len(buckets):
            bucket -= 1
        buckets[bucket] += 1
        game.reset()
    for i in range(len(buckets)):
        buckets[i] /= num_iters
    return buckets


def plot_experiments(*games, linestyles=(":", "-.", "--", "-"), alpha=0.6, linewidth=2.25, **kwargs):
    """Plot cooperation proportions for all the given games."""
    experiments = dict(((g.name), (run_experiment(g, **kwargs))) for g in games)
    fig, ax = plt.subplots(1)
    for (name, buckets), ls in zip(experiments.items(), repeat(linestyles)):
        bucket_xs = np.linspace(0, 1, num=len(buckets))
        ax.plot(bucket_xs, buckets, label=name, ls=ls, alpha=alpha, lw=linewidth)
    ax.set(xlabel="equilibrium cooperation probability", ylabel="probability of equilibrium")
    ax.legend()
    plt.show()


if __name__ == "__main__":
    run_experiment(pol_grad_decoupled_game)
# plot_experiments(
#     pol_grad_game,
#     pol_grad_decoupled_game,
#     ql_eps_greedy_true_avg_game,
#     ql_eps_greedy_run_avg_game,
#     ql_boltz_run_avg_game,
#     ql_boltz_true_avg_game,
#     ql_eps_greedy_decay_run_avg_decoupled_lr_decay_correction_game,
#     ql_eps_greedy_decay_run_avg_decoupled_game,
#     ql_eps_greedy_decay_true_avg_game,
#     ql_eps_greedy_decay_run_avg_game,
#     ql_eps_greedy_decay_run_avg_lr_decay_correction_game,
#     ql_eps_greedy_run_avg_lr_decay_correction_game,
#     ql_eps_greedy_run_avg_lr_decay_game,
#     ql_eps_greedy_run_avg_lr_correction_game,
# )
