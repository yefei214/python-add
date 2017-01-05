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
#登录对应接口的网页，抓取入参数据
Parameter = login.html('http://10.0.53.71:8081/api/index?keywords=' + Apiname + '&product=0&class1=0')
#print Apiname + " :" + Classname
#print Parameter
if not Parameter==False :
    #####################################################################################指定模版
    lj = open(Filename,'w')
    text = '''package user.http.%s;

import com.kuaidadi.framework.rpc.RpcCode;
import com.liangJian.test.kopUtils.DriverLogin;
import com.liangJian.test.kopUtils.KopBaseCase;
import net.sf.json.JSONObject;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.HashMap;
import java.util.Map;

/**
 * %s
 */
public class %s extends KopBaseCase {
    //private static final Log logger = LogFactory.getLog(%s.class);
    private DriverLogin dirverInfo;

    @Before
    /**司机登录，获取司机token和司机id*/
    public void before() {
        dirverInfo = new DriverLogin("18658868157","qwe123");
    }

    @Test
    public void testNormal() {
        String res = getBizMapAndPlatMapAndDoPost("%s",dirverInfo.did,dirverInfo.dToken,2);
        Map<String, Object> resMap = (Map<String, Object>)(JSONObject.fromObject(res));
        Map<String, Object> dataMap = (Map<String,Object>)resMap.get("data");
        Assert.assertEquals(RpcCode.SUCCESS, ((Integer)resMap.get("code")).intValue());
        Assert.assertNotNull(dataMap);
        //Assert.assertFalse(dataMap.get("driverRegisterResult").toString().isEmpty());
    }

    /**赋值业务参数
     * 赋值完整的平台参数
     * 使用完整的业务参数和平台参数发起post请求*/
    private String getBizMapAndPlatMapAndDoPost(String apiName,Long userId, String token, Integer userRole) {
        Map<String, Object> bizParamMap = createBusiParamMap();
        //System.out.println("=====bizParamMap======"+JsonUtil.toJson(bizParamMap));
        Map<String, Object> wholeplatParamMap = getWholePlatParam(apiName,userId,token,userRole);
        //System.out.println("=====wholeplatParamMap======"+JsonUtil.toJson(wholeplatParamMap));
        return doPostWithBizMapAndSpecialPlatMap(bizParamMap, wholeplatParamMap);
    }

    private Map<String, Object> createBusiParamMap() {
        Map<String, Object> map = new HashMap<String, Object>();
''' % (Package, Description, Classname, Classname, Apiname)
    #####################################################################################填充入参
    parame = ''
    i = 0
    for tup in Parameter:
        parame = parame + '        map.put("%s", "");//%s(%s) TODO \n' % (Parameter[i][0], Parameter[i][1], Parameter[i][2])
        i = i+1
    #####################################################################################生成文本
    text = text + parame + '''        return map;
    }
}
'''
    #####################################################################################写入文件
    lj.write(text)
