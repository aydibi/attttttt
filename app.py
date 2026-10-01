import streamlit as st
import numpy as np
from math import gcd
from Crypto.Cipher import DES, AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import random
import secrets

st.set_page_config(
    page_title="🦆 Mã hóa Vịt Vàng",
    page_icon="🦆",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@400;600;700&family=Fredoka:wght@500;600;700&display=swap');

/* ===== BACKGROUND: nắng vàng + biển xanh ===== */
.stApp {
    background:
        radial-gradient(circle at 15% 15%, rgba(255, 235, 130, 0.7) 0%, transparent 40%),
        radial-gradient(circle at 85% 20%, rgba(255, 210, 80, 0.55) 0%, transparent 42%),
        radial-gradient(ellipse at bottom, rgba(79, 195, 247, 0.75) 0%, transparent 60%),
        linear-gradient(180deg,
            #fff9c4 0%, #ffe082 18%, #ffd54f 35%,
            #ffca28 48%, #4fc3f7 70%, #29b6f6 88%, #0288d1 100%);
    background-attachment: fixed;
}
.stApp::after {
    content: "🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆 🦆";
    position: fixed; bottom: -10px; left: 0; right: 0;
    font-size: 26px; letter-spacing: 4px; opacity: 0.45;
    pointer-events: none; z-index: 0; text-align: center;
    overflow: hidden; white-space: nowrap;
    animation: duckFloat 5s ease-in-out infinite;
}
@keyframes duckFloat {
    0%, 100% { transform: translateY(0) scaleX(1); opacity: 0.4; }
    50%      { transform: translateY(-14px) scaleX(-1); opacity: 0.65; }
}
html, body, [class*="css"], .stMarkdown, p, label, div {
    font-family: 'Quicksand', 'Comic Sans MS', sans-serif !important;
}
h1 {
    font-family: 'Fredoka', sans-serif !important;
    color: #f57f17 !important; text-align: center !important;
    font-size: 3rem !important;
    text-shadow: 3px 3px 0 #fff9c4, 6px 6px 14px rgba(245, 127, 23, 0.45),
                 0 0 30px rgba(255, 213, 79, 0.65) !important;
    padding: 15px 0 5px 0 !important; letter-spacing: 1.5px;
}
h2, h3 { color: #01579b !important; font-weight: 700 !important; }

.stButton > button {
    background: linear-gradient(135deg, #fff176, #ffd54f, #f57f17) !important;
    color: #3e2723 !important; border-radius: 30px !important;
    border: 3px solid #fff9c4 !important;
    padding: 12px 28px !important; font-weight: 800 !important;
    font-size: 1.05rem !important;
    box-shadow: 0 8px 20px rgba(245, 127, 23, 0.5),
                inset 0 -3px 0 rgba(120, 60, 0, 0.35) !important;
    transition: all 0.3s ease !important; width: 100%;
}
.stButton > button:hover {
    transform: translateY(-4px) scale(1.03) rotate(-0.5deg);
    box-shadow: 0 14px 28px rgba(245, 127, 23, 0.7),
                inset 0 -3px 0 rgba(120, 60, 0, 0.45) !important;
    background: linear-gradient(135deg, #fff9c4, #ffe082, #ffb300) !important;
}

.stTextArea textarea, .stTextInput input, .stNumberInput input {
    border-radius: 16px !important;
    border: 2.5px solid #4fc3f7 !important;
    background-color: #fffef5 !important;
    padding: 12px !important; font-size: 1rem !important;
    color: #01579b !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: #f57f17 !important;
    background-color: #fffde7 !important;
    box-shadow: 0 0 0 4px rgba(255, 213, 79, 0.55) !important;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,
        #fff9c4 0%, #ffe082 30%, #ffd54f 55%,
        #4fc3f7 82%, #0288d1 100%);
    border-right: 3px dashed #f57f17;
}
[data-testid="stSidebar"] h2 {
    color: #3e2723 !important;
    font-family: 'Fredoka', sans-serif !important;
    text-shadow: 1px 1px 0 #fff9c4;
}

.stSelectbox > div > div, .stMultiSelect > div > div {
    border-radius: 16px !important;
    border: 2.5px solid #4fc3f7 !important;
    background-color: #fffef5 !important;
}
.stAlert {
    border-radius: 16px !important;
    border-left: 6px solid #f57f17 !important;
    background-color: #fffde7 !important;
}
.streamlit-expanderHeader, [data-testid="stExpander"] {
    border-radius: 16px !important;
    background-color: #fffde7 !important;
    border: 2px dashed #ffd54f !important;
}

.duck-bg {
    position: fixed; top: -10%; font-size: 34px;
    animation: duckSwim 14s linear infinite;
    opacity: 0.85; pointer-events: none; z-index: 0;
    filter: drop-shadow(2px 2px 6px rgba(120, 60, 0, 0.3));
}
@keyframes duckSwim {
    0%   { transform: translateY(-10vh) translateX(0) rotate(-10deg); opacity: 0; }
    10%  { opacity: 0.9; }
    25%  { transform: translateY(25vh) translateX(20px) rotate(6deg); }
    50%  { transform: translateY(50vh) translateX(-15px) rotate(-6deg); }
    75%  { transform: translateY(75vh) translateX(25px) rotate(10deg); }
    90%  { opacity: 0.9; }
    100% { transform: translateY(110vh) translateX(-20px) rotate(-10deg); opacity: 0; }
}
.duck-bg:nth-child(1)  { left: 3%;  animation-delay: 0s;    font-size: 40px; }
.duck-bg:nth-child(2)  { left: 16%; animation-delay: 2.5s;  font-size: 28px; }
.duck-bg:nth-child(3)  { left: 30%; animation-delay: 6s;    font-size: 36px; }
.duck-bg:nth-child(4)  { left: 44%; animation-delay: 1s;    font-size: 30px; }
.duck-bg:nth-child(5)  { left: 58%; animation-delay: 8s;    font-size: 42px; }
.duck-bg:nth-child(6)  { left: 72%; animation-delay: 4s;    font-size: 32px; }
.duck-bg:nth-child(7)  { left: 85%; animation-delay: 10s;   font-size: 26px; }
.duck-bg:nth-child(8)  { left: 94%; animation-delay: 5.5s;  font-size: 38px; }

.result-box {
    background:
        radial-gradient(circle at 20% 30%, rgba(255, 235, 130, 0.75) 0%, transparent 42%),
        radial-gradient(circle at 80% 70%, rgba(79, 195, 247, 0.6) 0%, transparent 42%),
        linear-gradient(135deg, #fffde7, #fff9c4, #e1f5fe);
    border: 3px dashed #f57f17; border-radius: 22px;
    padding: 18px 24px; margin-top: 15px;
    box-shadow: 0 8px 22px rgba(245, 127, 23, 0.35),
                inset 0 0 30px rgba(255, 249, 196, 0.7);
    position: relative;
}
.result-box::before {
    content: "🦆"; position: absolute; top: -22px; left: 20px;
    font-size: 34px; background: #fff9c4; border-radius: 50%;
    padding: 2px 8px; box-shadow: 0 3px 10px rgba(0,0,0,0.15);
    animation: duckBob 2.5s ease-in-out infinite;
}
@keyframes duckBob {
    0%, 100% { transform: translateY(0) rotate(-8deg); }
    50%      { transform: translateY(-4px) rotate(8deg); }
}
.result-box h4 {
    color: #f57f17 !important; margin: 0 0 10px 0 !important;
    font-family: 'Fredoka', sans-serif !important; font-size: 1.25rem !important;
}
.result-text {
    color: #01579b; font-size: 1.18rem; font-weight: 700;
    word-break: break-word; line-height: 1.5;
}
.duck-footer {
    text-align: center; color: #01579b;
    padding: 20px 0 30px 0; font-size: 1rem; font-weight: 700;
    text-shadow: 1px 1px 0 rgba(255, 249, 196, 0.95);
}
hr {
    border: none; height: 6px;
    background: radial-gradient(circle, #f57f17 30%, transparent 30%),
                radial-gradient(circle, #4fc3f7 30%, transparent 30%);
    background-size: 20px 20px;
    background-position: 0 0, 10px 10px;
    background-repeat: repeat-x; margin: 20px 0; opacity: 0.7;
}
.stCaption, small { color: #01579b !important; font-weight: 600 !important; }
.stRadio label, .stCheckbox label { color: #01579b !important; font-weight: 700 !important; }

/* Nút chọn nhóm */
.group-btn-active button {
    background: linear-gradient(135deg, #4fc3f7, #0288d1) !important;
    color: #fff9c4 !important;
    border-color: #fff9c4 !important;
}
</style>

<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
<div class="duck-bg">🦆</div>
""", unsafe_allow_html=True)


# ============================================================
# BẢNG CHỮ CÁI
# ============================================================
Z26 = "abcdefghijklmnopqrstuvwxyz"
Z29 = "aăâbcdđeêghiklmnoôơpqrstuưvxy"

def get_alphabet(use_z29):
    return Z29 if use_z29 else Z26

def char_to_num(c, alphabet):
    idx = alphabet.find(c.lower())
    return idx if idx >= 0 else -1

def num_to_char(num, alphabet):
    n = len(alphabet)
    return alphabet[num % n]

def mod_inverse(a, m):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError(f"Không có nghịch đảo modulo của {a} theo {m}")


# ============================================================
# 1. CAESAR
# ============================================================
def caesar_encrypt(text, k, alphabet):
    result = ""
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            new_c = num_to_char(idx + k, alphabet)
            result += new_c.upper() if c.isupper() else new_c
        else:
            result += c
    return result

def caesar_decrypt(text, k, alphabet):
    return caesar_encrypt(text, -k, alphabet)


# ============================================================
# 2. SUBSTITUTION
# ============================================================
def substitution_encrypt(text, key, alphabet):
    if len(key) != len(alphabet):
        raise ValueError(f"Khóa phải có đúng {len(alphabet)} ký tự")
    if len(set(key)) != len(key):
        raise ValueError("Khóa không được có ký tự trùng lặp")
    result = ""
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            new_c = key[idx]
            result += new_c.upper() if c.isupper() else new_c
        else:
            result += c
    return result

def substitution_decrypt(text, key, alphabet):
    result = ""
    for c in text:
        idx = key.find(c.lower())
        if idx >= 0:
            new_c = alphabet[idx]
            result += new_c.upper() if c.isupper() else new_c
        else:
            result += c
    return result


# ============================================================
# 3. VIGENERE
# ============================================================
def vigenere_encrypt(text, key, alphabet):
    key_low = key.lower()
    shifts = [alphabet.index(c) for c in key_low if c in alphabet]
    if not shifts:
        raise ValueError("Từ khóa không hợp lệ")
    result = ""
    ki = 0
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            shift = shifts[ki % len(shifts)]
            new_c = num_to_char(idx + shift, alphabet)
            result += new_c.upper() if c.isupper() else new_c
            ki += 1
        else:
            result += c
    return result

def vigenere_decrypt(text, key, alphabet):
    key_low = key.lower()
    shifts = [alphabet.index(c) for c in key_low if c in alphabet]
    if not shifts:
        raise ValueError("Từ khóa không hợp lệ")
    result = ""
    ki = 0
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            shift = shifts[ki % len(shifts)]
            new_c = num_to_char(idx - shift, alphabet)
            result += new_c.upper() if c.isupper() else new_c
            ki += 1
        else:
            result += c
    return result


# ============================================================
# 4. AFFINE
# ============================================================
def affine_encrypt(text, a, b, alphabet):
    n = len(alphabet)
    if gcd(a, n) != 1:
        raise ValueError(f"gcd({a}, {n}) phải = 1")
    result = ""
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            new_c = num_to_char(a * idx + b, alphabet)
            result += new_c.upper() if c.isupper() else new_c
        else:
            result += c
    return result

def affine_decrypt(text, a, b, alphabet):
    n = len(alphabet)
    a_inv = mod_inverse(a, n)
    result = ""
    for c in text:
        idx = char_to_num(c, alphabet)
        if idx >= 0:
            new_c = num_to_char(a_inv * (idx - b), alphabet)
            result += new_c.upper() if c.isupper() else new_c
        else:
            result += c
    return result


# ============================================================
# 5. HILL 2x2
# ============================================================
def hill_encrypt(text, K, alphabet):
    n = len(alphabet)
    idxs = [char_to_num(c, alphabet) for c in text if char_to_num(c, alphabet) >= 0]
    while len(idxs) % 2 != 0:
        idxs.append(0)
    result = ""
    for i in range(0, len(idxs), 2):
        p1, p2 = idxs[i], idxs[i + 1]
        c1 = (K[0][0] * p1 + K[0][1] * p2) % n
        c2 = (K[1][0] * p1 + K[1][1] * p2) % n
        result += num_to_char(c1, alphabet).upper()
        result += num_to_char(c2, alphabet).upper()
    return result

def hill_decrypt(text, K, alphabet):
    n = len(alphabet)
    det = (K[0][0] * K[1][1] - K[0][1] * K[1][0]) % n
    if gcd(det, n) != 1:
        raise ValueError(f"det(K)={det} phải nguyên tố cùng nhau với {n}")
    det_inv = mod_inverse(det, n)
    Kinv = [
        [(K[1][1] * det_inv) % n, (-K[0][1] * det_inv) % n],
        [(-K[1][0] * det_inv) % n, (K[0][0] * det_inv) % n]
    ]
    idxs = [char_to_num(c, alphabet) for c in text if char_to_num(c, alphabet) >= 0]
    while len(idxs) % 2 != 0:
        idxs.append(0)
    result = ""
    for i in range(0, len(idxs), 2):
        c1, c2 = idxs[i], idxs[i + 1]
        p1 = (Kinv[0][0] * c1 + Kinv[0][1] * c2) % n
        p2 = (Kinv[1][0] * c1 + Kinv[1][1] * c2) % n
        result += num_to_char(p1, alphabet)
        result += num_to_char(p2, alphabet)
    return result
    # ============================================================
# 6. DES
# ============================================================
def text_to_bytes(text, alphabet):
    n = len(alphabet)
    bytes_out = bytearray()
    for c in text.lower():
        idx = alphabet.find(c)
        if idx >= 0:
            bytes_out.append(idx % 256)
    return bytes(bytes_out)

def bytes_to_text(data, alphabet):
    n = len(alphabet)
    result = ""
    for b in data:
        result += alphabet[b % n]
    return result

def des_encrypt_text(plaintext, key_text, alphabet):
    key_bytes = text_to_bytes(key_text, alphabet)
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\x00' * (8 - len(key_bytes))
    key_bytes = key_bytes[:8]
    pt_bytes = text_to_bytes(plaintext, alphabet)
    pt_bytes = pad(pt_bytes, 8)
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    ct = cipher.encrypt(pt_bytes)
    return ct.hex().upper()

def des_decrypt_text(ciphertext_hex, key_text, alphabet):
    key_bytes = text_to_bytes(key_text, alphabet)
    if len(key_bytes) < 8:
        key_bytes = key_bytes + b'\x00' * (8 - len(key_bytes))
    key_bytes = key_bytes[:8]
    try:
        ct_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        raise ValueError("Bản mã phải là chuỗi Hexadecimal hợp lệ!")
    if len(ct_bytes) % 8 != 0:
        raise ValueError("Độ dài bản mã Hex phải là bội số của 8 bytes (16 ký tự Hex).")
    cipher = DES.new(key_bytes, DES.MODE_ECB)
    pt_bytes = unpad(cipher.decrypt(ct_bytes), 8)
    return bytes_to_text(pt_bytes, alphabet)


# ============================================================
# 7. AES
# ============================================================
def aes_encrypt_text(plaintext, key_text, alphabet):
    key_bytes = text_to_bytes(key_text, alphabet)
    if len(key_bytes) < 16:
        key_bytes = key_bytes + b'\x00' * (16 - len(key_bytes))
    key_bytes = key_bytes[:16]
    pt_bytes = text_to_bytes(plaintext, alphabet)
    pt_bytes = pad(pt_bytes, 16)
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    ct = cipher.encrypt(pt_bytes)
    return ct.hex().upper()

def aes_decrypt_text(ciphertext_hex, key_text, alphabet):
    key_bytes = text_to_bytes(key_text, alphabet)
    if len(key_bytes) < 16:
        key_bytes = key_bytes + b'\x00' * (16 - len(key_bytes))
    key_bytes = key_bytes[:16]
    try:
        ct_bytes = bytes.fromhex(ciphertext_hex)
    except ValueError:
        raise ValueError("Bản mã phải là chuỗi Hexadecimal hợp lệ!")
    if len(ct_bytes) % 16 != 0:
        raise ValueError("Độ dài bản mã Hex phải là bội số của 16 bytes (32 ký tự Hex).")
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    pt_bytes = unpad(cipher.decrypt(ct_bytes), 16)
    return bytes_to_text(pt_bytes, alphabet)


# ============================================================
# 8. RSA
# ============================================================
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def gen_prime(bits=8):
    while True:
        p = random.randint(2 ** (bits - 1), 2 ** bits - 1)
        if is_prime(p):
            return p

def rsa_gen_keys(bits=12):
    p = gen_prime(bits)
    q = gen_prime(bits)
    while q == p:
        q = gen_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if e >= phi:
        e = 3
        while gcd(e, phi) != 1:
            e += 2
    else:
        while gcd(e, phi) != 1:
            e += 2
    d = mod_inverse(e, phi)
    return (e, n), (d, n), (p, q, phi)

def text_to_number(text, alphabet):
    n = len(alphabet)
    num = 0
    for c in text.lower():
        idx = alphabet.find(c)
        if idx >= 0:
            num = num * n + idx
    return num

def number_to_text(num, alphabet):
    n = len(alphabet)
    if num == 0:
        return alphabet[0]
    chars = []
    while num > 0:
        chars.append(alphabet[num % n])
        num //= n
    return "".join(reversed(chars))

def rsa_encrypt(text, e, n, alphabet):
    m = text_to_number(text, alphabet)
    if m >= n:
        raise ValueError(
            f"Bản rõ quá lớn so với n={n}. Hãy chọn p,q lớn hơn hoặc bản rõ ngắn hơn."
        )
    c = pow(m, e, n)
    return str(c)

def rsa_decrypt(cipher_str, d, n, alphabet):
    try:
        c = int(cipher_str.strip())
    except ValueError:
        raise ValueError("Bản mã RSA phải là một số nguyên!")
    m = pow(c, d, n)
    return number_to_text(m, alphabet)


# ============================================================
# 9. HÀM BĂM
# ============================================================
def compute_hash(text, algo):
    data = text.encode("utf-8")
    if algo == "MD5":
        return hashlib.md5(data).hexdigest().upper()
    elif algo == "SHA-1":
        return hashlib.sha1(data).hexdigest().upper()
    elif algo == "SHA-256":
        return hashlib.sha256(data).hexdigest().upper()
    elif algo == "SHA-512":
        return hashlib.sha512(data).hexdigest().upper()
    return ""


# ============================================================
# HÀM XỬ LÝ TỔNG
# ============================================================
def process(text, encrypt, category, cipher_type, key_input, alphabet):
    if category == "🏛️ Mã hóa cổ điển":
        if cipher_type == "Dịch vòng (Caesar)":
            k = int(key_input)
            return caesar_encrypt(text, k, alphabet) if encrypt else caesar_decrypt(text, k, alphabet)
        elif cipher_type == "Thay thế (Substitution)":
            key = key_input.lower().strip()
            return substitution_encrypt(text, key, alphabet) if encrypt else substitution_decrypt(text, key, alphabet)
        elif cipher_type == "Vigenere":
            return vigenere_encrypt(text, key_input, alphabet) if encrypt else vigenere_decrypt(text, key_input, alphabet)
        elif cipher_type == "Affine":
            a, b = key_input
            return affine_encrypt(text, a, b, alphabet) if encrypt else affine_decrypt(text, a, b, alphabet)
        elif cipher_type == "Hill (2x2)":
            return hill_encrypt(text, key_input, alphabet) if encrypt else hill_decrypt(text, key_input, alphabet)

    elif category == "⚙️ Mã hóa hiện đại":
        if cipher_type == "DES":
            return des_encrypt_text(text, key_input, alphabet) if encrypt else des_decrypt_text(text, key_input, alphabet)
        else:
            return aes_encrypt_text(text, key_input, alphabet) if encrypt else aes_decrypt_text(text, key_input, alphabet)

    elif category == "🔑 Mã hóa công khai":
        e_k, d_k, n_k = key_input
        return rsa_encrypt(text, e_k, n_k, alphabet) if encrypt else rsa_decrypt(text, d_k, n_k, alphabet)

    return ""
    # ============================================================
# HEADER
# ============================================================
st.title("🦆 Ứng dụng Mã hóa Vịt Vàng 🦆")
st.markdown(
    "<p style='text-align:center; color:#01579b; font-size:1.18rem; font-weight:700; "
    "text-shadow:1px 1px 0 rgba(255,249,196,0.95);'>"
    "🌊 Cổ điển • Hiện đại (DES/AES) • Công khai (RSA) • Hàm băm 🌊<br>"
    "<span style='font-size:1rem;'>Trên hệ Z26 (tiếng Anh), Z29 (tiếng Việt) và Hexadecimal</span>"
    "</p>", unsafe_allow_html=True
)
st.markdown("---")


# ============================================================
# 🎯 MENU CHỌN NHÓM — Ở TRANG CHÍNH
# ============================================================
st.markdown("### 📂 Bước 1 — Chọn nhóm thuật toán")

if "category" not in st.session_state:
    st.session_state.category = "🏛️ Mã hóa cổ điển"

GROUPS = [
    ("🏛️ Mã hóa cổ điển", "Caesar • Substitution • Vigenere • Affine • Hill"),
    ("⚙️ Mã hóa hiện đại", "DES • AES"),
    ("🔑 Mã hóa công khai", "RSA"),
    ("🧮 Hàm băm", "MD5 • SHA-1 • SHA-256 • SHA-512"),
]

cols = st.columns(4)
for i, (gname, gdesc) in enumerate(GROUPS):
    with cols[i]:
        active = (st.session_state.category == gname)
        label = f"{'✅ ' if active else ''}{gname}"
        if st.button(label, key=f"grp_btn_{i}", use_container_width=True,
                     type="primary" if active else "secondary"):
            st.session_state.category = gname
            st.rerun()
        st.caption(gdesc)

category = st.session_state.category
st.info(f"👉 Đang chọn nhóm: **{category}**")
st.markdown("---")


# ============================================================
# ⚙️ SIDEBAR — CẤU HÌNH KHÓA
# ============================================================
with st.sidebar:
    st.header("🔑 Cấu hình khóa")
    st.caption(f"Nhóm: **{category}**")
    st.markdown("---")

    use_z29 = False
    alphabet = Z26
    n = 26
    system_type = "Z26 - Tiếng Anh 🇬🇧"

    # ----- CỔ ĐIỂN -----
    if category == "🏛️ Mã hóa cổ điển":
        cipher_type = st.selectbox(
            "🌿 Loại mã hóa:",
            ["Dịch vòng (Caesar)", "Thay thế (Substitution)",
             "Vigenere", "Affine", "Hill (2x2)"]
        )
        system_type = st.radio(
            "🌊 Hệ mã hóa:",
            ["Z26 - Tiếng Anh 🇬🇧", "Z29 - Tiếng Việt 🇻🇳"]
        )
        use_z29 = system_type.startswith("Z29")
        alphabet = get_alphabet(use_z29)
        n = len(alphabet)
        st.info(f"📖 Bảng chữ cái ({n} ký tự):\n`{alphabet}`")

        st.markdown("### 🔑 Khóa")
        if cipher_type == "Dịch vòng (Caesar)":
            key_input = st.number_input("Số dịch chuyển k:", min_value=0, max_value=n-1, value=3)
        elif cipher_type == "Thay thế (Substitution)":
            default_sub = "qwertyuiopasdfghjklzxcvbnm"
            if use_z29:
                default_sub = "aăâbcdđeêghiklmnoôơpqrstuưvxy"[::-1]
            key_input = st.text_input(f"Bảng thay thế ({n} ký tự):",
                                     value=default_sub[:n])
        elif cipher_type == "Vigenere":
            key_input = st.text_input("Từ khóa:", value="DUCK")
        elif cipher_type == "Affine":
            col1, col2 = st.columns(2)
            with col1:
                a_val = st.number_input("Hệ số a:", min_value=1, max_value=n-1, value=5)
            with col2:
                b_val = st.number_input("Hệ số b:", min_value=0, max_value=n-1, value=8)
            key_input = (int(a_val), int(b_val))
            if gcd(a_val, n) != 1:
                st.error(f"⚠️ gcd({a_val}, {n}) ≠ 1. Không hợp lệ!")
        elif cipher_type == "Hill (2x2)":
            st.markdown("Ma trận K = [[a, b], [c, d]]:")
            c1, c2 = st.columns(2)
            with c1:
                a_val = st.number_input("a:", 0, n-1, 3, key="hill_a")
                cc_val = st.number_input("c:", 0, n-1, 2, key="hill_c")
            with c2:
                b_val = st.number_input("b:", 0, n-1, 3, key="hill_b")
                d_val = st.number_input("d:", 0, n-1, 5, key="hill_d")
            key_input = [[int(a_val), int(b_val)], [int(cc_val), int(d_val)]]
            det = (a_val * d_val - b_val * cc_val) % n
            if gcd(det, n) != 1:
                st.error(f"⚠️ det(K)={det}, gcd≠1. Không khả nghịch!")
            else:
                st.success(f"✅ det(K) = {det}")

    # ----- HIỆN ĐẠI -----
    elif category == "⚙️ Mã hóa hiện đại":
        cipher_type = st.selectbox("🌿 Thuật toán:", ["DES", "AES"])
        system_type = st.radio(
            "🌊 Hệ mã hóa:",
            ["Z26 - Tiếng Anh 🇬🇧", "Z29 - Tiếng Việt 🇻🇳"]
        )
        use_z29 = system_type.startswith("Z29")
        alphabet = get_alphabet(use_z29)
        n = len(alphabet)
        st.info(f"📖 Bảng chữ cái ({n} ký tự):\n`{alphabet}`")

        st.markdown("### 🔑 Khóa (nhập bằng chữ cái)")
        if cipher_type == "DES":
            key_input = st.text_input("Khóa DES (~8 ký tự):", value="duckkey1")
            st.caption("Tự động chuyển thành 8 bytes (64 bit).")
        else:
            key_input = st.text_input("Khóa AES (~16 ký tự):", value="duckkeyaes12345")
            st.caption("Tự động chuyển thành 16 bytes (128 bit).")

    # ----- CÔNG KHAI -----
    elif category == "🔑 Mã hóa công khai":
        cipher_type = "RSA"
        system_type = st.radio(
            "🌊 Hệ mã hóa:",
            ["Z26 - Tiếng Anh 🇬🇧", "Z29 - Tiếng Việt 🇻🇳"]
        )
        use_z29 = system_type.startswith("Z29")
        alphabet = get_alphabet(use_z29)
        n = len(alphabet)
        st.info(f"📖 Bảng chữ cái ({n} ký tự):\n`{alphabet}`")

        st.markdown("### 🔑 Khóa RSA")
        if "rsa_keys" not in st.session_state:
            st.session_state.rsa_keys = rsa_gen_keys(bits=12)

        (e_k, n_k), (d_k, n_k2), (p_k, q_k, phi_k) = st.session_state.rsa_keys

        if st.button("🎲 Sinh lại khóa RSA"):
            st.session_state.rsa_keys = rsa_gen_keys(bits=12)
            st.rerun()

        st.success(f"**Công khai (e, n):** ({e_k}, {n_k})")
        with st.expander("🔒 Khóa bí mật & thông tin"):
            st.write(f"**Bí mật (d, n):** ({d_k}, {n_k2})")
            st.write(f"p = {p_k}, q = {q_k}, φ(n) = {phi_k}")

        key_input = (e_k, d_k, n_k)

    # ----- HÀM BĂM -----
    else:
        cipher_type = st.selectbox("🌿 Chọn hàm băm:", ["MD5", "SHA-1", "SHA-256", "SHA-512"])
        system_type = "Hash"
        key_input = None
        alphabet = ""
        n = 0
        st.info("ℹ️ Hàm băm không cần khóa — chỉ băm một chiều.")


# ============================================================
# 📝 KHU VỰC NHẬP + NÚT + KẾT QUẢ
# ============================================================
st.markdown(f"### 🧩 Bước 2 — Nhập dữ liệu cho **{cipher_type}**")

# ----- HÀM BĂM: GIAO DIỆN RIÊNG -----
if category == "🧮 Hàm băm":
    hash_text = st.text_area(
        "Nhập văn bản cần băm:",
        height=180,
        placeholder="Ví dụ: duck swims happily 🦆",
        key="hash_input"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        hash_btn = st.button("🧮 Tính mã băm 🦆", use_container_width=True, type="primary")
    with col_b:
        clear_hash_btn = st.button("🗑️ Xóa 🧹", use_container_width=True, key="clear_hash")

    if hash_btn:
        if not hash_text.strip():
            st.warning("🦆 Vui lòng nhập văn bản cần băm!")
        else:
            try:
                digest = compute_hash(hash_text, cipher_type)
                st.success(f"🦆 Băm thành công bằng {cipher_type}! 🌊")
                st.markdown(f"""
                <div class="result-box">
                    <h4>📤 Kết quả (Mã băm {cipher_type})</h4>
                    <div class="result-text" style="font-family:monospace;">{digest}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("ℹ️ Chi tiết"):
                    st.write(f"- Hàm băm: **{cipher_type}**")
                    st.write(f"- Độ dài: **{len(digest) * 4} bit** ({len(digest)} ký tự hex)")
                    st.write(f"- Văn bản gốc: `{hash_text}`")
                    st.write(f"- Mã băm: `{digest}`")
            except Exception as e:
                st.error(f"😢 Lỗi: {e}")

    if clear_hash_btn:
        st.rerun()

# ----- CÁC NHÓM KHÁC: 2 Ô + 3 NÚT -----
else:
    col_left, col_right = st.columns(2)

    if category == "⚙️ Mã hóa hiện đại":
        plain_label = "📝 Nhập bản rõ (chữ cái):"
        cipher_label = "🔒 Nhập bản mã (hex):"
        plain_ph = "Ví dụ: duck swims happily"
        cipher_ph = "Nhập bản mã Hex để giải mã..."
    elif category == "🔑 Mã hóa công khai":
        plain_label = "📝 Nhập bản rõ (chữ cái):"
        cipher_label = "🔒 Nhập bản mã (số nguyên):"
        plain_ph = "Ví dụ: hello"
        cipher_ph = "Ví dụ: 123456789"
    else:
        plain_label = "📝 Nhập văn bản cần mã hóa:"
        cipher_label = "🔒 Nhập văn bản cần giải mã:"
        plain_ph = "Ví dụ: duck swims happily 🦆"
        cipher_ph = "Ví dụ: gxfn vzlpv ujhyqad 🌊"

    with col_left:
        st.subheader("📝 Bản rõ")
        plain_text = st.text_area(plain_label, height=180, key="plain", placeholder=plain_ph)

    with col_right:
        st.subheader("🔒 Bản mã")
        cipher_text = st.text_area(cipher_label, height=180, key="cipher", placeholder=cipher_ph)

    st.markdown("---")
    st.markdown("### 🔘 Bước 3 — Hành động")

    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        encrypt_btn = st.button("🔒 Mã hóa 🦆", use_container_width=True, type="primary")
    with btn_col2:
        decrypt_btn = st.button("🔓 Giải mã 🌊", use_container_width=True)
    with btn_col3:
        clear_btn = st.button("🗑️ Xóa tất cả 🧹", use_container_width=True)

    # ----- MÃ HÓA -----
    if encrypt_btn:
        if not plain_text.strip():
            st.warning("🦆 Vui lòng nhập bản rõ nhé!")
        else:
            try:
                result = process(plain_text, True, category, cipher_type, key_input, alphabet)
                st.success("🦆 Mã hóa thành công! 🌊")
                st.markdown(f"""
                <div class="result-box">
                    <h4>📤 Kết quả (Bản mã)</h4>
                    <div class="result-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("ℹ️ Chi tiết"):
                    st.write(f"- Nhóm: **{category}**")
                    st.write(f"- Thuật toán: **{cipher_type}**")
                    st.write(f"- Hệ mã hóa: **{system_type}**")
                    st.write(f"- Khóa: **{key_input}**")
                    st.write(f"- Bản rõ: `{plain_text}`")
                    st.write(f"- Bản mã: `{result}`")
            except Exception as e:
                st.error(f"😢 Lỗi: {e}")

    # ----- GIẢI MÃ -----
    if decrypt_btn:
        if not cipher_text.strip():
            st.warning("🦆 Vui lòng nhập bản mã nhé!")
        else:
            try:
                result = process(cipher_text, False, category, cipher_type, key_input, alphabet)
                st.success("🦆 Giải mã thành công! 🌊")
                st.markdown(f"""
                <div class="result-box">
                    <h4>📤 Kết quả (Bản rõ)</h4>
                    <div class="result-text">{result}</div>
                </div>
                """, unsafe_allow_html=True)
                with st.expander("ℹ️ Chi tiết"):
                    st.write(f"- Nhóm: **{category}**")
                    st.write(f"- Thuật toán: **{cipher_type}**")
                    st.write(f"- Hệ mã hóa: **{system_type}**")
                    st.write(f"- Khóa: **{key_input}**")
                    st.write(f"- Bản mã: `{cipher_text}`")
                    st.write(f"- Bản rõ: `{result}`")
            except Exception as e:
                st.error(f"😢 Lỗi: {e}")

    if clear_btn:
        st.rerun()


# ============================================================
# HƯỚNG DẪN
# ============================================================
st.markdown("---")
with st.expander("📚 Hướng dẫn sử dụng chi tiết"):
    st.markdown("""
    ### 🦆 Cách dùng

    1. **Bước 1**: Bấm chọn **nhóm thuật toán** ở đầu trang (4 nút lớn).
    2. **Bước 2**: Vào **sidebar bên trái** để chọn thuật toán con + nhập khóa.
    3. **Bước 3**: Nhập bản rõ / bản mã vào 2 ô, rồi bấm **Mã hóa** hoặc **Giải mã**.

    ### 🔑 Định dạng khóa

    | Nhóm | Thuật toán | Khóa | Ví dụ |
    |---|---|---|---|
    | Cổ điển | Caesar | Số k | `3` |
    | Cổ điển | Substitution | Bảng 26/29 ký tự | `qwerty...` |
    | Cổ điển | Vigenere | Từ khóa chữ | `DUCK` |
    | Cổ điển | Affine | (a, b), gcd(a,n)=1 | `a=5, b=8` |
    | Cổ điển | Hill 2×2 | Ma trận a,b,c,d | `3, 3, 2, 5` |
    | Hiện đại | DES | Chữ cái (~8 ký tự) | `duckkey1` |
    | Hiện đại | AES | Chữ cái (~16 ký tự) | `duckkeyaes12345` |
    | Công khai | RSA | Sinh tự động | Nhấn 🎲 |
    | Hàm băm | MD5/SHA | Không cần khóa | — |

    ### 🌊 Ví dụ kiểm thử

    - **Caesar Z26:** `hello world`, k=3 → `khoor zruog`
    - **Vigenere Z26:** `ATTACKATDAWN`, key=`LEMON` → `LXFOPVEFRNHR`
    - **Affine Z26:** `affine cipher`, a=5, b=8 → `ihhwvc swfrcp`
    - **Hill Z26:** `help`, K=[[3,3],[2,5]] → `HIAT`
    - **DES:** bản rõ + khóa chữ cái → hex
    - **AES:** bản rõ + khóa chữ cái → hex
    - **RSA:** bản rõ chữ cái → số nguyên, rồi giải mã lại
    - **MD5("hello")** = `5D41402ABC4B2A76B9719D911017C592`
    """)

st.markdown(
    "<div class='duck-footer'>"
    "🦆 Made with <b>Streamlit</b> + <b>Python</b> 🦆<br>"
    "🌊 Vui vẻ như vịt vàng bơi nắng! ☀️"
    "</div>",
    unsafe_allow_html=True
)