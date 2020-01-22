# -*- coding:utf-8 -*-

from io import StringIO
import sys
import time
import unittest
import datetime
import re
from xml.sax import saxutils

class OutputRedirector(object):
    """ Wrapper to redirect stdout or stderr """
    def __init__(self, fp):
        self.fp = fp

    def write(self, s):
        self.fp.write(s)

    def writelines(self, lines):
        self.fp.writelines(lines)

    def flush(self):
        self.fp.flush()

stdout_redirector = OutputRedirector(sys.stdout)
stderr_redirector = OutputRedirector(sys.stderr)

TestResult = unittest.TestResult

#运行完用例后可直接获取 result获取运行结果
class _TestResult(TestResult):
    # note: _TestResult is a pure representation of results.
    # It lacks the output and reporting ability compares to unittest._TextTestResult.


    def __init__(self, stream='', descriptions='', verbosity=''):
        TestResult.__init__(self)
        self.stdout0 = None
        self.stderr0 = None
        self.success_count = 0
        self.skipped_count=0#add skipped_count
        self.failure_count = 0
        self.error_count = 0
        self.verbosity = verbosity

        #所有用例的结果 例:self.result.append((1, test, output, _exc_str,self.startTime,endTime))
        self.result = []


    def startTest(self, test):
        TestResult.startTest(self, test)
        # just one buffer for both stdout and stderr
        self.outputBuffer = StringIO()
        stdout_redirector.fp = self.outputBuffer
        stderr_redirector.fp = self.outputBuffer
        self.startTime=time.time()

    def complete_output(self):
        """
        Disconnect output redirection and return buffer.
        Safe to call multiple times.
        """
        if self.stdout0:
            sys.stdout = self.stdout0
            sys.stderr = self.stderr0
            self.stdout0 = None
            self.stderr0 = None
        return self.outputBuffer.getvalue()


    def stopTest(self, test):
        # Usually one of addSuccess, addError or addFailure would have been called.
        # But there are some path in unittest that would bypass this.
        # We must disconnect stdout in stopTest(), which is guaranteed to be called.
        self.complete_output()


    def addSuccess(self, test):
        endTime=time.time()
        self.success_count += 1
        TestResult.addSuccess(self, test)
        output = self.complete_output()
        # self.result.append((0, test, output, '',self.startTime,endTime))
        self.result.append((0, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('ok ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('.')

    def addSkip(self, test, reason):
        self.skipped_count+= 1
        TestResult.addSkip(self, test,reason)
        output = self.complete_output()
        # self.result.append((3, test,'',reason))
        self.result.append((3, test, output, ''))
        if self.verbosity > 1:
            sys.stderr.write('skip ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('s')

    def addError(self, test, err):
        endTime=time.time()
        self.error_count += 1
        TestResult.addError(self, test, err)
        _, _exc_str = self.errors[-1]
        output = self.complete_output()
        # self.result.append((2, test, output, _exc_str,self.startTime,endTime))
        self.result.append((2, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('E  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('E')

    def addFailure(self, test, err):
        endTime=time.time()
        self.failure_count += 1
        TestResult.addFailure(self, test, err)
        _, _exc_str = self.failures[-1]
        output = self.complete_output()
        # self.result.append((1, test, output, _exc_str,self.startTime,endTime))
        self.result.append((1, test, output, _exc_str))
        if self.verbosity > 1:
            sys.stderr.write('F  ')
            sys.stderr.write(str(test))
            sys.stderr.write('\n')
        else:
            sys.stderr.write('F')


