from src.question_duplicate_detector import fingerprint


def test_same_text_same_hash():
    assert fingerprint("abc") == fingerprint("abc")
