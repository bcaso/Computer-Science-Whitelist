Whitelist = {
        'gitee':['','io'],
        'github': ['','io'],          # 没法 用 @://github.*/* 来表示 .com 和 .io，因为这条规则是有问题的
        '': ['','edu'],               # 所有以 edu 结尾的域名(学校)
        'cnblogs':['www','com'],      # 博客园，加上 www 是为了过滤 https://recomm.cnblogs.com/ 这个地址
        'oschina':['my','net'],       # 开源中国博客
        'zhihu':['zhuanlan','com'],   # 知乎专栏
        'liaoxuefeng':['','com'],     # 廖雪峰的官方网站
        'ruanyifeng':['','com'],      # 阮一峰的网络日志
        'williamlong':['','info'],    # 月光博客
        'leetcode-cn':['','com/problems'], # 乐扣试题区，不好分类的网址

}
