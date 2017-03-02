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

Parameter = login.html('http://00.0.00.00:0000/000/iuiu?iui=' + Apiname + '&product=0&class1=0')
#print Apiname + " :" + Classname
#print Parameter
if not Parameter==False :
    lj = open(Filename,'w')
    text = '''%s;

/**
 * %s
 */
public class %s {
    //private static final Log logger = LogFactory.getLog(%s.class);

        String res = getBizMapAndPlatMapAndDoPost("%s", passLogin.passId, passLogin.passToken, 1);

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
