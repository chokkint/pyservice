from django.http import HttpResponse

from pyservice import utils as ResultUtils
from pyservice.settings import logger
from pywebservice import bizfunc as bizfunc
from pywebservice import tests as tt
# Create your tests here.
# 获取该业务员+该客户的通话记录
def test(request):
    error_msg = ''
    logger.info(bizfunc.dist(1))
    logger.info(bizfunc.inv(1))

    logger.info(request)
    str = bizfunc.dist(1)
    str2 = []
    for s in str:
        str2.append(s)
    print(str2)

    return HttpResponse(ResultUtils.createResult(ResultUtils.SysConstants.ERROR_CODE_SUCCESS, "test OK", str2))


def test2(request):
    ret = tt.test()
    print(ret)
    return HttpResponse(ResultUtils.createResult(ResultUtils.SysConstants.ERROR_CODE_SUCCESS, "test OK", ret))


