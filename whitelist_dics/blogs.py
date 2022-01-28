Whitelist = {
        'leetcode-cn':['','com/problems','0.8'],   # 乐扣试题区，不好分类的网址
        'github': ['','io','0.8'],                 # 没法 用 @://github.*/* 来表示 .com 和 .io，因为这条规则是有问题的
        'gitee':['','io','0.7'],
        'zhihu':['zhuanlan','com','0.7'],          # 知乎专栏
        'cnblogs':['www','com','0.6'],             # 博客园，加上 www 是为了过滤 https://recomm.cnblogs.com/ 这个地址
        'ruanyifeng':['','com','0.55'],            # 阮一峰的网络日志
        'oschina':['my','net','0.5'],              # 开源中国博客
        'liaoxuefeng':['','com/wiki','0.5'],       # 廖雪峰的官方网站
        'coolshell':['','cn/articles','0.5'],      # 酷壳
        'williamlong':['','info/articles','0.4'],  # 月光博客
        '': ['','edu','0.3'],                      # 所有以 edu 结尾的域名(学校)

}
