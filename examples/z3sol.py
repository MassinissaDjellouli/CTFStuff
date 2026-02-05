from z3.z3 import *
import struct


# --- Helper to decode IEEE-754 doubles from 0x... hex constants ---
def dbl_from_hex(h):
    h = h.replace("0x", "").upper()
    if len(h) != 16:
        raise ValueError(f"Hex string {h} must have exactly 16 hex digits (8 bytes)")
    return struct.unpack(">d", bytes.fromhex(h))[0]


# --- Variables as 64-bit signed integers (like 'long long') ---


# --- Integer → double (IEEE-754) casts ---
x = BitVec('x', 64)
y = BitVec('y', 64)
z = BitVec('z', 64)

rm = RNE()  # Rounding mode: Round to Nearest, ties to Even

x_d = fpSignedToFP(rm, x, Float64())
y_d = fpSignedToFP(rm, y, Float64())
z_d = fpSignedToFP(rm, z, Float64())

# --- Constants (from hex values in your C code) ---
pi = FPVal(dbl_from_hex("400921CAC083126F"), Float64())  # ≈ π
tpy = FPVal(dbl_from_hex("401921CAC083126F"), Float64())  # ≈ 2π
nine_point_nine_constant = FPVal(dbl_from_hex("4023CCCCCCCCCCCD"), Float64())  # ≈ 9.9
eps = FPVal(0.0001, Float64())

# --- Solver setup ---
s = Solver()

# Eq 1
expr1 = ((x_d * 2) - pi + (y_d * 3) + (z_d * 4) + tpy) - (
    pi + FPVal(28309.0, Float64())
)
s.add(Abs(expr1) < eps)

# Eq 2
expr2 = (
    (x_d * 2 - y_d) + FPVal(1.0, Float64()) + (z_d * 0.5) - FPVal(1.0, Float64())
) - FPVal(5412.0, Float64())
s.add(Abs(expr2) < eps)

# Eq 3
expr3 = (((y_d * 5 - x_d) * 2) - (z_d * 5.5)) * nine_point_nine_constant - nine_point_nine_constant * FPVal(
    -18449.0, Float64()
)
s.add(Abs(expr3) < eps)

# --- Solve ---
while s.check() == sat:
    m = s.model()
    print("[+] Solution found: " + str((m[x], m[y], m[z])))
    # s.add(Or(x_d != m[x_d], y_d != m[y_d], z_d != m[z_d]))
    
    