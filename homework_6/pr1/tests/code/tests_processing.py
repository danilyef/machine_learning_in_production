import pytest
from project.processing import Cleaner


@pytest.fixture
def cleaner():
    return Cleaner()


def test_lower_case(cleaner):
    assert cleaner.lower_case("HELLO WORLD") == "hello world"


def test_tokenize_numbers(cleaner):
    assert (
        cleaner.tokenize_numbers("There are 123 apples and 456 oranges")
        == "There are NUMBER apples and NUMBER oranges"
    )


def test_remove_emails(cleaner):
    assert (
        cleaner.remove_emails("Contact us at info@example.com or support@test.co.uk")
        == "Contact us at  or "
    )


def test_remove_square_brackets(cleaner):
    assert cleaner.remove_square_brackets("This is [hidden] text") == "This is  text"


def test_remove_round_brackets(cleaner):
    assert (
        cleaner.remove_round_brackets("This is (parenthetical) text") == "This is  text"
    )


def test_remove_urls(cleaner):
    text = "Visit https://www.example.com or www.test.org for more info"
    assert cleaner.remove_urls(text) == "Visit  or  for more info"


def test_remove_whitespace(cleaner):
    assert cleaner.remove_whitespace("Too    many    spaces") == "Too many spaces"


def test_clean(cleaner):
    text = """HELLO WORLD! [Hidden text] (Parenthetical text)
    Visit https://www.example.com or contact info@example.com
    There are 123 apples and 456 oranges"""

    expected = (
        "hello world! visit or contact there are NUMBER apples and NUMBER oranges"
    )
    assert cleaner.clean(text) == expected


def test_clean_with_multiple_urls_and_emails(cleaner):
    text = """Check out http://www.example.com and https://test.org. Contact us at info@example.com or support@test.co.uk"""

    expected = "check out and . contact us at or "
    assert cleaner.clean(text) == expected


def test_clean_with_nested_brackets(cleaner):
    text = "This is [nested (bracket)] text"
    expected = "this is text"
    assert cleaner.clean(text) == expected


def test_clean_with_multiple_whitespace_types(cleaner):
    text = "Too    many\tspaces\nand\rline\fbreaks"
    expected = "too many spaces and line breaks"
    assert cleaner.clean(text) == expected
