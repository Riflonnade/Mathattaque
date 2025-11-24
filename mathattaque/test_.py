import math

from config import (
    questions_faciles,
    questions_moyennes,
    SPECIAL_DAMAGE,
)
from entities import clamp
from questions import compute_precision, resolve_quiz
from ui import intervalle, green_from_precision


#
def test_clamp_inside_range():
    assert clamp(5, 0, 10) == 5


def test_clamp_below_range():
    assert clamp(-3, 0, 10) == 0


def test_clamp_above_range():
    assert clamp(42, 0, 10) == 10


#
def test_questions_faciles_format_et_reponse():
    """Vérifie le format 'a op b ' et la cohérence de la réponse."""
    for _ in range(20):
        expr, ans = questions_faciles()
        parts = expr.strip().split()
        assert len(parts) == 3
        a_str, op, b_str = parts
        a = int(a_str)
        b = int(b_str)

        assert 1 <= a <= 20
        assert 1 <= b <= 20
        assert op in {"+", "-", "*"}

        if op == "+":
            expected = a + b
        elif op == "-":
            expected = a - b
        else:  # "*"
            expected = a * b

        assert ans == expected


def test_questions_moyennes_format_et_reponse():
    """Vérifie le format 'a op b ' et la cohérence de la réponse (produit ou division)."""
    for _ in range(20):
        expr, ans = questions_moyennes()
        parts = expr.strip().split()
        assert len(parts) == 3
        a_str, op, b_str = parts
        a = int(a_str)
        b = int(b_str)

        assert 11 <= a <= 99
        assert 11 <= b <= 99
        assert op in {"*", "/"}

        if op == "*":
            expected = a * b
            assert ans == expected
        else:  # "/"
            expected = a / b
            assert math.isclose(ans, expected, rel_tol=1e-9)


#

def test_compute_precision_exacte():
    prec = compute_precision(10, 10)
    assert math.isclose(prec, 100.0)


def test_compute_precision_moitie():
    prec = compute_precision(15, 10)
    assert math.isclose(prec, 50.0)


def test_compute_precision_mauvaise_entree():
    prec = compute_precision("abc", 10)
    assert prec == 0.0


#

def test_resolve_quiz_victoire_p1_parfaite():
    winner, dmg, prec = resolve_quiz(10, 15, 10)
    assert winner == 1
    assert math.isclose(prec, 100.0)
    assert dmg == SPECIAL_DAMAGE


def test_resolve_quiz_egalite():
    winner, dmg, prec = resolve_quiz(10, 10, 10)
    assert winner == 0
    assert dmg == 0
    assert prec == 0


#

def test_intervalle_extremes_et_milieu():
    assert intervalle(0, 10, 0.0) == 0
    assert intervalle(0, 10, 1.0) == 10
    assert intervalle(0, 10, 0.5) == 5


def test_green_from_precision_bornes():
    assert green_from_precision(0) == (200, 255, 200)
    assert green_from_precision(100) == (0, 120, 0)


def test_green_from_precision_intermediaire():
    c_mid = green_from_precision(50)
    light = (200, 255, 200)
    dark = (0, 120, 0)
    for cm, cl, cd in zip(c_mid, light, dark):
        lo = min(cl, cd)
        hi = max(cl, cd)
        assert lo <= cm <= hi
