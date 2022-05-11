import json
from pyparsing import White
import pytest
from splitter.src import app
import boto3
import io


class DummyClient():
    def do_nothing(self, *args, return_value=None, return_none=False, **kwargs):
        service =self.service
        if  service == "lambda":
            return

        return self

    def __getattr__(self, attr):

        return self.do_nothing

    def download_fileobj(self,*args):
        file_name="TEST_TEST_TES_123"
        data_stream = open("lambdas/python/splitter/tests/resources/DATA_TEST.csv","rb")
        ASD = 15


@pytest.fixture()
def apigw_event():
    """ Generates S3 Bucket trigger event"""

    return json.load("../../events/event.json")

def test_parseCSV(monkeypatch, mocker):
    def aux():
        return DummyClient()

    def mock_callLambda():
        return 
    monkeypatch.setattr("splitter.src.app.s3_client",aux())
    monkeypatch.setattr("splitter.src.app.boto3",aux()) 
    monkeypatch.setattr(app,"callLambda",value=mock_callLambda)

    app.parseCSV("resumen-cuenta-test", "input/DATA_TEST.csv")    

    assert False
