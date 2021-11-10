import 仓库
import wiki
import 博客
import 论坛
import 软件下载站

lis = ['*://*/*']


def gen_urls(dic):
    for k,v in dic.items(): 
        url = '@*://'
        # 前缀
        if v[0] != '':
            url+=v[0] + '.'
        # 加域名
        url += k
        # 后缀
        if v[1] != '':    
            url+='.'+v[1]+'/*'
        else:
            ...

        #print(url) #    # @*://*.name.com/* 
        lis.append(url)

      
gen_urls(仓库.Whitelist)
gen_urls(wiki.Whitelist)
gen_urls(博客.Whitelist)
gen_urls(论坛.Whitelist)
gen_urls(软件下载站.Whitelist)

# 得到结果
for each in lis:
    print(each)

# 写入 uWhitelist_subscription.txt
f = open('./uWhitelist_subscription.txt', 'w')
for each in lis:
    f.write(each+'\n')

f.close()
