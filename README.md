🔐 ECDSA Δk Private Key Recovery

recover_from_delta_k.py

This project demonstrates a pure-Python ECDSA key recovery technique for the case where two signatures were generated with ephemeral nonces whose difference Δk = k₁ − k₂ is known (or guessed).

⚙️ It computes the private key d directly from two signatures and a known Δk,
then reconstructs and verifies the ephemeral keys k₁ and k₂.

⚠️ Research-Only Notice

🧠 This repository is intended for research and educational use only.
It shows how small nonce differences can weaken ECDSA if nonces are not securely generated.

❌ Do not use it to recover or exploit third-party private keys.

✨ Features

✅ Direct algebraic recovery — Computes d using a closed-form modular equation
✅ Ephemeral key recomputation — Verifies recovered d via (z + d·r)·s⁻¹ mod n
✅ Explicit error handling — Detects and reports non-invertible modular denominators
✅ Readable structure — Clear, step-by-step code with detailed docstrings
✅ Zero dependencies — Works with standard Python only

📂 File Structure
File	Description
recover_from_delta_k.py	Main recovery script (contains modinv, compute_private_key, compute_ephemeral_key, and main)
README.md	Documentation (this file)
🧮 Mathematical Overview

For two ECDSA signatures:

s₁ = k₁⁻¹ (z₁ + r₁·d) mod n  
s₂ = k₂⁻¹ (z₂ + r₂·d) mod n


and given the known difference

Δk = k₁ − k₂,

we can solve directly for d:

d = [Δk·s₁·s₂ − (s₂·z₁ − s₁·z₂)] · (s₂·r₁ − s₁·r₂)⁻¹ mod n


Recovered ephemeral keys:

k = (z + d·r) · s⁻¹ mod n


Verification step (for both signatures):

s ≡ k⁻¹ (z + r·d) mod n

⚙️ Usage

1️⃣ Insert your parameters in the script:

z1 = int("0x...", 16)
z2 = int("0x...", 16)
r1 = int("0x...", 16)
r2 = int("0x...", 16)
s1 = int("0x...", 16)
s2 = int("0x...", 16)
delta_k = 3141592653589793  # example Δk
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141


2️⃣ Run the script:

python3 recover_from_delta_k.py


🧾 Example output:

Prywatny klucz d = 0x1f7a3b...
Ephemeralny klucz k1 = 0x13c56a...
Ephemeralny klucz k2 = 0x13c568...
Różnica k1 - k2 = 3141592653589793

⚠️ Edge Cases
Condition	Result
(s₂·r₁ − s₁·r₂) % n == 0	Modular inverse does not exist → ValueError
Wrong Δk	Computed d is invalid; signature check fails
Wrong curve order n	Invalid modular domain → incorrect results
⚡ Performance Notes

Single-pair computation: instantaneous (<1 ms) on modern CPUs

Complexity: O(1) — one modular inverse + a few multiplications

Easily scales for batch testing over Δk ranges

🔍 Implementation Summary
Function	Purpose
modinv(a, n)	Modular inverse (Extended Euclidean Algorithm)
compute_private_key()	Recovers d from two signatures and Δk
compute_ephemeral_key()	Reconstructs k from (z, r, s, d)
main()	Demonstration entry point with example data
🧠 Verification Workflow

Compute d using compute_private_key()

Recompute k₁, k₂ via compute_ephemeral_key()

Verify: (k₁ - k₂) % n == Δk

Optional: confirm both signatures satisfy the ECDSA equation

🔒 Ethical Use

This project exists to educate developers and audit cryptographic systems.
It must not be used to recover unauthorized keys or attack live systems.

You may:

Audit your own wallet or ECDSA implementation

Test nonces or randomness in research datasets

You must not:

Attempt private key extraction from third-party data

Deploy this on production/mainnet systems

🪪 License

MIT License
© 2025 — Author: [ethicbrudhack]
