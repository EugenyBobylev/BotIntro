import pytest
from app.bot.TStack import TStack


def test_create_stack():
    stack = TStack()
    assert stack is not None
    assert stack.all_count() == 0


def test_push():
    stack = TStack()
    stack.push('bobylev', 'message_01')
    stack.push('user2', 'message_02')
    assert stack.all_count() == 2


def test_pop_empty_list():
    lst = [1, 2, 3]
    result3 = lst.pop()
    result2 = lst.pop()
    result1 = lst.pop()
    # IndexError: pop from empty list
    with pytest.raises(IndexError):
        result4 = lst.pop()

    assert result1 == 1
    assert result2 == 2
    assert result3 == 3


def test_pop():
    stack = TStack()
    stack.push('user1', 'message_01')
    stack.push('user2', 'message_02')
    stack.push('user2', 'message_03')

    assert stack.all_count() == 3
    message_03 = stack.pop('user2')
    message_01 = stack.pop('user1')
    message_none = stack.pop('user1')

    assert message_01 == 'message_01'
    assert message_03 == 'message_03'
    assert message_none is None
    assert stack.all_count() == 1


def test_count():
    stack = TStack()
    stack.push('user1', 'message_01')
    stack.push('user1', 'message_02')

    assert stack.count('user1') == 2
    assert stack.count('user2') == 0
