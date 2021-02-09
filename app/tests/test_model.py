from hypothesis import given
from hypothesis.strategies import text, integers
from src.model import (
    text_similarity_intersection,
    text_similarity_kld,
    text_similarity_cos,
    n_gram,
    process_text,
)
from src.service import app


@given(text())
def test_self_similarity_intersection(s):
    assert text_similarity_intersection(s, s) == 1


@given(text())
def test_self_similarity_kld(s):
    assert text_similarity_kld(s, s) == 1


@given(text())
def test_self_similarity_cos(s):
    assert text_similarity_cos(s, s) == 1


@given(text(), text())
def test_commutativity_intersection(s1, s2):
    assert text_similarity_intersection(s1, s2) == text_similarity_intersection(s2, s1)


@given(text(), text())
def test_commutativity_kld(s1, s2):
    assert text_similarity_kld(s1, s2) == text_similarity_kld(s2, s1)


@given(text(), text())
def test_commutativity_cos(s1, s2):
    assert text_similarity_cos(s1, s2) == text_similarity_cos(s2, s1)


@given(text())
def test_pertubation_kld(s):
    assert text_similarity_kld(s, s + " test words") < 1


@given(text(), integers())
def test_n_gram_reconstruction(s, n):
    words = process_text(s)
    grams = n_gram(words, n)
    for gram_id, gram in enumerate(grams):
        for word_id, gram_word in enumerate(gram):
            assert gram_word == words[gram_id + word_id]


def test_n_gram():
    assert n_gram(["one", "two", "three"], 2) == [["one", "two"], ["two", "three"]]


# WebServer Tests
import json


@given(text(), text())
def test_post(s1, s2):
    app.testing = True
    for model_type in ["Cos", "Intersection", "KLD"]:
        with app.test_client() as c:
            response = c.post(
                "/Similarity",
                headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "Metadata": {"Model": model_type},
                        "Data": {"FirstSample": s1, "SecondSample": s2},
                    }
                ),
            )
            score = response.json["Score"]
            assert 0 <= float(score) <= 1
            model = response.json["Model"]
            assert model == model_type
