import unittest.result
from public.common.util import logger

CASE_RESULT_TEXT = '' #用例运行结果


class MyTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """
    testName = ''


    def setUp(self):
        # logger.info('************ START test *************')
        global CASE_RESULT_TEXT
        CASE_RESULT_TEXT = '' #每个用例开始执行之前把该值设置为空

    def tearDown(self):
        # self.o.ev_obj.clear_attr()
        """检查用例运行结果
        注：如果抛出异常 又有断言则一条用例会生成2条结果(一条error 一条fail)
        """

        self._outcome.errors = list(self._outcome.errors)
        for i in range(len(self._outcome.errors)):
            error = self._outcome.errors[i][1]
            self._outcome.errors[i] = list(self._outcome.errors[i])
            if error:
                if CASE_RESULT_TEXT != '':
                    #如果有断言结果 则不用error结果
                    self._outcome.errors[i][1] = None

        if CASE_RESULT_TEXT != '':
            #如果有断言结果 则不用error结果
            self._outcome.errors[i][1] = None
            self.assertTrue(False,CASE_RESULT_TEXT)







    @classmethod
    def setUpClass(self):
        logger.info('************ CLASS  START ************')

    @classmethod
    def tearDownClass(self):
        logger.info('************ CLASS End  ************')