from django.shortcuts import render
from django.shortcuts import HttpResponse
from urllib import request
from urllib import parse
import json
from django.core.serializers import serialize
from iosapp import models
# Create your views here.

authData = {
    "appid": "wxf135ce909dd515d7",
    "secret": "243c8ba21a5335a765deebc152520803",
    "code": "",
    "grant_type": "authorization_code"
}

wx_acess_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
wx_userinfo_url = "https://api.weixin.qq.com/sns/userinfo"
wx_auth_url = "https://api.weixin.qq.com/sns/auth"
wx_refresh_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"

def index(res):
    secureinfo = getSecureInfoFromDB()
    if (secureinfo == None):
        print("none of secureinfo")
        queryString = parse.urlencode(authData)
        u = request.urlopen(wx_acess_url + '?' + queryString)
        resquest = u.read()
        dic = eval(resquest.decode("utf-8"))
        print(dic)
        if "access_token" in dic:
            print(dic["access_token"])
            print(dic["openid"])
            getUserInfo(dic["access_token"], dic["openid"])
        else:
            print("error")
    else:
        print(secureinfo)

    return HttpResponse("hello world")

# 获取用户信息
def getUserInfo(access_token,openid):
    accessdata = {
        "access_token": access_token,
        "openid": openid
    }
    queryString = parse.urlencode(accessdata)
    u = request.urlopen(wx_userinfo_url+'?'+queryString)
    res = u.read()
    dic = eval(res.decode("utf-8"))
    print(dic)
    findOrCreateUserInfoModel(dic)
    return res

# 从数据库中读取密钥
def getSecureInfoFromDB():
    secureInfo = models.SecureInfo.objects.all().first()
    return secureInfo

# 获取刷新后的token
def getRefreshToken(refresh_token):
    para = {
        "appid": authData["appid"],
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    paraString = parse.urlencode(para)
    u = request.urlopen(wx_refresh_url + '?' + paraString)
    res = u.read()
    dic = eval(res.decode("utf-8"))
    return dic["access_token"]

# 检验授权access_token是否有效
def checkAccessToken(openid, access_token):
    para = {
        "access_token": access_token,
        "openid": openid
    }
    paraString = parse.urlencode(para)
    u = request.urlopen(wx_auth_url + '?' + paraString)
    res = u.read()
    dic = eval(res.decode("utf-8"))
    if "errcode" in dic:
        print(dic["errmsg"])
        return False
    else:
        print(dic)
        return True

#已授权登录
def loginWithoutCode(req):
    if req.method == 'GET':
        openid = req.GET.get('openid')
    secureinfo = getSecureInfoFromDB()
    jsonString = ""
    if (secureinfo == None):     #本地无密钥,则为第一次登录
        return HttpResponse(status=300)
    else:
        access_token = secureinfo.accessToken
        refresh_token = secureinfo.refreshToken
        # 检查token是否有效
        if(checkAccessToken(openid, access_token)):
            # 若有效,直接获取用户信息然后返回
            return getUserInfo(access_token, openid)
        else:             #若无效,则refresh
            new_access_token = getRefreshToken(refresh_token)
            obj = models.SecureInfo.objects.first()
            obj.accessToken = new_access_token
            obj.save()
            getUserInfo(new_access_token, openid)
            jsonString = getUserInfo(new_access_token, openid)
            return HttpResponse(jsonString)

#根据code 登录
def loginWithCode(req):
    if req.method == 'POST':
        code = req.POST.get('code')
        print(code)
    authData['code'] = code
    queryString = parse.urlencode(authData)
    u = request.urlopen(wx_acess_url + '?' + queryString)
    resquest = u.read()
    dic = eval(resquest.decode("utf-8"))
    if "access_token" in dic:
        secureinfo = getSecureInfoFromDB()
        if(secureinfo == None):
            secureInfo = models.SecureInfo.objects.create(accessToken=dic["access_token"],
                                                          refreshToken=dic["refresh_token"])
            print(secureInfo)
        else:
            obj = models.SecureInfo.objects.first()
            obj.accessToken = dic["access_token"]
            obj.refreshToken = dic["refresh_token"]
            obj.save()
            print(obj)
        return HttpResponse(getUserInfo(dic["access_token"], dic["openid"]))
    else:
        return HttpResponse(status=301)

def findOrCreateUserInfoModel(dic):
    try:
        userInfo = models.UserInfo.objects.get(openid=dic["openid"])
    except models.UserInfo.DoesNotExist:
        print("no userinfo")
        userInfo = models.UserInfo.objects.create(openid=dic["openid"],
                                                  headimgurl=dic["headimgurl"],
                                                  nickname=dic["nickname"],
                                                  sex=dic["sex"],
                                                  province=dic["province"],
                                                  city=dic["city"],
                                                  country=dic["country"],
                                                  unionid=dic["unionid"])
    return userInfo

def loadAllComments(request):
    comments = models.CommentInfo.objects.all()
    jsonData = serialize('json', comments)
    return HttpResponse(jsonData)

def loadCommentByDayid(request):
    if request.method == 'GET':
        dayid = request.GET.get("dayid")
    comments = models.CommentInfo.objects.filter(dayid=dayid)
    rets = []
    for comment in comments:
        ret = {}
        try:
            userinfo = models.UserInfo.objects.get(openid=comment.openid)
            ret["id"] = comment.id
            ret["nickname"] = userinfo.nickname
            ret["headimgurl"] = userinfo.headimgurl
            ret["created"] = comment.created
            ret["dayid"] = comment.dayid
            ret["content"] = comment.content
            rets.append(ret)
        except:
            return HttpResponse(status=404)
    return HttpResponse(json.dumps(rets))


def createComment(request):
    if request.method == 'POST':
        openid = request.POST.get("openid")
        content = request.POST.get("content")
        created = request.POST.get("created")
        dayid = request.POST.get("dayid")
    newComment = models.CommentInfo.objects.create(openid=openid,
                                                   content=content,
                                                   created=created,
                                                   dayid=dayid)
    comments = models.CommentInfo.objects.filter(dayid=dayid)
    rets = []
    for comment in comments:
        ret = {}
        try:
            userinfo = models.UserInfo.objects.get(openid=comment.openid)
            ret["id"] = comment.id
            ret["nickname"] = userinfo.nickname
            ret["headimgurl"] = userinfo.headimgurl
            ret["created"] = comment.created
            ret["dayid"] = comment.dayid
            ret["content"] = comment.content
            rets.append(ret)
        except:
            return HttpResponse(status=404)
    return HttpResponse(json.dumps(rets))


