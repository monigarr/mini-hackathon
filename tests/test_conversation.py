from src.conversation.engine import ConversationEngine
from src.models.session import ConversationState, SessionManager


def test_happy_path_single_filer_generates_pdf() -> None:
    manager = SessionManager()
    engine = ConversationEngine()
    session = manager.create_session()

    first = engine.start_session(session)
    assert "Question 1 of 5" in first

    second = engine.process_message(
        session, "Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000"
    )
    assert "Question 2 of 5" in second

    third = engine.process_message(session, "Single")
    assert "Question 3 of 5" in third

    fourth = engine.process_message(session, "No, I am independent")
    assert "Question 4 of 5" in fourth

    done = engine.process_message(session, "Yes, correct")
    assert "Download" in done
    assert session.state == ConversationState.COMPLETE
    assert session.question_count == 4
    assert session.pdf_bytes is not None


def test_off_topic_redirect_does_not_increment_question_count() -> None:
    manager = SessionManager()
    engine = ConversationEngine()
    session = manager.create_session()
    engine.start_session(session)

    before = session.question_count
    response = engine.process_message(session, "Can I deduct my home office?")

    assert session.question_count == before
    assert "outside this prototype" in response


def test_invalid_w2_reprompt_does_not_increment_question_count() -> None:
    manager = SessionManager()
    engine = ConversationEngine()
    session = manager.create_session()
    engine.start_session(session)

    response = engine.process_message(session, "wages only")

    assert session.question_count == 1
    assert "Please try again" in response


def test_no_sixth_question_when_correction_unclear() -> None:
    manager = SessionManager()
    engine = ConversationEngine()
    session = manager.create_session()
    engine.start_session(session)
    engine.process_message(session, "Box 1 40000, Box 2 2400, Box 4 40000, Box 6 40000")
    engine.process_message(session, "Single")
    engine.process_message(session, "No")
    engine.process_message(session, "No, wrong")

    assert session.question_count == 5
    response = engine.process_message(session, "something else")

    assert "5-question limit" in response
    assert session.question_count == 5

