from pytest import fixture
from snowflake.snowpark import Session
from snowflake.snowpark.functions import lit
from streamlit.testing.v1 import AppTest
import add as add
import ui as ui

@fixture
def session():
    session = Session.builder.config('local_testing', True).create()
    yield session
    session.close()

@fixture(autouse=True)
def set_up(session: Session):
    session.sproc.register(add.increment_by_one_fn, name='core.increment_by_one')
    session.udf.register(add.add_fn, name='core.add')

def test_streamlit():
    at = AppTest.from_function(ui.run_streamlit)
    at.run()

    at.number_input('numToAdd1').set_value(6).run()
    at.number_input('numToAdd2').set_value(3).run()
    assert (at.dataframe[0].value[:].values == [[9]]).all()

    at.number_input('numToIncrement').set_value(4).run()
    assert (at.dataframe[1].value[:].values == [[5]]).all()
    assert not at.exception
