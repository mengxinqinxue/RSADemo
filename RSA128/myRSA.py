import random
import re
class myRSA():
    def __init__(self):
        self.Chr_Len = 5 #单个字符补足后的长度，十进制bit
        self.NLen = 128 #生成密钥对模的长度，二进制bit
        self.GroupLen = 30  # 分组长度，十进制bit
        self.Enc_GroupLen = 32 #加密后分组的长度

    def Str2Bin(self,OriginalData):
        '''
        字符转二进制
        :param OriginalData: 原始数据，string类型
        :return: 返回二进制数据结果，list类型
        '''
        list = []
        for c in OriginalData:
            list.append(bin(ord(c)).replace('0b',''))
        return list

    def Str2Ord(self,OriginalData):
        '''
        字符转二进制
        :param OriginalData: 原始数据，string类型
        :return: 返回二进制数据结果，list类型
        '''
        list = []
        for c in OriginalData:
            list.append(ord(c))
        return list

    def Bin2Str(self,DecData):
        '''
        解密后的数据转字符
        :param EncData: 解密后的数据，十进制list类型
        :return: 返回字符，str类型
        '''
        list = []
        for b in DecData:
                list.append(chr(int(b,2)))
        return list

    def Ord2Str(self,DecData):
        '''
        解密后的数据转字符
        :param EncData: 解密后的数据，十进制list类型
        :return: 返回字符，str类型
        '''
        list = []
        for b in DecData:
                list.append(chr(b))
        return list

    def MillerRabin_IsPrime(self,p):
        '''
        Miller-Rabin检验超大素数
        费马小定理+二次探测
        :p：待判定的素数
        :return: 返回判断结果，int类型
        '''
        if(p == 2):
            return 1
        elif(p % 2 == 0):
            p = p + 1
        m,s,Test_vetor,k = p-1, 0, [2,3,5,7,31,61,24251,9875321], 0
        while (m % 2 == 0):
            m, k = int(m / 2), k+1
        for i in range(len(Test_vetor)):
            a = Test_vetor[i]
            x = self.PowerMod(a,m,p)
            for j in range(k):
                y = self.PowerMod(x,2,p)
                if ((y == 1) and (x != p-1) and (x != 1)):
                    return 0
                x = y
            if (x != 1):
                return 0
        return 1

    def GetPimeNumber(self,limit_lower, limit_upper):
        '''
        在某段区域范围内随机找出一个素数
        :param limit_lower: 区域下限
        :param limit_upper: 区域上限
        :return: 
        '''
        t = 0
        rand = random.randint(limit_lower, limit_upper)
        if rand % 10 % 2 == 0:
            rand = rand + 1
        while (t == 0):
            if self.MillerRabin_IsPrime(rand) == 1:
                t = 1
            else:
                rand = rand + 2
                if rand%5 == 0:
                    rand = rand + 2
        return rand

    def GetLCM(self,p, q):
        '''
        计算(p-1,q-1)最小公倍数
        :param p:int类型 
        :param q: int类型
        :return: 
        '''
        a, b = p-1, q-1
        c = a % b
        while (c != 0):
            a = b
            b = c
            c = a % b
        return int((p - 1) * (q - 1) / b)

    def getDecKey(self,LCM, E):
        '''
        最小公倍数法，此方法不稳定，素数越大，越不适用
        :param LCM: 最小公倍数，int类型
        :param E：密钥素数，int类型
        :return: 
        '''
        a = int((E - 1) / LCM) + 1
        b = int((E * LCM - 1) / LCM) * 2
        for n in range(a, b + 1):
            if (n * LCM + 1) % E == 0:
                print(n,LCM,E,a,b)
                res = (n * LCM + 1) / E
                if 1 == self.MillerRabin_IsPrime(res):
                    return res
        return 0

    def Euclid_DecKey(self,E, N):
        '''
        拓展欧几里得算法，求解另一个密钥D
        :param E: 密钥素数，int类型
        :param N: 模，int类型
        :return: 密钥D结果
        '''
        x, y, t = [E], [N], 0
        while (x[t] != 1 and y[t] != 1):
            y.append(self.PowerMod(y[t],1,x[t]))
            x.append(self.PowerMod(x[t],1,y[t+1]))
            t = t + 1
        d = 1
        for i in range(t):
            k = (x[t - 1] * d - 1) // y[t]
            t = t - 1
            d = (1 + y[t] * k) // x[t]
        return d

    def Chr_Padding(self,List,GroupLen):
        '''
        对每个分组补足长度到指定GroupLen位数
        :param List: 分组数据，list类型，十进制
        :param GroupLen: 字符补足后的长度
        :return: 返回补足完成后的分组数据，list类型
        '''
        for i in range(len(List)):
            List[i] = str(List[i])
            if len(List[i]) < GroupLen:
                for j in range(GroupLen - len(List[i])):
                    List[i] = '0'+List[i]
        return List

    def PChr_Combine(self,List):
        '''
        对补足后的字符进行合并分组，每组长度为int(NLen/Chr_Len),如果最后分组不足则不需补满
        :param List: 待合并数据，list字符类型
        :param NLen: 公钥模长度，单位bit
        :return: 返回待加密的分组
        '''
        L,k = [''],0
        t = self.NLen//4//self.Chr_Len
        GroupNum = len(List)//t+1
        for i in range(len(List)):
            if ((i+1)%t == 1 and (i+1) != 1):
                k = k+1
                L.append('')
            L[k] = L[k]+List[i]
        return L

    def PowerMod(self,base, N, mod):
        '''
        模重复平方算法，计算base**N % mod
        :param base: 基数
        :param N: int类型
        :param mod: 模
        :return: 计算结果，int类型
        '''
        a = 1
        while (N > 0):
            if (N % 2 == 1):
                a = (a * base) % mod
            base = (base * base) % mod
            N = int(N // 2)
        return a

    def RSA_PairKey_Get(self):
        a, b = 3333333333333333, 9999999999999999
        while 1:
            p = self.GetPimeNumber(a, b)
            q = self.GetPimeNumber(a, b)
            N = p * q
            if len(str(N)*4) == self.NLen:
                break
        E = self.GetPimeNumber(a, b)
        D = self.Euclid_DecKey(E, (p - 1) * (q - 1))
        return  E,D,N

    def Message_Enc(self,M,Key,N):
        '''
        明文加密
        :param M: 待加密明文，十进制数
        :param Key: 加密密钥，十进制数
        :param N: 公钥模，十进制数
        :return: 加密后的密文，十进制数
        '''
        return self.PowerMod(M, E, N)

    def Message_Dec(self,M,Ley,N):
        '''
        密文解密
        :param M: 待解密的密文
        :param Ley: 密钥，十进制数
        :param N: 公钥模，十进制数
        :return: 解密后的原文，十进制数
        '''
        return self.PowerMod(M, E, N)

    def L_Message_Enc(self,List,Key,N):
        '''
        对List里的每个字符串转数字后加密再补足
        :param L: list，数字字符串
        :param Ley: 密钥，十进制数
        :param N: 公钥模，十进制数
        :return: 加密后的补足的数字字符串
        '''
        for i in range(len(List)):
            List[i] = self.PowerMod(int(List[i]), Key, N)
        GroupLen = self.Enc_GroupLen
        for i in range(len(List)):
            List[i] = str(List[i])
            if len(List[i]) < GroupLen:
                for j in range(GroupLen - len(List[i])):
                    List[i] = '0'+List[i]
        return List


    def L_Message_Dec(self, L, Key, N):
        '''
        对L里的每个数字字符串进行解密
        :param L: 加密后的list，字符串十进制
        :param Key: 密钥，十进制数
        :param N: 公钥模，十进制数
        :return: 解密后的数字字符串
        '''
        for i in range(len(L)):
            L[i] = str(self.PowerMod(int(L[i]), Key, N))
        return self.Chr_Padding(L,self.GroupLen)

    def Win_Message_Enc(self, s, E, N):
        res1 = self.Str2Ord(s) #字符串转10进制Ascll码
        res3 = self.Chr_Padding(res1, self.Chr_Len) #Ascll补足
        res4 = self.PChr_Combine(res3) #字符拼接分组
        res4 = self.Chr_Padding(res4, self.GroupLen) #分组补足
        res5 = self.L_Message_Enc(res4, E, N) #加密结果
        res8 = "".join(res5)
        return res8

    def Win_Message_Dec(self, s, D, N):
        s = re.findall(r'.{32}', s)
        res6 = self.L_Message_Dec(s, D, N) #解密结果含补足，十进制
        res8 = "".join(res6) #解密分组合并
        res9 = re.findall(r'.{5}', res8) #按字符分组长度分割
        for i in range(len(res9)): #十进制Acsll转字符
            res9[i] = chr(int(res9[i]))
        res10 = ""
        for i in range(len(res9)):#去补足
            if res9[i] != '\x00':
                res10 = res10 + res9[i]
        return res10
