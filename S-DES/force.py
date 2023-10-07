import threading
import time

# S盒子
SBox_1 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 0, 2]]

SBox_2 = [[0, 1, 2, 3],
          [2, 3, 1, 0],
          [3, 0, 1, 2],
          [2, 1, 0, 3]]


# 置换P10
def P10(key):
    return key[2] + key[4] + key[1] + key[6] + key[3] + key[9] + key[0] + key[8] + key[7] + key[5]


# 左移
def Shift(key, n):
    left_part = key[:n]
    right_part = key[n:]
    return right_part + left_part


# 置换P8
def P8(key):
    return key[5] + key[2] + key[6] + key[3] + key[7] + key[4] + key[9] + key[8]


# 初始置换IP
def IP(value):
    return value[1] + value[5] + value[2] + value[0] + value[3] + value[7] + value[4] + value[6]


# 最终置换逆IP
def IP_re(value):
    return value[3] + value[0] + value[2] + value[4] + value[6] + value[1] + value[7] + value[5]


# 置换P4
def P4(value):
    return value[1] + value[3] + value[2] + value[0]


# 映射F
def F(value, K):
    value_EP = value[3] + value[0] + value[1] + value[2] + value[1] + value[2] + value[3] + value[0]
    result = bin(int(value_EP, 2) ^ int(K, 2))[2:].rjust(8, '0')
    result_L = result[:4]
    result_R = result[4:]
    PL_row = int(result_L[0] + result_L[3], 2)
    PL_col = int(result_L[1] + result_L[2], 2)
    PL = bin(SBox_1[PL_row][PL_col])[2:].rjust(2, '0')
    PR_row = int(result_R[0] + result_R[3], 2)
    PR_col = int(result_R[1] + result_R[2], 2)
    PR = bin(SBox_2[PR_row][PR_col])[2:].rjust(2, '0')
    F_result = P4(PL + PR)
    return F_result


# 复合函数Fk
def Fk(L, R, SK):
    F_result = F(R, SK)
    L = bin(int(L, 2) ^ int(F_result, 2))[2:].rjust(4, '0')
    Fk_result = L + R
    return Fk_result


# 交换
def SW(value):
    return value[4:] + value[:4]


# 加密
def EncryptBinary(plaintext, key):
    plaintext_IP = IP(plaintext)
    K1 = P8(Shift(P10(key), 1))
    K2 = P8(Shift(P10(key), 3))
    plaintext_Fk1 = Fk(plaintext_IP[:4], plaintext_IP[4:], K1)
    plaintext_Fk1 = SW(plaintext_Fk1)
    plaintext_Fk2 = Fk(plaintext_Fk1[:4], plaintext_Fk1[4:], K2)
    ciphertext = IP_re(plaintext_Fk2)
    return ciphertext


# 解密
def DecryptBinary(ciphertext, key):
    ciphertext_IP = IP(ciphertext)
    K1 = P8(Shift(P10(key), 1))
    K2 = P8(Shift(P10(key), 3))
    ciphertext_Fk1 = Fk(ciphertext_IP[:4], ciphertext_IP[4:], K2)
    ciphertext_Fk1 = SW(ciphertext_Fk1)
    ciphertext_Fk2 = Fk(ciphertext_Fk1[:4], ciphertext_Fk1[4:], K1)
    plaintext = IP_re(ciphertext_Fk2)
    return plaintext


# 暴力破解密钥
def brute_force_decrypt(ciphertext, plaintext, start_key, end_key, result, start_time):
    for key in range(start_key, end_key + 1):
        key_binary = bin(key)[2:].rjust(10, '0')
        decrypted_plaintext = DecryptBinary(ciphertext, key_binary)
        if decrypted_plaintext == plaintext:
            result.value = key_binary
            elapsed_time = time.time() - start_time
            result.elapsed_time = elapsed_time
            return


# 多线程破解密钥
def multi_thread_brute_force_decrypt(ciphertext, plaintext, num_threads=4):
    key_range = 2 ** 10 - 1
    keys_per_thread = key_range // num_threads
    threads = []
    result = threading.Event()

    start_time = time.time()

    for i in range(num_threads):
        start_key = i * keys_per_thread
        end_key = (i + 1) * keys_per_thread - 1
        if i == num_threads - 1:
            end_key = key_range
        thread = threading.Thread(target=brute_force_decrypt, args=(ciphertext, plaintext, start_key, end_key, result, start_time))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result.value, result.elapsed_time


# 测试代码
ciphertext1 = "10101010"
plaintext1 = "10010110"
ciphertext2 = "10101010"
plaintext2 = "10010110"

print("破解中...")
result1, time1 = multi_thread_brute_force_decrypt(ciphertext1, plaintext1)
result2, time2 = multi_thread_brute_force_decrypt(ciphertext2, plaintext2)

print("破解完成！")
print("明文1对应的密钥为：" + result1)
print("明文2对应的密钥为：" + result2)
print("破解明文1的时间为：" + str(time1) + "秒")
print("破解明文2的时间为：" + str(time2) + "秒")