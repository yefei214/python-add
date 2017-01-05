#coding=utf-8
import os,sys
import login

Apiname = sys.argv[1]
#Classname = iname.split('.')
#Classname = Classname[-1]
#Classname = Classname[0].upper() + Classname[1:] + 'Test'
Classname =  sys.argv[2]
Classname =  Classname[0].upper() + Classname[1:] + 'Test'
Package = sys.argv[-1]
Filename = "./Template/" + Package + "/" + Classname + ".java"
Description = sys.argv[3]

#print 'http://10.0.53.71:8081/api/index?keywords=' + Apiname + '&product=0&class1=0'
Parameter = login.html('http://10.0.53.71:8081/api/index?keywords=' + Apiname + '&product=0&class1=0')
#http://10.0.53.71:8081/api/index?keywords=lj.bi.submitLog&product=0&class1=0
#print Apiname + " :" + Classname
#print Parameter

if not Parameter==False :
    lj = open(Filename,'w')
    text = '''package user.http.%s;

import com.kuaidadi.framework.rpc.RpcCode;
import com.liangJian.test.kopUtils.KopBaseCase;
import net.sf.json.JSONObject;
import org.junit.Assert;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

/**
 * %s
 */
public class %s extends KopBaseCase {

    //private static final Log logger = LogFactory.getLog(%s.class);

    @Test
    public void testNormal() {
        String res = getBizMapAndPlatMapAndDoPost("%s");
        Map<String, Object> resMap = (Map<String, Object>)(JSONObject.fromObject(res));
        Map<String, Object> dataMap = (Map<String,Object>)resMap.get("data");
        Assert.assertEquals(RpcCode.SUCCESS, ((Integer)resMap.get("code")).intValue());
        Assert.assertNotNull(dataMap);
        //Assert.assertFalse(dataMap.get("driverRegisterResult").toString().isEmpty());
    }

    /**赋值业务参数
     * 赋值完整的平台参数
     * 使用完整的业务参数和平台参数发起post请求*/
    private String getBizMapAndPlatMapAndDoPost(String apiName) {
        Map<String, Object> bizParamMap = createBusiParamMap();
        //System.out.println("=====bizParamMap======"+JsonUtil.toJson(bizParamMap));
        Map<String, Object> wholeplatParamMap = getWholePlatParam(apiName);
        //System.out.println("=====wholeplatParamMap======"+JsonUtil.toJson(wholeplatParamMap));
        return doPostWithBizMapAndSpecialPlatMap(bizParamMap, wholeplatParamMap);
    }

    private Map<String, Object> createBusiParamMap() {
        Map<String, Object> map = new HashMap<String, Object>();
''' % (Package, Description, Classname, Classname, Apiname)
    #####################################################################################
    parame = ''
    i = 0
    for tup in Parameter:
        parame = parame + '        map.put("%s", "");//%s(%s) TODO \n' % (Parameter[i][0], Parameter[i][1], Parameter[i][2])
        i = i+1
    #####################################################################################
    text = text + parame + '''        return map;
    }
}
'''
    #####################################################################################
    lj.write(text)