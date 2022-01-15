import 仓库
import wiki
import 博客
import 论坛
import 软件下载站

lis = []
lis_total = []

# 规则 @*://*.v2ex.com 与 @*://v2ex.com/* 的拦截效果不同，后者没效果
# 规则 @*://前缀.域名.后缀/* 有时没效果
# 所以将所有的规则改为 @*://*.前缀.域名.后缀/*
# 如果前缀是 www. 就不要写在 Whitelist 的 value[0] 中 

'''
with prefix
@*://*.prefix.domain_name.suffix/*
no prefix
@*://*.domain_name.suffix/*
no prefix and no domain name, only the suffix
@*://*.suffix/*
'''

def gen_urls(whitelist_dic):
    for k,v in whitelist_dic.items(): 
        url = '@*://*.'
        # 前缀
        if v[0] != '':
            url+=v[0] + '.'
        # 加域名
        if k != '':
            url += k.lower() # uBlacklist 对域名区分大小写 @*://*.stackoverflow.com/* 与 @*://*.StackOverflow.com/* 拦截效果不同
        else:
            url = url[:-1]   # change url('@*://*.') to '@*://*', 为了添加指定后缀的域名，如 @*://*.edu

        # 后缀
        if v[1] != '':    
            url+='.'+v[1]+'/*'

        #print(url)
        lis.append(url)
        lis_total.append(url)

def gen_subscription_txt(filename, lis):
    filename = 'whitelists/' + filename
    f = open(filename, 'w')
    for each in lis:
        f.write(each+'\n')
    f.close()

def gen_whitelist_rule_txt():
    f = open('whitelists/whitelist.txt', 'w')
    f.write(r'*://*/*')
    f.close()
      

gen_whitelist_rule_txt()

gen_urls(仓库.Whitelist)
gen_subscription_txt('仓库.txt', lis)

lis.clear()

gen_urls(wiki.Whitelist)
gen_subscription_txt('wiki.txt', lis)

lis.clear()

gen_urls(博客.Whitelist)
gen_subscription_txt('博客.txt', lis)

lis.clear()

gen_urls(论坛.Whitelist)
gen_subscription_txt('论坛.txt', lis)

lis.clear()

gen_urls(软件下载站.Whitelist)
gen_subscription_txt('软件下载站.txt', lis)

lis.clear()


# 汇总列表，一般不用
f = open('whitelists/whitelists_combined.txt', 'w')
for each in lis_total:
    f.write(each+'\n')
f.close()
